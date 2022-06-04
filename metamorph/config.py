from os import remove
import yaml
import requests
import pydot
import re



remove_lower = lambda text: re.sub('[a-z]', '', text)
# TODO add api key option
# TODO handle same languages follow case
class Config:
    def __init__(self,file:str=None, start = "en", goal = "en" ,translator="GoogleTranslator", flow = None,):
        self.glv =1
        self.goal = goal
        self.start = start
        self.flow = flow
        self.translator = translator
        if file is not None:
            self.load_file(file)

    def load_file(self,file:str):
        with open(file, 'r') as file:
            conf = yaml.safe_load(file)
            self.translator= conf['translator']
            self.goal = conf['goal']
            self.start = conf['start']
            self.flow = conf['flow']

    def print_diagram(self):
        return self.recursive_print_diagram({self.start : self.flow},self.start)
    def recursive_print_diagram(self,sub,kk,depth=1,lines=[],show_translator=False):
        tran = remove_lower(self.translator) if show_translator else ""
        s = ""
        if sub[kk] is not None:
            tlines = lines+[depth]
            s = (" ---" + tran +"--> " if depth !=1 else "") + kk
            for i,k in enumerate(sub[kk].keys()):
                if i == 0:
                    s = s + "" +""  
                else:
                    for i in range(2):
                        s = s + "\n"
                        for j in range(depth):
                            s = s + (" |" if j+1 in tlines else "  ")
                            if j < depth-1:
                                s = s + "        " + " "*len(tran)
                s = s + self.recursive_print_diagram(sub[kk],k,depth=depth+1,lines=tlines if i+1 != len(sub[kk].keys()) else lines)
            return s
        else:
            return " ---" + tran+ "--> " + kk + " ---" +tran + "--> " + self.goal
    
c = Config('config.yml')
s=c.print_diagram()
print(s)
