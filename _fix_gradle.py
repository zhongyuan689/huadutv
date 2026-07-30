import re
p = r'C:\Users\zjtyl\Desktop\box-main\build.gradle'
s = open(p, 'rb').read().decode('utf-8')
# only replace the non-comment line(s): line starts with optional whitespace then 'maven { url ...'
new_s, n = re.subn(
    r"(?m)^(\s*)maven \{ url 'http://9xi4o\.tk/maven2' \}(?!\s*; allowInsecureProtocol)",
    r"\1maven { url 'http://9xi4o.tk/maven2'; allowInsecureProtocol = true }",
    s
)
print('replacements:', n)
open(p, 'wb').write(new_s.encode('utf-8'))
print('--- after ---')
for i, l in enumerate(new_s.split('\n'), 1):
    if '9xi4o' in l:
        print(i, repr(l))
