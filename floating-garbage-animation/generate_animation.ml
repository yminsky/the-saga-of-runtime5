open Base
open Stdio

(* Configuration *)
let block_width = 80
let block_height = 40
let block_spacing = 5
let timeline_spacing = 120

(* Colors *)
let sweep_color = "#4682B4"  (* Blue *)
let mark_color = "#228B22"   (* Green *)
let merged_color = "#6B46C1" (* Purple *)
let arrow_color = "#666666"

type element_type =
  | Label of { text : string; x : int; y : int }
  | Timeline of { runtime : int; y : int; phases : int }
  | Allocation of { x : int; y : int; id : string }
  | Collection of { x : int; y : int; id : string }
  | Bar of { from_x : int; to_x : int; y : int; label : string; id : string }

type frame = {
  id : int;
  elements : element_type list;
}

let generate_svg_element = function
  | Label { text; x; y } ->
      Printf.sprintf {|<text x="%d" y="%d" class="label">%s</text>|} x y text
  
  | Timeline { runtime; y; phases } ->
      let rec generate_blocks x i acc =
        if i >= phases then acc
        else
          let block = 
            if runtime = 4 then
              let phase_type = if i % 2 = 0 then "sweep" else "mark" in
              let color = if String.equal phase_type "sweep" then sweep_color else mark_color in
              let label = if String.equal phase_type "sweep" then "S" else "M" in
              [
                Printf.sprintf {|<rect x="%d" y="%d" width="%d" height="%d" fill="%s" stroke="black" />|}
                  x y block_width block_height color;
                Printf.sprintf {|<text x="%d" y="%d" text-anchor="middle" class="phase-label">%s</text>|}
                  (x + block_width/2) (y + block_height/2 + 5) label
              ]
            else (* runtime 5 *)
              [
                Printf.sprintf {|<rect x="%d" y="%d" width="%d" height="%d" fill="%s" stroke="black" />|}
                  x y (block_width * 2 + block_spacing) block_height merged_color;
                Printf.sprintf {|<text x="%d" y="%d" text-anchor="middle" class="phase-label">S/M</text>|}
                  (x + block_width + block_spacing/2) (y + block_height/2 + 5)
              ]
          in
          let next_x = 
            if runtime = 4 then x + block_width + block_spacing
            else x + (block_width * 2 + block_spacing) + block_spacing
          in
          generate_blocks next_x (i + 1) (acc @ block)
      in
      String.concat ~sep:"\n" (generate_blocks 100 0 [])
  
  | Allocation { x; y; id } ->
      let size = 6 in
      Printf.sprintf {|<polygon points="%d,%d %d,%d %d,%d" fill="#228B22" class="allocation %s" />|}
        x (y - size) (x - size) (y + size) (x + size) (y + size) id
  
  | Collection { x; y; id } ->
      let size = 6 in
      Printf.sprintf {|<polygon points="%d,%d %d,%d %d,%d" fill="#DC143C" class="collection %s" />|}
        x (y - size) (x - size) (y + size) (x + size) (y + size) id
  
  | Bar { from_x; to_x; y; label; id } ->
      let mid_x = (from_x + to_x) / 2 in
      Printf.sprintf {|<g class="bar %s">
<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2" />
<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2" />
<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2" />
<text x="%d" y="%d" text-anchor="middle" class="bar-label">%s cycles</text>
</g>|}
        id
        from_x y to_x y arrow_color
        from_x (y - 5) from_x (y + 5) arrow_color
        to_x (y - 5) to_x (y + 5) arrow_color
        mid_x (y - 8) label

