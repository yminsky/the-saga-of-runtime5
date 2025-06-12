#!/usr/bin/env python3

import json

class HeapAnimation:
    def __init__(self, width=1400, height=700):
        self.width = width
        self.height = height
        self.colors = {
            'marked': '#4CAF50',      # Green for marked objects
            'unmarked': '#FF5252',    # Red for unmarked objects
            'root': '#2196F3',        # Blue for roots
            'background': '#F5F5F5',  # Light gray background
            'section_bg': 'white',    # White section background
            'arrow': '#333333',       # Darker for better visibility
            'arrow_active': '#8B1538', # Burgundy for active arrows
            'text': '#333333',        # Dark gray for text
            'sweep_highlight': '#DDDDDD'  # Gray for sweep highlight
        }
        self.frames = []
        self.heap_dims = None
        self.scan_time_ms = 100  # Time per frame in auto-advance mode (milliseconds)
        
    def create_frame(self, roots, heap_slots, connections, title="", sweep_position=None, active_connections=None):
        """Create a single frame of the animation"""
        frame = {
            'title': title,
            'roots': roots,
            'heap_slots': heap_slots,
            'connections': connections,
            'sweep_position': sweep_position,
            'active_connections': active_connections or []
        }
        self.frames.append(frame)
        
    def generate_animation(self):
        """Generate the complete animation sequence"""
        # Grid configuration
        cols = 10
        rows = 5
        slot_size = 60
        slot_spacing = 15
        margin = 30  # Margin from heap edges
        
        # Calculate exact heap dimensions based on grid
        heap_width = margin * 2 + cols * slot_size + (cols - 1) * slot_spacing
        heap_height = margin * 2 + rows * slot_size + (rows - 1) * slot_spacing
        
        # Define heap position
        heap_x = 180
        heap_y = 100
        
        # Store dimensions for HTML generation
        self.heap_dims = (heap_x, heap_y, heap_width, heap_height)
        
        # Calculate actual positions for grid slots
        heap_slots = []
        slot_id = 0
        for row in range(rows):
            for col in range(cols):
                x = heap_x + margin + col * (slot_size + slot_spacing)
                y = heap_y + margin + row * (slot_size + slot_spacing)
                heap_slots.append({
                    'id': slot_id,
                    'x': x,
                    'y': y,
                    'object': None
                })
                slot_id += 1
        
        # Root positions
        roots = [
            {'x': 90, 'y': 252.5, 'id': 'r1'},
            {'x': 90, 'y': 322.5, 'id': 'r2'},
            {'x': 90, 'y': 392.5, 'id': 'r3'}
        ]
        
        # Heap configuration - easy to modify
        heap_config = {
            'objects': [
                # Reachable objects
                {'id': 'obj0', 'slot': 5, 'points_to': ['obj3']},
                {'id': 'obj1', 'slot': 12, 'points_to': ['obj4']},
                {'id': 'obj2', 'slot': 18, 'points_to': []},
                {'id': 'obj3', 'slot': 15, 'points_to': ['obj5']},
                {'id': 'obj4', 'slot': 23, 'points_to': []},
                {'id': 'obj5', 'slot': 25, 'points_to': []},
                # Garbage objects
                {'id': 'obj6', 'slot': 31, 'points_to': ['obj7']},
                {'id': 'obj7', 'slot': 34, 'points_to': []},
                {'id': 'obj8', 'slot': 37, 'points_to': []},
                {'id': 'obj9', 'slot': 8, 'points_to': []},
                {'id': 'obj10', 'slot': 42, 'points_to': []},
            ],
            'roots': [
                {'id': 'r1', 'points_to': 'obj0'},
                {'id': 'r2', 'points_to': 'obj1'},
                {'id': 'r3', 'points_to': 'obj2'},
            ]
        }
        
        # Build reachability set
        reachable = set()
        def mark_reachable(obj_id):
            if obj_id in reachable:
                return
            reachable.add(obj_id)
            for obj in heap_config['objects']:
                if obj['id'] == obj_id:
                    for target in obj['points_to']:
                        mark_reachable(target)
                    break
        
        # Start from roots
        for root in heap_config['roots']:
            mark_reachable(root['points_to'])
        
        # Initialize heap with objects
        for obj in heap_config['objects']:
            slot_id = obj['slot']
            if slot_id < len(heap_slots):
                heap_slots[slot_id]['object'] = {
                    'id': obj['id'],
                    'state': 'unmarked',
                    'reachable': obj['id'] in reachable
                }
        
        # Build connections list
        connections = []
        # Root connections
        for root in heap_config['roots']:
            connections.append({'from': root['id'], 'to': root['points_to']})
        # Object connections
        for obj in heap_config['objects']:
            for target in obj['points_to']:
                connections.append({'from': obj['id'], 'to': target})
        
        # Frame 1: Initial state - all objects unmarked
        self.create_frame(roots, heap_slots, connections, "Marking")
        
        # Track all traversed connections during marking
        traversed_connections = []
        
        # Frame 2: Mark objects directly reachable from roots with active arrows
        heap_slots = self.copy_heap_slots(heap_slots)
        new_traversals = [{'from': 'r1', 'to': 'obj0'}, {'from': 'r2', 'to': 'obj1'}, {'from': 'r3', 'to': 'obj2'}]
        traversed_connections.extend(new_traversals)
        for slot in heap_slots:
            if slot['object'] and slot['object']['id'] in ['obj0', 'obj1', 'obj2']:
                slot['object']['state'] = 'marked'
        self.create_frame(roots, heap_slots, connections, "Marking", active_connections=traversed_connections.copy())
        
        # Frame 3: Mark objects reachable from obj0
        heap_slots = self.copy_heap_slots(heap_slots)
        new_traversals = [{'from': 'obj0', 'to': 'obj3'}]
        traversed_connections.extend(new_traversals)
        for slot in heap_slots:
            if slot['object'] and slot['object']['id'] == 'obj3':
                slot['object']['state'] = 'marked'
        self.create_frame(roots, heap_slots, connections, "Marking", active_connections=traversed_connections.copy())
        
        # Frame 4: Mark objects reachable from obj1 and obj3
        heap_slots = self.copy_heap_slots(heap_slots)
        new_traversals = [{'from': 'obj1', 'to': 'obj4'}, {'from': 'obj3', 'to': 'obj5'}]
        traversed_connections.extend(new_traversals)
        for slot in heap_slots:
            if slot['object'] and slot['object']['id'] in ['obj4', 'obj5']:
                slot['object']['state'] = 'marked'
        self.create_frame(roots, heap_slots, connections, "Marking", active_connections=traversed_connections.copy())
        
        # Sweep through each slot in order
        current_heap = self.copy_heap_slots(heap_slots)
        current_connections = connections.copy()
        
        for slot_idx in range(len(current_heap)):
            slot = current_heap[slot_idx]
            
            if slot['object']:
                obj = slot['object']
                if obj['state'] == 'unmarked':
                    # Remove garbage object
                    removed_id = obj['id']
                    slot['object'] = None
                    # Remove connections to/from this object
                    current_connections = [conn for conn in current_connections 
                                         if conn['from'] != removed_id and conn['to'] != removed_id]
                    self.create_frame(roots, self.copy_heap_slots(current_heap), current_connections, 
                                    "Sweeping", slot_idx, active_connections=[])
                else:  # marked
                    # Turn marked back to unmarked for next cycle
                    obj['state'] = 'unmarked'
                    self.create_frame(roots, self.copy_heap_slots(current_heap), current_connections, 
                                    "Sweeping", slot_idx, active_connections=[])
            else:
                # Empty slot - still show we're scanning it
                self.create_frame(roots, self.copy_heap_slots(current_heap), current_connections, 
                                "Sweeping", slot_idx, active_connections=[])
        
        # Final frame
        self.create_frame(roots, current_heap, current_connections, "Sweeping", sweep_position=None, active_connections=[])
        
    def copy_heap_slots(self, heap_slots):
        """Deep copy heap slots"""
        new_slots = []
        for slot in heap_slots:
            new_slot = {
                'id': slot['id'],
                'x': slot['x'],
                'y': slot['y'],
                'object': None
            }
            if slot['object']:
                new_slot['object'] = {
                    'id': slot['object']['id'],
                    'state': slot['object']['state'],
                    'reachable': slot['object']['reachable']
                }
            new_slots.append(new_slot)
        return new_slots
        
    def generate_html(self):
        """Generate the HTML file with the animation"""
        if not self.heap_dims:
            raise ValueError("Must call generate_animation() before generate_html()")
            
        heap_x, heap_y, heap_width, heap_height = self.heap_dims
        
        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Heap Marking Animation</title>
    <style>
        body {{
            margin: 0;
            padding: 20px;
            font-family: Arial, sans-serif;
            background-color: #f0f0f0;
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
        #container {{
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            padding: 20px;
        }}
        svg {{
            display: block;
        }}
        #controls {{
            margin-top: 20px;
            text-align: center;
        }}
        #title {{
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 20px;
            text-align: center;
            color: #333;
        }}
        .control-hint {{
            margin-top: 10px;
            font-size: 14px;
            color: #666;
        }}
    </style>
