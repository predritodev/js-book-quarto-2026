
import re
import os

def get_blocks(content):
    # Split by separator and filter empty
    parts = re.split(r'\n---\n', content)
    return [p.strip() for p in parts if p.strip()]

def find_reto(blocks, title_pattern):
    for i, block in enumerate(blocks):
        if re.search(title_pattern, block, re.IGNORECASE):
            return blocks.pop(i)
    return None

def migrate():
    # Load files
    with open('retos-cap1.qmd', 'r') as f: r1 = get_blocks(f.read())
    with open('soluciones-cap1.qmd', 'r') as f: s1 = get_blocks(f.read())
    
    with open('retos-cap5.qmd', 'r') as f: r5 = get_blocks(f.read())
    with open('soluciones-cap5.qmd', 'r') as f: s5 = get_blocks(f.read())
    
    with open('retos-cap10.qmd', 'r') as f: r10 = get_blocks(f.read())
    with open('soluciones-cap10.qmd', 'r') as f: s10 = get_blocks(f.read())

    # Chapter 2 content
    r2_content = []
    s2_content = []

    # Migration List (Pattern, Source Retos, Source Sols)
    targets = [
        (r'Reto 1\.10: Quiero pizza', r1, s1, '1.10'),
        (r'Reto 1\.12: Backticks', r1, s1, '1.12'),
        (r'Reto 1\.15: Interpolación de cadenas', r1, s1, '1.15'),
        (r'Reto 1\.17: length en cadenas', r1, s1, '1.17'),
        (r'Reto 1\.21: El método repeat', r1, s1, '1.21'),
        (r'Reto 1\.22: Interpolación de cadenas clásico', r1, s1, '1.22'),
        (r'Reto 4\.5: Spread operator con cadenas', r5, s5, '4.5'),
        (r'Reto 9\.2: Multiples maneras de expandir cadenas', r10, s10, '9.2'),
        (r'Reto 9\.3: Invertir una cadena', r10, s10, '9.3')
    ]

    for pattern, r_src, s_src, id_raw in targets:
        reto_block = find_reto(r_src, pattern)
        if reto_block:
            r2_content.append(reto_block)
            # For solutions, they don't have titles usually, they have ## Reto X.Y
            # I'll search by the ID in the search or just use the numbering if possible
            # Actually, solutions usually start with ## Reto X.Y
            sol_id_pattern = rf'## Reto {id_raw}'
            sol_block = find_reto(s_src, sol_id_pattern)
            if sol_block:
                s2_content.append(sol_block)

    # Write Cap 2
    with open('retos-cap2.qmd', 'w') as f:
        f.write('# Cadenas\n\n' + '\n\n---\n\n'.join(r2_content) + '\n')
    
    with open('soluciones-cap2.qmd', 'w') as f:
        f.write('# Soluciones - Cadenas\n\n' + '\n\n---\n\n'.join(s2_content) + '\n')

    # Save remaining
    with open('retos-cap1.qmd', 'w') as f: f.write('# Tipos de Datos y Coerción\n\n' + '\n\n---\n\n'.join(r1) + '\n')
    with open('soluciones-cap1.qmd', 'w') as f: f.write('# Soluciones - Tipos de Datos y Coerción\n\n' + '\n\n---\n\n'.join(s1) + '\n')
    
    with open('retos-cap5.qmd', 'w') as f: f.write('# Arreglos\n\n' + '\n\n---\n\n'.join(r5) + '\n')
    with open('soluciones-cap5.qmd', 'w') as f: f.write('# Soluciones - Arreglos\n\n' + '\n\n---\n\n'.join(s5) + '\n')
    
    with open('retos-cap10.qmd', 'w') as f: f.write('# Objetos Globales y Utilidades\n\n' + '\n\n---\n\n'.join(r10) + '\n')
    with open('soluciones-cap10.qmd', 'w') as f: f.write('# Soluciones - Objetos Globales y Utilidades\n\n' + '\n\n---\n\n'.join(s10) + '\n')

if __name__ == "__main__":
    migrate()
