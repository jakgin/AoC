import os

# Get the current directory
current_dir = os.getcwd()

# Find the highest numbered folder
max_num = 0
for folder_name in os.listdir(current_dir):
    if folder_name.isdigit():
        max_num = max(max_num, int(folder_name))

# Create the next numbered folder
new_folder_name = str(max_num + 1)
if len(new_folder_name) == 1:
    new_folder_name = "0" + new_folder_name
new_folder_path = os.path.join(current_dir, new_folder_name)
os.makedirs(new_folder_path)

# Create main.go file
file_path = os.path.join(new_folder_path, "main.go")
with open(file_path, "w") as file:
    file.write(
        """package main
    
import (
    "fmt"
    "os"
)

func main() {
}
"""
    )

file_path = os.path.join(new_folder_path, "in.txt")
with open(file_path, "w") as f:
    ...

print("Done!")
