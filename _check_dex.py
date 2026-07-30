import zipfile, traceback
try:
    apk = r'C:\Users\zjtyl\Desktop\花都影视_源码构建.apk'
    z = zipfile.ZipFile(apk)
    dexs = [n for n in z.namelist() if n.endswith('.dex')]
    print('DEX files:', dexs)
    blob = b''
    for d in dexs:
        blob += z.read(d)
    print('Total dex bytes:', len(blob))
    keys = ['showAutostartTipIfNeeded', 'BootHelper', 'CustomDns', 'Dns.SYSTEM',
            'DEFAULT_LIVE_URL', 'DEFAULT_STORE_API_URL', 'ghfast.top', 'jsdelivr']
    for k in keys:
        print('%-28s count=%d' % (k, blob.count(k.encode('utf-8'))))
except Exception as e:
    traceback.print_exc()
