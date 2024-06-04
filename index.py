import os
import re

def get_properties(class_name):
    properties = []
    with open(class_name) as f:
        for line in f:
            if line.startswith("    private"):
                temp = line.split("$")[1].split(";")[0].split(" ")[0]
                ignoredFields = ["id", "createdAt", "updatedAt", "createdBy", "updatedBy"]
                if temp not in ignoredFields:
                    properties.append(temp)
    return properties

def modify_code(file_path):
    with open(file_path) as f:
        code = f.read()

    properties = get_properties(file_path)
    properties_str = ",".join(properties)
    properties_str = properties_str.replace(",", "', '")
    properties_str = "'" + properties_str + "'"
    replace = False
    # print(file_path, properties_str)

    # Check and update #[Gedmo\\Blameable
    blameable_match = re.search(r"(?<=#\[Gedmo\\Blameable\(on: 'change', field: \[)([^{}]+)(?=\]\)\]\n    private \$updatedBy)", code)
    if blameable_match:
        existing_fields = blameable_match.group(1)
        if existing_fields != properties_str:
            # print(blameable_match.group(1), properties_str)
            code = code.replace(existing_fields, properties_str)
            replace = True
            print(f"Updated @Gedmo\\Blameable for {file_path}")

    # Check and update #[Gedmo\\Timestampable
    timestampable_match = re.search(r"(?<=#\[Gedmo\\Timestampable\(on: 'change', field: \[)([^{}]+)(?=\]\)\]\n    private \$updatedAt)", code)
    if timestampable_match:
        existing_fields = timestampable_match.group(1)
        if existing_fields != properties_str:
            # print(timestampable_match.group(1), properties_str)
            code = code.replace(existing_fields, properties_str)
            replace = True
            print(f"Updated @Gedmo\\Timestampable for {file_path}")

    if replace:
        with open(file_path, "w") as f:
            f.write(code)

# Directory path where all the PHP files are stored
directory_path = r""

for file_path in os.listdir(directory_path):
    if file_path.endswith(".php"):
        modify_code(os.path.join(directory_path, file_path))