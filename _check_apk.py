import zipfile, traceback

apk = r'C:\Users\zjtyl\Desktop\花都影视_源码构建.apk'
try:
    z = zipfile.ZipFile(apk)
    names = z.namelist()
    print('Total entries:', len(names))
    # find manifest
    if 'AndroidManifest.xml' not in names:
        print('NO AndroidManifest.xml in APK!')
        print('Sample entries:', names[:10])
    else:
        data = z.read('AndroidManifest.xml')
        print('manifest size:', len(data))
        keys = ['HomeActivity', 'category.HOME', 'category.LAUNCHER',
                'BootReceiver', 'RECEIVE_BOOT', 'BootHelper',
                'com.github.tvbox.osc.bbox']
        for k in keys:
            b16 = k.encode('utf-16-le')
            b8 = k.encode('utf-8')
            print('%-28s utf16=%d utf8=%d' % (k, data.count(b16), data.count(b8)))
except Exception as e:
    traceback.print_exc()
