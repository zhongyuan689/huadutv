# -*- coding: utf-8 -*-
import os

p = r'C:\Users\zjtyl\Desktop\box-main\app\src\main\java\com\github\tvbox\osc\bbox\ui\activity\HomeActivity.java'
data = open(p, 'rb').read()
text = data.decode('utf-8', errors='replace')
lines = text.split('\n')

def keep(ch):
    o = ord(ch)
    if o < 128:
        return True
    if 0x4E00 <= o <= 0x9FFF:    # CJK unified
        return True
    if 0x3400 <= o <= 0x4DBF:    # CJK ext A
        return True
    if 0x3000 <= o <= 0x303F:    # CJK punctuation
        return True
    # common fullwidth punctuation
    if 0xFF01 <= o <= 0xFF0F:
        return True
    if 0xFF1A <= o <= 0xFF20:
        return True
    if 0xFF3B <= o <= 0xFF40:
        return True
    if 0xFF5B <= o <= 0xFF65:
        return True
    return False

cleaned = []
removed = 0
for line in lines:
    new = ''.join(c for c in line if keep(c))
    removed += len(line) - len(new)
    cleaned.append(new)

out = '\n'.join(cleaned)
# strip any BOM if present, write UTF-8 no BOM
if out.startswith('\ufeff'):
    out = out[1:]
with open(p, 'wb') as f:
    f.write(out.encode('utf-8'))

print('removed garbled chars:', removed)
print('lines:', len(cleaned))
print('wrote UTF-8 (no BOM)')

# sanity: report any line that still has odd number of double quotes AND contains (" )
prob = []
for i, line in enumerate(cleaned):
    q = line.count('"')
    if q % 2 != 0 and ('LOG' in line or 'Toast' in line or '"' in line):
        prob.append((i+1, line))
print('suspicious quote lines:', len(prob))
for ln, l in prob[:10]:
    print('  L%04d: %s' % (ln, l[:140]))
