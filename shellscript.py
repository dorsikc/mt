import os
import sys
import requests

class MT:
    ModuleInstalledMessage = ["Module '{module}' installed/updated successfuly!"]
    Modules = []
    DefaultProjectDirection = "C:/cell3/mt/projects/"
    ModuleCreatedMessage = ["Project '{module}' created successfuly!"]
    ProjectTypes = [
        {"id":"module", "files":[{"content":"# On Init ScriptShell\ndef OnInit():\n    # Your code here\n    return", "name":"module.py"}]},
        {"id":"console", "files":[{"content":"# Basic console application template\ndef Main():\n    print('Hello, World!')\n    return\nif __name__ == '__main__':\n    Main()", "name":"ConsoleApplication.py"}]},

        {"id":"dev_multifile", "files":[{"content":"File #1", "name":"File_1.txt"}, {"content":"File #2", "name":"File_2.txt"}]}
    ]
    ProjectTypesMessage = [
        "Module - Template of MT module",
        "Console - Basic console application template"
    ]
    ModuleExist = ["Project '{project}' already exist!"]
    ModuleListMessage = ["Module list"]
    AboutMessage = ["Information: MT 0.2.1-alpha"]
    InvalidProjectType = ["Invalid project type!"]
    HelpMessage = {
        "mt help":"Show this",
        "mt install <module>":"Install module from official GITHUB repository",
        "mt list":"Show list of modules (include custom module messages only!)",
        "mt about//mt":"Show about MT information",
        "mt !INSTALLFROM <username> <repository> <branch> <path to module folder> <module>":"Install module from additional GitHub repository",
        "mt !INSTALLPIP <lib>":"Install Python library",
        "mt new <project type (mt prlist)> <project name> <path (optional)>":"Create new project by template",
        "mt prlist":"Show list of project types"
    }

    def Init():
        Shell.CommandList["mt"] = "Main MT prefix command"
        Shell.StartMessages.append("MT initialized successfully!")
        if not os.path.exists("C:/cell3"): os.makedirs("C:/cell3")
        if not os.path.exists("C:/cell3/mt"): os.makedirs("C:/cell3/mt")
        if not os.path.exists("C:/cell3/mt/modules"): os.makedirs("C:/cell3/mt/modules")
        if not os.path.exists("C:/cell3/mt/projects"): os.makedirs("C:/cell3/mt/projects")
        for folder in os.listdir("C:/cell3/mt/modules"):
            for file in os.listdir(f"C:/cell3/mt/modules/{folder}"):
                if file.endswith(".py"):
                    with open(f"C:/cell3/mt/modules/{folder}/{file}", "r", encoding="utf-8") as _f:
                        exec(_f.read(), globals())
                        if "OnInit" in globals(): return globals()["OnInit"]()
    def InitCommandDef(command: str):
        for folder in os.listdir("C:/cell3/mt/modules"):
            for file in os.listdir(f"C:/cell3/mt/modules/{folder}"):
                if file.endswith(".py"):
                    with open(f"C:/cell3/mt/modules/{folder}/{file}", "r", encoding="utf-8") as _f:
                        exec(_f.read(), globals())
                        if "OnExecute" in globals(): return globals()["OnExecute"](command)
    def InitSimpleDef(cmd: str):
        for folder in os.listdir("C:/cell3/mt/modules"):
            for file in os.listdir(f"C:/cell3/mt/modules/{folder}"):
                if file.endswith(".py"):
                    with open(f"C:/cell3/mt/modules/{folder}/{file}", "r", encoding="utf-8") as _f:
                        exec(_f.read(), globals())
                        if cmd in globals(): return globals()[cmd]()

