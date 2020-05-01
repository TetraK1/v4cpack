import zipfile

from pathlib import Path

packfp = Path('./v4cpack.pk3').resolve()

pack = zipfile.ZipFile(packfp)
karts = []
for fname in pack.namelist():
    if fname[-1] == '/': continue
    if fname.split('/')[-1][:6] != 'S_SKIN': continue
    with pack.open(fname) as f:
        text = f.read().decode()
    lines = text.split('\n')
    props = {}
    for line in lines:
        line = line.split('=')
        key = line[0].strip()
        try: value = line[1].strip()
        except IndexError: continue
        props[key] = value
    karts.append({
        'name': props['realname'],
        'speed': max(min(int(props['kartspeed']), 9), 1),
        'weight': max(min(int(props['kartweight']), 9), 1)
    })
pack.close()

karts = sorted(karts, key=lambda k: k['name'])

with open('names.txt', 'w') as f:
    for kart in karts:
        f.write(kart['name'] + '\n')

table = [[[] for j in range(9)] for i in range(9)]
for kart in karts:
    table[kart['speed'] - 1][kart['weight'] - 1].append(kart['name'])

with open('table.csv', 'w') as f:
    f.write('W/S')
    for i in range(1,10):
        f.write(f',Speed {i}')
    f.write('\n')
    for weight in range(1,10):
        f.write(f'Weight {weight}')
        for speed in range(1, 10):
            f.write(',"')
            for kart in table[speed - 1][weight - 1]:
                f.write(kart + '\n')
            f.write('"')
        f.write('\n')