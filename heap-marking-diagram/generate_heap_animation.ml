open Base
open Stdio

type color =
  { marked : string
  ; unmarked : string
  ; root : string
  ; background : string
  ; section_bg : string
  ; arrow : string
  ; arrow_active : string
  ; text : string
  ; sweep_highlight : string
  }

type position =
  { x : int
  ; y : int
  }

type heap_object =
  { id : string
  ; slot : int
  ; points_to : string list
  }

type root =
  { id : string
  ; points_to : string
  }

type heap_config =
  { objects : heap_object list
  ; roots : root list
  }

type object_state =
  | Marked
  | Unmarked
[@@deriving equal]

type slot_object =
  { id : string
  ; state : object_state
  ; reachable : bool
  }

type heap_slot =
  { id : int
  ; x : int
  ; y : int
  ; obj : slot_object option
  }

type connection =
  { from_id : string
  ; to_id : string
  }

type animation_frame =
  { title : string
  ; roots : position list
  ; heap_slots : heap_slot list
  ; connections : connection list
  ; sweep_position : int option
  ; active_connections : connection list
  }

let colors =
  { marked = "#4CAF50"
  ; unmarked = "#FF5252"
  ; root = "#2196F3"
  ; background = "#F5F5F5"
  ; section_bg = "white"
  ; arrow = "#333333"
  ; arrow_active = "#8B1538"
  ; text = "#333333"
  ; sweep_highlight = "#DDDDDD"
  }
;;

let width = 1100
let height = 600
let scan_time_ms = 70

(* Grid configuration *)
let cols = 10
let rows = 5
let slot_size = 60
let slot_spacing = 15
let margin = 30

(* Calculate exact heap dimensions based on grid *)
let heap_width = (margin * 2) + (cols * slot_size) + ((cols - 1) * slot_spacing)
let heap_height = (margin * 2) + (rows * slot_size) + ((rows - 1) * slot_spacing)

(* Define heap position *)
let heap_x = 180
let heap_y = 100

(* Heap configuration - easy to modify *)
let heap_config =
  { objects =
      [ (* Reachable objects *)
        { id = "obj0"; slot = 3; points_to = [ "obj3" ] }
      ; { id = "obj1"; slot = 11; points_to = [ "obj4"; "obj10" ] }
      ; { id = "obj2"; slot = 18; points_to = [] }
      ; { id = "obj3"; slot = 14; points_to = [ "obj5" ] }
      ; { id = "obj4"; slot = 13; points_to = [] }
      ; { id = "obj5"; slot = 27; points_to = [] }
      ; (* Garbage objects *)
        { id = "obj6"; slot = 31; points_to = [ "obj7" ] }
      ; { id = "obj7"; slot = 34; points_to = [] }
      ; { id = "obj8"; slot = 37; points_to = [] }
      ; { id = "obj9"; slot = 8; points_to = [] }
      ; { id = "obj10"; slot = 42; points_to = [ "obj8" ] }
      ]
  ; roots =
      [ { id = "r1"; points_to = "obj0" }
      ; { id = "r2"; points_to = "obj1" }
      ; { id = "r3"; points_to = "obj2" }
      ]
  }
;;

(* Build reachability set *)
let build_reachable_set (config : heap_config) =
  let reachable = ref [] in
  let rec mark_reachable obj_id =
    if List.mem !reachable obj_id ~equal:String.equal
    then ()
    else (
      reachable := obj_id :: !reachable;
      match
        List.find config.objects ~f:(fun (obj : heap_object) ->
          String.equal obj.id obj_id)
      with
      | Some obj -> List.iter obj.points_to ~f:mark_reachable
      | None -> ())
  in
  List.iter config.roots ~f:(fun (r : root) -> mark_reachable r.points_to);
  !reachable
;;

(* Initialize heap slots *)
let init_heap_slots (config : heap_config) reachable =
  let slots = ref [] in
  for row = 0 to rows - 1 do
    for col = 0 to cols - 1 do
      let slot_id = (row * cols) + col in
      let x = heap_x + margin + (col * (slot_size + slot_spacing)) in
      let y = heap_y + margin + (row * (slot_size + slot_spacing)) in
      let obj =
        match List.find config.objects ~f:(fun obj -> obj.slot = slot_id) with
        | Some obj ->
          Some
            { id = obj.id
            ; state = Unmarked
            ; reachable = List.mem reachable obj.id ~equal:String.equal
            }
        | None -> None
      in
      slots := { id = slot_id; x; y; obj } :: !slots
    done
  done;
  List.rev !slots
