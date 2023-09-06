import os
import pandas as pd
import ast

def calculate_atfd(class_node):
    atfd = 0
    
    # Create a set to keep track of accessed attributes outside the class
    foreign_attributes = set()
    
    for method_node in ast.walk(class_node):
        if isinstance(method_node, ast.FunctionDef):
            for subnode in ast.walk(method_node):
                if isinstance(subnode, ast.Attribute):
                    attr_owner = subnode.value.id if isinstance(subnode.value, ast.Name) else None
                    if attr_owner and attr_owner != class_node.name:
                        foreign_attributes.add(subnode.attr)
    
    atfd = len(foreign_attributes)
    return atfd

def process_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    tree = ast.parse(content) #error
    
    class_atfd = []
    total_atfd = 0
    
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_name = node.name
            class_methods_atfd = calculate_atfd(node)
            class_atfd.append((class_name, class_methods_atfd))
            total_atfd += class_methods_atfd
    
    return class_atfd, total_atfd

def find_py_files(directory):

    py_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                py_files.append(os.path.join(root, file))
    return py_files

directory_path = "C:\\Users\\HP\\Desktop\\Thesis\\atfd\\python_projects-main"
py_files = find_py_files(directory_path)

data = []

for py_file in py_files:
    class_atfd, total_atfd = process_file(py_file) #error
    class_atfd_str = ', '.join([f"{class_name} ({atfd})" for class_name, atfd in class_atfd])
    data.append({"File Path": py_file, "File Name": os.path.basename(py_file), "Classes (ATFD)": class_atfd_str, "Total ATFD": total_atfd})

# Create a DataFrame
df = pd.DataFrame(data)

excel_file_path = "atfd.xlsx"
df.to_excel(excel_file_path, index=False)
print(f"List of .py files with ATFD exported to {excel_file_path}")
