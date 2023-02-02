# Get total physical memory (in bytes)
$TotalMemory = (Get-CimInstance -ClassName Win32_ComputerSystem).TotalPhysicalMemory

# Get available physical memory (in bytes)
$AvailableMemory = (Get-CimInstance -ClassName Win32_PerfFormattedData_PerfOS_Memory).AvailableBytes

# Convert values to GB
$TotalMemory = [int64]$TotalMemory/1024/1024/1024
$AvailableMemory = [int64]$AvailableMemory/1024/1024/1024

# Calculate used memory
$UsedMemory = $TotalMemory - $AvailableMemory

# Output used and total memory in GB
Write-Output ("{0:N2} GB / {1:N2} GB" -f $UsedMemory, $TotalMemory)
