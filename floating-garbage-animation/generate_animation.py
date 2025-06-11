#!/usr/bin/env python3
"""
Generate HTML for the floating garbage animation.
"""

def generate_html():
    # Configuration
    block_width = 80
    block_height = 40
    block_spacing = 5
    timeline_spacing = 120
    
    # Colors
    sweep_color = "#4682B4"  # Blue
    mark_color = "#228B22"   # Green
    merged_color = "#6B46C1" # Purple
    allocation_color = "#DC143C"  # Red
    arrow_color = "#666666"
    
    # Generate frames data
    frames = []
    
    # Frame 1: Initial Runtime 4 Timeline
    frames.append({
        'id': 1,
        'elements': [
            {'type': 'label', 'text': 'Runtime 4', 'x': 10, 'y': 25},
            {'type': 'timeline', 'runtime': 4, 'y': 40, 'phases': 6}
        ]
    })
    
    # Frame 2: Allocation in Sweep Phase
    frames.append({
        'id': 2,
        'elements': [
            {'type': 'label', 'text': 'Runtime 4', 'x': 10, 'y': 25},
            {'type': 'timeline', 'runtime': 4, 'y': 40, 'phases': 6},
            {'type': 'allocation', 'x': 100 + block_width//2, 'y': 40 + block_height + 15, 'id': 'sweep-alloc'}
        ]
    })
    
    # Frame 3: Collection Point for Sweep Allocation
    frames.append({
        'id': 3,
        'elements': [
            {'type': 'label', 'text': 'Runtime 4', 'x': 10, 'y': 25},
            {'type': 'timeline', 'runtime': 4, 'y': 40, 'phases': 6},
            {'type': 'allocation', 'x': 100 + block_width//2, 'y': 40 + block_height + 15, 'id': 'sweep-alloc'},
            {'type': 'bar', 'from_x': 100 + block_width//2, 'to_x': 100 + (block_width + block_spacing) * 2 + block_width//2,
             'y': 40 + block_height + 25, 'label': '1', 'id': 'sweep-bar'},
            {'type': 'collection', 'x': 100 + (block_width + block_spacing) * 2 + block_width//2, 
             'y': 40 + block_height + 15, 'id': 'sweep-collect'}
        ]
    })
    
    # Frame 4: Add Mark Allocation
    frames.append({
        'id': 4,
        'elements': [
            {'type': 'label', 'text': 'Runtime 4', 'x': 10, 'y': 25},
            {'type': 'timeline', 'runtime': 4, 'y': 40, 'phases': 6},
            {'type': 'allocation', 'x': 100 + block_width//2, 'y': 40 + block_height + 15, 'id': 'sweep-alloc'},
            {'type': 'bar', 'from_x': 100 + block_width//2, 'to_x': 100 + (block_width + block_spacing) * 2 + block_width//2,
             'y': 40 + block_height + 25, 'label': '1', 'id': 'sweep-bar'},
            {'type': 'collection', 'x': 100 + (block_width + block_spacing) * 2 + block_width//2, 
             'y': 40 + block_height + 15, 'id': 'sweep-collect'},
            {'type': 'allocation', 'x': 100 + block_width + block_spacing + block_width//2, 
             'y': 40 + block_height + 45, 'id': 'mark-alloc'}
        ]
    })
    
    # Frame 5: Collection Point for Mark Allocation
    # Collection happens in [S] after the next [M], which is position 4 (0-indexed)
    frames.append({
        'id': 5,
        'elements': [
            {'type': 'label', 'text': 'Runtime 4', 'x': 10, 'y': 25},
            {'type': 'timeline', 'runtime': 4, 'y': 40, 'phases': 6},
            {'type': 'allocation', 'x': 100 + block_width//2, 'y': 40 + block_height + 15, 'id': 'sweep-alloc'},
            {'type': 'bar', 'from_x': 100 + block_width//2, 'to_x': 100 + (block_width + block_spacing) * 2 + block_width//2,
             'y': 40 + block_height + 25, 'label': '1', 'id': 'sweep-bar'},
            {'type': 'collection', 'x': 100 + (block_width + block_spacing) * 2 + block_width//2, 
             'y': 40 + block_height + 15, 'id': 'sweep-collect'},
            {'type': 'allocation', 'x': 100 + block_width + block_spacing + block_width//2, 
             'y': 40 + block_height + 45, 'id': 'mark-alloc'},
            {'type': 'bar', 'from_x': 100 + block_width + block_spacing + block_width//2,
             'to_x': 100 + (block_width + block_spacing) * 4 + block_width//2,
             'y': 40 + block_height + 55, 'label': '1.5', 'id': 'mark-bar'},
            {'type': 'collection', 'x': 100 + (block_width + block_spacing) * 4 + block_width//2,
             'y': 40 + block_height + 45, 'id': 'mark-collect'}
        ]
    })
    
    # Frame 6: Add Runtime 5 Timeline
    rt5_y = 40 + timeline_spacing
    frames.append({
        'id': 6,
        'elements': [
            {'type': 'label', 'text': 'Runtime 4', 'x': 10, 'y': 25},
            {'type': 'timeline', 'runtime': 4, 'y': 40, 'phases': 6},
            {'type': 'allocation', 'x': 100 + block_width//2, 'y': 40 + block_height + 15, 'id': 'sweep-alloc'},
            {'type': 'bar', 'from_x': 100 + block_width//2, 'to_x': 100 + (block_width + block_spacing) * 2 + block_width//2,
             'y': 40 + block_height + 25, 'label': '1', 'id': 'sweep-bar'},
            {'type': 'collection', 'x': 100 + (block_width + block_spacing) * 2 + block_width//2, 
             'y': 40 + block_height + 15, 'id': 'sweep-collect'},
            {'type': 'allocation', 'x': 100 + block_width + block_spacing + block_width//2, 
             'y': 40 + block_height + 45, 'id': 'mark-alloc'},
            {'type': 'bar', 'from_x': 100 + block_width + block_spacing + block_width//2,
             'to_x': 100 + (block_width + block_spacing) * 4 + block_width//2,
             'y': 40 + block_height + 55, 'label': '1.5', 'id': 'mark-bar'},
            {'type': 'collection', 'x': 100 + (block_width + block_spacing) * 4 + block_width//2,
             'y': 40 + block_height + 45, 'id': 'mark-collect'},
            {'type': 'label', 'text': 'Runtime 5', 'x': 10, 'y': rt5_y - 15},
            {'type': 'timeline', 'runtime': 5, 'y': rt5_y, 'phases': 3}
        ]
    })
    
    # Frame 7: Runtime 5 First Allocation
    # First allocation point in first half of S/M (aligned with S)
    rt5_alloc_x1 = 100 + block_width//2  # Aligned with sweep allocation
    rt5_alloc_x2 = 100 + block_width + block_spacing + block_width//2  # Aligned with mark allocation
    frames.append({
        'id': 7,
        'elements': [
            {'type': 'label', 'text': 'Runtime 4', 'x': 10, 'y': 25},
            {'type': 'timeline', 'runtime': 4, 'y': 40, 'phases': 6},
            {'type': 'allocation', 'x': 100 + block_width//2, 'y': 40 + block_height + 15, 'id': 'sweep-alloc'},
            {'type': 'bar', 'from_x': 100 + block_width//2, 'to_x': 100 + (block_width + block_spacing) * 2 + block_width//2,
             'y': 40 + block_height + 25, 'label': '1', 'id': 'sweep-bar'},
            {'type': 'collection', 'x': 100 + (block_width + block_spacing) * 2 + block_width//2, 
             'y': 40 + block_height + 15, 'id': 'sweep-collect'},
            {'type': 'allocation', 'x': 100 + block_width + block_spacing + block_width//2, 
             'y': 40 + block_height + 45, 'id': 'mark-alloc'},
            {'type': 'bar', 'from_x': 100 + block_width + block_spacing + block_width//2,
             'to_x': 100 + (block_width + block_spacing) * 4 + block_width//2,
             'y': 40 + block_height + 55, 'label': '1.5', 'id': 'mark-bar'},
            {'type': 'collection', 'x': 100 + (block_width + block_spacing) * 4 + block_width//2,
             'y': 40 + block_height + 45, 'id': 'mark-collect'},
            {'type': 'label', 'text': 'Runtime 5', 'x': 10, 'y': rt5_y - 15},
            {'type': 'timeline', 'runtime': 5, 'y': rt5_y, 'phases': 3},
            {'type': 'allocation', 'x': rt5_alloc_x1, 'y': rt5_y + block_height + 15, 'id': 'rt5-alloc1'}
        ]
    })
    
    # Frame 8: Runtime 5 Second Allocation
    frames.append({
        'id': 8,
        'elements': [
            {'type': 'label', 'text': 'Runtime 4', 'x': 10, 'y': 25},
            {'type': 'timeline', 'runtime': 4, 'y': 40, 'phases': 6},
            {'type': 'allocation', 'x': 100 + block_width//2, 'y': 40 + block_height + 15, 'id': 'sweep-alloc'},
            {'type': 'bar', 'from_x': 100 + block_width//2, 'to_x': 100 + (block_width + block_spacing) * 2 + block_width//2,
             'y': 40 + block_height + 25, 'label': '1', 'id': 'sweep-bar'},
            {'type': 'collection', 'x': 100 + (block_width + block_spacing) * 2 + block_width//2, 
             'y': 40 + block_height + 15, 'id': 'sweep-collect'},
            {'type': 'allocation', 'x': 100 + block_width + block_spacing + block_width//2, 
             'y': 40 + block_height + 45, 'id': 'mark-alloc'},
            {'type': 'bar', 'from_x': 100 + block_width + block_spacing + block_width//2,
             'to_x': 100 + (block_width + block_spacing) * 4 + block_width//2,
             'y': 40 + block_height + 55, 'label': '1.5', 'id': 'mark-bar'},
            {'type': 'collection', 'x': 100 + (block_width + block_spacing) * 4 + block_width//2,
             'y': 40 + block_height + 45, 'id': 'mark-collect'},
            {'type': 'label', 'text': 'Runtime 5', 'x': 10, 'y': rt5_y - 15},
            {'type': 'timeline', 'runtime': 5, 'y': rt5_y, 'phases': 3},
            {'type': 'allocation', 'x': rt5_alloc_x1, 'y': rt5_y + block_height + 15, 'id': 'rt5-alloc1'},
            {'type': 'allocation', 'x': rt5_alloc_x2, 'y': rt5_y + block_height + 45, 'id': 'rt5-alloc2'}
        ]
    })
    
    # Frame 9: Runtime 5 First Collection
    # First allocation is collected 2 full cycles later
    # Collection happens in the middle of the first half of the third [S/M] block
    rt5_collect_x = 100 + (block_width * 2 + block_spacing) * 2 + block_width//2
    frames.append({
        'id': 9,
        'elements': [
            {'type': 'label', 'text': 'Runtime 4', 'x': 10, 'y': 25},
            {'type': 'timeline', 'runtime': 4, 'y': 40, 'phases': 6},
            {'type': 'allocation', 'x': 100 + block_width//2, 'y': 40 + block_height + 15, 'id': 'sweep-alloc'},
            {'type': 'bar', 'from_x': 100 + block_width//2, 'to_x': 100 + (block_width + block_spacing) * 2 + block_width//2,
             'y': 40 + block_height + 25, 'label': '1', 'id': 'sweep-bar'},
            {'type': 'collection', 'x': 100 + (block_width + block_spacing) * 2 + block_width//2, 
             'y': 40 + block_height + 15, 'id': 'sweep-collect'},
            {'type': 'allocation', 'x': 100 + block_width + block_spacing + block_width//2, 
             'y': 40 + block_height + 45, 'id': 'mark-alloc'},
            {'type': 'bar', 'from_x': 100 + block_width + block_spacing + block_width//2,
             'to_x': 100 + (block_width + block_spacing) * 4 + block_width//2,
             'y': 40 + block_height + 55, 'label': '1.5', 'id': 'mark-bar'},
            {'type': 'collection', 'x': 100 + (block_width + block_spacing) * 4 + block_width//2,
             'y': 40 + block_height + 45, 'id': 'mark-collect'},
            {'type': 'label', 'text': 'Runtime 5', 'x': 10, 'y': rt5_y - 15},
            {'type': 'timeline', 'runtime': 5, 'y': rt5_y, 'phases': 3},
            {'type': 'allocation', 'x': rt5_alloc_x1, 'y': rt5_y + block_height + 15, 'id': 'rt5-alloc1'},
            {'type': 'bar', 'from_x': rt5_alloc_x1, 'to_x': rt5_collect_x,
             'y': rt5_y + block_height + 25, 'label': '2', 'id': 'rt5-bar1'},
            {'type': 'collection', 'x': rt5_collect_x, 'y': rt5_y + block_height + 15, 'id': 'rt5-collect1'}
        ]
    })
    
    # Frame 10: Runtime 5 Second Allocation and Collection
    frames.append({
        'id': 10,
        'elements': [
            {'type': 'label', 'text': 'Runtime 4', 'x': 10, 'y': 25},
            {'type': 'timeline', 'runtime': 4, 'y': 40, 'phases': 6},
            {'type': 'allocation', 'x': 100 + block_width//2, 'y': 40 + block_height + 15, 'id': 'sweep-alloc'},
            {'type': 'bar', 'from_x': 100 + block_width//2, 'to_x': 100 + (block_width + block_spacing) * 2 + block_width//2,
             'y': 40 + block_height + 25, 'label': '1', 'id': 'sweep-bar'},
            {'type': 'collection', 'x': 100 + (block_width + block_spacing) * 2 + block_width//2, 
             'y': 40 + block_height + 15, 'id': 'sweep-collect'},
            {'type': 'allocation', 'x': 100 + block_width + block_spacing + block_width//2, 
             'y': 40 + block_height + 45, 'id': 'mark-alloc'},
            {'type': 'bar', 'from_x': 100 + block_width + block_spacing + block_width//2,
             'to_x': 100 + (block_width + block_spacing) * 4 + block_width//2,
             'y': 40 + block_height + 55, 'label': '1.5', 'id': 'mark-bar'},
            {'type': 'collection', 'x': 100 + (block_width + block_spacing) * 4 + block_width//2,
             'y': 40 + block_height + 45, 'id': 'mark-collect'},
            {'type': 'label', 'text': 'Runtime 5', 'x': 10, 'y': rt5_y - 15},
            {'type': 'timeline', 'runtime': 5, 'y': rt5_y, 'phases': 3},
            {'type': 'allocation', 'x': rt5_alloc_x1, 'y': rt5_y + block_height + 15, 'id': 'rt5-alloc1'},
            {'type': 'bar', 'from_x': rt5_alloc_x1, 'to_x': rt5_collect_x,
             'y': rt5_y + block_height + 25, 'label': '2', 'id': 'rt5-bar1'},
            {'type': 'collection', 'x': rt5_collect_x, 'y': rt5_y + block_height + 15, 'id': 'rt5-collect1'},
            {'type': 'allocation', 'x': rt5_alloc_x2, 'y': rt5_y + block_height + 45, 'id': 'rt5-alloc2'}
        ]
    })
    
    # Frame 11: Runtime 5 Both Collections Complete
    frames.append({
        'id': 11,
        'elements': [
            {'type': 'label', 'text': 'Runtime 4', 'x': 10, 'y': 25},
            {'type': 'timeline', 'runtime': 4, 'y': 40, 'phases': 6},
            {'type': 'allocation', 'x': 100 + block_width//2, 'y': 40 + block_height + 15, 'id': 'sweep-alloc'},
            {'type': 'bar', 'from_x': 100 + block_width//2, 'to_x': 100 + (block_width + block_spacing) * 2 + block_width//2,
             'y': 40 + block_height + 25, 'label': '1', 'id': 'sweep-bar'},
            {'type': 'collection', 'x': 100 + (block_width + block_spacing) * 2 + block_width//2, 
             'y': 40 + block_height + 15, 'id': 'sweep-collect'},
            {'type': 'allocation', 'x': 100 + block_width + block_spacing + block_width//2, 
             'y': 40 + block_height + 45, 'id': 'mark-alloc'},
            {'type': 'bar', 'from_x': 100 + block_width + block_spacing + block_width//2,
             'to_x': 100 + (block_width + block_spacing) * 4 + block_width//2,
             'y': 40 + block_height + 55, 'label': '1.5', 'id': 'mark-bar'},
            {'type': 'collection', 'x': 100 + (block_width + block_spacing) * 4 + block_width//2,
             'y': 40 + block_height + 45, 'id': 'mark-collect'},
            {'type': 'label', 'text': 'Runtime 5', 'x': 10, 'y': rt5_y - 15},
            {'type': 'timeline', 'runtime': 5, 'y': rt5_y, 'phases': 3},
            {'type': 'allocation', 'x': rt5_alloc_x1, 'y': rt5_y + block_height + 15, 'id': 'rt5-alloc1'},
            {'type': 'bar', 'from_x': rt5_alloc_x1, 'to_x': rt5_collect_x,
             'y': rt5_y + block_height + 25, 'label': '2', 'id': 'rt5-bar1'},
            {'type': 'collection', 'x': rt5_collect_x, 'y': rt5_y + block_height + 15, 'id': 'rt5-collect1'},
            {'type': 'allocation', 'x': rt5_alloc_x2, 'y': rt5_y + block_height + 45, 'id': 'rt5-alloc2'},
            {'type': 'bar', 'from_x': rt5_alloc_x2, 'to_x': rt5_collect_x,
             'y': rt5_y + block_height + 55, 'label': '2', 'id': 'rt5-bar2'},
            {'type': 'collection', 'x': rt5_collect_x, 'y': rt5_y + block_height + 45, 'id': 'rt5-collect2'}
        ]
    })
    
    # Frame 12 is just frame 11 (final comparison)
    frames.append(frames[-1])
    
    # Generate SVG elements
    def generate_svg_elements(elements):
        svg_parts = []
        
        for elem in elements:
            if elem['type'] == 'label':
                svg_parts.append(f'<text x="{elem["x"]}" y="{elem["y"]}" class="label">{elem["text"]}</text>')
            
            elif elem['type'] == 'timeline':
                x = 100
                if elem['runtime'] == 4:
                    # Alternating S and M blocks
                    for i in range(elem['phases']):
                        phase_type = 'sweep' if i % 2 == 0 else 'mark'
                        color = sweep_color if phase_type == 'sweep' else mark_color
                        label = 'S' if phase_type == 'sweep' else 'M'
                        svg_parts.append(f'<rect x="{x}" y="{elem["y"]}" width="{block_width}" '
                                       f'height="{block_height}" fill="{color}" stroke="black" />')
                        svg_parts.append(f'<text x="{x + block_width//2}" y="{elem["y"] + block_height//2 + 5}" '
                                       f'text-anchor="middle" class="phase-label">{label}</text>')
                        x += block_width + block_spacing
                else:  # runtime 5
                    # Merged S/M blocks that are twice as wide
                    for i in range(elem['phases']):
                        svg_parts.append(f'<rect x="{x}" y="{elem["y"]}" width="{block_width * 2 + block_spacing}" '
                                       f'height="{block_height}" fill="{merged_color}" stroke="black" />')
                        svg_parts.append(f'<text x="{x + block_width + block_spacing//2}" '
                                       f'y="{elem["y"] + block_height//2 + 5}" '
                                       f'text-anchor="middle" class="phase-label">S/M</text>')
                        x += (block_width * 2 + block_spacing) + block_spacing
            
            elif elem['type'] == 'allocation':
                # Green triangle pointing up
                size = 6
                svg_parts.append(f'<polygon points="{elem["x"]},{elem["y"]-size} '
                               f'{elem["x"]-size},{elem["y"]+size} {elem["x"]+size},{elem["y"]+size}" '
                               f'fill="#228B22" class="allocation {elem["id"]}" />')
            
            elif elem['type'] == 'collection':
                # Red triangle pointing up
                size = 6
                svg_parts.append(f'<polygon points="{elem["x"]},{elem["y"]-size} '
                               f'{elem["x"]-size},{elem["y"]+size} {elem["x"]+size},{elem["y"]+size}" '
                               f'fill="#DC143C" class="collection {elem["id"]}" />')
            
            elif elem['type'] == 'arrow':
                # Curved arrow
                mid_y = min(elem['from_y'], elem['to_y']) - 20
                svg_parts.append(f'<path d="M {elem["from_x"]} {elem["from_y"]} '
                               f'Q {(elem["from_x"] + elem["to_x"])//2} {mid_y} '
                               f'{elem["to_x"]} {elem["to_y"]}" '
                               f'fill="none" stroke="{arrow_color}" stroke-width="2" '
                               f'marker-end="url(#arrowhead)" class="arrow {elem["id"]}" />')
            
            elif elem['type'] == 'bar':
                # Horizontal bar with label
                svg_parts.append(f'<g class="bar {elem["id"]}">')
                svg_parts.append(f'<line x1="{elem["from_x"]}" y1="{elem["y"]}" '
                               f'x2="{elem["to_x"]}" y2="{elem["y"]}" '
                               f'stroke="{arrow_color}" stroke-width="2" />')
                # End caps
                svg_parts.append(f'<line x1="{elem["from_x"]}" y1="{elem["y"] - 5}" '
                               f'x2="{elem["from_x"]}" y2="{elem["y"] + 5}" '
                               f'stroke="{arrow_color}" stroke-width="2" />')
                svg_parts.append(f'<line x1="{elem["to_x"]}" y1="{elem["y"] - 5}" '
                               f'x2="{elem["to_x"]}" y2="{elem["y"] + 5}" '
                               f'stroke="{arrow_color}" stroke-width="2" />')
                # Label
                mid_x = (elem['from_x'] + elem['to_x']) // 2
                svg_parts.append(f'<text x="{mid_x}" y="{elem["y"] - 8}" '
                               f'text-anchor="middle" class="bar-label">{elem["label"]} cycles</text>')
                svg_parts.append('</g>')
        
        return '\n'.join(svg_parts)
    
    # Generate HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Floating Garbage Animation</title>
    <style>
        body {{
            margin: 0;
            padding: 20px;
            font-family: Arial, sans-serif;
            background-color: white;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }}
        
        #animation-container {{
            width: 90%;
            max-width: 1200px;
        }}
        
        svg {{
            display: block;
            margin: 0 auto;
            width: 100%;
            height: auto;
            max-width: 100%;
        }}
        
        .label {{
            font-size: 16px;
            font-weight: bold;
        }}
        
        .phase-label {{
            font-size: 14px;
            fill: white;
            font-weight: bold;
        }}
        
        .frame {{
            display: none;
        }}
        
        .frame.active {{
            display: block;
        }}
        
        .allocation, .collection, .arrow, .bar {{
            opacity: 0;
            animation: fadeIn 0.5s forwards;
        }}
        
        @keyframes fadeIn {{
            to {{ opacity: 1; }}
        }}
        
        .bar-label {{
            font-size: 12px;
            fill: #666;
        }}
    </style>
</head>
<body>
    <div id="animation-container">
        <svg width="800" height="250" viewBox="0 0 800 250">
            <defs>
                <marker id="arrowhead" markerWidth="10" markerHeight="7" 
                        refX="9" refY="3.5" orient="auto">
                    <polygon points="0 0, 10 3.5, 0 7" fill="{arrow_color}" />
                </marker>
            </defs>
"""
    
    # Generate frame groups
    for i, frame in enumerate(frames):
        active_class = 'active' if i == 0 else ''
        html += f'            <g class="frame frame-{i+1} {active_class}">\n'
        html += '                ' + generate_svg_elements(frame['elements']).replace('\n', '\n                ')
        html += '\n            </g>\n'
    
    html += f"""        </svg>
    </div>
    
    <script>
        let currentFrame = 1;
        const totalFrames = {len(frames)};
        
        function showFrame(n) {{
            // Hide all frames
            document.querySelectorAll('.frame').forEach(frame => {{
                frame.classList.remove('active');
            }});
            
            // Show current frame
            document.querySelector('.frame-' + n).classList.add('active');
            
            currentFrame = n;
        }}
        
        function nextFrame() {{
            if (currentFrame < totalFrames) {{
                showFrame(currentFrame + 1);
            }}
        }}
        
        function prevFrame() {{
            if (currentFrame > 1) {{
                showFrame(currentFrame - 1);
            }}
        }}
        
        // Keyboard navigation
        document.addEventListener('keydown', (e) => {{
            if (e.key === 'ArrowRight' || e.key === ' ') {{
                e.preventDefault();
                nextFrame();
            }} else if (e.key === 'ArrowLeft') {{
                e.preventDefault();
                prevFrame();
            }}
        }});
        
        // Initialize
        showFrame(1);
    </script>
</body>
</html>"""
    
    return html

if __name__ == '__main__':
    html = generate_html()
    with open('index.html', 'w') as f:
        f.write(html)
    print("Generated index.html")