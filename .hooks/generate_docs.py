import os
import re
import yaml

def process_yaml(var_path):
    var_dict = {}
    description = ""
    with open(var_path, 'r') as file:
        lines = file.readlines()

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith('#'):
            description = line.lstrip('# ').strip()
        elif ':' in line:
            var_name, var_value = line.split(':', 1)
            var_value = var_value.strip()
            # Accumulate lines for this value until we reach a new key or the end of the file
            while (i + 1 < len(lines) and
                   not (lines[i + 1].strip().startswith('#') or ':' in lines[i + 1])):
                i += 1
                var_value += '\n' + lines[i].strip()  # Join lines with newline
            # Now process the complete value string
            if var_value.startswith('{{') and var_value.endswith('}}'):
                pass  # Keep Ansible expressions as-is
            else:
                var_value = yaml.safe_load(var_value)
            var_dict[var_name.strip()] = (var_value, description)
            description = ""  # Reset description for next variable
        i += 1  # Move on to the next line

    return var_dict



def generate_row(var, value_desc_tuple):
    value, description = value_desc_tuple
    if value is None:
        value_str = '`None`'
    elif isinstance(value, str) and (value.startswith('{{') and value.endswith('}}')):
        value_str = f'`{value.replace("|", "\\|")}`'  # Escape the pipe character
    elif isinstance(value, list):
        # If value is a list, convert the list to a string, escape the pipe characters,
        # and enclose it in backticks
        value_str = f'`{", ".join(value).replace("|", "\\|")}`'  # Escape the pipe character
    else:
        # For other types, convert them to string, escape the pipe characters,
        # and enclose it in backticks
        value_str = f'`{str(value).replace("|", "\\|")}`'  # Escape the pipe character
    # Escape the pipe characters in the description as well
    description = description.replace("|", "\\|")
    return f"| `{var}` | {value_str} | {description} |"


def generate_table(role_path):
    os_vars = {}
    general_vars = {}

    # Function to process a directory and update a dictionary with the processed YAML files
    def process_directory(directory_path, target_dict):
        for var_file in os.listdir(directory_path):
            os_family = os.path.splitext(var_file)[0]  # e.g., 'redhat', 'debian'
            var_path = os.path.join(directory_path, var_file)
            if os.path.exists(var_path):
                vars_dict = process_yaml(var_path)
                if os_family == 'main':
                    target_dict.update(vars_dict)
                else:
                    os_family_cap = os_family.capitalize()
                    target_dict.setdefault(os_family_cap, {}).update(vars_dict)

    # Process vars and defaults directories
    vars_directory_path = os.path.join(role_path, 'vars')
    defaults_directory_path = os.path.join(role_path, 'defaults')

    if os.path.exists(vars_directory_path):
        process_directory(vars_directory_path, os_vars)

    if os.path.exists(defaults_directory_path):
        process_directory(defaults_directory_path, general_vars)

    general_table_header = "| Variable | Default Value | Description |\n| --- | --- | --- |\n"
    general_table_rows = "\n".join([generate_row(var, value_desc_tuple) for var, value_desc_tuple in general_vars.items()])
    general_table = general_table_header + general_table_rows

    os_tables = []
    for os_family, var_dict in os_vars.items():
        table_header = f"| Variable | Default Value ({os_family}) | Description |\n| --- | --- | --- |\n"
        table_rows = "\n".join([generate_row(var, value_desc_tuple) for var, value_desc_tuple in var_dict.items()])
        os_tables.append(table_header + table_rows)

    return general_table + "\n" + "\n".join(os_tables)


def main():
    roles_path = "roles"
    for role_name in os.listdir(roles_path):
        role_path = os.path.join(roles_path, role_name)
        if os.path.isdir(role_path):
            table = generate_table(role_path)
            readme_path = os.path.join(role_path, "README.md")
            if os.path.exists(readme_path):
                with open(readme_path, 'r') as file:
                    readme_content = file.read()
                if "<!--- end vars table -->" in readme_content:
                    new_readme_content = readme_content.split("<!--- vars table -->")[0] + \
                         "<!--- vars table -->\n" + table + "\n" + \
                         "<!--- end vars table -->" + \
                         readme_content.split("<!--- end vars table -->")[1]
                    with open(readme_path, 'w') as file:
                        file.write(new_readme_content)
                else:
                    print(f"Marker not found in {readme_path}")
            else:
                print(f"{readme_path} does not exist")

if __name__ == "__main__":
    main()