class Shell:
    StartMessages = ["ScriptShell 01", "Type -h for more information"]
    HelpMessages = ["==Help"]
    CWD = os.getcwd()
    SYS = sys
    EXE = SYS.executable
    ARGV = SYS.argv
    InputFormat = f"{CWD}> "
    CommandList = {
        "-e//-exit":"Exit",
        "-h//-help":"Output help",
        "-r//-restart//-reload":"Restart",
        "win <cmd>":"Execute Windows command",
        "echo <var>//echo.":"Print string",
        "cls//clear":"Clear console"
    }
    UnRegCommandList = []
    Exception_Unknown = "Unknown Exception"
    Exception_Python = "Python Exception"
    Exception_Command = "Command Exception"
    Exception_Args = "Argument Exception"
    Exception_Global = "Exception"
    Exception_Install = "Installing Exception"
    ExceptionFormat = "{exception}: {message}."
    Message_Exit = ["Exit.."]
    Message_Restart = ["Restarting.."]
    Message_Clear = []
    Message_Win = []
    Message_Python = []
    Message_Echo = []
    Message_EchoDot = []
    ClearOnRestart = True
    Working = False

    def RaiseException(exception: str, message: str): print(Shell.ExceptionFormat.format(exception=exception, message=message))
    def AddCommand(command: str, messages: str, execute): Shell.UnRegCommandList.append({"cmd":command, "oninitmsg":messages, "exec":execute})

    def Execute(command: str):
        cret = True
        cc_ = MT.InitCommandDef(command)
        if cc_ == "break": cret = False; return "break"
        if Shell.Working and cret == True:
            try:
                cmd = command.split()[0]
                args = command.split()[1:]

                if cmd == "-h" or cmd == "-help":
                    for msg in Shell.HelpMessages:
                        print(msg)
                    for cmd, desc in Shell.CommandList.items():
                        print(f"{cmd} -- {desc}")
                elif cmd == "-r" or cmd == "-restart" or cmd == "-reload":
                    MT.InitSimpleDef("OnRestart")
                    for msg in Shell.Message_Restart: print(msg)
                    Shell.Working = False
                    if Shell.ClearOnRestart: os.system("cls")
                    os.execl(Shell.EXE, Shell.EXE, *Shell.ARGV)
                elif cmd == "-e" or cmd == "-exit":
                    MT.InitSimpleDef("OnExit")
                    for msg in Shell.Message_Exit: print(msg)
                    Shell.Working = False
                    os._exit(0)
                    sys.exit()
                elif cmd == "win":
                    MT.InitSimpleDef("OnExecuteWin")
                    for msg in Shell.Message_Win: print(msg)
                    os.system(" ".join(args))
                elif cmd == "echo":
                    for msg in Shell.Message_Echo: print(msg)
                    print(" ".join(args))
                elif cmd == "echo.":
                    for msg in Shell.Message_EchoDot: print(msg)
                    print("")
                elif cmd == "cls" or cmd == "clear":
                    MT.InitSimpleDef("OnClearing")
                    for msg in Shell.Message_Clear: print(msg)
                    os.system("cls")
                elif any(cmd in __c for __c in ["py", "py3", "python", "python3"]):
                    try:
                        for msg in Shell.Message_Python: print(msg)
                        exec(" ".join(args))
                    except Exception as e: Shell.RaiseException(Shell.Exception_Python, e)
                elif cmd == "mt":
                    if len(args) > 0:
                        if args[0] == "install":
                            try:
                                if requests.get(f"https://raw.githubusercontent.com/dorsikc/mt/main/modules/{args[1]}/files.txt").status_code != 404:
                                    req_ = requests.get(f"https://raw.githubusercontent.com/dorsikc/mt/main/modules/{args[1]}/files.txt")
                                    files = req_.text.split("\n")
                                    for file in files:
                                        if not os.path.exists(f"C:/cell3/mt/modules/{args[1]}"):
                                            os.makedirs(f"C:/cell3/mt/modules/{args[1]}")
                                        if not os.path.exists(f"C:/cell3/mt/modules/{args[1]}/{file}"):
                                            with open(f"C:/cell3/mt/modules/{args[1]}/{file}", "w", encoding="utf-8") as f:
                                                req_ = requests.get(f"https://raw.githubusercontent.com/dorsikc/mt/main/modules/{args[1]}/{file}")
                                                f.write(req_.text)
                                    for msg in MT.ModuleInstalledMessage: print(msg.format(module=args[1]))
                                elif requests.get(f"https://raw.githubusercontent.com/dorsikc/mt/main/modules/{args[1]}/module.py").status_code != 404:
                                    req = requests.get(f"https://raw.githubusercontent.com/dorsikc/mt/main/modules/{args[1]}/module.py")
                                    if not os.path.exists(f"C:/cell3/mt/modules/{args[1]}"):
                                        os.makedirs(f"C:/cell3/mt/modules/{args[1]}")
                                    with open(f"C:/cell3/mt/modules/{args[1]}/module.py", "w", encoding="utf-8") as f:
                                        f.write(req.text)
                                    for msg in MT.ModuleInstalledMessage: print(msg.format(module=args[1]))
                                else: print("Module not found or not supported")
                            except Exception as e: Shell.RaiseException(Shell.Exception_Install, e)
                        
                        # mt !INSTALLFROM {username} {repository} {branch} {path to module folder} {module}
                        elif args[0] == "!INSTALLFROM":
                            try:
                                if requests.get(f"https://raw.githubusercontent.com/{args[1]}/{args[2]}/{args[3]}/{args[4]}/{args[5]}/files.txt").status_code != 404:
                                    req_ = requests.get(f"https://raw.githubusercontent.com/{args[1]}/{args[2]}/{args[3]}/{args[4]}/{args[5]}/files.txt")
                                    files = req_.text.split("\n")
                                    for file in files:
                                        if not os.path.exists(f"C:/cell3/mt/modules/{args[5]}"):
                                            os.makedirs(f"C:/cell3/mt/modules/{args[5]}")
                                        if not os.path.exists(f"C:/cell3/mt/modules/{args[5]}/{file}"):
                                            with open(f"C:/cell3/mt/modules/{args[5]}/{file}", "w", encoding="utf-8") as f:
                                                req_ = requests.get(f"https://raw.githubusercontent.com/{args[1]}/{args[2]}/{args[3]}/{args[4]}/{args[5]}/{file}")
                                                f.write(req_.text)
                                    for msg in MT.ModuleInstalledMessage: print(msg.format(module=args[5]))
                                elif requests.get(f"https://raw.githubusercontent.com/{args[1]}/{args[2]}/{args[3]}/{args[4]}/{args[5]}/module.py").status_code != 404:
                                    req = requests.get(f"https://raw.githubusercontent.com/{args[1]}/{args[2]}/{args[3]}/{args[4]}/{args[5]}/module.py")
                                    if not os.path.exists(f"C:/cell3/mt/modules/{args[5]}"):
                                        os.makedirs(f"C:/cell3/mt/modules/{args[5]}")
                                    with open(f"C:/cell3/mt/modules/{args[5]}/module.py", "w", encoding="utf-8") as f:
                                        f.write(req.text)
                                    for msg in MT.ModuleInstalledMessage: print(msg.format(module=args[5]))
                                else: print("Module not found or not supported")
                            except Exception as e: Shell.RaiseException(Shell.Exception_Install, e)

                        elif args[0] == "list":
                            for msg in MT.ModuleListMessage: print(msg)
                            cc_ = MT.InitSimpleDef("OnModuleList")
                            if cc_ == "break": cret = False; return "break"
                        elif args[0] == "prlist":
                            for msg in MT.ProjectTypesMessage: print(msg)
                        elif args[0] == "about":
                            for msg in MT.AboutMessage: print(msg)
                        elif args[0] == "help":
                            for cmd, desc in MT.HelpMessage.items():
                                print(f"{cmd} -- {desc}")
                        elif args[0] == "new":
                            try:
                                project_type_found = False
                                for projecttype in MT.ProjectTypes:
                                    if args[1].lower() == str(projecttype["id"]).lower():
                                        project_type_found = True
                                        ddir = MT.DefaultProjectDirection
                                        if len(args) > 3: 
                                            ddir = " ".join(args[3:])
                                        if not os.path.exists(f"{ddir}/{args[2]}"):
                                            os.makedirs(f"{ddir}/{args[2]}")
                                            # Исправлено создание файлов
                                            for file in projecttype["files"]:
                                                with open(f"{ddir}/{args[2]}/{file["name"]}", "w", encoding="utf-8") as f:
                                                    f.write(file["content"])
                                            with open(f"{ddir}/{args[2]}/project.txt", "w", encoding="utf-8") as f_:
                                                f_.write(f"project_type={projecttype["id"]}\n")

                                            print(MT.ModuleCreatedMessage[0].format(module=args[2]))
                                        else:
                                            print(MT.ModuleExist[0].format(project=args[2]))
                                        break
                                if not project_type_found:
                                    print(MT.InvalidProjectType[0])
                            except Exception as e:
                                Shell.RaiseException(Shell.Exception_Global, e)
                        elif args[0] == "!INSTALLPIP":
                            try: __import__(args[1])
                            except ImportError: os.system(f"pip install {args[1]}")
                            except Exception as e: Shell.RaiseException(Shell.Exception_Global, e)
                        else: Shell.RaiseException(Shell.Exception_Command, f"Unknown command '{cmd}'")
                    else: Shell.Execute("mt about")

                else:
                    if len(Shell.UnRegCommandList) > 0:
                        for _cmd in Shell.UnRegCommandList:
                            if cmd == _cmd["cmd"]:
                                for _msg in _cmd["oninitmsg"]: print(_msg)
                                _cmd["exec"](command)
                            else: Shell.RaiseException(Shell.Exception_Command, f"Unknown command '{cmd}'")
                    else: Shell.RaiseException(Shell.Exception_Command, f"Unknown command '{cmd}'")

            except Exception as e: Shell.RaiseException(Shell.Exception_Global, f"Command error ({e})")

if __name__ == "__main__":
    #def _test(*command): print("Executed!")
    #Shell.UnRegCommandList.append({"cmd":"test", "oninitmsg":[], "exec":_test})

    Shell.Working = True

    MT.Init()

    for message in Shell.StartMessages: print(message)

    MT.InitSimpleDef("PostInit")
    while Shell.Working:
        Input = input(Shell.InputFormat)
        if Input.startswith("//"): continue
        else:
            cc_ = Shell.Execute(Input)
            if cc_ == "break": continue