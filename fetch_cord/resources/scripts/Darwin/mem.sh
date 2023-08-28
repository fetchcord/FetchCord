# Get total physical memory (in bytes)
TotalMemory=$(cat /proc/meminfo | grep MemTotal | awk '{print $2}')

# Get available physical memory (in bytes)
AvailableMemory=$(cat /proc/meminfo | grep MemFree | awk '{print $2}')

# Convert values to GB
TotalMemory=$(expr $TotalMemory / 1024 / 1024)
AvailableMemory=$(expr $AvailableMemory / 1024 / 1024)

# Calculate used memory
UsedMemory=$(expr $TotalMemory - $AvailableMemory)

# Output used and total memory in GB
echo "$UsedMemory GB / $TotalMemory GB"
