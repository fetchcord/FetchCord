@wmic os get Version | findstr /v "^$" | find /v "Version"