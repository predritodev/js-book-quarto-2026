
import re
import os

# Ultra-safe fragments
targets = [
    "Operadores + y - con cadenas y números",
    "Operadores `+` y `-` con cadenas y números",
    "typeof de expresiones extrañas",
    "`typeof` de expresiones extrañas",
    "length en cadenas y arreglos",
    "`length` en cadenas y arreglos",
    "Restas de cadenas y números",
    "El método repeat de las cadenas",
    "El método `repeat` de las cadenas",
    "Invertir una cadena con split",
    "Invertir una cadena con `split`"
]

def get_blocks(content):
    parts = re.split(r'\n---\n', content)
    intro = parts[0]
    blocks = [p.strip() for p in parts[1:] if p.strip()]
    return intro, blocks

def move():
    with open('retos-cap2.qmd', 'r') as f: r2_intro, r2_blocks = get_blocks(f.read())
    with open('soluciones-cap2.qmd', 'r') as f: s2_intro, s2_blocks = get_blocks(f.read())

    for ch in [1, 5, 10]:
        r_file = f'retos-cap{ch}.qmd'
        s_file = f'soluciones-cap{ch}.qmd'
        if not os.path.exists(r_file): continue
        
        with open(r_file, 'r') as f: r_intro, r_blocks = get_blocks(f.read())
        with open(s_file, 'r') as f: s_intro, s_blocks = get_blocks(f.read())
        
        new_r = []
        moved_s = []
        
        for rb in r_blocks:
            found = False
            for t in targets:
                if t in rb:
                    found = True
                    break
            
            if found:
                if rb not in r2_blocks:
                    r2_blocks.append(rb)
                mid_match = re.search(r'\(#(sec-sol-.*?)\)', rb)
                if mid_match:
                    sid = mid_match.group(1)
                    for sb in s_blocks:
                        if f'{{#{sid}}}' in sb:
                            if sb not in s2_blocks:
                                s2_blocks.append(sb)
                                moved_s.append(sb)
                            break
            else:
                new_r.append(rb)
        
        new_s = [sb for sb in s_blocks if sb not in moved_s]
        
        with open(r_file, 'w') as f: f.write(r_intro + '\n\n---\n\n' + '\n\n---\n\n'.join(new_r) + '\n')
        with open(s_file, 'w') as f: f.write(s_intro + '\n\n---\n\n' + '\n\n---\n\n'.join(new_s) + '\n')

    with open('retos-cap2.qmd', 'w') as f: f.write(r2_intro + '\n\n---\n\n' + '\n\n---\n\n'.join(r2_blocks) + '\n')
    with open('soluciones-cap2.qmd', 'w') as f: f.write(s2_intro + '\n\n---\n\n' + '\n\n---\n\n'.join(s2_blocks) + '\n')

if __name__ == "__main__":
    move()