;;

(* Root positions *)
let root_positions = [ { x = 90; y = 252 }; { x = 90; y = 322 }; { x = 90; y = 392 } ]

(* Build connections list *)
let build_connections (config : heap_config) =
  let connections = ref [] in
  (* Root connections *)
  List.iter config.roots ~f:(fun (r : root) ->
    connections := { from_id = r.id; to_id = r.points_to } :: !connections);
  (* Object connections *)
  List.iter config.objects ~f:(fun (obj : heap_object) ->
    List.iter obj.points_to ~f:(fun target ->
      connections := { from_id = obj.id; to_id = target } :: !connections));
  List.rev !connections
;;

(* Update object state in slots *)
let update_object_states slots obj_ids new_state =
  List.map slots ~f:(fun slot ->
    match slot.obj with
    | None -> slot
    | Some obj when List.mem obj_ids obj.id ~equal:String.equal ->
      { slot with obj = Some { obj with state = new_state } }
    | _ -> slot)
;;

(* Generate frames *)
let generate_frames () =
  let reachable = build_reachable_set heap_config in
  let initial_slots = init_heap_slots heap_config reachable in
  let connections = build_connections heap_config in
  let frames = ref [] in
  (* Frame 1: Initial state - all objects unmarked *)
  frames
  := { title = "Marking"
     ; roots = root_positions
     ; heap_slots = initial_slots
     ; connections
     ; sweep_position = None
     ; active_connections = []
     }
     :: !frames;
  (* Depth-first marking *)
  let current_slots = ref initial_slots in
  let traversed_connections = ref [] in
  (* Helper to find object by ID in current slots *)
  let find_obj_slot obj_id =
    List.find !current_slots ~f:(fun slot ->
      match slot.obj with
      | Some obj -> String.equal obj.id obj_id
      | None -> false)
  in
  (* DFS marking function *)
  let rec dfs_mark from_id obj_id =
    match find_obj_slot obj_id with
    | None -> ()
    | Some slot ->
      (match slot.obj with
       | None -> ()
       | Some obj when equal_object_state obj.state Marked -> ()
       | Some _ ->
         (* Mark this object *)
         current_slots := update_object_states !current_slots [ obj_id ] Marked;
         (* Add traversal edge *)
         traversed_connections := !traversed_connections @ [ { from_id; to_id = obj_id } ];
         (* Create frame *)
         frames
         := { title = "Marking"
            ; roots = root_positions
            ; heap_slots = !current_slots
            ; connections
            ; sweep_position = None
            ; active_connections = !traversed_connections
            }
            :: !frames;
         (* Find object in config to get its pointers *)
         (match List.find heap_config.objects ~f:(fun o -> String.equal o.id obj_id) with
          | None -> ()
          | Some heap_obj ->
            (* Recursively mark each pointed-to object *)
            List.iter heap_obj.points_to ~f:(fun target_id -> dfs_mark obj_id target_id)))
  in
  (* Start DFS from each root *)
  List.iter heap_config.roots ~f:(fun root -> dfs_mark root.id root.points_to);
  (* Use the final marked slots for sweep phase *)
  let slots = !current_slots in
  (* Sweep phase *)
  let sweep_frame current_slots current_connections slot_idx =
    let slot = List.nth_exn current_slots slot_idx in
    match slot.obj with
    | None ->
      (* Empty slot - still show we're scanning it *)
      { title = "Sweeping"
      ; roots = root_positions
      ; heap_slots = current_slots
      ; connections = current_connections
      ; sweep_position = Some slot_idx
      ; active_connections = []
      }
    | Some obj ->
      if equal_object_state obj.state Unmarked
      then (
        (* Remove garbage object *)
        let new_slots =
          List.mapi current_slots ~f:(fun i s ->
            if i = slot_idx then { s with obj = None } else s)
        in
        let new_connections =
          List.filter current_connections ~f:(fun conn ->
            not (String.equal conn.from_id obj.id || String.equal conn.to_id obj.id))
        in
        { title = "Sweeping"
        ; roots = root_positions
        ; heap_slots = new_slots
        ; connections = new_connections
        ; sweep_position = Some slot_idx
        ; active_connections = []
        })
      else (
        (* Turn marked back to unmarked *)
        let new_slots =
          List.mapi current_slots ~f:(fun i s ->
            if i = slot_idx
            then (
              match s.obj with
              | Some o -> { s with obj = Some { o with state = Unmarked } }
              | None -> s)
            else s)
        in
        { title = "Sweeping"
        ; roots = root_positions
        ; heap_slots = new_slots
        ; connections = current_connections
        ; sweep_position = Some slot_idx
        ; active_connections = []
        })
  in
  (* Sweep through each slot *)
  let rec sweep_slots current_slots current_connections slot_idx =
    if slot_idx >= List.length current_slots
    then
      (* Final frame *)
      frames
      := { title = "Sweeping"
         ; roots = root_positions
         ; heap_slots = current_slots
         ; connections = current_connections
         ; sweep_position = None
         ; active_connections = []
         }
         :: !frames
    else (
      let new_frame = sweep_frame current_slots current_connections slot_idx in
      frames := new_frame :: !frames;
      sweep_slots new_frame.heap_slots new_frame.connections (slot_idx + 1))
  in
  sweep_slots slots connections 0;
  List.rev !frames
;;

(* JSON encoding helpers *)
let json_string s = Printf.sprintf "\"%s\"" s
let json_int i = Int.to_string i

let json_option f = function
  | None -> "null"
  | Some x -> f x
;;

let json_list : ('a -> string) -> 'a list -> string =
  fun f lst -> "[" ^ String.concat ~sep:", " (List.map lst ~f) ^ "]"
;;

let json_object pairs =
  "{"
  ^ String.concat
      ~sep:", "
      (List.map pairs ~f:(fun (k, v) -> Printf.sprintf "\"%s\": %s" k v))
  ^ "}"
;;

let position_to_json : position -> string =
  fun pos -> json_object [ "x", json_int pos.x; "y", json_int pos.y ]
;;

let object_state_to_string = function
  | Marked -> "marked"
  | Unmarked -> "unmarked"
;;

let slot_to_json slot =
  let obj_json =
    match slot.obj with
    | None -> "null"
    | Some obj ->
      json_object
        [ "id", json_string obj.id
        ; "state", json_string (object_state_to_string obj.state)
        ; ("reachable", if obj.reachable then "true" else "false")
        ]
  in
  json_object
    [ "id", json_int slot.id
    ; "x", json_int slot.x
    ; "y", json_int slot.y
    ; "object", obj_json
    ]
;;

let connection_to_json conn =
  json_object [ "from", json_string conn.from_id; "to", json_string conn.to_id ]
;;

let frame_to_json (frame : animation_frame) =
  let (roots : position list) = frame.roots in
  let roots_json = json_list position_to_json roots in
  let heap_slots_json = json_list slot_to_json frame.heap_slots in
  let connections_json = json_list connection_to_json frame.connections in
  let active_connections_json = json_list connection_to_json frame.active_connections in
  json_object
    [ "title", json_string frame.title
    ; "roots", roots_json
    ; "heap_slots", heap_slots_json
    ; "connections", connections_json
    ; "sweep_position", json_option json_int frame.sweep_position
    ; "active_connections", active_connections_json
    ]
;;

(* Generate HTML *)
let generate_html frames =
  let frames_json = json_list frame_to_json frames in
  Printf.sprintf
    {|<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Heap Marking Animation</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
            background-color: white;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            overflow: hidden;
        }
        #container {
            display: flex;
            flex-direction: column;
            align-items: center;
            width: 100%%;
            height: 100vh;
        }
        #svg-wrapper {
            flex: 1;
            display: flex;
            align-items: center;
            justify-content: center;
            width: 100%%;
        }
        svg {
            display: block;
            transform-origin: center center;
        }
        #controls {
            padding: 10px;
            text-align: center;
            background-color: white;
        }
        #title {
            font-size: 24px;
            font-weight: bold;
            padding: 10px;
            text-align: center;
            color: #333;
            background-color: white;
        }
        .control-hint {
            font-size: 14px;
            color: #666;
        }
    </style>
