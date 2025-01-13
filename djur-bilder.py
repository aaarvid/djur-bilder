from PIL import Image, ImageDraw, ImageFont
import os
import unicodedata

# filnamn på format djurets-namn_tl.jpg
# djurnamn med mellanrum anges med - 
# tl - top left, tr - top right, bl - bottom left, br - bottom right



def add_text_with_position_from_filename(image_path, output_path):
    # Load your image
    image = Image.open(image_path)

    # Extract the filename (without the directory path)
    file_name = os.path.basename(image_path)

    # Split the filename to extract position info (assume format: `name_position.ext`)
    base_name, _ = os.path.splitext(file_name)
    parts = base_name.split("_")

    # Ensure the filename has exactly two parts
    if len(parts) != 2:
        print(f"Skipping file '{file_name}': Expected exactly two parts separated by '_'.")
        return

    #extract position
    position = parts[-1].lower()

    # Extract the first file name part as text to render
    text_to_render = unicodedata.normalize('NFC', parts[0].replace("-", " ").upper())

    #old
    #text_to_render = parts[0].capitalize()

    # Create a Draw object
    draw = ImageDraw.Draw(image)

    # Dynamically calculate font size as a percentage of image width
    font_size = int(image.width * 0.05)  # Font size is 5% of image width
    font_path = os.path.join("fonts","Nunito-Bold.ttf")

    # Load a font
    try:
        font = ImageFont.truetype(font_path, size=font_size)
    except IOError:
        font = ImageFont.load_default()  # Use default font if TTF is not available


    # Calculate text size using font.getbbox
    text_bbox = font.getbbox(text_to_render)  # Returns (left, top, right, bottom)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    # Define padding and rounded rectangle properties relative to font size
    padding = font_size // 2  # Padding around the text
    corner_radius = font_size // 8  # Radius for the rounded corners

    # Default position values based on filename's position code
    if position == "tl":  # Top-left
        box_x0, box_y0 = padding, padding
        box_x1, box_y1 = text_width + 2 * padding, text_height + 2 * padding
    elif position == "tr":  # Top-right
        box_x0, box_y0 = image.width - text_width - 2 * padding, padding
        box_x1, box_y1 = image.width - padding, text_height + 2 * padding
    elif position == "bl":  # Bottom-left
        box_x0, box_y0 = padding, image.height - text_height - 2 * padding
        box_x1, box_y1 = text_width + 2 * padding, image.height - padding
    elif position == "br":  # Bottom-right
        box_x0, box_y0 = image.width - text_width - 2 * padding, image.height - text_height - 2 * padding
        box_x1, box_y1 = image.width - padding, image.height - padding
    else:  # Default to top-left
        box_x0, box_y0 = padding, padding
        box_x1, box_y1 = text_width + 2 * padding, text_height + 2 * padding
        print(f"position didn't match, default position top left for {file_name}")

    # Draw a rounded rectangle
    draw.rounded_rectangle(
        [(box_x0, box_y0), (box_x1, box_y1)],
        radius=corner_radius,
        fill=(40, 59, 52, 100)  # Semi-transparent dark green
        #outline="white",      # Optional: Outline color
        #width=3               # Optional: Outline width
    )
  
    # Calculate text position (center the text within the box)

    text_x = box_x0 + ((box_x1 - box_x0)*0.5) - (text_width*0.5)

    chars_to_check = {'å', 'ä', 'ö', 'Å', 'Ä', 'Ö'}

    if any(char in text_to_render for char in chars_to_check):
        #has åäö
        text_y = box_y0 + ((box_y1 - box_y0)*0.5) - (text_height*0.5)

    else:
        #doesn't have åäö
        text_y = box_y0 + ((box_y1 - box_y0)*0.5) - (text_height*0.9)


    # Draw the text
    draw.text((text_x, text_y), text_to_render, font=font, fill="white")

    # Save the result
    image.save(output_path)

def process_all_images(input_dir, output_dir):
  
    # Ensure the input directory exists
    if not os.path.exists(input_dir):
        print(f"Error: Input directory '{input_dir}' does not exist.")
        return

    os.makedirs(output_dir, exist_ok=True)

    image_count = 0  # Initialize counter

    # Process each file in the input directory
    for file_name in os.listdir(input_dir):
        input_path = os.path.join(input_dir, file_name)
        
        # Skip non-image files
        if not os.path.isfile(input_path) or not file_name.lower().endswith((".png", ".jpg", ".jpeg")):
            continue
        
        # Generate the output file path
        base_name, _ = os.path.splitext(file_name)
        output_path = os.path.join(output_dir, f"{base_name}_withname.jpg")

        # Process the image
        add_text_with_position_from_filename(input_path, output_path)
        print(f"Processed: {input_path} -> {output_path}")

        image_count += 1  # Increment counter

    print(f"{image_count} images processed completely.")

process_all_images(
    input_dir="input",  # Input folder containing images
    output_dir="output"  # Output folder for rendered images
)
