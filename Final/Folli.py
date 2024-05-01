import re
from MetaParser import functionParser

class functions:
    def __init__(self, funcName, funcParameters, funcScope):
        self.funcName = funcName
        self.parameters = funcParameters
        self.funcScope = funcScope


program = """ 
static void sugar ("string", ) {
     System.out.println("I just got sweet!");
}

static int cheap ("string", ) {
     System.out.println("I just got scammed!");
}

static char fancy (String[] args) {
    System.out.println("I just got 100 dollars!");
}


static boolean main ("string", ) {
     int number = 3;
     int fool = 4 * 5;
}
 """


functionList = []


regex = re.search(r'(?P<cppNonAccessModifier>static)[\s]*?(?P<cppReturnType>int|double|String|char|boolean|void)\s*(?P<cppFuncName>[a-zA-Z]*)[\s]*?\((?P<cppParameters>.*)\)[\s]*?{[\s]*?(?P<cppScope>[\s\S]*?)[\s]*?}(?P<after>[\s\S]*)', program)

while regex:
    functionList.append(functions(regex.group("cppFuncName"), regex.group("cppParameters"),regex.group("cppScope")))
    regex = re.search(r'(?P<cppNonAccessModifier>static)[\s]*?(?P<cppReturnType>int|double|String|char|boolean|void)\s*(?P<cppFuncName>[a-zA-Z]*)[\s]*?\((?P<cppParameters>.*)\)[\s]*?{[\s]*?(?P<cppScope>[\s\S]*?)[\s]*?}(?P<after>[\s\S]*)', regex.group("after"))

main = None
i = 0
for obj in functionList:
    if functionList[i].funcName == "main":
        originScope = functionList[i].funcScope
        parser = functionParser()
        parser.parse(originScope.strip())         #MAY BE THE ISSUE
        #print(originScope)
    else:
        print("NOT AT MAIN")
    i += 1

    