</head>
<body>
    <div id="container">
        <div id="title"></div>
        <div id="svg-wrapper">
            <svg id="animation" width="%d" height="%d" viewBox="0 0 %d %d" preserveAspectRatio="xMidYMid meet">
                <defs>
                    <marker id="arrowhead" markerWidth="15" markerHeight="15" refX="15" refY="7.5" orient="auto">
                        <polygon points="0,0 15,7.5 0,15" fill="%s" stroke="none"/>
                    </marker>
                </defs>
            </svg>
        </div>
        <div id="controls">
            <div class="control-hint">Left/Right or Space: navigate | C: skip to end of phase | D: debug mode | R: reset</div>
        </div>
    </div>

    <script>
        const frames = %s;
        let currentFrame = 0;
        let autoAdvanceInterval = null;
        const scanTimeMs = %d;
        let debugMode = false;

        const svg = document.getElementById('animation');
        const titleElement = document.getElementById('title');

        function drawFrame(frameIndex) {
            const frame = frames[frameIndex];
            titleElement.textContent = frame.title;

            // Clear SVG except defs
            while (svg.childNodes.length > 1) {
                svg.removeChild(svg.lastChild);
            }

            // Stack section
            drawSection(40, 200, 100, 250, 'Stack');

            // Heap section
            drawSection(%d, %d, %d, %d, 'Heap');

            // Draw heap slots (grid)
            frame.heap_slots.forEach((slot, idx) => {
                const isBeingSwept = frame.sweep_position === idx;
                drawHeapSlot(slot, isBeingSwept, idx);
            });

            // Draw connections
            frame.connections.forEach(conn => {
                const isActive = frame.active_connections.some(ac =>
                    ac.from === conn.from && ac.to === conn.to
                );
                drawConnection(conn, frame.heap_slots, isActive);
            });

            // Draw roots
            frame.roots.forEach((root, index) => {
                drawObject(55, 230 + index * 70, 70, 45, 'root');
            });

            // Draw legend
            drawLegend();
        }

        function drawSection(x, y, width, height, label) {
            const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
            rect.setAttribute('x', x);
            rect.setAttribute('y', y);
            rect.setAttribute('width', width);
            rect.setAttribute('height', height);
            rect.setAttribute('fill', '%s');
            rect.setAttribute('stroke', '#CCCCCC');
            rect.setAttribute('stroke-width', '2');
            rect.setAttribute('rx', '8');
            rect.setAttribute('ry', '8');
            svg.appendChild(rect);

            const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
            text.setAttribute('x', x + width/2);
            text.setAttribute('y', y - 15);
            text.setAttribute('text-anchor', 'middle');
            text.setAttribute('font-family', 'Arial, sans-serif');
            text.setAttribute('font-size', '24');
            text.setAttribute('font-weight', 'bold');
            text.setAttribute('fill', '%s');
            text.textContent = label;
            svg.appendChild(text);
        }

        function drawHeapSlot(slot, isBeingSwept, slotIndex) {
            // Draw slot background if being swept
            if (isBeingSwept) {
                const bg = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
                bg.setAttribute('x', slot.x - 5);
                bg.setAttribute('y', slot.y - 5);
                bg.setAttribute('width', 65);
                bg.setAttribute('height', 65);
                bg.setAttribute('fill', '%s');
                bg.setAttribute('rx', '3');
                bg.setAttribute('ry', '3');
                svg.appendChild(bg);
            }

            // Draw object if present
            if (slot.object) {
                drawObject(slot.x, slot.y, 55, 55, slot.object.state);
            }

            // Draw slot number in debug mode
            if (debugMode) {
                const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
                text.setAttribute('x', slot.x + 27.5);
                text.setAttribute('y', slot.y + (slot.object ? 20 : 27.5));
                text.setAttribute('text-anchor', 'middle');
                text.setAttribute('font-family', 'Arial, sans-serif');
                text.setAttribute('font-size', '12');
                text.setAttribute('font-weight', 'bold');
                text.setAttribute('fill', slot.object ? 'white' : '#666');
                text.textContent = slotIndex;
                svg.appendChild(text);
            }
        }

        function drawObject(x, y, width, height, type) {
            const colors = {
                'root': '%s',
                'marked': '%s',
                'unmarked': '%s'
            };

            const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
            rect.setAttribute('x', x);
            rect.setAttribute('y', y);
            rect.setAttribute('width', width);
            rect.setAttribute('height', height);
            rect.setAttribute('fill', colors[type]);
            rect.setAttribute('stroke', '#333333');
            rect.setAttribute('stroke-width', '2');
            rect.setAttribute('rx', '6');
            rect.setAttribute('ry', '6');
            svg.appendChild(rect);
        }

        function drawConnection(conn, heap_slots, isActive) {
            // Find positions
            let fromX, fromY, toX, toY;

            if (conn.from.startsWith('r')) {
                // From root
                const rootIndex = parseInt(conn.from[1]) - 1;
                fromX = 125;
                fromY = 252.5 + rootIndex * 70;
            } else {
                // From heap object
                const fromSlot = heap_slots.find(s => s.object && s.object.id === conn.from);
                if (!fromSlot) return;
                fromX = fromSlot.x + 27.5;
                fromY = fromSlot.y + 27.5;
            }

            // To heap object
            const toSlot = heap_slots.find(s => s.object && s.object.id === conn.to);
            if (!toSlot) return;
            toX = toSlot.x + 27.5;
            toY = toSlot.y + 27.5;

            // Adjust endpoints
            if (conn.from.startsWith('r')) {
                toX -= 27.5;
            }

            const color = isActive ? '%s' : '%s';
            drawArrow(fromX, fromY, toX, toY, color);
        }

        function drawArrow(x1, y1, x2, y2, color) {
            const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
            line.setAttribute('x1', x1);
            line.setAttribute('y1', y1);
            line.setAttribute('x2', x2);
            line.setAttribute('y2', y2);
            line.setAttribute('stroke', color || '%s');
            line.setAttribute('stroke-width', '2.5');
            svg.appendChild(line);

            // Calculate arrow direction
            const dx = x2 - x1;
            const dy = y2 - y1;
            const length = Math.sqrt(dx*dx + dy*dy);
            if (length === 0) return;

            // Normalize
            const ndx = dx / length;
            const ndy = dy / length;

            // Arrowhead size
            const arrowLength = 15;
            const arrowWidth = 7;

            // Calculate arrowhead points
            const baseX = x2 - ndx * arrowLength;
            const baseY = y2 - ndy * arrowLength;

            // Perpendicular vector
            const perpX = -ndy;
            const perpY = ndx;

            // Three points of the arrowhead
            const points = `${x2},${y2} ${baseX + perpX * arrowWidth},${baseY + perpY * arrowWidth} ${baseX - perpX * arrowWidth},${baseY - perpY * arrowWidth}`;

            const polygon = document.createElementNS('http://www.w3.org/2000/svg', 'polygon');
            polygon.setAttribute('points', points);
            polygon.setAttribute('fill', color || '%s');
            svg.appendChild(polygon);
        }

        function drawLegend() {
            // Legend background
            const legendBg = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
            legendBg.setAttribute('x', '910');
            legendBg.setAttribute('y', '240');
            legendBg.setAttribute('width', '170');
            legendBg.setAttribute('height', '160');
            legendBg.setAttribute('fill', '#FAFAFA');
            legendBg.setAttribute('stroke', '#AAAAAA');
            legendBg.setAttribute('stroke-width', '1');
            legendBg.setAttribute('stroke-dasharray', '5,5');
            legendBg.setAttribute('rx', '5');
            legendBg.setAttribute('ry', '5');
            svg.appendChild(legendBg);

            // Legend title
            const legendTitle = document.createElementNS('http://www.w3.org/2000/svg', 'text');
            legendTitle.setAttribute('x', '995');
            legendTitle.setAttribute('y', '265');
            legendTitle.setAttribute('text-anchor', 'middle');
            legendTitle.setAttribute('font-family', 'Arial, sans-serif');
            legendTitle.setAttribute('font-size', '16');
            legendTitle.setAttribute('font-weight', 'bold');
            legendTitle.setAttribute('fill', '%s');
            legendTitle.textContent = 'Legend';
            svg.appendChild(legendTitle);

            // Legend entries
            const entries = [
                {color: '%s', label: 'Root'},
                {color: '%s', label: 'Marked'},
                {color: '%s', label: 'Unmarked'}
            ];

            entries.forEach((entry, index) => {
                const y = 290 + index * 35;

                // Color box
                const box = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
                box.setAttribute('x', '930');
                box.setAttribute('y', y);
                box.setAttribute('width', '20');
                box.setAttribute('height', '20');
                box.setAttribute('fill', entry.color);
                box.setAttribute('stroke', '#333333');
                box.setAttribute('stroke-width', '1.5');
                box.setAttribute('rx', '3');
                box.setAttribute('ry', '3');
                svg.appendChild(box);

                // Label
                const label = document.createElementNS('http://www.w3.org/2000/svg', 'text');
                label.setAttribute('x', '955');
                label.setAttribute('y', y + 15);
                label.setAttribute('font-family', 'Arial, sans-serif');
                label.setAttribute('font-size', '14');
                label.setAttribute('fill', '%s');
                label.textContent = entry.label;
                svg.appendChild(label);
            });
        }

        function nextFrame() {
            if (currentFrame < frames.length - 1) {
                currentFrame++;
                drawFrame(currentFrame);
            } else {
                stopAutoAdvance();
            }
        }

        function prevFrame() {
            if (currentFrame > 0) {
                currentFrame--;
                drawFrame(currentFrame);
            }
        }

        function startAutoAdvance() {
            if (autoAdvanceInterval) return; // Already running

            autoAdvanceInterval = setInterval(() => {
                nextFrame();
            }, scanTimeMs);
        }

        function stopAutoAdvance() {
            if (autoAdvanceInterval) {
                clearInterval(autoAdvanceInterval);
                autoAdvanceInterval = null;
            }
        }

        // Keyboard navigation
        document.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowRight' || e.key === ' ') {
                e.preventDefault();
                stopAutoAdvance();
                nextFrame();
            } else if (e.key === 'ArrowLeft') {
                e.preventDefault();
                stopAutoAdvance();
                prevFrame();
            } else if (e.key === 'c' || e.key === 'C') {
                e.preventDefault();
                if (autoAdvanceInterval) {
                    stopAutoAdvance();
                } else {
                    // Start auto-advance that stops at phase end
                    const currentPhase = frames[currentFrame].title;
                    autoAdvanceInterval = setInterval(() => {
                        if (currentFrame < frames.length - 1) {
                            const nextFrame = frames[currentFrame + 1];
                            if (nextFrame.title === currentPhase) {
                                currentFrame++;
                                drawFrame(currentFrame);
                            } else {
                                // Reached end of current phase
                                stopAutoAdvance();
                            }
                        } else {
                            // Reached last frame
                            stopAutoAdvance();
                        }
                    }, scanTimeMs);
                }
            } else if (e.key === 'd' || e.key === 'D') {
                e.preventDefault();
                debugMode = !debugMode;
                drawFrame(currentFrame);
            } else if (e.key === 'r' || e.key === 'R') {
                e.preventDefault();
                stopAutoAdvance();
                currentFrame = 0;
                drawFrame(currentFrame);
            }
        });

        // Handle window resize
        function handleResize() {
            const wrapper = document.getElementById('svg-wrapper');
            const svg = document.getElementById('animation');
            const wrapperRect = wrapper.getBoundingClientRect();

            // Calculate scale to fit
            const scaleX = wrapperRect.width / %d;
            const scaleY = wrapperRect.height / %d;
            const scale = Math.min(scaleX, scaleY, 1.5); // Cap at 1.5x to avoid pixelation

            // Apply transform
            svg.style.transform = 'scale(' + scale + ')';
        }

        window.addEventListener('resize', handleResize);

        // Initial draw
        drawFrame(0);
        handleResize();
    </script>
</body>
</html>|}
    width
    height
    width
    height
    colors.arrow
    frames_json
    scan_time_ms
    heap_x
    heap_y
    heap_width
    heap_height
    colors.section_bg
    colors.text
    colors.sweep_highlight
    colors.root
    colors.marked
    colors.unmarked
    colors.arrow_active
    colors.arrow
    colors.arrow
    colors.arrow
    colors.text
    colors.root
    colors.marked
    colors.unmarked
    colors.text
    width
    height
;;

let () =
  let frames = generate_frames () in
  let html = generate_html frames in
  Out_channel.write_all "heap-marking-diagram/heap_animation.html" ~data:html;
  printf "Generated heap-marking-diagram/heap_animation.html\n"
;;
