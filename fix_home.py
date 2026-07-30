import codecs, re

p = r'C:\Users\zjtyl\Desktop\box-main\app\src\main\java\com\github\tvbox\osc\bbox\ui\activity\HomeActivity.java'
data = open(p, 'rb').read()
gb = codecs.getdecoder('gb18030')
text, _ = gb(data, 'replace')

# Split on any line ending, strip \r
raw_lines = re.split(r'\r\n|\r|\n', text)
lines = [l.rstrip('\r') for l in raw_lines]

print('Raw splits: %d, stripped: %d' % (len(raw_lines), len(lines)))

out = []
fixed = 0

for line in lines:
    # Fix 1: BootHelper split
    if 'verifyPermissions' in line and 'BootHelper' in line:
        idx = line.index('verifyPermissions(this);')
        part1 = line[:idx + len('verifyPermissions(this);')]
        out.append(part1)
        out.append('        com.github.tvbox.osc.bbox.receiver.BootHelper.showAutostartTipIfNeeded(this);')
        fixed += 1
        continue
    
    # Fix 2: Truncated LOG.i strings
    if 'LOG.i' in line and '"' in line:
        log_idx = line.index('LOG.i("')
        rest = line[log_idx + len('LOG.i("'):]
        if '"' not in rest:
            line = '                LOG.i("");'
            fixed += 1
        elif '\ufffd' in line:
            line = line.replace('\ufffd', '')
            fixed += 1
    
    # Fix 3: Comment + if on same line (fragments check)
    if 'fragments.size()' in line and 'doExit' not in line and 'if' not in line:
        line = '        // 检查fragments状态        if (this.fragments.size() <= 0 || this.sortFocused >= this.fragments.size() || this.sortFocused < 0) {'
        fixed += 1
    
    # Fix 4: Long garbled comment before "else if (sortFocused != 0)"
    if 'sortFocused != 0' in line and len(line) > 100:
        line = '        // 如果当前不是第一个界面，则将列表设置到上一个界面        else if (this.sortFocused != 0) {'
        fixed += 1
    
    # Fix 5: Toast with garbled text
    if 'Toast.makeText' in line and 'mContext' in line:
        if '\ufffd' in line:
            line = '            Toast.makeText(mContext, "再按一次返回键退出应用", Toast.LENGTH_SHORT).show();'
            fixed += 1
    
    # Fix 6: Any remaining \ufffd
    if '\ufffd' in line:
        line = line.replace('\ufffd', '')
        fixed += 1
    
    # Fix 7: Lines that are just \r -> empty
    if line.strip() == '':
        out.append('')
        continue
    
    out.append(line)

print('In: %d, Out: %d, Fixed: %d' % (len(lines), len(out), fixed))

# Write as UTF-8 with Unix line endings (no \r)
with open(p, 'w', encoding='utf-8', newline='\n') as f:
    f.write('\n'.join(out))
    f.write('\n')  # trailing newline

# Verify
data2 = open(p, 'rb').read()
text2 = data2.decode('utf-8')
lines2 = text2.split('\n')
print('Verify: %d lines' % len(lines2))

with open(r'C:\Users\zjtyl\Desktop\box-main\_verify.txt', 'w', encoding='utf-8') as f:
    for lineno in [113, 114, 115, 116, 369, 370, 371, 372, 554, 555, 556, 568, 569, 570]:
        idx = lineno - 1
        if idx < len(lines2):
            f.write('Line %d: %s\n' % (lineno, repr(lines2[idx])))
