
import re
import os

chapter_titles = {
    1: "Tipos de Datos y Coerción",
    2: "Cadenas",
    3: "Operadores de Igualdad y Comparación",
    4: "El Alcance (Scope)",
    5: "Arreglos",
    6: "Objetos",
    7: "Funciones",
    8: "Estructuras de Control Modernas",
    9: "Programación Asíncrona",
    10: "Objetos Globales y Utilidades"
}

string_titles = [
    "Quiero pizza",
    "Backticks y el operador de corto circuito and",
    "Interpolación de cadenas",
    "Interpolación de cadenas clásico",
    "Spread operator con cadenas",
    "Multiples maneras de expandir cadenas",
    "Invertir una cadena con split, reverse y join",
    "Operadores + y - con cadenas y números",
    "typeof de expresiones extrañas",
    "¿Concatenaciones o sumas aritméticas?",
    "length en cadenas y arreglos",
    "Restas de cadenas y números",
    "El método repeat de las cadenas"
]

def get_blocks(content):
    content = re.sub(r'\n---\n+', '\n---\n', content)
    parts = re.split(r'\n---\n', content)
    blocks = [p.strip() for p in parts if p.strip()]
    return blocks

def process():
    all_retos = []
    all_sols = []
    
    for ch in range(1, 11):
        for prefix in ['retos', 'soluciones']:
            file = f'{prefix}-cap{ch}.qmd'
            if not os.path.exists(file): continue
            with open(file, 'r') as f:
                content = f.read()
                # Remove chapter title line
                content = re.sub(r'^# .*\n', '', content)
                blocks = get_blocks(content)
                for b in blocks:
                    if prefix == 'retos':
                        all_retos.append(b)
                    else:
                        all_sols.append(b)

    # Match Reto to Solucion
    pairs = []
    found_sol_indices = set()
    for r_block in all_retos:
        sol_id_match = re.search(r'\(#(sec-sol-.*?)\)', r_block)
        if sol_id_match:
            sol_id = sol_id_match.group(1)
            found = False
            for i, s_block in enumerate(all_sols):
                if i not in found_sol_indices and f'{{#{sol_id}}}' in s_block:
                    pairs.append((r_block, s_block))
                    found_sol_indices.add(i)
                    found = True
                    break

    # Now we have pairs. Classify them.
    # Grouping by original "logic" (using headers/titles)
    final_groups = {i: [] for i in range(1, 11)}
    
    for r_block, s_block in pairs:
        # 1. Check if string
        is_string = False
        for st in string_titles:
            if st in r_block:
                is_string = True
                break
        
        if is_string:
            final_groups[2].append((r_block, s_block))
            continue
            
        # 2. Otherwise determine chapter from original header if possible
        match = re.search(r'## Reto ([\d\.]+)', r_block)
        if match:
            curr_ch = int(match.group(1).split('.')[0])
            # Mapping from "before this migration" state:
            # 1 -> 1
            # 3 -> 3 (was 2)
            # 4 -> 4 (was 3)
            # 5 -> 5 (was 4)
            # 6 -> 6 (was 5)
            # 7 -> 7 (was 6)
            # 8 -> 8 (was 7)
            # 9 -> 9 (was 8)
            # 10 -> 10 (was 9)
            if curr_ch in final_groups:
                final_groups[curr_ch].append((r_block, s_block))

    # Phase 3: Writing back and renumbering
    id_map = {}
    
    # We'll first update all headers and build the global ID map
    processed_chapters = {}
    for ch, items in final_groups.items():
        new_retos = []
        new_sols = []
        for y, (r, s) in enumerate(items, 1):
            # Update Reto header and ID
            r_match = re.search(r'## Reto [\d\.]+: (.*?) \{#(.*?)\}', r)
            if r_match:
                title = r_match.group(1)
                old_id = r_match.group(2)
                new_id = f'sec-cap{ch}-reto{y}'
                id_map[old_id] = new_id
                r = re.sub(r'## Reto [\d\.]+: (.*?) \{#.*?\}', f'## Reto {ch}.{y}: {title} {{#{new_id}}}', r)
                
            # Update Solution header and ID
            s_match = re.search(r'## Reto [\d\.]+ \{#(.*?)\}', s)
            if s_match:
                old_sid = s_match.group(1)
                new_sid = f'sec-sol-cap{ch}-reto{y}'
                id_map[old_sid] = new_sid
                s = re.sub(r'## Reto [\d\.]+ \{#.*?\}', f'## Reto {ch}.{y} {{#{new_sid}}}', s)
            
            new_retos.append(r)
            new_sols.append(s)
        processed_chapters[ch] = (new_retos, new_sols)

    # Global replacement of links and teaser text
    for ch, (retos, sols) in processed_chapters.items():
        final_retos = []
        for r in retos:
            for old, new in id_map.items():
                r = r.replace(f'#{old}', f'#{new}')
            final_retos.append(r)
            
        final_sols = []
        for y, s in enumerate(sols, 1):
            for old, new in id_map.items():
                s = s.replace(f'#{old}', f'#{new}')
            # Fix teaser text
            s = re.sub(r'La respuesta del \[Reto [\d\.]+\]', f'La respuesta del [Reto {ch}.{y}]', s)
            final_sols.append(s)
            
        # Write files
        with open(f'retos-cap{ch}.qmd', 'w') as f:
            f.write(f'# {chapter_titles[ch]}\n\n' + '\n\n---\n\n'.join(final_retos) + '\n')
            
        with open(f'soluciones-cap{ch}.qmd', 'w') as f:
            f.write(f'# Soluciones - {chapter_titles[ch]}\n\n' + '\n\n---\n\n'.join(final_sols) + '\n')

if __name__ == "__main__":
    process()
