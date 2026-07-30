$p = "C:\Users\zjtyl\Desktop\box-main\app\src\main\java\com\github\tvbox\osc\bbox\ui\activity\HomeActivity.java"
$bytes = [System.IO.File]::ReadAllBytes($p)
$gb18030 = [System.Text.Encoding]::GetEncoding('GB18030')
$text = $gb18030.GetString($bytes)
$lines = $text -split "`n"
Write-Output "Total lines: $($lines.Count)"

$found = $false
for ($i = 0; $i -lt $lines.Count; $i++) {
    $line = $lines[$i]
    if ($line -match '\ufffd') {
        Write-Output "BAD Line $($i+1): $line"
        $found = $true
    }
}
if (-not $found) { Write-Output "No bad chars!" }

Write-Output ""
Write-Output "Context 366-376:"
for ($i = 365; $i -lt 376; $i++) { Write-Output "  $($i+1): $($lines[$i])" }

Write-Output ""
Write-Output "Context 550-560:"
for ($i = 549; $i -lt 560; $i++) { Write-Output "  $($i+1): $($lines[$i])" }

Write-Output ""
Write-Output "Context 585-595:"
for ($i = 584; $i -lt 595; $i++) { Write-Output "  $($i+1): $($lines[$i])" }
