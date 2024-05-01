import re
from MetaParser import functionParser

class functions:
    def __init__(self, funcName, funcParameters, funcScope):
        self.funcName = funcName
        self.parameters = funcParameters
        self.funcScope = funcScope


program = """ 
static int main (intList) {
    String f = True;  
    if (3>1) {
        System.out.println(f);
    } 
}
"""


functionList = []


regex = re.search('(?P<cppNonAccessModifier>static)[\s]*?(?P<cppReturnType>int|double|String|char|boolean|void)\s*(?P<cppFuncName>[a-zA-Z]*)[\s]*?\((?P<cppParameters>.*)\)[\s]*?{[\s]*(?P<cppScope>.+[\s\S]*?)}\n+(?P<after>[\s\S]*)', program)

while regex:
    functionList.append(functions(regex.group("cppFuncName"), regex.group("cppParameters"),regex.group("cppScope")))
    regex = re.search("(?P<cppNonAccessModifier>static)[\s]*?(?P<cppReturnType>int|double|String|char|boolean|void)\s*(?P<cppFuncName>[a-zA-Z]*)[\s]*?\((?P<cppParameters>.*)\)[\s]*?{[\s]*(?P<cppScope>.+[\s\S]*?)}\n+(?P<after>[\s\S]*)", regex.group("after"))

main = None
i = 0
for obj in functionList:
    if functionList[i].funcName == "main":
        originScope = functionList[i].funcScope
        parser = functionParser()
        parser.parse(originScope.strip())         #MAY BE THE ISSUE
        #print(originScope)
    #else:
    #    print("NOT AT MAIN")
    i += 1

    
