p = r'C:\Users\zjtyl\Desktop\box-main\app\src\main\java\com\github\tvbox\osc\bbox\ui\activity\HomeActivity.java'
data = open(p, 'rb').read()
import codecs
decoder = codecs.getdecoder('gb18030')
text, _ = decoder(data, 'replace')
lines = text.split('\n')

# Write all lines to a file for inspection
with open(r'C:\Users\zjtyl\Desktop\box-main\_all_lines.txt', 'w', encoding='utf-8') as f:
    for i, line in enumerate(lines):
        f.write('%04d | %s\n' % (i+1, line))

print('Written %d lines' % len(lines))
