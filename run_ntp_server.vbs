Set objShell = CreateObject("Wscript.Shell")
objShell.CurrentDirectory = "C:\Users\USUARIO\proyectos\ntp"
objShell.Run "%comspec% /k conda activate ntp_server && python main.py", 0, True
