@echo off
setlocal enabledelayedexpansion

for /f "delims=" %%a in ('reg query HKLM\Software\Microsoft\Windows\CurrentVersion\Uninstall /f "Package" /s ^| find /c "HKEY_LOCAL_MACHINE"') do (
  set result=%%a
)

echo %result% packages
