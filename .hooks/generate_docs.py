import os
import re

def process_yaml(var_path):
    """Process a YAML file to extract variables, their values, and descriptions.

    Args:
        var_path (str): Path to the YAML file.

    Returns:
        dict: A dictionary where keys are variable names and values are tuples
              containing the variable value and description.
    """
    with open(var_path, 'r') as file:
        lines = file.readlines()

    var_dict = {}
    description = None
    var_name = None
    var_value = None
    is_list = False
    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith('#'):
            if var_name:  # Save previous variable if a description is found
                var_dict[var_name] = (var_value, description)
                var_name = None  # reset var_name for next variable
            description = stripped_line.lstrip('# ').strip()
        elif ':' in stripped_line:
            var_name, var_value = stripped_line.split(':', 1)
            var_name = var_name.strip()
            var_value = var_value.strip()
            is_list = False
        elif stripped_line.startswith('- ') and var_name:
            item = stripped_line.lstrip('- ').strip()
            if not is_list:
                var_value = [item]
                is_list = True
            else:
                var_value.append(item)

    if var_name:  # Save last variable
        var_dict[var_name] = (var_value, description)

    return var_dict



def extract_descriptions(readme_path):
    """Extract variable descriptions from a README file.

    Args:
        readme_path (str): Path to the README file.

    Returns:
        dict: A dictionary where keys are variable names and values are descriptions.
    """
    with open(readme_path, 'r') as file:
        content = file.read()

    descriptions = {}
    for match in re.finditer(r"\|\s*`([^`]+)`\s*\|\s*`([^`]+)`\s*\|\s*([^|]+)\s*\|", content):
        var_name, default_value, description = match.groups()
        descriptions[var_name] = description.strip()

    return descriptions

def generate_table(role_path):
    """Generate a markdown table of variables, their default values, and descriptions
       from the YAML files in the specified role path.

    Args:
        role_path (str): Path to the role directory containing the vars subdirectory
                         and YAML files.

    Returns:
        str: A string representing the markdown table.
    """
    os_vars = {}
    general_vars = {}

    for var_file in os.listdir(os.path.join(role_path, 'vars')):
        os_family = os.path.splitext(var_file)[0]  # e.g., 'redhat', 'debian'
        var_path = os.path.join(role_path, 'vars', var_file)
        if os.path.exists(var_path):
            vars_dict = process_yaml(var_path)

            if os_family == 'main':
                general_vars.update(vars_dict)
            else:
                os_family_cap = os_family.capitalize()
                os_vars.setdefault(os_family_cap, {}).update(vars_dict)

    # Generate table for general variables
    general_table_header = "| Variable | Default Value | Description |\n| --- | --- | --- |\n"
    general_table_rows = "".join([f"| `{var}` | `{str(value).replace('|', '\\|')}` | {desc} |\n" for var, (value, desc) in general_vars.items()])

    general_table = general_table_header + general_table_rows

    # Generate tables for OS-specific variables
    os_tables = []
    for os_family, var_dict in os_vars.items():
        table_header = f"| Variable | Default Value ({os_family}) | Description |\n| --- | --- | --- |\n"
        table_rows = "".join([f"| `{var}` | `{str(value).replace('|', '\\|')}` | {desc} |\n" for var, (value, desc) in var_dict.items()])
        os_tables.append(table_header + table_rows)

    return general_table + "\n" + "\n".join(os_tables)

def main():
    """Main function to generate markdown tables for each role and update README files.

    This function does not take any arguments or return any values. It reads from the
    'roles' directory, generates markdown tables for each role, and updates the README
    files with the new tables.
    """
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
