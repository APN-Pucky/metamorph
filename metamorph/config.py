from os import remove
import yaml
import requests
import pydot
import re



def is_end(dic):
    b = dic is None or (len(dic.keys()) == 1 and 'extra' in dic.keys())
    return b
def no_extra(dic):
    r = []
    for k in dic.keys():
        if k != "extra":
            r = r + [k]
    return r

remove_lower = lambda text: re.sub('[a-z]', '', text)
# TODO add api key option
# TODO handle same languages follow case
class Config:
    def __init__(self,file:str=None, start = None, goal = None ,translator="GoogleTranslator", flow = None,):
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
            self.flow = conf['flow']
            if 'goal' in conf:
                self.goal = conf['goal']
            if 'start' in conf:
                self.start = conf['start']
                self.flow = {self.start : self.flow}
            self.fill_missing(self.flow)
            print(self.flow)
    def default_extra(self,direct,k):
        if "extra" not in direct[k]:
            direct[k]["extra"] = {}
        if "translator" not in direct[k]["extra"]:
            direct[k]["extra"]["translator"] = self.translator
        if "translator_short" not in direct[k]["extra"]:
            direct[k]["extra"]["translator_short"] = remove_lower(self.translator)
 
        if "language" not in direct[k]["extra"]:
            direct[k]["extra"]["language"] =  k
 

    def fill_missing(self,direct):
        for k in no_extra(direct):
            print(direct[k])
            if is_end(direct[k]):
                if self.goal is not None:
                    direct[k] = {self.goal:{"extra":{"translator":self.translator, "language" : k}}}
                else:
                    if direct[k] is None:
                        direct[k] = {}
                    self.default_extra(direct,k)
                continue
            self.default_extra(direct,k)
            self.fill_missing(direct[k])


    def print_diagram(self):
        s = ""
        for k in no_extra(self.flow):
            s = s + self.recursive_print_diagram(self.flow,k) + "\n\n"
        return s

    def recursive_print_diagram(self,sub,kk,depth=1,lines=[],show_arrows=True,nodes="language",arrows="translator_short"):
        tran = sub[kk]["extra"][arrows] if show_arrows else ""
        s = ""
        if not is_end(sub[kk]):
            tlines = lines+[depth]
            s = (" ---" + tran +"--> " if depth !=1 else "") + sub[kk]["extra"][nodes]
            for i,k in enumerate(no_extra(sub[kk])):
                if i == 0:
                    s = s + "" +""  
                else:
                    for i in range(2):
                        s = s + "\n"
                        for j in range(depth):
                            s = s + (" |" if j+1 in tlines else "  ")
                            if j < depth-1:
                                s = s + "        " + " "*len(tran)
                s = s + self.recursive_print_diagram(sub[kk],k,depth=depth+1,lines=tlines if i+1 != len(no_extra(sub[kk])) else lines)
            return s
        else:
                return " ---" + tran+ "--> " + sub[kk]["extra"][nodes]
    
c = Config('config.yml')
s=c.print_diagram()
print(s)
