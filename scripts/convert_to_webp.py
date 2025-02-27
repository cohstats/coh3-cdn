import os
from PIL import Image
import glob

# WebP conversion quality setting (0-100)
WEBP_QUALITY = 85

def convert_png_to_webp(source_path, counters):
    """Convert a PNG file to WebP format."""
    try:
        # Create the webp filename
        webp_path = os.path.splitext(source_path)[0] + '.webp'
        
        # If webp version doesn't exist, convert the file
        if not os.path.exists(webp_path):
            print(f"Converting {source_path} to WebP...")
            image = Image.open(source_path)
            
            # Save as WebP with good quality, preserving transparency
            image.save(webp_path, 'WEBP', quality=WEBP_QUALITY, lossless=False)
            print(f"Created: {webp_path}")
            counters['converted'] += 1
        else:
            print(f"Skipping {source_path} - WebP version already exists")
            counters['skipped'] += 1
            
    except Exception as e:
        print(f"Error converting {source_path}: {str(e)}")
        counters['errors'] += 1

def main():
    # Get the absolute path to the public directory (one level up from scripts)
    public_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'public')
    
    # Find all PNG files recursively
    png_files = []
    for root, dirs, files in os.walk(public_dir):
        for file in files:
            if file.lower().endswith('.png'):
                png_files.append(os.path.join(root, file))
    
    if not png_files:
        print("No PNG files found in the public directory.")
        return
    
    print(f"Found {len(png_files)} PNG files")
    
    # Initialize counters
    counters = {
        'converted': 0,
        'skipped': 0,
        'errors': 0
    }
    
    # Convert each PNG file
    for png_file in png_files:
        convert_png_to_webp(png_file, counters)
    
    # Print summary
    print("\nConversion Summary:")
    print(f"WebP quality setting: {WEBP_QUALITY}%")
    print(f"Total PNG files found: {len(png_files)}")
    print(f"Files already having WebP version: {counters['skipped']}")
    print(f"Files converted to WebP: {counters['converted']}")
    if counters['errors'] > 0:
        print(f"Errors encountered: {counters['errors']}")

if __name__ == "__main__":
    main() 