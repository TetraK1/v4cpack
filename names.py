import zipfile

from pathlib import Path

packfp = Path('./v4cpack.pk3').resolve()

pack = zipfile.ZipFile(packfp)
names = []
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
    names.append(props['realname'])

names.sort()
with open('names.txt', 'w') as f:
    for name in names:
        f.write(name)
        f.write('\n')

pack.close()
pack = zipfile.ZipFile(packfp, mode='a')
pack.write('yuh.txt', arcname='hibiki/yuh.txt')
pack.close()