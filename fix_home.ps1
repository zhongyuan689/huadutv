$p = "C:\Users\zjtyl\Desktop\box-main\app\src\main\java\com\github\tvbox\osc\bbox\ui\activity\HomeActivity.java"
$bytes = [System.IO.File]::ReadAllBytes($p)
$gb18030 = [System.Text.Encoding]::GetEncoding('GB18030')
$text = $gb18030.GetString($bytes)
$lines = $text -split "`n"
Write-Output "Total lines: $($lines.Count)"

# Fix 1: Line 114 - split BootHelper onto new line
$line114 = $lines[113]
$idx = $line114.IndexOf('verifyPermissions(this);')
if ($idx -ge 0) {
    $end = $idx + 'verifyPermissions(this);'.Length
    $part1 = $line114.Substring(0, $end)
    $lines[113] = $part1
    # Insert new line after 114
    $newLine = '        com.github.tvbox.osc.bbox.receiver.BootHelper.showAutostartTipIfNeeded(this);'
    $newLines = @()
    for ($i = 0; $i -lt 114; $i++) { $newLines += $lines[$i] }
    $newLines += $newLine
    for ($i = 114; $i -lt $lines.Count; $i++) { $newLines += $lines[$i] }
    $lines = $newLines
    Write-Output "Line 114 fixed OK (now line 115)"
} else {
    Write-Output "WARNING: verifyPermissions not found"
}

# Now fix other broken lines by replacing with known-correct text
# Line 370: "            } else {" - correct
# Line 369 and 371: "LOG.i(" strings with garbled Chinese

# For lines that need Chinese fixes, we need to know the original text
# Strategy: Find lines with \ufffd replacement characters and replace them

# Find all \ufffd lines
Write-Output "`nSearching for replacement chars..."
$found = $false
for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -match '\ufffd') {
        Write-Output "Line $($i+1): $($lines[$i])"
        $found = $true
    }
}
if (-not $found) { Write-Output "No replacement chars found!" }

# Show context
Write-Output "`nContext 365-376:"
for ($i = 365; $i -lt 376; $i++) { Write-Output "  $($i+1): $($lines[$i])" }

Write-Output "`nContext 550-560:"
for ($i = 549; $i -lt 560; $i++) { Write-Output "  $($i+1): $($lines[$i])" }

Write-Output "`nContext 585-595:"
for ($i = 584; $i -lt 595; $i++) { Write-Output "  $($i+1): $($lines[$i])" }
