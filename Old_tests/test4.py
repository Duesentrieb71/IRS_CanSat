globalVar = 0

def changeGlobal():
    global globalVar
    globalVar = 1

def printGlobal():
    print(globalVar)

if __name__ == "__main__":
    changeGlobal()
    printGlobal()