let generate_frames () =
  let rt5_y = 40 + timeline_spacing in
  let rt5_alloc_x1 = 100 + block_width/2 in
  let rt5_alloc_x2 = 100 + block_width + block_spacing + block_width/2 in
  let rt5_collect_x = 100 + (block_width * 2 + block_spacing) * 2 + block_width/2 in
  
  let frames = [
    (* Frame 1: Initial Runtime 4 Timeline *)
    {
      id = 1;
      elements = [
        Label { text = "Runtime 4"; x = 10; y = 25 };
        Timeline { runtime = 4; y = 40; phases = 6 };
      ]
    };
    
    (* Frame 2: Allocation in Sweep Phase *)
    {
      id = 2;
      elements = [
        Label { text = "Runtime 4"; x = 10; y = 25 };
        Timeline { runtime = 4; y = 40; phases = 6 };
        Allocation { x = 100 + block_width/2; y = 40 + block_height + 15; id = "sweep-alloc" };
      ]
    };
    
    (* Frame 3: Collection Point for Sweep Allocation *)
    {
      id = 3;
      elements = [
        Label { text = "Runtime 4"; x = 10; y = 25 };
        Timeline { runtime = 4; y = 40; phases = 6 };
        Allocation { x = 100 + block_width/2; y = 40 + block_height + 15; id = "sweep-alloc" };
        Bar { 
          from_x = 100 + block_width/2; 
          to_x = 100 + (block_width + block_spacing) * 2 + block_width/2;
          y = 40 + block_height + 25; 
          label = "1"; 
          id = "sweep-bar" 
        };
        Collection { 
          x = 100 + (block_width + block_spacing) * 2 + block_width/2; 
          y = 40 + block_height + 15; 
          id = "sweep-collect" 
        };
      ]
    };
    
    (* Frame 4: Add Mark Allocation *)
    {
      id = 4;
      elements = [
        Label { text = "Runtime 4"; x = 10; y = 25 };
        Timeline { runtime = 4; y = 40; phases = 6 };
        Allocation { x = 100 + block_width/2; y = 40 + block_height + 15; id = "sweep-alloc" };
        Bar { 
          from_x = 100 + block_width/2; 
          to_x = 100 + (block_width + block_spacing) * 2 + block_width/2;
          y = 40 + block_height + 25; 
          label = "1"; 
          id = "sweep-bar" 
        };
        Collection { 
          x = 100 + (block_width + block_spacing) * 2 + block_width/2; 
          y = 40 + block_height + 15; 
          id = "sweep-collect" 
        };
        Allocation { 
          x = 100 + block_width + block_spacing + block_width/2; 
          y = 40 + block_height + 45; 
          id = "mark-alloc" 
        };
      ]
    };
    
    (* Frame 5: Collection Point for Mark Allocation *)
    {
      id = 5;
      elements = [
        Label { text = "Runtime 4"; x = 10; y = 25 };
        Timeline { runtime = 4; y = 40; phases = 6 };
        Allocation { x = 100 + block_width/2; y = 40 + block_height + 15; id = "sweep-alloc" };
        Bar { 
          from_x = 100 + block_width/2; 
          to_x = 100 + (block_width + block_spacing) * 2 + block_width/2;
          y = 40 + block_height + 25; 
          label = "1"; 
          id = "sweep-bar" 
        };
        Collection { 
          x = 100 + (block_width + block_spacing) * 2 + block_width/2; 
          y = 40 + block_height + 15; 
          id = "sweep-collect" 
        };
        Allocation { 
          x = 100 + block_width + block_spacing + block_width/2; 
          y = 40 + block_height + 45; 
          id = "mark-alloc" 
        };
        Bar {
          from_x = 100 + block_width + block_spacing + block_width/2;
          to_x = 100 + (block_width + block_spacing) * 4 + block_width/2;
          y = 40 + block_height + 55;
          label = "1.5";
          id = "mark-bar"
        };
        Collection {
          x = 100 + (block_width + block_spacing) * 4 + block_width/2;
          y = 40 + block_height + 45;
          id = "mark-collect"
        };
      ]
    };
    
    (* Frame 6: Add Runtime 5 Timeline *)
    {
      id = 6;
      elements = [
        Label { text = "Runtime 4"; x = 10; y = 25 };
        Timeline { runtime = 4; y = 40; phases = 6 };
        Allocation { x = 100 + block_width/2; y = 40 + block_height + 15; id = "sweep-alloc" };
        Bar { 
          from_x = 100 + block_width/2; 
          to_x = 100 + (block_width + block_spacing) * 2 + block_width/2;
          y = 40 + block_height + 25; 
          label = "1"; 
          id = "sweep-bar" 
        };
        Collection { 
          x = 100 + (block_width + block_spacing) * 2 + block_width/2; 
          y = 40 + block_height + 15; 
          id = "sweep-collect" 
        };
        Allocation { 
          x = 100 + block_width + block_spacing + block_width/2; 
          y = 40 + block_height + 45; 
          id = "mark-alloc" 
        };
        Bar {
          from_x = 100 + block_width + block_spacing + block_width/2;
          to_x = 100 + (block_width + block_spacing) * 4 + block_width/2;
          y = 40 + block_height + 55;
          label = "1.5";
          id = "mark-bar"
        };
        Collection {
          x = 100 + (block_width + block_spacing) * 4 + block_width/2;
          y = 40 + block_height + 45;
          id = "mark-collect"
        };
        Label { text = "Runtime 5"; x = 10; y = rt5_y - 15 };
        Timeline { runtime = 5; y = rt5_y; phases = 3 };
      ]
    };
    
    (* Frame 7: Runtime 5 First Allocation *)
    {
      id = 7;
      elements = [
        Label { text = "Runtime 4"; x = 10; y = 25 };
        Timeline { runtime = 4; y = 40; phases = 6 };
        Allocation { x = 100 + block_width/2; y = 40 + block_height + 15; id = "sweep-alloc" };
        Bar { 
          from_x = 100 + block_width/2; 
          to_x = 100 + (block_width + block_spacing) * 2 + block_width/2;
          y = 40 + block_height + 25; 
          label = "1"; 
          id = "sweep-bar" 
        };
        Collection { 
          x = 100 + (block_width + block_spacing) * 2 + block_width/2; 
          y = 40 + block_height + 15; 
          id = "sweep-collect" 
        };
        Allocation { 
          x = 100 + block_width + block_spacing + block_width/2; 
          y = 40 + block_height + 45; 
          id = "mark-alloc" 
        };
        Bar {
          from_x = 100 + block_width + block_spacing + block_width/2;
          to_x = 100 + (block_width + block_spacing) * 4 + block_width/2;
          y = 40 + block_height + 55;
          label = "1.5";
          id = "mark-bar"
        };
        Collection {
          x = 100 + (block_width + block_spacing) * 4 + block_width/2;
          y = 40 + block_height + 45;
          id = "mark-collect"
        };
        Label { text = "Runtime 5"; x = 10; y = rt5_y - 15 };
        Timeline { runtime = 5; y = rt5_y; phases = 3 };
        Allocation { x = rt5_alloc_x1; y = rt5_y + block_height + 15; id = "rt5-alloc1" };
      ]
    };
    
    (* Frame 8: Runtime 5 First Collection *)
    {
      id = 8;
      elements = [
        Label { text = "Runtime 4"; x = 10; y = 25 };
        Timeline { runtime = 4; y = 40; phases = 6 };
        Allocation { x = 100 + block_width/2; y = 40 + block_height + 15; id = "sweep-alloc" };
        Bar { 
          from_x = 100 + block_width/2; 
          to_x = 100 + (block_width + block_spacing) * 2 + block_width/2;
          y = 40 + block_height + 25; 
          label = "1"; 
          id = "sweep-bar" 
        };
        Collection { 
          x = 100 + (block_width + block_spacing) * 2 + block_width/2; 
          y = 40 + block_height + 15; 
          id = "sweep-collect" 
        };
        Allocation { 
          x = 100 + block_width + block_spacing + block_width/2; 
          y = 40 + block_height + 45; 
          id = "mark-alloc" 
        };
        Bar {
          from_x = 100 + block_width + block_spacing + block_width/2;
          to_x = 100 + (block_width + block_spacing) * 4 + block_width/2;
          y = 40 + block_height + 55;
          label = "1.5";
          id = "mark-bar"
        };
        Collection {
          x = 100 + (block_width + block_spacing) * 4 + block_width/2;
          y = 40 + block_height + 45;
          id = "mark-collect"
        };
        Label { text = "Runtime 5"; x = 10; y = rt5_y - 15 };
        Timeline { runtime = 5; y = rt5_y; phases = 3 };
        Allocation { x = rt5_alloc_x1; y = rt5_y + block_height + 15; id = "rt5-alloc1" };
        Bar {
          from_x = rt5_alloc_x1;
          to_x = rt5_collect_x;
          y = rt5_y + block_height + 25;
          label = "2";
          id = "rt5-bar1"
        };
        Collection { x = rt5_collect_x; y = rt5_y + block_height + 15; id = "rt5-collect1" };
      ]
    };
    
    (* Frame 9: Runtime 5 Second Allocation *)
    {
      id = 9;
      elements = [
        Label { text = "Runtime 4"; x = 10; y = 25 };
        Timeline { runtime = 4; y = 40; phases = 6 };
        Allocation { x = 100 + block_width/2; y = 40 + block_height + 15; id = "sweep-alloc" };
        Bar { 
          from_x = 100 + block_width/2; 
          to_x = 100 + (block_width + block_spacing) * 2 + block_width/2;
          y = 40 + block_height + 25; 
          label = "1"; 
          id = "sweep-bar" 
        };
        Collection { 
          x = 100 + (block_width + block_spacing) * 2 + block_width/2; 
          y = 40 + block_height + 15; 
          id = "sweep-collect" 
        };
        Allocation { 
          x = 100 + block_width + block_spacing + block_width/2; 
          y = 40 + block_height + 45; 
          id = "mark-alloc" 
        };
        Bar {
          from_x = 100 + block_width + block_spacing + block_width/2;
          to_x = 100 + (block_width + block_spacing) * 4 + block_width/2;
          y = 40 + block_height + 55;
          label = "1.5";
          id = "mark-bar"
        };
        Collection {
          x = 100 + (block_width + block_spacing) * 4 + block_width/2;
          y = 40 + block_height + 45;
          id = "mark-collect"
        };
        Label { text = "Runtime 5"; x = 10; y = rt5_y - 15 };
        Timeline { runtime = 5; y = rt5_y; phases = 3 };
        Allocation { x = rt5_alloc_x1; y = rt5_y + block_height + 15; id = "rt5-alloc1" };
        Bar {
          from_x = rt5_alloc_x1;
          to_x = rt5_collect_x;
          y = rt5_y + block_height + 25;
          label = "2";
          id = "rt5-bar1"
        };
        Collection { x = rt5_collect_x; y = rt5_y + block_height + 15; id = "rt5-collect1" };
        Allocation { x = rt5_alloc_x2; y = rt5_y + block_height + 45; id = "rt5-alloc2" };
      ]
    };
    
    (* Frame 10: Runtime 5 Second Collection *)
    {
      id = 10;
      elements = [
        Label { text = "Runtime 4"; x = 10; y = 25 };
        Timeline { runtime = 4; y = 40; phases = 6 };
        Allocation { x = 100 + block_width/2; y = 40 + block_height + 15; id = "sweep-alloc" };
        Bar { 
          from_x = 100 + block_width/2; 
          to_x = 100 + (block_width + block_spacing) * 2 + block_width/2;
          y = 40 + block_height + 25; 
          label = "1"; 
          id = "sweep-bar" 
        };
        Collection { 
          x = 100 + (block_width + block_spacing) * 2 + block_width/2; 
          y = 40 + block_height + 15; 
          id = "sweep-collect" 
        };
        Allocation { 
          x = 100 + block_width + block_spacing + block_width/2; 
          y = 40 + block_height + 45; 
          id = "mark-alloc" 
        };
        Bar {
          from_x = 100 + block_width + block_spacing + block_width/2;
          to_x = 100 + (block_width + block_spacing) * 4 + block_width/2;
          y = 40 + block_height + 55;
          label = "1.5";
          id = "mark-bar"
        };
        Collection {
          x = 100 + (block_width + block_spacing) * 4 + block_width/2;
          y = 40 + block_height + 45;
          id = "mark-collect"
        };
        Label { text = "Runtime 5"; x = 10; y = rt5_y - 15 };
        Timeline { runtime = 5; y = rt5_y; phases = 3 };
        Allocation { x = rt5_alloc_x1; y = rt5_y + block_height + 15; id = "rt5-alloc1" };
        Bar {
          from_x = rt5_alloc_x1;
          to_x = rt5_collect_x;
          y = rt5_y + block_height + 25;
          label = "2";
          id = "rt5-bar1"
        };
        Collection { x = rt5_collect_x; y = rt5_y + block_height + 15; id = "rt5-collect1" };
        Allocation { x = rt5_alloc_x2; y = rt5_y + block_height + 45; id = "rt5-alloc2" };
        Bar {
          from_x = rt5_alloc_x2;
          to_x = rt5_collect_x;
          y = rt5_y + block_height + 55;
          label = "1.5";
          id = "rt5-bar2"
        };
        Collection { x = rt5_collect_x; y = rt5_y + block_height + 45; id = "rt5-collect2" };
      ]
    };
  ] in
  frames

