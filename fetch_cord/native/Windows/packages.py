import winreg


def get_installed_software():
    software_list = []
    software_path = "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall"
    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, software_path) as software:
        try:
            for i in range(0, winreg.QueryInfoKey(software)[0]):
                software_name = winreg.EnumKey(software, i)
                with winreg.OpenKey(software, software_name) as subkey:
                    try:
                        software_list.append(
                            winreg.QueryValueEx(subkey, "DisplayName")[0]
                        )
                    except EnvironmentError:
                        pass
        except WindowsError:
            pass

    return software_list


def fetch() -> str:
    return f"{len(get_installed_software())} packages"
