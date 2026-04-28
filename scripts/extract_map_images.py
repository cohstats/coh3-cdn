import os
import argparse
import subprocess
import shutil
from pathlib import Path
from PIL import Image

# WebP conversion quality setting (0-100)
WEBP_QUALITY = 85

def discover_map_folders(extracted_dir):
    """
    Scan both standard and community map paths.
    Returns a list of tuples: (map_code, map_folder_path)
    """
    map_folders = []
    
    # Standard maps path
    standard_maps_path = Path(extracted_dir) / "data" / "scenarios" / "multiplayer"
    if standard_maps_path.exists():
        for item in standard_maps_path.iterdir():
            if item.is_dir() and item.name != "community":
                map_folders.append((item.name, str(item)))
    
    # Community maps path
    community_maps_path = Path(extracted_dir) / "data" / "scenarios" / "multiplayer" / "community"
    if community_maps_path.exists():
        for item in community_maps_path.iterdir():
            if item.is_dir():
                map_folders.append((item.name, str(item)))
    
    return map_folders

def find_rrtex_file(map_folder, map_code):
    """
    Locate {map_code}_mm_handmade.rrtex file in the map folder.
    Returns the path to the file if found, None otherwise.
    """
    rrtex_filename = f"{map_code}_mm_handmade.rrtex"
    rrtex_path = Path(map_folder) / rrtex_filename
    
    if rrtex_path.exists():
        return str(rrtex_path)
    
    # Also check in subdirectories
    for item in Path(map_folder).rglob(rrtex_filename):
        return str(item)
    
    return None

