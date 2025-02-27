import os
import argparse
import requests
import tempfile
from PIL import Image

# GitHub API settings
GITHUB_API_URL = "https://api.github.com/repos/Janne252/coh-replay-analyzer-discord-bot/contents/data/scenario-preview-images/coh3"
RAW_CONTENT_URL = "https://raw.githubusercontent.com/Janne252/coh-replay-analyzer-discord-bot/master/data/scenario-preview-images/coh3"

# WebP conversion quality setting (0-100)
WEBP_QUALITY = 85

def download_file(url, target_path):
    """Download a file from URL to target path."""
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for bad status codes
    
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(response.content)
        temp_file.flush()
        return temp_file.name

def get_map_name(filename):
    """Extract map name from filename."""
    return filename.split('.')[0]

def get_file_type(filename):
    """Determine the type of map file (colored, tm, or base)."""
    if '.colored.' in filename:
        return 'colored'
    elif '.tm.' in filename:
        return 'tm'
    else:
        return 'base'

def convert_to_webp(source_path, target_path):
    """Convert image to WebP format while preserving transparency."""
    image = Image.open(source_path)
    image.save(target_path, 'WEBP', quality=WEBP_QUALITY, lossless=False)

def get_png_files_list():
    """Get list of PNG files from GitHub repository."""
    response = requests.get(GITHUB_API_URL)
    response.raise_for_status()
    
    files = response.json()
    return [f['name'] for f in files if f['name'].endswith('.png')]

def ensure_webp_versions(maps_dir):
    """Check all PNG files in maps directory and ensure they have WebP versions."""
    print("\nChecking for missing WebP versions...")
    
    # Initialize counters
    counters = {
        'png_files_found': 0,
        'webp_created': 0,
        'already_exists': 0,
        'errors': 0
    }
    
    # Walk through all directories in maps folder
    for root, dirs, files in os.walk(maps_dir):
        for file in files:
            if file.endswith('.png'):
                counters['png_files_found'] += 1
                png_path = os.path.join(root, file)
                # Create corresponding WebP filename
                webp_path = os.path.splitext(png_path)[0] + '.webp'
                
                try:
                    if not os.path.exists(webp_path):
                        print(f"Converting: {file} to WebP")
                        convert_to_webp(png_path, webp_path)
                        counters['webp_created'] += 1
                    else:
                        counters['already_exists'] += 1
                except Exception as e:
                    print(f"Error converting {file}: {str(e)}")
                    counters['errors'] += 1
    
    # Print summary
    if counters['png_files_found'] > 0:
        print("\nPNG to WebP Check Summary:")
        print(f"PNG files found: {counters['png_files_found']}")
        print(f"WebP versions created: {counters['webp_created']}")
        print(f"WebP versions already existed: {counters['already_exists']}")
        if counters['errors'] > 0:
            print(f"Errors encountered: {counters['errors']}")
    else:
        print("No PNG files found in maps directory")

def process_map_files(target_base_dir, overwrite=False):
    """Process map files from GitHub repository to target directory."""
    # Create maps directory if it doesn't exist
    maps_dir = os.path.join(target_base_dir, 'public', 'maps')
    if not os.path.exists(maps_dir):
        os.makedirs(maps_dir)
        print(f"Created directory: {maps_dir}")

    # Initialize counters
    counters = {
        'maps_processed': 0,
        'files_converted': 0,
        'files_skipped': 0,
        'errors': 0
    }

    try:
        # Get list of PNG files from GitHub
        print("Fetching file list from GitHub...")
        png_files = get_png_files_list()
    except Exception as e:
        print(f"Error fetching file list: {str(e)}")
        return counters

    # Group files by map name
    map_files = {}
    for file in png_files:
        map_name = get_map_name(file)
        if map_name not in map_files:
            map_files[map_name] = []
        map_files[map_name].append(file)

    print(f"\nUsing WebP quality setting: {WEBP_QUALITY}%")
    print(f"Found {len(map_files)} maps to process")

    # Process each map
    for map_name, files in map_files.items():
        print(f"\nProcessing map: {map_name}")
        map_dir = os.path.join(maps_dir, map_name)
        
        # Create map directory if it doesn't exist
        if not os.path.exists(map_dir):
            os.makedirs(map_dir)
            print(f"Created directory: {map_dir}")

        # Process each file for the map
        for source_file in files:
            try:
                file_type = get_file_type(source_file)
                
                # Determine target filename
                if file_type == 'colored':
                    target_file = f"{map_name}.marked.colored.webp"
                elif file_type == 'tm':
                    target_file = f"{map_name}.marked.tm.webp"
                elif file_type == 'base':
                    target_file = f"{map_name}.marked.webp"
                
                target_path = os.path.join(map_dir, target_file)

                # Check if file should be converted
                if not os.path.exists(target_path) or overwrite:
                    # Download and convert file
                    source_url = f"{RAW_CONTENT_URL}/{source_file}"
                    print(f"Downloading: {source_file}")
                    temp_file = download_file(source_url, target_path)
                    
                    try:
                        convert_to_webp(temp_file, target_path)
                        print(f"Converted: {target_file}")
                        counters['files_converted'] += 1
                    finally:
                        # Clean up temporary file
                        if os.path.exists(temp_file):
                            os.unlink(temp_file)
                else:
                    print(f"Skipped existing file: {target_file}")
                    counters['files_skipped'] += 1

            except Exception as e:
                print(f"Error processing {source_file}: {str(e)}")
                counters['errors'] += 1

        counters['maps_processed'] += 1

    # Print summary
    print("\nSync Summary:")
    print(f"WebP quality setting: {WEBP_QUALITY}%")
    print(f"Maps processed: {counters['maps_processed']}")
    print(f"Files converted to WebP: {counters['files_converted']}")
    print(f"Files skipped (already exist): {counters['files_skipped']}")
    if counters['errors'] > 0:
        print(f"Errors encountered: {counters['errors']}")
    
    # Final check for any PNG files without WebP versions
    ensure_webp_versions(maps_dir)

def main():
    parser = argparse.ArgumentParser(description='Sync map images from coh-replay-analyzer repository')
    parser.add_argument('--overwrite', action='store_true', help='Overwrite existing files')
    args = parser.parse_args()

    try:
        # Get the workspace directory (one level up from scripts)
        workspace_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Process the files
        process_map_files(workspace_dir, args.overwrite)
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1

    return 0

if __name__ == "__main__":
    exit(main()) 