from PIL import Image, ImageDraw
import argparse
import io
import os
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, mm

def generate_mm_paper(format="A4", orientation="portrait", 
                     main_color=(0, 0, 255), minor_color=(200, 200, 255),
                     main_thickness=1, minor_thickness=1, 
                     margin=10,
                     output="mm_paper.pdf"):
    """
    Generate millimeter paper with customizable grid colors
    
    Parameters:
    - format: 'A3' or 'A4'
    - orientation: 'portrait' or 'landscape'
    - main_color: RGB tuple for major grid lines (every 10mm)
    - minor_color: RGB tuple for minor grid lines (every 1mm)
    - main_thickness: thickness of main grid lines in pixels
    - minor_thickness: thickness of minor grid lines in pixels
    - margin: margin size in mm (default: 10mm)
    - output: output filename
    """
    # Define paper dimensions in mm
    if format.upper() == "A3":
        width_mm, height_mm = 297, 420  # A3 dimensions in mm
    else:  # default to A4
        width_mm, height_mm = 210, 297  # A4 dimensions in mm
    
    # Apply orientation
    if orientation.lower() == "landscape":
        width_mm, height_mm = height_mm, width_mm
    
    # Use high DPI for the image generation to get good quality lines
    dpi = 300  # High resolution for quality
    mm_to_px = dpi / 25.4  # 1 inch = 25.4 mm
    width_px = int(width_mm * mm_to_px)
    height_px = int(height_mm * mm_to_px)
    
    # Calculate margin in pixels
    margin_px = int(margin * mm_to_px)
    
    # Create a white image
    img = Image.new('RGB', (width_px, height_px), color='white')
    draw = ImageDraw.Draw(img)
    
    # Calculate grid area boundaries (respecting margins)
    grid_start_x = margin_px
    grid_end_x = width_px - margin_px
    grid_start_y = margin_px
    grid_end_y = height_px - margin_px
    
    # Calculate grid dimensions
    grid_width_mm = width_mm - (2 * margin)
    grid_height_mm = height_mm - (2 * margin)
    
    # Draw minor lines (1mm apart)
    for i in range(0, grid_width_mm + 1):
        x = grid_start_x + int(i * mm_to_px)
        draw.line([(x, grid_start_y), (x, grid_end_y)], fill=minor_color, width=minor_thickness)
    
    for i in range(0, grid_height_mm + 1):
        y = grid_start_y + int(i * mm_to_px)
        draw.line([(grid_start_x, y), (grid_end_x, y)], fill=minor_color, width=minor_thickness)
    
    # Draw main lines (10mm apart)
    # Adjust starting point to ensure main lines align with standard grid points
    main_start_x = margin % 10  # Start at the first 10mm point after margin
    main_start_y = margin % 10
    
    for i in range(main_start_x, grid_width_mm + 1, 10):
        x = grid_start_x + int(i * mm_to_px)
        draw.line([(x, grid_start_y), (x, grid_end_y)], fill=main_color, width=main_thickness)
    
    for i in range(main_start_y, grid_height_mm + 1, 10):
        y = grid_start_y + int(i * mm_to_px)
        draw.line([(grid_start_x, y), (grid_end_x, y)], fill=main_color, width=main_thickness)

    # Determine if we need to create a PDF or just save the image
    if output.lower().endswith('.pdf'):
        # Option 1: Create a temporary file
        temp_img_path = "temp_grid_image.png"
        img.save(temp_img_path, format='PNG')
        
        # Create PDF with correct dimensions
        c = canvas.Canvas(output, pagesize=(width_mm*mm, height_mm*mm))
        c.drawImage(temp_img_path, 0, 0, width=width_mm*mm, height=height_mm*mm)
        c.save()
        
        # Clean up the temporary file
        os.remove(temp_img_path)
    else:
        # Save directly as image
        img.save(output)
    
    print(f"Millimeter paper created: {output}")
    print(f"Format: {format}, Orientation: {orientation}")
    print(f"Dimensions: {width_mm}mm x {height_mm}mm")
    print(f"Margin: {margin}mm")
    print(f"Grid area: {grid_width_mm}mm x {grid_height_mm}mm")

def parse_color(color_str):
    """Convert color string 'R,G,B' to RGB tuple"""
    try:
        r, g, b = map(int, color_str.split(','))
        if not all(0 <= x <= 255 for x in (r, g, b)):
            raise ValueError
        return (r, g, b)
    except:
        raise argparse.ArgumentTypeError("Color must be in format 'R,G,B' with values from 0-255")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate millimeter paper in A3 or A4 format.')
    parser.add_argument('--format', choices=['A3', 'A4'], default='A4', 
                        help='Paper format: A3 or A4 (default: A4)')
    parser.add_argument('--orientation', choices=['portrait', 'landscape'], default='portrait',
                        help='Paper orientation (default: portrait)')
    parser.add_argument('--main-color', type=parse_color, default=(0, 0, 255),
                        help='Color for main lines (10mm) in R,G,B format (default: 0,0,255 - blue)')
    parser.add_argument('--minor-color', type=parse_color, default=(200, 200, 255),
                        help='Color for minor lines (1mm) in R,G,B format (default: 200,200,255 - light blue)')
    parser.add_argument('--main-thickness', type=int, default=1,
                        help='Thickness of main lines in pixels (default: 1)')
    parser.add_argument('--minor-thickness', type=int, default=1,
                        help='Thickness of minor lines in pixels (default: 1)')
    parser.add_argument('--margin', type=int, default=10,
                        help='Margin size in mm (default: 10)')
    parser.add_argument('--output', default='mm_paper.pdf',
                        help='Output filename (default: mm_paper.pdf)')
    
    args = parser.parse_args()
    
    generate_mm_paper(
        args.format, 
        args.orientation,
        args.main_color, 
        args.minor_color,
        args.main_thickness,
        args.minor_thickness,
        args.margin,
        args.output
    )