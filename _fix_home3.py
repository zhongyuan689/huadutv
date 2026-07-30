p = r'C:\Users\zjtyl\Desktop\box-main\app\src\main\java\com\github\tvbox\osc\bbox\ui\activity\HomeActivity.java'
s = open(p, 'rb').read().decode('utf-8', errors='replace')
lines = s.split('\n')
print('LINE1 before:', repr(lines[0]))
lines[0] = 'package com.github.tvbox.osc.bbox.ui.activity;'
out = '\n'.join(lines)
open(p, 'wb').write(out.encode('utf-8'))
print('LINE1 after :', repr(lines[0]))
# verify head bytes
b = open(p, 'rb').read(8)
print('head hex    :', b.hex())
