ps_code = r'''
$p = "C:\Users\zjtyl\Desktop\box-main\app\src\main\java\com\github\tvbox\osc\bbox\ui\activity\HomeActivity.java"
$bytes = [System.IO.File]::ReadAllBytes($p)
$text = [System.Text.Encoding]::GetEncoding('GB18030').GetString($bytes)
$lines = $text.Split("`n")
Write-Output ("Total lines: " + $lines.Count)
$out = @()
$fixed = 0
foreach ($line in $lines) {
    if ($line -match 'verifyPermissions.*BootHelper') {
        $idx = $line.IndexOf('verifyPermissions(this);')
        $end = $idx + 'verifyPermissions(this);'.Length
        $out += $line.Substring(0, $end)
        $out += '        com.github.tvbox.osc.bbox.receiver.BootHelper.showAutostartTipIfNeeded(this);'
        $fixed++
        continue
    }
    if ($line -match 'LOG\.i\("') {
        $hasEnd = $line -match 'LOG\.i\("[^"]*"'
        if (-not $hasEnd) {
            $line = '                LOG.i("");'
            $fixed++
        }
    }
    if ($line -match '\ufffd') {
        $line = $line -replace '\ufffd', ''
        $fixed++
    }
    $out += $line
}
Write-Output ("Fixed: " + $fixed)
$utf8 = New-Object System.Text.UTF8Encoding $false
[System.IO.File]::WriteAllText($p, ($out -join "`n"), $utf8)
$bytes2 = [System.IO.File]::ReadAllBytes($p)
$text2 = [System.Text.Encoding]::UTF8.GetString($bytes2)
$lines2 = $text2.Split("`n")
Write-Output ("Verify: " + $lines2.Count + " lines")
$issues = 0
for ($i = 0; $i -lt $lines2.Count; $i++) {
    $l = $lines2[$i]
    if ($l.IndexOf("`u{fffd}") -ge 0 -or $l.IndexOf("`u{0000}") -ge 0) {
        Write-Output ("Issue line " + ($i+1) + ": " + $l.Substring(0, [Math]::Min(80, $l.Length)))
        $issues++
    }
}
Write-Output ("Total issues: " + $issues)
'''

with open(r'C:\Users\zjtyl\Desktop\box-main\_psout.ps1', 'w', encoding='utf-8-sig') as f:
    f.write(ps_code)

import subprocess, os
result = subprocess.run(
    ['powershell', '-ExecutionPolicy', 'Bypass', '-File', r'C:\Users\zjtyl\Desktop\box-main\_psout.ps1'],
    capture_output=True, timeout=30
)
# Output in latin-1 to handle any non-UTF8 bytes
stdout = result.stdout.encode('latin-1', errors='replace').decode('latin-1')
stderr = result.stderr.encode('latin-1', errors='replace').decode('latin-1')
print(stdout)
if stderr:
    print('STDERR:', stderr[:300])
