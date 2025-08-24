import os
import zipfile
import shutil

def process_cbz_files(directory):
    # Iterate through all files in the directory
    for filename in os.listdir(directory):
        if filename.lower().endswith('.cbz'):
            # Full path to the cbz file
            cbz_path = os.path.join(directory, filename)
            
            # Create folder name (same as cbz file without extension)
            folder_name = os.path.splitext(filename)[0]
            folder_path = os.path.join(directory, folder_name)
            
            # Create folder if it doesn't exist
            os.makedirs(folder_path, exist_ok=True)
            
            # Extract cbz file
            with zipfile.ZipFile(cbz_path, 'r') as zip_ref:
                zip_ref.extractall(folder_path)
            
            # Remove ComicInfo.xml if it exists
            comic_info_path = os.path.join(folder_path, 'ComicInfo.xml')
            if os.path.exists(comic_info_path):
                os.remove(comic_info_path)
                print(f"Removed ComicInfo.xml from {folder_name}")
            
            print(f"Processed: {filename}")

if __name__ == "__main__":
    directory = r"C:\Users\fueqq\Downloads\AyuGram Desktop"
    process_cbz_files(directory)