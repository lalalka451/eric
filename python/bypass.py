import os

def merge_files(input_dir, file_extensions, output_file, file_name_filter=None, folder_name_filter=None, encoding='utf-8'):
    with open(output_file, 'w', encoding=encoding) as outfile:
        for root, dirs, files in os.walk(input_dir):
            if folder_name_filter:
                dirs[:] = [d for d in dirs if d not in folder_name_filter]
            for filename in files:
                if should_process_file(filename, file_extensions, file_name_filter):
                    process_file(root, filename, outfile, encoding)
    
    print(f"All files with extensions {', '.join(file_extensions)} have been merged into {output_file}")

def should_process_file(filename, file_extensions, file_name_filter):
    if 'copy' in filename.lower():
        return False
    if not any(filename.endswith(ext) for ext in file_extensions):
        return False
    if file_name_filter and filename in file_name_filter:
        return False
    return True

def process_file(root, filename, outfile, encoding):
    file_path = os.path.join(root, filename)
    if 'site-pack' in file_path or 'node_modules' in file_path:
        return
    
    print(f"Merging file: {file_path}")
    try:
        with open(file_path, 'r', encoding=encoding) as infile:
            outfile.write(f"File: {file_path}\\{filename}\n")  # Write the file name
            outfile.write(infile.read())
            outfile.write("\n\n")  # Adds a newline between file contents
    except UnicodeDecodeError as e:
        print(f"Could not decode {file_path}: {e}")

if __name__ == "__main__":
    input_directory = input("Enter the input directory path: ")
    file_extensions = [".tsx",".ts", ".py", ".sh", ".yaml", ".js", ".cs", ".h", ".cpp", ".yml", ".java",".xml","json","properties",".kt",".kts"]
    folder_name_filter = ["build","frontend","target",".idea","node_modules","venv","public"]
    file_name_filter = ["test_", ".git","output.txt","package.json","package-lock.json","index.js.map"]
    output_file_path = rf"{input_directory}\output.txt"

    merge_files(input_directory, file_extensions, output_file_path, file_name_filter, folder_name_filter, encoding='utf-8')
