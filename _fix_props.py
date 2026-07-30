import re
p = r'C:\Users\zjtyl\Desktop\box-main\gradle.properties'
s = open(p, 'rb').read().decode('utf-8')
print('BOM?', s.startswith('\ufeff'))
new_jvm = ('-Xmx2048m'
           ' --add-opens java.base/java.io=ALL-UNNAMED'
           ' --add-opens java.base/java.lang=ALL-UNNAMED'
           ' --add-opens java.base/java.lang.reflect=ALL-UNNAMED'
           ' --add-opens java.base/java.util=ALL-UNNAMED'
           ' --add-opens java.base/java.util.regex=ALL-UNNAMED'
           ' --add-opens java.base/java.util.concurrent=ALL-UNNAMED')
s2, n = re.subn(r'org\.gradle\.jvmargs=.*', 'org.gradle.jvmargs=' + new_jvm, s)
print('subn:', n)
open(p, 'wb').write(s2.encode('utf-8'))
print('written; jvmargs line:')
for l in s2.split('\n'):
    if 'jvmargs' in l:
        print(repr(l))
