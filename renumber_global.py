
import re
import os

def renumber():
    # Phase 1: Collect all reto headers and build mapping
    # id_map[old_id] = new_id
    id_map = {}
    
    # We'll store (file_path, line_index, title, old_id, new_id)
    retos_to_update = []
    
    for ch in range(1, 11):
        filename = f'retos-cap{ch}.qmd'
        if not os.path.exists(filename): continue
        
        with open(filename, 'r') as f:
            lines = f.readlines()
            
        y = 1
        for i, line in enumerate(lines):
            # Match any "## Reto ... {#...}"
            match = re.search(r'## Reto [\d\.]+: (.*?) \{#(sec-cap\d+-reto\d+|sec-array-\d+)\}', line)
            if match:
                title = match.group(1).strip()
                old_id = match.group(2)
                new_id = f'sec-cap{ch}-reto{y}'
                id_map[old_id] = new_id
                retos_to_update.append({
                    'file': filename,
                    'line_idx': i,
                    'title': title,
                    'new_header': f'## Reto {ch}.{y}: {title} {{#{new_id}}}\n'
                })
                y += 1
                
    # Solution IDs
    for ch in range(1, 11):
        filename = f'soluciones-cap{ch}.qmd'
        if not os.path.exists(filename): continue
        
        with open(filename, 'r') as f:
            lines = f.readlines()
            
        y = 1
        for i, line in enumerate(lines):
            # Match "## Reto X.Y {#...}"
            match = re.search(r'## Reto [\d\.]+ \{#(sec-sol-cap\d+-reto\d+|sec-sol-array-\d+)\}', line)
            if match:
                old_id = match.group(1)
                new_id = f'sec-sol-cap{ch}-reto{y}'
                id_map[old_id] = new_id
                retos_to_update.append({
                    'file': filename,
                    'line_idx': i,
                    'new_header': f'## Reto {ch}.{y} {{#{new_id}}}\n'
                })
                y += 1

    # Phase 2: Apply header updates
    # Group by file to avoid re-opening
    from collections import defaultdict
    by_file = defaultdict(list)
    for item in retos_to_update:
        by_file[item['file']].append(item)
        
    for filename, items in by_file.items():
        with open(filename, 'r') as f:
            lines = f.readlines()
        for item in items:
            lines[item['line_idx']] = item['new_header']
        with open(filename, 'w') as f:
            f.writelines(lines)

    # Phase 3: Update all internal links globally
    # This is a broad replacement of #old_id with #new_id
    for ch in range(1, 11):
        for prefix in ['retos', 'soluciones']:
            filename = f'{prefix}-cap{ch}.qmd'
            if not os.path.exists(filename): continue
            
            with open(filename, 'r') as f:
                content = f.read()
                
            for old_id, new_id in id_map.items():
                content = content.replace(f'#{old_id}', f'#{new_id}')
            
            # Special case: Update solution teaser text "La respuesta del [Reto X.Y]"
            # We need to find the correct local number for each block in solutions
            if prefix == 'soluciones':
                # We'll use a sequential replacement for "La respuesta del [Reto ...]"
                y_sol = 1
                def repl_teaser(m):
                    nonlocal y_sol
                    res = f'La respuesta del [Reto {ch}.{y_sol}]'
                    y_sol += 1
                    return res
                content = re.sub(r'La respuesta del \[Reto [\d\.]+\]', repl_teaser, content)

            with open(filename, 'w') as f:
                f.write(content)

if __name__ == "__main__":
    renumber()
