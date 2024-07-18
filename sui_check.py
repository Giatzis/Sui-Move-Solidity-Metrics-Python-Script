import re

def count_lines_of_code(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return 0, 0, 0
    
    total_lines = len(lines)
    code_lines = [line for line in lines if line.strip() and not line.strip().startswith('//')]
    
    in_block_comment = False
    actual_code_lines = []
    comment_lines = 0
    for line in lines:
        stripped_line = line.strip()
        if in_block_comment:
            comment_lines += 1
            if '*/' in stripped_line:
                in_block_comment = False
                stripped_line = stripped_line.split('*/', 1)[1].strip()
            else:
                continue
        if '/*' in stripped_line:
            comment_lines += 1
            if '*/' in stripped_line:
                stripped_line = stripped_line.split('/*')[0] + stripped_line.split('*/', 1)[1]
            else:
                in_block_comment = True
                stripped_line = stripped_line.split('/*', 1)[0].strip()
        elif stripped_line.startswith('//'):
            comment_lines += 1
        
        if stripped_line and not stripped_line.startswith('//') and not in_block_comment:
            actual_code_lines.append(stripped_line)
    
    return total_lines, len(actual_code_lines), comment_lines

def count_functions(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return 0
    
    function_pattern = re.compile(r'\b(public\s+fun|fun)\b')
    functions = function_pattern.findall(content)
    return len(functions)

def count_imports(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return 0
    
    import_pattern = re.compile(r'\buse\b')
    imports = [line for line in lines if import_pattern.search(line)]
    return len(imports)

def count_structs(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return 0
    
    struct_pattern = re.compile(r'\bstruct\b')
    structs = struct_pattern.findall(content)
    return len(structs)

def calculate_cyclomatic_complexity(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return 0
    
    complexity = 0
    function_pattern = re.compile(r'\b(public\s+fun|fun)\b')
    decision_pattern = re.compile(r'\b(if|else if|for|while|match|case)\b')
    
    in_function = False
    for line in lines:
        stripped_line = line.strip()
        if function_pattern.search(stripped_line):
            in_function = True
            complexity += 1  # Start with one for the function itself
        if in_function and decision_pattern.search(stripped_line):
            complexity += 1
        if in_function and stripped_line.endswith('}'):
            in_function = False
    
    return complexity

if __name__ == "__main__":
    file_path = 'path to contract, e.x. C:\\Users\\Desktop\\coin.move'
    
    total_lines, lines_of_code, comment_lines = count_lines_of_code(file_path)
    number_of_functions = count_functions(file_path)
    number_of_imports = count_imports(file_path)
    number_of_structs = count_structs(file_path)
    cyclomatic_complexity = calculate_cyclomatic_complexity(file_path)
    
    print(f"Total Lines: {total_lines}")
    print(f"Lines of Code: {lines_of_code}")
    print(f"Comment Lines: {comment_lines}")
    print(f"Number of Functions: {number_of_functions}")
    print(f"Number of Imports: {number_of_imports}")
    print(f"Number of Structs: {number_of_structs}")
    print(f"Cyclomatic Complexity: {cyclomatic_complexity}")