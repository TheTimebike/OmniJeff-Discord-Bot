import threading, os, json, sys, glob

tokenToPick = sys.argv[1]

with open("../tokenHolster.txt", 'r') as jsonfile:
    tokenHolster = json.load(jsonfile)

try:
    disToken = tokenHolster[tokenToPick]
except Exception as ex:
    print("The token passed is not valid")
    if coreConfig["mode"] == "debug" or coreConfig["mode"] == "experimental":
        print(ex)
    exit()

if not os.path.isfile("./settings.config"):
    print("Config file missing, automated shutdown")
    exit()

with open("./settings.config", 'r') as jsonfile:
    coreConfig = json.load(jsonfile)

threadDict, moduleDict = {}, {}
class Module():
    def __init__(self, sepModule):
        self.configExists = os.path.isfile("../modules/{0}".format(sepModule))
        with open("../modules/{0}/settings.config".format(sepModule), 'r') as jsonfile:
            self.config = json.load(jsonfile)
        self.name = sepModule

def loadModule(dirModule): ## Creates a class for the module, checks the config for validity and then creates a subprocess
    moduleDict[dirModule] = Module(sepModule = dirModule)
    localModuleClass = moduleDict[dirModule]
    if localModuleClass.config["status"] != "enabled":
        print("FATAL: Module {0} is disabled in the config".format(localModuleClass.name))
        return
    if localModuleClass.config["author"] != "TheTimebike" and localModuleClass.config["mode"] != "experimental":
        print("WARNING: Module {0} is not an official add-on")
        return
    print("Initialised module: {0}".format(localModuleClass.name))
    os.system("python ../modules/{0}/Main.py {1}".format(localModuleClass.name, disToken))

modList = next(os.walk('../modules/'))[1]
for sepModule in modList:
    try:
        threadDict[sepModule] = threading.Thread(target=loadModule, args=(sepModule,)).start()
    except Exception as ex:
        print("Error while loading: {0}".format(sepModule))
        if coreConfig["mode"] == "debug" or coreConfig["mode"] == "experimental":
            print(ex)
