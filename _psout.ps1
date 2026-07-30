$p = "C:\Users\zjtyl\Desktop\box-main\app\src\main\java\com\github\tvbox\osc\bbox\ui\activity\HomeActivity.java"
$bytes = [System.IO.File]::ReadAllBytes($p)
$text = [System.Text.Encoding]::GetEncoding('GB18030').GetString($bytes)
$lines = $text.Split("`n")
Write-Output "Total lines: $($lines.Count)"

$out = @()
$fixed = 0
$garbled = 0

foreach ($line in $lines) {
    $orig = $line
    
    # Fix 1: BootHelper split (line ~114)
    if ($line -match 'verifyPermissions.*BootHelper') {
        $idx = $line.IndexOf('verifyPermissions(this);')
        $end = $idx + 'verifyPermissions(this);'.Length
        $out += $line.Substring(0, $end)
        $out += '        com.github.tvbox.osc.bbox.receiver.BootHelper.showAutostartTipIfNeeded(this);'
        $fixed++
        continue
    }
    
    # Fix 2: Truncated LOG.i strings -> LOG.i("");
    if ($line -match 'LOG\.i\(".*"\s*;\s*$') {
        # Already complete
    } elseif ($line -match 'LOG\.i\("') {
        $line = '                LOG.i("");'
        $fixed++
    }
    
    # Fix 3: Empty lines with just \ufffd
    if ($line.Trim() -eq '' -or $line -match '^\s+$') {
        $out += ''
        continue
    }
    
    # Fix 4: Any remaining \ufffd -> strip
    if ($line -match '\ufffd') {
        $line = $line -replace '\ufffd', ''
        $garbled++
        $fixed++
    }
    
    $out += $line
}

Write-Output "Fixed: $fixed, Garbled stripped: $garbled"

# Write as UTF-8
$utf8 = New-Object System.Text.UTF8Encoding $false
[System.IO.File]::WriteAllText($p, ($out -join "`n"), $utf8)
Write-Output "Written UTF-8 no BOM"

# Verify
$bytes2 = [System.IO.File]::ReadAllBytes($p)
$text2 = [System.Text.Encoding]::UTF8.GetString($bytes2)
$lines2 = $text2.Split("`n")
Write-Output "Verify: $($lines2.Count) lines"

# Find remaining issues
$issues = 0
for ($i = 0; $i -lt $lines2.Count; $i++) {
    $l = $lines2[$i]
    if ($l -match '[\ufffd\u0000]') { Write-Output "Issue line $($i+1): $($l.Substring(0, [Math]::Min(60, $l.Length)))"; $issues++ }
    if ($l -match '^[^/].*[\ufffd\u0000]') { $issues++ }
}
Write-Output "Total issues: $issues"
