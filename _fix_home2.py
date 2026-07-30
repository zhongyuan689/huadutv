import re
p = r'C:\Users\zjtyl\Desktop\box-main\app\src\main\java\com\github\tvbox\osc\bbox\ui\activity\HomeActivity.java'

data = open(p, 'rb').read()
# 1) strip UTF-8 BOM if present
if data[:3] == b'\xef\xbb\xbf':
    data = data[3:]
    print('stripped BOM')
else:
    print('no BOM at head; bytes[:4]=', data[:4].hex())

s = data.decode('utf-8', errors='replace')
lines = s.split('\n')

fixed = 0
for i, l in enumerate(lines):
    if l.count('"') % 2 == 1 and not l.lstrip().startswith('//'):
        body = l.rstrip()
        if body.endswith(');'):
            body = body[:-2] + '");'
        elif body.endswith(';'):
            body = body[:-1] + '";'
        else:
            body = body + '"'
        lines[i] = body
        fixed += 1
        print('L%d fixed odd-quote -> %r' % (i + 1, body[:80]))

out = '\n'.join(lines)
open(p, 'wb').write(out.encode('utf-8'))
print('wrote UTF-8 no-BOM; fixed lines:', fixed, 'total lines:', len(lines))
