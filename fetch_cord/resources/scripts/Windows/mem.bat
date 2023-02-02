@echo off

setlocal EnableExtensions DisableDelayedExpansion

:GetTotalMemory
for /F "skip=1" %%M in ('%SystemRoot%\System32\wbem\wmic.exe ComputerSystem GET TotalPhysicalMemory') do set "TotalMemory=%%M" & goto GetAvailableMemory
:GetAvailableMemory
for /F "skip=1" %%M in ('%SystemRoot%\System32\wbem\wmic.exe OS GET FreePhysicalMemory') do set "AvailableMemory=%%M" & goto ProcessValues

:ProcessValues
set "TotalMemory=%TotalMemory:~0,-6%"
set /A TotalMemory+=50
set /A TotalMemory/=1073
set /A TotalMemory*=1024
set /A AvailableMemory/=1024
set /A UsedMemory=TotalMemory - AvailableMemory
set /A TotalMemory/=1024
set /A UsedMemory/=1024

echo %UsedMemory% GB / %TotalMemory% GB
endlocal