$Font = (Get-ItemProperty -Path "HKCU:\Console").FaceName

if ($Font -eq "__DefaultTTFont__") {
    $RegistryPath = "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Console\TrueTypeFont"
    $DefaultFont = (Get-ItemProperty -Path $RegistryPath).00
    Write-Host "$DefaultFont"
}
else {
    Write-Host "$Font"
}