</head>
<body>
    <div id="container">
        <div id="title"></div>
        <svg id="animation" width="{self.width}" height="{self.height}" viewBox="0 0 {self.width} {self.height}">
            <defs>
                <marker id="arrowhead" markerWidth="15" markerHeight="15" refX="15" refY="7.5" orient="auto">
                    <polygon points="0,0 15,7.5 0,15" fill="{self.colors['arrow']}" stroke="none"/>
                </marker>
            </defs>
        </svg>
        <div id="controls">
            <div class="control-hint">Use ← → or Space to navigate | C to auto-advance</div>
        </div>
    </div>
    
    <script>
        const frames = {json.dumps(self.frames)};
        let currentFrame = 0;
        let autoAdvanceInterval = null;
        const scanTimeMs = {self.scan_time_ms};
        
        const svg = document.getElementById('animation');
        const titleElement = document.getElementById('title');
        
        function drawFrame(frameIndex) {{
            const frame = frames[frameIndex];
            titleElement.textContent = frame.title;
            
            // Clear SVG except defs
            while (svg.childNodes.length > 1) {{
                svg.removeChild(svg.lastChild);
            }}
            
            // Background
            const bg = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
            bg.setAttribute('x', '0');
            bg.setAttribute('y', '0');
            bg.setAttribute('width', '{self.width}');
            bg.setAttribute('height', '{self.height}');
            bg.setAttribute('fill', '{self.colors['background']}');
            svg.appendChild(bg);
            
            // Stack section
            drawSection(40, 200, 100, 250, 'Stack');
            
            // Heap section
            drawSection({heap_x}, {heap_y}, {heap_width}, {heap_height}, 'Heap');
            
            // Draw heap slots (grid)
            frame.heap_slots.forEach((slot, idx) => {{
                const isBeingSwept = frame.sweep_position === idx;
                drawHeapSlot(slot, isBeingSwept);
            }});
            
            // Draw connections
            frame.connections.forEach(conn => {{
                const isActive = frame.active_connections.some(ac => 
                    ac.from === conn.from && ac.to === conn.to
                );
                drawConnection(conn, frame.heap_slots, isActive);
            }});
            
            // Draw roots
            frame.roots.forEach((root, index) => {{
                drawObject(55, 230 + index * 70, 70, 45, 'root');
            }});
            
            // Draw legend
            drawLegend();
        }}
        
        function drawSection(x, y, width, height, label) {{
            const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
            rect.setAttribute('x', x);
            rect.setAttribute('y', y);
            rect.setAttribute('width', width);
            rect.setAttribute('height', height);
            rect.setAttribute('fill', '{self.colors['section_bg']}');
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
            text.setAttribute('fill', '{self.colors['text']}');
            text.textContent = label;
            svg.appendChild(text);
        }}
        
        function drawHeapSlot(slot, isBeingSwept) {{
            // Draw slot background if being swept
            if (isBeingSwept) {{
                const bg = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
                bg.setAttribute('x', slot.x - 5);
                bg.setAttribute('y', slot.y - 5);
                bg.setAttribute('width', 65);
                bg.setAttribute('height', 65);
                bg.setAttribute('fill', '{self.colors['sweep_highlight']}');
                bg.setAttribute('rx', '3');
                bg.setAttribute('ry', '3');
                svg.appendChild(bg);
            }}
            
            // Draw object if present
            if (slot.object) {{
                drawObject(slot.x, slot.y, 55, 55, slot.object.state);
            }}
        }}
        
        function drawObject(x, y, width, height, type) {{
            const colors = {{
                'root': '{self.colors['root']}',
                'marked': '{self.colors['marked']}',
                'unmarked': '{self.colors['unmarked']}'
            }};
            
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
        }}
        
        function drawConnection(conn, heap_slots, isActive) {{
            // Find positions
            let fromX, fromY, toX, toY;
            
            if (conn.from.startsWith('r')) {{
                // From root
                const rootIndex = parseInt(conn.from[1]) - 1;
                fromX = 125;
                fromY = 252.5 + rootIndex * 70;
            }} else {{
                // From heap object
                const fromSlot = heap_slots.find(s => s.object && s.object.id === conn.from);
                if (!fromSlot) return;
                fromX = fromSlot.x + 27.5;
                fromY = fromSlot.y + 27.5;
            }}
            
            // To heap object
            const toSlot = heap_slots.find(s => s.object && s.object.id === conn.to);
            if (!toSlot) return;
            toX = toSlot.x + 27.5;
            toY = toSlot.y + 27.5;
            
            // Adjust endpoints
            if (conn.from.startsWith('r')) {{
                toX -= 27.5;
            }}
            
            const color = isActive ? '{self.colors['arrow_active']}' : '{self.colors['arrow']}';
            drawArrow(fromX, fromY, toX, toY, color);
        }}
        
        function drawArrow(x1, y1, x2, y2, color) {{
            const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
            line.setAttribute('x1', x1);
            line.setAttribute('y1', y1);
            line.setAttribute('x2', x2);
            line.setAttribute('y2', y2);
            line.setAttribute('stroke', color || '{self.colors['arrow']}');
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
            const points = `${{x2}},${{y2}} ${{baseX + perpX * arrowWidth}},${{baseY + perpY * arrowWidth}} ${{baseX - perpX * arrowWidth}},${{baseY - perpY * arrowWidth}}`;
            
            const polygon = document.createElementNS('http://www.w3.org/2000/svg', 'polygon');
            polygon.setAttribute('points', points);
            polygon.setAttribute('fill', color || '{self.colors['arrow']}');
            svg.appendChild(polygon);
        }}
        
        function drawLegend() {{
            // Legend background
            const legendBg = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
            legendBg.setAttribute('x', '1200');
            legendBg.setAttribute('y', '240');
            legendBg.setAttribute('width', '180');
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
            legendTitle.setAttribute('x', '1280');
            legendTitle.setAttribute('y', '265');
            legendTitle.setAttribute('text-anchor', 'middle');
            legendTitle.setAttribute('font-family', 'Arial, sans-serif');
            legendTitle.setAttribute('font-size', '16');
            legendTitle.setAttribute('font-weight', 'bold');
            legendTitle.setAttribute('fill', '{self.colors['text']}');
            legendTitle.textContent = 'Legend';
            svg.appendChild(legendTitle);
            
            // Legend entries
            const entries = [
                {{color: '{self.colors['root']}', label: 'Root'}},
                {{color: '{self.colors['marked']}', label: 'Marked'}},
                {{color: '{self.colors['unmarked']}', label: 'Unmarked'}}
            ];
            
            entries.forEach((entry, index) => {{
                const y = 290 + index * 35;
                
                // Color box
                const box = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
                box.setAttribute('x', '1220');
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
                label.setAttribute('x', '1245');
                label.setAttribute('y', y + 15);
                label.setAttribute('font-family', 'Arial, sans-serif');
                label.setAttribute('font-size', '14');
                label.setAttribute('fill', '{self.colors['text']}');
                label.textContent = entry.label;
                svg.appendChild(label);
            }});
        }}
        
        function nextFrame() {{
            if (currentFrame < frames.length - 1) {{
                currentFrame++;
                drawFrame(currentFrame);
            }} else {{
                stopAutoAdvance();
            }}
        }}
        
        function prevFrame() {{
            if (currentFrame > 0) {{
                currentFrame--;
                drawFrame(currentFrame);
            }}
        }}
        
        function startAutoAdvance() {{
            if (autoAdvanceInterval) return; // Already running
            
            autoAdvanceInterval = setInterval(() => {{
                nextFrame();
            }}, scanTimeMs);
        }}
        
        function stopAutoAdvance() {{
            if (autoAdvanceInterval) {{
                clearInterval(autoAdvanceInterval);
                autoAdvanceInterval = null;
            }}
        }}
        
        // Keyboard navigation
        document.addEventListener('keydown', (e) => {{
            if (e.key === 'ArrowRight' || e.key === ' ') {{
                e.preventDefault();
                stopAutoAdvance();
                nextFrame();
            }} else if (e.key === 'ArrowLeft') {{
                e.preventDefault();
                stopAutoAdvance();
                prevFrame();
            }} else if (e.key === 'c' || e.key === 'C') {{
                e.preventDefault();
                if (autoAdvanceInterval) {{
                    stopAutoAdvance();
                }} else {{
                    startAutoAdvance();
                }}
            }}
        }});
        
        // Initial draw
        drawFrame(0);
    </script>
</body>
</html>'''
        return html
        
    def save_html(self, filename='heap_animation.html'):
        """Save the animation as an HTML file"""
        self.generate_animation()
        html = self.generate_html()
        with open(filename, 'w') as f:
            f.write(html)
        print(f"Generated {filename}")

if __name__ == '__main__':
    animation = HeapAnimation()
    animation.save_html()