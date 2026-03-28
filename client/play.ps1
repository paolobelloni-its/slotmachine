param(
  [string]$HostName = "127.0.0.1",
  [int]$Port = 7777
)

$client = New-Object System.Net.Sockets.TcpClient
$client.Connect($HostName, $Port)

$stream = $client.GetStream()
$reader = New-Object System.IO.StreamReader($stream)
$writer = New-Object System.IO.StreamWriter($stream)
$writer.AutoFlush = $true

function Read-Available {
  $out = ""
  Start-Sleep -Milliseconds 80
  while ($stream.DataAvailable) {
    $buf = New-Object byte[] 4096
    $n = $stream.Read($buf, 0, $buf.Length)
    if ($n -le 0) { break }
    $out += [System.Text.Encoding]::UTF8.GetString($buf, 0, $n)
    Start-Sleep -Milliseconds 20
  }
  return $out
}

# banner iniziale
$banner = Read-Available
if ($banner) { Write-Host -NoNewline $banner }

try {
  while ($true) {
    $cmd = Read-Host ">"

    $writer.WriteLine($cmd)

    Start-Sleep -Milliseconds 80
    $resp = Read-Available
    if ($resp) { Write-Host -NoNewline $resp }

    if ($cmd.ToLower() -in @("quit","exit")) { break }
  }
}
finally {
  $reader.Close()
  $writer.Close()
  $stream.Close()
  $client.Close()
}