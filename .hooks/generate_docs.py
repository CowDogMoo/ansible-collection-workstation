import yaml
import os

def generate_table(role_path):
    variables = {}
    descriptions = {}
    for var_file in ["defaults/main.yml", "vars/main.yml"]:
        var_path = os.path.join(role_path, var_file)
        if os.path.exists(var_path):
            with open(var_path, 'r') as file:
                lines = file.readlines()
            for i, line in enumerate(lines):
                if line.strip().startswith('#'):
                    description = line.strip('# ').strip()
                    var_line = lines[i + 1].strip()
                    var_name, var_value = var_line.split(':', 1)
                    variables[var_name.strip()] = var_value.strip()
                    descriptions[var_name.strip()] = description

    table_header = "| Variable | Default Value | Description |\n| --- | --- | --- |\n"
    table_rows = "".join([f"| `{var}` | `{variables[var].replace('|', '\\|')}` | {descriptions[var]} |\n"
                          for var in variables])

    return table_header + table_rows


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