def convert_rrtex_to_png_webp(rrtex_path, image_extractor_path, output_dir, map_code):
    """
    Convert RRTEX file to PNG and WebP using the coh3-image-extractor tool.
    Returns True if successful, False otherwise.
    """
    try:
        # Create temporary directory for conversion output
        temp_dir = Path(output_dir) / "temp_conversion"
        temp_dir.mkdir(parents=True, exist_ok=True)
        
        # Run the image extractor to convert to PNG
        extractor_script = Path(image_extractor_path) / "scripts" / "main.py"
        
        # Create a temporary directory for just this file
        temp_input_dir = temp_dir / "input"
        temp_input_dir.mkdir(exist_ok=True)
        
        # Copy the rrtex file to temp input
        temp_rrtex = temp_input_dir / f"{map_code}_mm_handmade.rrtex"
        shutil.copy2(rrtex_path, temp_rrtex)
        
        # Convert to PNG first
        temp_output_dir = temp_dir / "output"
        temp_output_dir.mkdir(exist_ok=True)
        
        result = subprocess.run(
            ["python", str(extractor_script), "--src", str(temp_input_dir), 
             "--format", "png", "--dst", str(temp_output_dir)],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode != 0:
            print(f"Warning: Image extractor returned code {result.returncode}")
            print(f"stderr: {result.stderr}")
            return False
        
        # Find the generated PNG file
        png_files = list(temp_output_dir.rglob("*.png"))
        if not png_files:
            print(f"Warning: No PNG file generated for {map_code}")
            return False
        
        png_file = png_files[0]
        
        # Rename and move PNG to final location
        final_png = Path(output_dir) / f"{map_code}.png"
        shutil.copy2(png_file, final_png)
        
        # Convert PNG to WebP
        convert_png_to_webp(str(final_png), str(Path(output_dir) / f"{map_code}.webp"))
        
        # Cleanup temp directory
        shutil.rmtree(temp_dir, ignore_errors=True)
        
        return True
        
    except Exception as e:
        print(f"Error converting {rrtex_path}: {str(e)}")
        return False

def convert_png_to_webp(png_path, webp_path):
    """Convert PNG file to WebP format."""
    image = Image.open(png_path)
    image.save(webp_path, 'WEBP', quality=WEBP_QUALITY, lossless=False)

def check_existing_files(maps_dir, map_code):
    """
    Check if PNG and WebP files already exist for the map.
    Returns True if both exist, False otherwise.
    """
    map_folder = Path(maps_dir) / map_code
    png_path = map_folder / f"{map_code}.png"
    webp_path = map_folder / f"{map_code}.webp"
    
    return png_path.exists() and webp_path.exists()

def organize_map_images(temp_files_dir, maps_dir, map_code):
    """
    Move PNG and WebP files to public/maps/{map_code}/ directory.
    Creates the map folder if it doesn't exist.
    """
    map_folder = Path(maps_dir) / map_code
    map_folder.mkdir(parents=True, exist_ok=True)
    
    # Move PNG and WebP files
    png_source = Path(temp_files_dir) / f"{map_code}.png"
    webp_source = Path(temp_files_dir) / f"{map_code}.webp"
    
    if png_source.exists():
        shutil.copy2(png_source, map_folder / f"{map_code}.png")
    
    if webp_source.exists():
        shutil.copy2(webp_source, map_folder / f"{map_code}.webp")

def generate_summary_report(processed, skipped, errors):
    """
    Generate markdown summary of the extraction process.
    Returns the summary as a string.
    """
    summary = "# Map Image Extraction Summary\n\n"
    summary += f"## Statistics\n\n"
    summary += f"- **Maps Processed**: {len(processed)}\n"
    summary += f"- **Maps Skipped** (already exist): {len(skipped)}\n"
    summary += f"- **Maps Failed**: {len(errors)}\n"
    summary += f"- **Total Maps Discovered**: {len(processed) + len(skipped) + len(errors)}\n\n"

    if processed:
        summary += "## Successfully Processed Maps\n\n"
        for map_code in sorted(processed):
            summary += f"- `{map_code}`\n"
        summary += "\n"

    if skipped:
        summary += "## Skipped Maps (Already Exist)\n\n"
        for map_code in sorted(skipped):
            summary += f"- `{map_code}`\n"
        summary += "\n"

    if errors:
        summary += "## Failed Maps\n\n"
        for map_code, error in sorted(errors):
            summary += f"- `{map_code}`: {error}\n"
        summary += "\n"

    return summary

def main():
    parser = argparse.ArgumentParser(
        description='Extract map minimap images from COH3 ScenariosMP.sga files'
    )
    parser.add_argument(
        '--src',
        required=True,
        help='Source directory containing extracted ScenariosMP.sga files'
    )
    parser.add_argument(
        '--image-extractor-path',
        required=True,
        help='Path to coh3-image-extractor repository'
    )
    parser.add_argument(
        '--output-dir',
        default='public/maps',
        help='Base output directory (defaults to public/maps)'
    )
    parser.add_argument(
        '--overwrite',
        action='store_true',
        help='Overwrite existing files (default: False)'
    )

    args = parser.parse_args()

    # Get absolute paths
    workspace_dir = Path(__file__).parent.parent
    src_dir = Path(args.src)
    image_extractor_path = Path(args.image_extractor_path)

    # Determine output directory
    if Path(args.output_dir).is_absolute():
        maps_dir = Path(args.output_dir)
    else:
        maps_dir = workspace_dir / args.output_dir

    # Create temporary directory for conversion
    temp_dir = workspace_dir / "temp_map_conversion"
    temp_dir.mkdir(parents=True, exist_ok=True)

    # Track results
    processed = []
    skipped = []
    errors = []

    print(f"Discovering maps in: {src_dir}")
    print(f"Output directory: {maps_dir}")
    print(f"Overwrite mode: {args.overwrite}")
    print(f"WebP quality: {WEBP_QUALITY}%\n")

    # Discover all map folders
    map_folders = discover_map_folders(src_dir)
    print(f"Found {len(map_folders)} map folders\n")

    for map_code, map_folder in map_folders:
        print(f"Processing: {map_code}")

        # Check if files already exist and skip if overwrite is False
        if not args.overwrite and check_existing_files(maps_dir, map_code):
            print(f"  Skipped (files already exist)\n")
            skipped.append(map_code)
            continue

        # Find the RRTEX file
        rrtex_file = find_rrtex_file(map_folder, map_code)
        if not rrtex_file:
            error_msg = "RRTEX file not found"
            print(f"  Warning: {error_msg}\n")
            errors.append((map_code, error_msg))
            continue

        print(f"  Found RRTEX: {Path(rrtex_file).name}")

        # Convert RRTEX to PNG and WebP
        success = convert_rrtex_to_png_webp(
            rrtex_file,
            image_extractor_path,
            temp_dir,
            map_code
        )

        if not success:
            error_msg = "Conversion failed"
            print(f"  Error: {error_msg}\n")
            errors.append((map_code, error_msg))
            continue

        # Organize the files into the maps directory
        organize_map_images(temp_dir, maps_dir, map_code)
        print(f"  Success: Created {map_code}.png and {map_code}.webp\n")
        processed.append(map_code)

    # Clean up temporary directory
    shutil.rmtree(temp_dir, ignore_errors=True)

    # Generate and print summary
    summary = generate_summary_report(processed, skipped, errors)
    print("\n" + "="*60)
    print(summary)
    print("="*60)

    # Save summary to file
    summary_file = workspace_dir / "map_extraction_summary.md"
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(summary)
    print(f"\nSummary saved to: {summary_file}")

    # Return exit code based on results
    if errors and not processed:
        return 1  # All failed
    return 0  # At least some succeeded or all skipped

if __name__ == "__main__":
    exit(main())

