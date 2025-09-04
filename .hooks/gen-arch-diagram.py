#!/usr/bin/env python3
"""
Ansible Collection Mermaid Diagram Generator

Generates a Mermaid diagram from an Ansible collection structure.
"""

from pathlib import Path
import argparse

class AnsibleCollectionAnalyzer:
    def __init__(self, collection_path: str):
        self.collection_path = Path(collection_path)
        self.structure = {
            'roles': [],
            'modules': [],
            'playbooks': [],
            'workflows': []
        }

    def analyze(self):
        """Analyze the Ansible collection structure"""
        # Analyze roles
        roles_path = self.collection_path / 'roles'
        if roles_path.exists():
            for role_dir in roles_path.iterdir():
                if role_dir.is_dir() and not role_dir.name.startswith('.'):
                    self.structure['roles'].append({
                        'name': role_dir.name,
                        'has_molecule': (role_dir / 'molecule').exists()
                    })

        # Analyze modules
        modules_path = self.collection_path / 'plugins' / 'modules'
        if modules_path.exists():
            for module_file in modules_path.glob('*.py'):
                if not module_file.name.startswith('__'):
                    self.structure['modules'].append(module_file.stem)

        # Analyze playbooks
        playbooks_path = self.collection_path / 'playbooks'
        if playbooks_path.exists():
            for item in playbooks_path.iterdir():
                if item.is_dir() and not item.name.startswith('.'):
                    self.structure['playbooks'].append({
                        'name': item.name,
                        'has_molecule': (item / 'molecule').exists()
                    })

        # Analyze GitHub workflows
        workflows_path = self.collection_path / '.github' / 'workflows'
        if workflows_path.exists():
            for workflow_file in workflows_path.glob('*.yml'):
                self.structure['workflows'].append(workflow_file.stem)

        return self.structure

def generate_mermaid(structure):
    """Generate Mermaid diagram"""
    lines = ["```mermaid", "graph TD"]
    lines.append("    Collection[Ansible Collection]")

    # Add modules
    if structure['modules']:
        lines.append("    Collection --> Modules[📦 Modules]")
        for i, module in enumerate(structure['modules']):
            lines.append(f"    Modules --> M{i}[{module}]")

    # Add roles
    if structure['roles']:
        lines.append("    Collection --> Roles[🎭 Roles]")
        for i, role in enumerate(structure['roles']):
            role_label = role['name']
            if role['has_molecule']:
                role_label += " ✅"
            lines.append(f"    Roles --> R{i}[{role_label}]")

    # Add playbooks
    if structure['playbooks']:
        lines.append("    Collection --> Playbooks[📚 Playbooks]")
        for i, playbook in enumerate(structure['playbooks']):
            pb_label = playbook['name']
            if playbook['has_molecule']:
                pb_label += " ✅"
            lines.append(f"    Playbooks --> P{i}[{pb_label}]")

    # Add workflows
    if structure['workflows']:
        lines.append("    Collection --> Workflows[🔄 CI/CD]")
        for i, workflow in enumerate(structure['workflows']):
            lines.append(f"    Workflows --> W{i}[{workflow}]")

    lines.append("```")
    return '\n'.join(lines)

def main():
    parser = argparse.ArgumentParser(
        description='Generate Mermaid diagram from Ansible collection'
    )
    parser.add_argument('path', nargs='?', default='.',
                       help='Path to Ansible collection (default: current directory)')
    parser.add_argument('-o', '--output', default='arch-diagram/collection_mermaid.md',
                       help='Output file (default: arch-diagram/collection_mermaid.md)')

    args = parser.parse_args()

    # Analyze collection
    analyzer = AnsibleCollectionAnalyzer(args.path)
    structure = analyzer.analyze()

    # Generate Mermaid diagram
    mermaid_content = generate_mermaid(structure)

    # Save to file
    output_file = Path(args.output)
    output_file.write_text(mermaid_content)

    print(f"✓ Mermaid diagram saved to {output_file}")
    print(f"\nCollection summary:")
    print(f"  • Roles: {len(structure['roles'])}")
    print(f"  • Modules: {len(structure['modules'])}")
    print(f"  • Playbooks: {len(structure['playbooks'])}")
    print(f"  • Workflows: {len(structure['workflows'])}")
    print(f"\nPaste the contents of {output_file} into your README.md")

if __name__ == "__main__":
    main()
