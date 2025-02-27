import os
import shutil

def count_files_in_directory(directory):
    """Count total number of files in a directory and its subdirectories."""
    total_files = 0
    for root, dirs, files in os.walk(directory):
        total_files += len(files)
    return total_files

def flatten_export_directory():
    # Get the absolute path to the public directory (one level up from scripts)
    public_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'public')
    export_dir = os.path.join(public_dir, 'export')
    flatten_dir = os.path.join(public_dir, 'export_flatten')
    
    # Initialize counters
    counters = {
        'copied': 0,
        'overwritten': 0,
        'errors': 0
    }
    
    # Create export_flatten directory if it doesn't exist
    if not os.path.exists(flatten_dir):
        os.makedirs(flatten_dir)
        print(f"Created directory: {flatten_dir}")
    
    # Count initial files
    initial_export_files = count_files_in_directory(export_dir)
    initial_flatten_files = count_files_in_directory(flatten_dir)
    
    print(f"\nInitial state:")
    print(f"Files in /export: {initial_export_files}")
    print(f"Files in /export_flatten: {initial_flatten_files}\n")
    
    # Walk through all files in export directory
    for root, dirs, files in os.walk(export_dir):
        for file in files:
            try:
                source_path = os.path.join(root, file)
                target_path = os.path.join(flatten_dir, file)
                
                # Check if file already exists in flatten directory
                if os.path.exists(target_path):
                    print(f"Overwriting: {file}")
                    counters['overwritten'] += 1
                else:
                    print(f"Copying: {file}")
                    counters['copied'] += 1
                
                # Copy the file (will overwrite if exists)
                shutil.copy2(source_path, target_path)
                
            except Exception as e:
                print(f"Error processing {file}: {str(e)}")
                counters['errors'] += 1
    
    # Count final files
    final_export_files = count_files_in_directory(export_dir)
    final_flatten_files = count_files_in_directory(flatten_dir)
    
    # Print summary
    print("\nFlattening Summary:")
    print(f"New files copied: {counters['copied']}")
    print(f"Files overwritten: {counters['overwritten']}")
    if counters['errors'] > 0:
        print(f"Errors encountered: {counters['errors']}")
    print(f"Total files processed: {counters['copied'] + counters['overwritten']}")
    
    print(f"\nFinal state:")
    print(f"Files in /export: {final_export_files}")
    print(f"Files in /export_flatten: {final_flatten_files}")
    
    if final_flatten_files != len(set(os.listdir(flatten_dir))):
        print("\nWarning: Some filenames might have been overwritten due to name conflicts when flattening!")

if __name__ == "__main__":
    flatten_export_directory() 