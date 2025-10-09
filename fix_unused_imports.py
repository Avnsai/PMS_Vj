#!/usr/bin/env python3
"""
Script to automatically remove unused imports from TypeScript files
based on TypeScript compiler errors.
"""

import re
import subprocess
import json
from pathlib import Path
from collections import defaultdict

def get_typescript_errors():
    """Run TypeScript compiler and get all errors."""
    result = subprocess.run(
        ['yarn', 'build'],
        cwd='/app/frontend',
        capture_output=True,
        text=True
    )
    return result.stderr + result.stdout

def parse_unused_errors(output):
    """Parse TypeScript output for unused variable errors."""
    unused_pattern = re.compile(r"src/(.*?)\((\d+),(\d+)\): error TS6133: '(.+?)' is declared but its value is never read\.")
    unused_type_pattern = re.compile(r"src/(.*?)\((\d+),(\d+)\): error TS6196: '(.+?)' is declared but never used\.")
    
    unused_vars = defaultdict(list)
    
    for match in unused_pattern.finditer(output):
        file_path, line, col, var_name = match.groups()
        unused_vars[file_path].append({
            'line': int(line),
            'col': int(col),
            'name': var_name,
            'type': 'variable'
        })
    
    for match in unused_type_pattern.finditer(output):
        file_path, line, col, type_name = match.groups()
        unused_vars[file_path].append({
            'line': int(line),
            'col': int(col),
            'name': type_name,
            'type': 'type_declaration'
        })
    
    return unused_vars

def remove_unused_imports(file_path, unused_items):
    """Remove unused imports from a TypeScript file."""
    full_path = Path('/app/frontend/src') / file_path
    
    if not full_path.exists():
        return False
    
    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')
    
    # Group unused items by line
    unused_by_line = defaultdict(list)
    for item in unused_items:
        unused_by_line[item['line']].append(item['name'])
    
    modified = False
    new_lines = []
    
    for line_num, line in enumerate(lines, 1):
        if line_num in unused_by_line:
            unused_names = unused_by_line[line_num]
            
            # Handle import statements
            if line.strip().startswith('import'):
                new_line = line
                for name in unused_names:
                    # Remove from named imports
                    new_line = re.sub(rf',?\s*{re.escape(name)}\s*,?', '', new_line)
                    # Clean up double commas
                    new_line = re.sub(r',\s*,', ',', new_line)
                    # Clean up trailing/leading commas in braces
                    new_line = re.sub(r'\{\s*,', '{', new_line)
                    new_line = re.sub(r',\s*\}', '}', new_line)
                    new_line = re.sub(r'\{\s*\}', '{}', new_line)
                
                # If import is now empty, skip the line
                if re.search(r'import\s+\{\s*\}\s+from', new_line) or new_line.strip() == 'import':
                    modified = True
                    continue
                
                if new_line != line:
                    modified = True
                    new_lines.append(new_line)
                else:
                    new_lines.append(line)
            
            # Handle const/let declarations
            elif 'const' in line or 'let' in line:
                # Check if entire line should be removed
                should_remove = False
                for name in unused_names:
                    if re.search(rf'\b(const|let)\s+{re.escape(name)}\b', line):
                        should_remove = True
                        break
                
                if should_remove:
                    modified = True
                    continue
                else:
                    new_lines.append(line)
            
            # Handle type/interface declarations
            elif 'interface' in line or 'type' in line:
                should_remove = False
                for name in unused_names:
                    if re.search(rf'\b(interface|type)\s+{re.escape(name)}\b', line):
                        should_remove = True
                        break
                
                if should_remove:
                    # Remove the entire interface/type declaration
                    modified = True
                    # Skip this line and continue
                    in_declaration = True
                    brace_count = line.count('{') - line.count('}')
                    if brace_count <= 0:
                        continue
                    # Mark to skip subsequent lines of this declaration
                    skip_until_closed = brace_count
                    new_lines.append(f'// REMOVED_TYPE: {name}')
                    continue
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)
    
    if modified:
        # Write back
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
        return True
    
    return False

def main():
    print("Running TypeScript compiler to find unused imports...")
    output = get_typescript_errors()
    
    print("Parsing errors...")
    unused_vars = parse_unused_errors(output)
    
    print(f"Found unused variables in {len(unused_vars)} files")
    
    fixed_count = 0
    for file_path, items in sorted(unused_vars.items()):
        print(f"Processing {file_path}: {len(items)} unused items")
        if remove_unused_imports(file_path, items):
            fixed_count += 1
            print(f"  ✓ Fixed {file_path}")
    
    print(f"\n✅ Processed {fixed_count} files")
    print("\nRun 'yarn build' again to check remaining errors.")

if __name__ == '__main__':
    main()
