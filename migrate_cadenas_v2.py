
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

# Fragments that are unique to the titles
targets = [
    {"frag": "Quiero pizza", "src_cap": 1},
    {"frag": "Backticks y el operador de corto circuito", "src_cap": 1},
    {"frag": "Interpolación de cadenas", "src_cap": 1}, # This might match both classic and modern
    {"frag": "length en cadenas y arreglos", "src_cap": 1},
    {"frag": "El método repeat de las cadenas", "src_cap": 1},
    {"frag": "Interpolación de cadenas clásico", "src_cap": 1},
    {"frag": "Spread operator con cadenas", "src_cap": 5},
    {"frag": "Multiples maneras de expandir cadenas", "src_cap": 10},
    {"frag": "Invertir una cadena con split", "src_cap": 10},
]

def get_blocks(content):
    parts = re.split(r'\n---\n', content)
    intro = parts[0]
    blocks = [p.strip() for p in parts[1:] if p.strip()]
    return intro, blocks

def migrate():
    # We will read cap 2 first to append to it if it exists
    cap2_retos = []
    cap2_sols = []
    if os.path.exists('retos-cap2.qmd'):
        with open('retos-cap2.qmd', 'r') as f:
            c2_intro, cap2_retos = get_blocks(f.read())
    else:
        c2_intro = "# Cadenas"
        
    if os.path.exists('soluciones-cap2.qmd'):
        with open('soluciones-cap2.qmd', 'r') as f:
            c2s_intro, cap2_sols = get_blocks(f.read())
    else:
        c2s_intro = "# Soluciones - Cadenas"

    # Process each source
    for ch in range(1, 11):
        r_file = f'retos-cap{ch}.qmd'
        s_file = f'soluciones-cap{ch}.qmd'
        
        if ch == 2 or not os.path.exists(r_file): continue
        
        with open(r_file, 'r') as f: r_intro, r_blocks = get_blocks(f.read())
        with open(s_file, 'r') as f: s_intro, s_blocks = get_blocks(f.read())
        
        new_r_blocks = []
        new_s_blocks = []
        
        moved_this_round_sols = []
        
        for r_block in r_blocks:
            found_to_move = False
            for t in targets:
                if t['frag'] in r_block:
                    found_to_move = True
                    break
            
            if found_to_move:
                if r_block not in cap2_retos:
                    cap2_retos.append(r_block)
                # Find Solution
                sol_id_match = re.search(r'\[Ver solución\]\(#(sec-sol-.*?)\)', r_block)
                if sol_id_match:
                    sol_id = sol_id_match.group(1)
                    for s_block in s_blocks:
                        if f'{{#{sol_id}}}' in s_block:
                            if s_block not in cap2_sols:
                                cap2_sols.append(s_block)
                            moved_this_round_sols.append(s_block)
                            break
            else:
                new_r_blocks.append(r_block)
        
        # Clean current chapter solutions
        final_s_blocks = [s for s in s_blocks if s not in moved_this_round_sols]
        
        # Write back
        with open(r_file, 'w') as f:
            f.write(r_intro + '\n\n---\n\n' + '\n\n---\n\n'.join(new_r_blocks) + '\n')
        with open(s_file, 'w') as f:
            f.write(s_intro + '\n\n---\n\n' + '\n\n---\n\n'.join(final_s_blocks) + '\n')

    # Update Cap 2
    with open('retos-cap2.qmd', 'w') as f:
        f.write('# Cadenas\n\n---\n\n' + '\n\n---\n\n'.join(cap2_retos) + '\n')
    with open('soluciones-cap2.qmd', 'w') as f:
        f.write('# Soluciones - Cadenas\n\n---\n\n' + '\n\n---\n\n'.join(cap2_sols) + '\n')

if __name__ == "__main__":
    migrate()
