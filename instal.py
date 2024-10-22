import os
import re

def find_js_imports(file_path):
    """Find all import statements in the given JavaScript file."""
    imports = []
    import_pattern = r"import\s+.*?\s+from\s+['\"](.*?)['\"]"
    
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            matches = re.findall(import_pattern, content)
            imports.extend(matches)
            print(f"Found JS imports in {file_path}: {imports}")  # Debugging output
    except Exception as e:
        print(f"Error reading JS file {file_path}: {e}")
    
    return imports

def find_python_imports(file_path):
    """Find all import statements in the given Python file."""
    imports = []
    import_pattern = r"^(import\s+\S+|from\s+\S+\s+import\s+\S+)"
    
    try:
        with open(file_path, 'r') as file:
            content = file.readlines()
            for line in content:
                match = re.match(import_pattern, line.strip())
                if match:
                    imports.append(match.group(0))
            print(f"Found Python imports in {file_path}: {imports}")  # Debugging output
    except Exception as e:
        print(f"Error reading Python file {file_path}: {e}")
    
    return imports

def generate_install_commands(imports, language):
    """Generate install commands for the found imports based on the language."""
    commands = []
    if language == 'js':
        for module in imports:
            commands.append(f"npm install {module}")
    elif language == 'python':
        for module in imports:
            commands.append(f"pip install {module}")
    return commands

def save_commands_to_file(commands, output_path):
    """Save the generated commands to a specified file."""
    try:
        with open(output_path, 'w') as file:
            for command in commands:
                file.write(command + '\n')
        print(f"Commands saved to {output_path}")  # Debugging output
    except Exception as e:
        print(f"Error saving commands to file: {e}")

def main():
    # Get user input for the root directory
    root_directory = input("Enter the path to the root directory containing code files: ")
    print(f"Root directory provided: {root_directory}")  # Debugging output
    
    # Check if the root directory is valid
    if not os.path.isdir(root_directory):
        print("The specified directory does not exist.")
        return

    # Get user input for paths to exclude
    exclude_paths = input("Enter paths to exclude (comma-separated): ").split(',')
    exclude_paths = [path.strip() for path in exclude_paths]  # Clean up whitespace
    print(f"Excluding paths: {exclude_paths}")  # Debugging output

    all_imports = {'js': [], 'python': []}
    
    # Loop through the root directory and find all code files
    for root, _, files in os.walk(root_directory):
        # Check if the current root directory should be excluded
        if any(excluded in root for excluded in exclude_paths):
            print(f"Skipping excluded directory: {root}")  # Debugging output
            continue
        
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith('.js'):
                print(f"Processing JS file: {file_path}")  # Debugging output
                imports = find_js_imports(file_path)
                all_imports['js'].extend(imports)
            elif file.endswith('.py'):
                print(f"Processing Python file: {file_path}")  # Debugging output
                imports = find_python_imports(file_path)
                all_imports['python'].extend(imports)

    # Generate install commands from all imports found
    commands = []
    for lang, imports in all_imports.items():
        commands.extend(generate_install_commands(imports, lang))

    # Get output path
    output_directory = input("Enter the directory to save the installer commands: ")
    print(f"Output directory provided: {output_directory}")  # Debugging output
    
    # Check if the output directory is valid
    if not os.path.isdir(output_directory):
        print("The specified output directory does not exist.")
        return

    # Save commands to file
    output_path = os.path.join(output_directory, 'install_commands.txt')
    save_commands_to_file(commands, output_path)

if __name__ == "__main__":
    main()