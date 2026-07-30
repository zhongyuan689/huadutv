p = r'C:\Users\zjtyl\Desktop\box-main\app\src\main\java\com\github\tvbox\osc\bbox\ui\activity\HomeActivity.java'
data = open(p, 'rb').read()
text = data.decode('utf-8-sig')
lines = text.split('\n')

with open(r'C:\Users\zjtyl\Desktop\box-main\_full.txt', 'w', encoding='utf-8') as f:
    for i, line in enumerate(lines):
        f.write('%04d | %s\n' % (i+1, line))

print('%d lines' % len(lines))
