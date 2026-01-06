
import re
import os

def renumber():
    id_map = {}
    reto_headers = []
    sol_headers = []
    
    # 1. Collect all and build map
    for ch in range(1, 11):
        r_file = f'retos-cap{ch}.qmd'
        if os.path.exists(r_file):
            with open(r_file, 'r') as f: lines = f.readlines()
            y = 1
            for i, line in enumerate(lines):
                # Header format: ## Reto ... {#...}
                match = re.search(r'## Reto [\d\.]+: (.*?) \{#(.*?)\}', line)
                if match:
                    title = match.group(1).strip()
                    old_id = match.group(2)
                    new_id = f'sec-cap{ch}-reto{y}'
                    id_map[old_id] = new_id
                    reto_headers.append({
                        'file': r_file, 'line_idx': i, 'title': title, 
                        'new_line': f'## Reto {ch}.{y}: {title} {{#{new_id}}}\n'
                    })
                    y += 1

        s_file = f'soluciones-cap{ch}.qmd'
        if os.path.exists(s_file):
            with open(s_file, 'r') as f: lines = f.readlines()
            y = 1
            for i, line in enumerate(lines):
                # Header format: ## Reto X.Y {#...}
                match = re.search(r'## Reto [\d\.]+ \{#(.*?)\}', line)
                if match:
                    old_id = match.group(1)
                    new_id = f'sec-sol-cap{ch}-reto{y}'
                    id_map[old_id] = new_id
                    sol_headers.append({
                        'file': s_file, 'line_idx': i,
                        'new_line': f'## Reto {ch}.{y} {{#{new_id}}}\n',
                        'ch': ch, 'y': y
                    })
                    y += 1

    # 2. Apply headers
    from collections import defaultdict
    files_to_update = defaultdict(list)
    for h in reto_headers + sol_headers:
        files_to_update[h['file']].append(h)
        
    for filename, headers in files_to_update.items():
        with open(filename, 'r') as f: lines = f.readlines()
        for h in headers:
            lines[h['line_idx']] = h['new_line']
        with open(filename, 'w') as f: f.writelines(lines)

    # 3. Apply global link updates and teaser text
    for ch in range(1, 11):
        for prefix in ['retos', 'soluciones']:
            file = f'{prefix}-cap{ch}.qmd'
            if not os.path.exists(file): continue
            with open(file, 'r') as f: content = f.read()
            
            # Replace IDs in links
            for old, new in id_map.items():
                content = content.replace(f'#{old}', f'#{new}')
            
            # Fix teaser text in solutions
            if prefix == 'soluciones':
                y_s = 1
                def repl_t(m):
                    nonlocal y_s
                    res = f'La respuesta del [Reto {ch}.{y_s}]'
                    y_s += 1
                    return res
                content = re.sub(r'La respuesta del \[Reto [\d\.]+\]', repl_t, content)
            
            with open(file, 'w') as f: f.write(content)

if __name__ == "__main__":
    renumber()
