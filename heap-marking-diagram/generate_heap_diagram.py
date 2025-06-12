#!/usr/bin/env python3

import xml.etree.ElementTree as ET
from xml.dom import minidom
import random
import math

class HeapDiagram:
    def __init__(self, width=1400, height=700):
        self.width = width
        self.height = height
        self.svg = ET.Element('svg', {
            'width': str(width),
            'height': str(height),
            'viewBox': f'0 0 {width} {height}',
            'xmlns': 'http://www.w3.org/2000/svg'
        })
        self.defs = ET.SubElement(self.svg, 'defs')
        # Define colors
        self.colors = {
            'marked': '#4CAF50',      # Green for marked objects
            'unmarked': '#FF5252',    # Red for unmarked objects
            'root': '#2196F3',        # Blue for roots
            'background': '#F5F5F5',  # Light gray background
            'section_bg': 'white',    # White section background
            'arrow': '#333333',       # Darker for better visibility
            'text': '#333333'         # Dark gray for text
        }
        
    def add_background(self):
        """Add a background to the entire diagram"""
        ET.SubElement(self.svg, 'rect', {
            'x': '0',
            'y': '0',
            'width': str(self.width),
            'height': str(self.height),
            'fill': self.colors['background']
        })
        
    def add_section(self, x, y, width, height, label, add_background=True):
        """Add a labeled section (Stack, Heap)"""
        if add_background:
            # Section background
            ET.SubElement(self.svg, 'rect', {
                'x': str(x),
                'y': str(y),
                'width': str(width),
                'height': str(height),
                'fill': self.colors['section_bg'],
                'stroke': '#CCCCCC',
                'stroke-width': '2',
                'rx': '8',
                'ry': '8'
            })
        
        # Section label
        ET.SubElement(self.svg, 'text', {
            'x': str(x + width/2),
            'y': str(y - 15),
            'text-anchor': 'middle',
            'font-family': 'Arial, sans-serif',
            'font-size': '24',
            'font-weight': 'bold',
            'fill': self.colors['text']
        }).text = label
        
    def add_object(self, x, y, width, height, obj_type='unmarked', label=None):
        """Add an object (marked, unmarked, or root)"""
        color = self.colors.get(obj_type, self.colors['unmarked'])
        
        rect = ET.SubElement(self.svg, 'rect', {
            'x': str(x),
            'y': str(y),
            'width': str(width),
            'height': str(height),
            'fill': color,
            'stroke': '#333333',
            'stroke-width': '2',
            'rx': '6',
            'ry': '6'
        })
        
        if label:
            ET.SubElement(self.svg, 'text', {
                'x': str(x + width/2),
                'y': str(y + height/2 + 6),
                'text-anchor': 'middle',
                'font-family': 'Arial, sans-serif',
                'font-size': '16',
                'fill': 'white',
                'font-weight': 'bold'
            }).text = label
            
        return (x + width/2, y + height/2)  # Return center point for arrows
        
    def add_arrow(self, x1, y1, x2, y2):
        """Add a straight arrow between two points with larger arrowhead"""
        # Create straight line
        ET.SubElement(self.svg, 'line', {
            'x1': str(x1),
            'y1': str(y1),
            'x2': str(x2),
            'y2': str(y2),
            'stroke': self.colors['arrow'],
            'stroke-width': '2.5'
        })
        
        # Calculate arrow direction
        dx = x2 - x1
        dy = y2 - y1
        length = math.sqrt(dx*dx + dy*dy)
        if length == 0:
            return
            
        # Normalize
        dx /= length
        dy /= length
        
        # Arrowhead size
        arrow_length = 15
        arrow_width = 7
        
        # Calculate arrowhead points
        # Base of the arrow (back from the tip)
        base_x = x2 - dx * arrow_length
        base_y = y2 - dy * arrow_length
        
        # Perpendicular vector for width
        perp_x = -dy
        perp_y = dx
        
        # Three points of the arrowhead
        p1_x = x2
        p1_y = y2
        p2_x = base_x + perp_x * arrow_width
        p2_y = base_y + perp_y * arrow_width
        p3_x = base_x - perp_x * arrow_width
        p3_y = base_y - perp_y * arrow_width
        
        # Create arrowhead as a filled polygon
        points = f"{p1_x},{p1_y} {p2_x},{p2_y} {p3_x},{p3_y}"
        ET.SubElement(self.svg, 'polygon', {
            'points': points,
            'fill': self.colors['arrow'],
            'stroke': 'none'
        })
        
    def add_arrowhead_marker(self):
        """Add larger, more visible arrowhead marker definition"""
        marker = ET.SubElement(self.defs, 'marker', {
            'id': 'arrowhead',
            'markerWidth': '15',
            'markerHeight': '15',
            'refX': '15',
            'refY': '7.5',
            'orient': 'auto'
        })
        # Much larger, filled triangle arrowhead
        ET.SubElement(marker, 'polygon', {
            'points': '0,0 15,7.5 0,15',
            'fill': self.colors['arrow'],
            'stroke': 'none'
        })
        
    def add_key(self, x, y):
        """Add a visually distinct key/legend"""
        # Key background with distinct styling
        key_bg = ET.SubElement(self.svg, 'rect', {
            'x': str(x - 10),
            'y': str(y - 10),
            'width': '180',
            'height': '160',
            'fill': '#FAFAFA',
            'stroke': '#AAAAAA',
            'stroke-width': '1',
            'stroke-dasharray': '5,5',
            'rx': '5',
            'ry': '5'
        })
        
        # Key title
        ET.SubElement(self.svg, 'text', {
            'x': str(x + 70),
            'y': str(y + 15),
            'text-anchor': 'middle',
            'font-family': 'Arial, sans-serif',
            'font-size': '16',
            'font-weight': 'bold',
            'fill': self.colors['text']
        }).text = 'Legend'
        
        # Key entries
        entries = [
            ('root', 'Root'),
            ('marked', 'Marked'),
            ('unmarked', 'Unmarked')
        ]
        
        y_offset = 40
        for obj_type, description in entries:
            # Small colored square
            ET.SubElement(self.svg, 'rect', {
                'x': str(x + 10),
                'y': str(y + y_offset),
                'width': '20',
                'height': '20',
                'fill': self.colors[obj_type],
                'stroke': '#333333',
                'stroke-width': '1.5',
                'rx': '3',
                'ry': '3'
            })
            
            # Description text
            ET.SubElement(self.svg, 'text', {
                'x': str(x + 35),
                'y': str(y + y_offset + 15),
                'font-family': 'Arial, sans-serif',
                'font-size': '14',
                'fill': self.colors['text']
            }).text = description
            
            y_offset += 35
            
    def check_overlap(self, x, y, size, existing_objects):
        """Check if a new object would overlap with existing ones"""
        for ex_x, ex_y in existing_objects:
            if (abs(x - ex_x) < size + 20 and abs(y - ex_y) < size + 20):
                return True
        return False
        
    def generate(self):
        """Generate the complete heap diagram showing post-marking phase"""
        self.add_background()
        
        # Set random seed for reproducibility
        random.seed(123)  # Changed seed for different layout
        
        # Stack section (smaller)
        stack_x, stack_y = 40, 200
        stack_width, stack_height = 100, 250
        self.add_section(stack_x, stack_y, stack_width, stack_height, "Stack")
        
        # Add stack entries (roots)
        root1 = self.add_object(stack_x + 15, stack_y + 30, 70, 45, 'root')
        root2 = self.add_object(stack_x + 15, stack_y + 100, 70, 45, 'root')
        root3 = self.add_object(stack_x + 15, stack_y + 170, 70, 45, 'root')
        
        # Heap section (much larger)
        heap_x, heap_y = 180, 100
        heap_width, heap_height = 1000, 450
        self.add_section(heap_x, heap_y, heap_width, heap_height, "Heap")
        
        # Manually place objects for better control over layout
        obj_size = 55
        
        # Place marked objects in a more structured way to avoid confusing arrows
        marked_positions = [
            (heap_x + 250, heap_y + 150),    # 0 - connected to R1
            (heap_x + 500, heap_y + 100),    # 1 - connected to R2
            (heap_x + 800, heap_y + 200),    # 2 - connected to R3
            (heap_x + 350, heap_y + 300),    # 3 - child of 0
            (heap_x + 600, heap_y + 270),    # 4 - child of 1
            (heap_x + 150, heap_y + 380),    # 5 - child of 3
        ]
        
        marked_objects = []
        for x, y in marked_positions:
            obj = self.add_object(x, y, obj_size, obj_size, 'marked')
            marked_objects.append(obj)
        
        # Place unmarked objects - some connected, some isolated
        unmarked_positions = [
            (heap_x + 800, heap_y + 350),    # 0 - part of garbage cycle (moved left)
            (heap_x + 650, heap_y + 380),    # 1 - part of garbage cycle (moved left)
            (heap_x + 450, heap_y + 380),    # 2 - isolated (moved up to stay in bounds)
            (heap_x + 650, heap_y + 50),     # 3 - isolated (moved left to avoid overlap)
            (heap_x + 370, heap_y + 50),     # 4 - isolated (moved left to avoid overlap)
        ]
        
        unmarked_objects = []
        for x, y in unmarked_positions:
            obj = self.add_object(x, y, obj_size, obj_size, 'unmarked')
            unmarked_objects.append(obj)
        
        # Add arrows from roots to marked objects
        self.add_arrow(root1[0] + 35, root1[1], marked_objects[0][0] - 27, marked_objects[0][1])
        self.add_arrow(root2[0] + 35, root2[1], marked_objects[1][0] - 27, marked_objects[1][1])
        self.add_arrow(root3[0] + 35, root3[1], marked_objects[2][0] - 27, marked_objects[2][1])
        
        # Add simple tree structure for marked objects
        # From object 0 to 3
        self.add_arrow(marked_objects[0][0], marked_objects[0][1] + 27, 
                      marked_objects[3][0], marked_objects[3][1] - 27)
        # From object 1 to 4
        self.add_arrow(marked_objects[1][0], marked_objects[1][1] + 27, 
                      marked_objects[4][0], marked_objects[4][1] - 27)
        # From object 3 to 5
        self.add_arrow(marked_objects[3][0], marked_objects[3][1] + 27, 
                      marked_objects[5][0], marked_objects[5][1] - 27)
        
        # Add simple connection between two unmarked objects
        self.add_arrow(unmarked_objects[0][0] - 27, unmarked_objects[0][1], 
                      unmarked_objects[1][0] + 27, unmarked_objects[1][1])
        
        # Add key/legend (smaller)
        self.add_key(1210, 250)
        
    def save(self, filename):
        """Save the SVG to a file"""
        # Convert to pretty-printed string
        rough_string = ET.tostring(self.svg, encoding='unicode')
        reparsed = minidom.parseString(rough_string)
        pretty_xml = reparsed.toprettyxml(indent='  ')
        
        # Remove extra blank lines
        lines = pretty_xml.split('\n')
        pretty_xml = '\n'.join([line for line in lines if line.strip()])
        
        with open(filename, 'w') as f:
            f.write(pretty_xml)
            
if __name__ == '__main__':
    diagram = HeapDiagram()
    diagram.generate()
    diagram.save('heap_marking.svg')
    print("Generated heap_marking.svg")