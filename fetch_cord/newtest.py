from fetch_cord.computer.Computer import Computer

if __name__ == '__main__':
    pc = Computer()
    
    print('Detected OS : ' + pc.os)

    if pc.neofetchwin:
        print('Detected Neofetch : neofetch-win')

    if pc.neofetch:
        print('Detected Neofetch : neofetch')

    if len(pc.cpulist) == 0:
        print('No CPU detected !')
    else:
        for cpu in pc.cpulist:
            print('Detected CPU : ' + cpu.model)

    if len(pc.disklist) == 0:
        print('No Disk detected !')
    else:
        for disk in pc.disklist:
            print('Detected Disk : ' + disk)

    print('Detected Memory : ' + pc.memory)
    print('Detected OS info : ' + pc.osinfo)
    print('Detected Motherboard : ' + pc.motherboard)