def ReadAlias():
    with open("C:/cell3/mt/modules/pyexec/alias.txt", "r", encoding="utf-8") as f:
        return f.readlines()

def OnExecute(*s: list):
    MT.HelpMessage[f"mt {ReadAlias()[0]} <command>"] = "Execute Python command"
    MT.HelpMessage["mt pyexec_alias <alias>"] = "Set alias for pyexec command"

    if len(s) > 1:
        args = s[1:]
        if args[0] == ReadAlias()[0]:
            exec(" ".join(args[1:]))
            return "break"
        elif args[0] == "pyexec_alias":
            with open("C:/cell3/mt/modules/pyexec/alias.txt", "w", encoding="utf-8") as f:
                f.write(" ".join(args[1:]))
            print("PYEXEC Alias successfuly updated!")
            return "break"