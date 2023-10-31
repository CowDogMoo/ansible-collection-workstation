import os
import yaml

def generate_table(role_path):
    os_vars = {}
    general_vars = {}

    for var_file in os.listdir(os.path.join(role_path, 'vars')):
        os_family = os.path.splitext(var_file)[0]  # e.g., 'redhat', 'debian'
        var_path = os.path.join(role_path, 'vars', var_file)
        if os.path.exists(var_path):
            with open(var_path, 'r') as file:
                lines = file.readlines()

            # Process the lines to extract variables and descriptions
            i = 0
            while i < len(lines):
                if lines[i].strip().startswith('#'):
                    description = lines[i].strip('# ').strip()
                    i += 1
                    if i < len(lines) and ':' in lines[i]:
                        var_line = lines[i].strip()
                        var_name, var_value = var_line.split(':', 1)
                        if os_family == 'main':
                            general_vars[var_name.strip()] = (var_value.strip(), description)
                        else:
                            os_family_cap = os_family.capitalize()
                            os_vars.setdefault(os_family_cap, {})[var_name.strip()] = (var_value.strip(), description)
                i += 1

    # Generate table for general variables
    general_table_header = "| Variable | Default Value | Description |\n| --- | --- | --- |\n"
    general_table_rows = "".join([f"| `{var}` | `{value.replace('|', '\\|')}` | {desc} |\n" for var, (value, desc) in general_vars.items()])

    general_table = general_table_header + general_table_rows

    # Generate tables for OS-specific variables
    os_tables = []
    for os_family, var_dict in os_vars.items():
        table_header = f"| Variable | Default Value ({os_family}) | Description |\n| --- | --- | --- |\n"
        table_rows = "".join([f"| `{var}` | `{value.replace('|', '\\|')}` | {desc} |\n" for var, (value, desc) in var_dict.items()])
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
                                         "<!--- vars table -->\n" + table + \
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
