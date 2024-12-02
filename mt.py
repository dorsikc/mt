import os
import sys
import requests

class MT:
    Exception_Unknown = "Unknown Exception"
    Exception_Python = "Python Exception"
    Exception_Command = "Command Exception"
    Exception_Args = "Argument Exception"
    Exception_Global = "Exception"
    Exception_Install = "Installing Exception"
    ExceptionFormat = "{exception}: {message}."


    ModuleInstalledMessage = ["Module '{module}' installed/updated successfuly!"]
    Modules = []
    DefaultProjectDirection = "C:/cell3/mt/projects/"
    ModuleCreatedMessage = ["Project '{module}' created successfuly!"]
    ProjectTypes = [
        {"id":"module", "projectfileproperties":[], "createfolder":True, "commands":[], "files":[{"content":"# On Init ScriptShell\ndef OnInit():\n    # Your code here\n    return", "name":"module.py"}]},
        {"id":"console", "projectfileproperties":[], "createfolder":True, "commands":[], "files":[{"content":"# Basic console application template\ndef Main():\n    print('Hello, World!')\n    return\nif __name__ == '__main__':\n    Main()", "name":"ConsoleApplication.py"}]},

        {"id":"dev_multifile", "projectfileproperties":[], "createfolder":True, "commands":[], "files":[{"content":"File #1", "name":"File_1.txt"}, {"content":"File #2", "name":"File_2.txt"}]},
        {"id":"dev_command", "projectfileproperties":[], "createfolder":False, "commands":["dotnet new console --name {pr_name} --output {pr_path}/{pr_name}"], "files":[]},
        {"id":"dev_projectprop", "projectfileproperties":[["newkey","value"]], "createfolder":True, "commands":[], "files":[]}
    ]
    ProjectTypesForListCommand = [
        {"id":"dotnet", "command":"dotnet new {com_list} --name {pr_name} --output {pr_path}/{pr_name}"}
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

    def RaiseException(exception: str, message: str): print(MT.ExceptionFormat.format(exception=exception, message=message))

    def ReadProjectFileProp(file: str, prop: str):
        with open(file, "r", encoding="utf-8") as f_:
            for line in f_.readlines():
                if str(line).startswith(prop):
                    return str(line).split("=")[1]
                else: return False

    def Execute(command: list):
        cret = True
        cc_ = MT.InitCommandDef(command)
        if cc_ == "break": cret = False; return "break"
        if cret == True:
            #try:
                args = command[1:]
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
                        except Exception as e: MT.RaiseException(MT.Exception_Install, e)
                        
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
                        except Exception as e: MT.RaiseException(MT.Exception_Install, e)

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
                            for projecttype in MT.ProjectTypesForListCommand:
                                if args[1].lower() == projecttype["id"].lower():
                                    ddir = MT.DefaultProjectDirection
                                    if len(args) > 4:
                                        ddir = " ".join(args[4:])
                                    if not os.path.exists(f"{ddir}/{args[3]}"):
                                        os.makedirs(f"{ddir}/{args[3]}")
                                        os.system(str(projecttype["command"]).format(pr_name=args[3], pr_path=ddir, pr_type=args[2], com_list=args[2]))
                                        print(MT.ModuleCreatedMessage[0].format(module=args[3]))
                                    else:
                                        print(MT.ModuleExist[0].format(project=args[3]))

                            if args[1].lower() == "project":
                                project_type_found = False
                                for projecttype in MT.ProjectTypes:
                                    if args[2].lower() == str(projecttype["id"]).lower():
                                        project_type_found = True
                                        ddir = MT.DefaultProjectDirection
                                        if len(args) > 4: 
                                            ddir = " ".join(args[4:])
                                        if not os.path.exists(f"{ddir}/{args[3]}"):
                                            if projecttype["createfolder"] == True: os.makedirs(f"{ddir}/{args[3]}")

                                            for __command in projecttype["commands"]:
                                                os.system(str(__command).format(pr_name=args[3], pr_path=ddir, pr_type=args[2]))
                                            for file in projecttype["files"]:
                                                with open(f"{ddir}/{args[3]}/{file["name"]}", "w", encoding="utf-8") as f:
                                                    f.write(file["content"])
                                            with open(f"{ddir}/{args[3]}/project.txt", "w", encoding="utf-8") as f_:
                                                f_.write(f"project_type={projecttype["id"]}\n")
                                                for prop_ in projecttype["projectfileproperties"]:
                                                    f_.write(f"{prop_[0]}={prop_[1]}\n")

                                            print(MT.ModuleCreatedMessage[0].format(module=args[3]))
                                        else:
                                            print(MT.ModuleExist[0].format(project=args[3]))
                                        break
                                if not project_type_found:
                                    print(MT.InvalidProjectType[0])

                            else:
                                MT.RaiseException(MT.Exception_Args, f"Unknown creation type: {args[1]}")
                        except Exception as e:
                            MT.RaiseException(MT.Exception_Global, e)
                    elif args[0] == "!INSTALLPIP":
                        try: __import__(args[1])
                        except ImportError: os.system(f"pip install {args[1]}")
                        except Exception as e: MT.RaiseException(MT.Exception_Global, e)
                        else: MT.RaiseException(MT.Exception_Command, f"Unknown command!")
                    else: MT.RaiseException(MT.Exception_Command, f"Unknown command! ({command}||{args})")

            #except Exception as e: MT.RaiseException(MT.Exception_Global, f"Command error ({e})")

if __name__ == "__main__":
    Input = sys.argv
    if len(Input) == 1:
        MT.Execute(["mt", "about"])
        pass

    cc_ = MT.Execute(Input)
    if cc_ == "break": pass