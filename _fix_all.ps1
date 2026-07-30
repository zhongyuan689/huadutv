$p = "C:\Users\zjtyl\Desktop\box-main\app\src\main\java\com\github\tvbox\osc\bbox\ui\activity\HomeActivity.java"
$bytes = [System.IO.File]::ReadAllBytes($p)
$gb18030 = [System.Text.Encoding]::GetEncoding('GB18030')
$text = $gb18030.GetString($bytes)
$lines = $text -split "`n"

$out = @()
$fixedCount = 0

foreach ($line in $lines) {
    $orig = $line
    
    # Fix 1: BootHelper call on same line as verifyPermissions - split
    if ($line -match 'verifyPermissions.*BootHelper') {
        $idx = $line.IndexOf('verifyPermissions(this);')
        $part1 = $line.Substring(0, $idx + 'verifyPermissions(this);'.Length)
        $out += $part1
        $out += '        com.github.tvbox.osc.bbox.receiver.BootHelper.showAutostartTipIfNeeded(this);'
        $fixedCount++
        continue
    }
    
    # Fix 2: LOG.i with truncated strings -> LOG.i("");
    if ($line -match 'LOG\.i\("[^"]+"\s*;\s*$' -and $line -notmatch 'LOG\.i\("[^"]+"\)\s*;\s*$') {
        # Check if string is incomplete (has no closing quote followed by );)
        $line = '                LOG.i("");'
        $fixedCount++
    }
    
    # Fix 3: Comment with garbled chars about fragments check
    if ($line -match 'if.*fragments\.size\(\)\s*<=' -or $line -match 'doExit\(\)') {
        # These lines are correct, just the comment on the previous line was garbled
    }
    
    # Fix 4: Line with garbled comment about fragments state check (before if condition)
    if ($line -match '妫.*鏌.*fragments|检查.*fragments') {
        $line = '        // 检查fragments状态        if (this.fragments.size() <= 0 || this.sortFocused >= this.fragments.size() || this.sortFocused < 0) {'
        $fixedCount++
    }
    
    # Fix 5: Line with very long garbled comment (else if sortFocused != 0)
    if ($line -match '婵.*鐏' -or ($line -match 'sortFocused\s*!=\s*0' -and $line.Length -gt 100)) {
        $line = '        // 如果当前不是第一个界面，则将列表设置到上一个界面        else if (this.sortFocused != 0) {'
        $fixedCount++
    }
    
    # Fix 6: Toast message with garbled text
    if ($line -match 'Toast.*makeText.*mContext.*$') {
        if ($line -match '閫.*鍑哄簲鐢') {
            $line = '            Toast.makeText(mContext, "再按一次返回键退出应用", Toast.LENGTH_SHORT).show();'
            $fixedCount++
        }
    }
    
    # Fix 7: Other garbled comments (any line with \ufffd)
    if ($line -match '\ufffd') {
        # Just strip the replacement characters
        $line = $line -replace '\ufffd', ''
        $fixedCount++
    }
    
    $out += $line
}

Write-Output "Lines in: $($lines.Count), Lines out: $($out.Count), Fixed: $fixedCount"

# Write as UTF-8 (no BOM)
$utf8 = New-Object System.Text.UTF8Encoding $false
[System.IO.File]::WriteAllText($p, ($out -join "`n"), $utf8)
Write-Output "Written as UTF-8 no BOM"

# Verify
$bytes2 = [System.IO.File]::ReadAllBytes($p)
$text2 = [System.Text.Encoding]::UTF8.GetString($bytes2)
$lines2 = $text2 -split "`n"
Write-Output "Verify: $($lines2.Count) lines"

# Show key lines
Write-Output ""
Write-Output "Line 115: $($lines2[114])"
Write-Output "Line 370: $($lines2[369])"
Write-Output "Line 372: $($lines2[371])"
Write-Output "Line 555: $($lines2[554])"
Write-Output "Line 556: $($lines2[555])"
Write-Output "Line 569: $($lines2[568])"