let generate_frame_html frame =
  let elements_html = 
    List.map frame.elements ~f:generate_svg_element
    |> String.concat ~sep:"\n                "
  in
  let active_class = if frame.id = 1 then " active" else "" in
  Printf.sprintf {|            <g class="frame frame-%d%s">
                %s
            </g>|} frame.id active_class elements_html

let generate_html () =
  let frames = generate_frames () in
  let frames_html = 
    List.map frames ~f:generate_frame_html
    |> String.concat ~sep:"\n"
  in
  Printf.sprintf {|<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Floating Garbage Animation</title>
    <style>
        body {
            margin: 0;
            padding: 10px;
            font-family: Arial, sans-serif;
            background-color: white;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        
        #animation-container {
            width: 98%%;
            max-width: 100%%;
        }
        
        svg {
            display: block;
            margin: 0 auto;
            width: 100%%;
            height: auto;
            max-width: 100%%;
        }
        
        .label {
            font-size: 16px;
            font-weight: bold;
        }
        
        .phase-label {
            font-size: 14px;
            fill: white;
            font-weight: bold;
        }
        
        .frame {
            display: none;
        }
        
        .frame.active {
            display: block;
        }
        
        .allocation, .collection, .arrow, .bar {
            opacity: 0;
            animation: fadeIn 0.5s forwards;
        }
        
        @keyframes fadeIn {
            to { opacity: 1; }
        }
        
        .bar-label {
            font-size: 12px;
            fill: #666;
        }
    </style>
</head>
<body>
    <div id="animation-container">
        <svg viewBox="0 0 700 260" preserveAspectRatio="xMidYMid meet">
            <defs>
                <marker id="arrowhead" markerWidth="10" markerHeight="7" 
                        refX="9" refY="3.5" orient="auto">
                    <polygon points="0 0, 10 3.5, 0 7" fill="%s" />
                </marker>
            </defs>
%s
        </svg>
    </div>
    
    <script>
        let currentFrame = 1;
        const totalFrames = %d;
        
        function showFrame(n) {
            // Hide all frames
            document.querySelectorAll('.frame').forEach(frame => {
                frame.classList.remove('active');
            });
            
            // Show current frame
            document.querySelector('.frame-' + n).classList.add('active');
            
            currentFrame = n;
        }
        
        function nextFrame() {
            if (currentFrame < totalFrames) {
                showFrame(currentFrame + 1);
            }
        }
        
        function prevFrame() {
            if (currentFrame > 1) {
                showFrame(currentFrame - 1);
            }
        }
        
        // Keyboard navigation
        document.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowRight' || e.key === ' ') {
                e.preventDefault();
                nextFrame();
            } else if (e.key === 'ArrowLeft') {
                e.preventDefault();
                prevFrame();
            }
        });
        
        // Initialize
        showFrame(1);
    </script>
</body>
</html>|} arrow_color frames_html (List.length frames)

let () =
  let html = generate_html () in
  Out_channel.write_all "index.html" ~data:html;
  printf "Generated index.html\n"