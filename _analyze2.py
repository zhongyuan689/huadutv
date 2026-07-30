p = r'C:\Users\zjtyl\Desktop\box-main\app\src\main\java\com\github\tvbox\osc\bbox\ui\activity\HomeActivity.java'
data = open(p, 'rb').read()
text = data.decode('utf-8', errors='replace')
lines = text.split('\n')

# white-list of valid chars to KEEP
def keep(ch):
    o = ord(ch)
    if o < 128:
        return True
    if 0x4E00 <= o <= 0x9FFF:   # CJK
        return True
    if 0x3400 <= o <= 0x4DBF:   # CJK ext A
        return True
    if 0x3000 <= o <= 0x303F:   # CJK punctuation
        return True
    if 0xFF01 <= o <= 0xFF0F:   # fullwidth ! " # $ % & ' ( ) * + , - . /
        return True
    if 0xFF1A <= o <= 0xFF20:   # fullwidth : ; < = > ? @
        return True
    if 0xFF3B <= o <= 0xFF40:   # fullwidth [ \ ] ^ _
        return True
    if 0xFF5B <= o <= 0xFF65:   # fullwidth { | } ~ and katakana
        return True
    return False

garbled_lines = []
for i, line in enumerate(lines):
    if any(not keep(c) for c in line):
        garbled_lines.append((i+1, line))

print('Total garbled lines:', len(garbled_lines))
for ln, line in garbled_lines[:25]:
    print('L%04d: %r' % (ln, line[:140]))

# Also detect lines that look like truncated string literals (LOG.i etc.)
print('\n--- LOG.i / truncated-string candidate lines ---')
for i, line in enumerate(lines):
    if 'LOG.i' in line or 'Toast' in line:
        if '"' in line:
            # count quotes
            q = line.count('"')
            if q % 2 != 0:
                print('L%04d (odd quotes): %r' % (i+1, line[:140]))
        else:
            # LOG.i( without any quote -> truncated
            print('L%04d (no quote): %r' % (i+1, line[:140]))
