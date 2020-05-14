import os
import re
import zipfile

from pathlib import Path

char_folder = Path('chars')
all_files = []

#get paths of all files in char_folder
for root, dirs, files in os.walk(char_folder):
    for fname in files:
        p = Path(root) / fname
        #p = p.relative_to(char_folder)
        all_files.append(p)

sskins = [f for f in all_files if f.name[:6] == 'S_SKIN']

#sort sskins on character realname
ss_dict = {}
for s in sskins:
    with open(s) as f: text = f.read()
    text = text.strip().splitlines()
    text = [line.split('=') for line in text]
    text = [line for line in text if len(line) == 2]
    text = {line[0].strip(): line[1].strip() for line in text}
    ss_dict[text['realname']] = s
sskins = [ss_dict[key] for key in sorted(ss_dict)]

#write files to pack
#sskin_files is the list of names used in the S_SKIN to indicate minimap and sound filenames
sskin_files = ['facerank', 'facewant', 'facemmap', 'DSKGLOAT', 'DSKWIN', 'DSKLOSE', 'DSKSLOW', 'DSKHURT1', 'DSKHURT2', 'DSKATTK1', 'DSKATTK2', 'DSKBOST1', 'DSKBOST2', 'DSKHITEM' ]
pack = zipfile.ZipFile('v4cpack.pk3', 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9)
#regex for matching sprite filenames
r = re.compile(r'^.{4}([A-S]\d){1,2}')
with pack:
    for s_index, s in enumerate(sskins):
        #get names of the minimap and sound files from the S_SKIN
        with open(s) as sf: stext = sf.read().strip()
        not_sprite_names = []
        for line in stext.splitlines():
            line = [i.strip() for i in line.split('=')]
            if len(line) != 2: continue
            if line[0] == 'realname': 
                p = (100 * s_index) // len(sskins)
                print(f'{p}%\tAdding {line[1]}')
            if line[0] not in sskin_files: continue
            not_sprite_names.append(line[1])

        #get all files in S_SKIN folder, split into different lists
        files = [f for f in all_files if f.parent == s.parent and f != s]
        not_sprites = []
        sprites = []
        others = []
        for f in files:
            for name in not_sprite_names:
                if not f.name.startswith(name): continue
                not_sprites.append(f)
                break
            else:
                if r.match(f.name):
                    sprites.append(f)
                else:
                    others.append(f)
        
        #write non-sprite files first, then S_SKIN, and lastly sprites
        for f in not_sprites: pack.write(f, f.relative_to(char_folder))
        for f in others: pack.write(f, f.relative_to(char_folder))
        pack.write(s, s.relative_to(char_folder))
        for f in sprites: pack.write(f, f.relative_to(char_folder))
print(f'{len(sskins)} skins added')