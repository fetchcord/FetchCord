Get-WmiObject -Class Win32_Battery | Select-Object DeviceID | ForEach-Object {$_.DeviceID}