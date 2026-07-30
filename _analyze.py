import collections

p = r'C:\Users\zjtyl\Desktop\box-main\app\src\main\java\com\github\tvbox\osc\bbox\ui\activity\HomeActivity.java'
data = open(p, 'rb').read()
# Try GB18030 then UTF-8
try:
    text = data.decode('gb18030')
    enc = 'gb18030'
except Exception:
    text = data.decode('utf-8', errors='replace')
    enc = 'utf-8-replace'
print('decoded with', enc, 'len', len(text))

# Count non-ASCII chars by block
blocks = collections.Counter()
nonascii = 0
for ch in text:
    o = ord(ch)
    if o < 128:
        continue
    nonascii += 1
    if 0x4E00 <= o <= 0x9FFF:
        blocks['CJK'] += 1
    elif 0xFF00 <= o <= 0xFFEF:
        blocks['FULLWIDTH'] += 1
    elif 0xF000 <= o <= 0xFFFF:
        blocks['PUA_or_other_high'] += 1
    elif 0x3000 <= o <= 0x303F:
        blocks['CJK_punct'] += 1
    elif 0x2000 <= o <= 0x206F:
        blocks['gen_punct'] += 1
    else:
        blocks['other_%04X' % (o & 0xFF00)] += 1

print('non-ascii chars:', nonascii)
for k, v in blocks.most_common(20):
    print('  %-20s %d' % (k, v))

# Show a few sample lines containing non-CJK non-ascii
print('\n--- sample garbled lines ---')
show = 0
for i, line in enumerate(text.split('\n')):
    na = [c for c in line if ord(c) >= 128 and not (0x4E00 <= ord(c) <= 0x9FFF) and not (0x3000 <= ord(c) <= 0x303F)]
    if na and show < 12:
        print('%04d: %s' % (i+1, line[:120]))
        show += 1
