from os import remove
import yaml
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

class Config:
    def __init__(self,file:str=None, start = None, goal = None ,translator=None, flow = None,):
        if file is not None:
            self.load_file(file)
        if goal is not None:
            self.goal = goal
        if start is not None:
            self.start = start
        if flow is not None:
            self.flow = flow
        if translator is not None:
            self.translator = translator

        self.flow = {self.start : self.flow}
        self.fill_missing(self.flow)

    def load_file(self,file:str):
        with open(file, 'r') as file:
            conf = yaml.safe_load(file)
            self.translator= conf['translator']
            self.flow = conf['flow']
            if 'goal' in conf:
                self.goal = conf['goal']
            if 'start' in conf:
                self.start = conf['start']
    def default_extra(self,direct,k):
        if "extra" not in direct[k]:
            direct[k]["extra"] = {}
        if "translator" not in direct[k]["extra"]:
            direct[k]["extra"]["translator"] = self.translator
        if "translator_short" not in direct[k]["extra"]:
            direct[k]["extra"]["translator_short"] = remove_lower(self.translator)
 
        if "language" not in direct[k]["extra"]:
            direct[k]["extra"]["language"] =  k
        if "result" not in direct[k]["extra"]:
            direct[k]["extra"]["result"] =  ""
 

    def fill_missing(self,direct):
        for k in no_extra(direct):
            if is_end(direct[k]):
                if self.goal is not None:
                    direct[k] = {self.goal:{}}
                    self.default_extra(direct,k)
                    self.default_extra(direct[k],self.goal)
                else:
                    if direct[k] is None:
                        direct[k] = {}
                    self.default_extra(direct,k)
                continue
            self.default_extra(direct,k)
            self.fill_missing(direct[k])


    def str_diagram(self,nodes="language",arrows=None):
        s = ""
        for k in no_extra(self.flow):
            s = s + self.recursive_str_diagram(self.flow,k,nodes=nodes,arrows=arrows) + "\n\n"
        return s

    def recursive_get_str_max_length(self,sub,key):
        ret = len(sub["extra"][key])
        for k in no_extra(sub):
            m = self.recursive_get_str_max_length(sub[k],key)
            if m > ret:
                ret =m
        return ret


    def recursive_str_diagram(self,sub,kk,depth=1,lines=[],nodes="language",arrows=None,len_nodes=None,len_arrows=None):
        if len_arrows is None:
            len_arrows =0
            if  arrows is not None:
                len_arrows = self.recursive_get_str_max_length(sub[kk],arrows)
            else:
                len_arrows = 0
        if len_nodes is None:
            len_nodes = self.recursive_get_str_max_length(sub[kk],nodes)
            len_nodes = len_nodes +1
        tran = sub[kk]["extra"][arrows] if arrows is not None else ""
        tran = tran + "-"*(len_arrows-len(tran)-7)
        node = sub[kk]["extra"][nodes]
        node = node + " "*(len_nodes -len(node))
        s = ""
        if not is_end(sub[kk]):
            tlines = lines+[depth]
            s = ("---" + tran +"--> " if depth !=1 else "") + node
            for i,k in enumerate(no_extra(sub[kk])):
                if i == 0:
                    s = s + "|" +""  
                else:
                    for l in range(2):
                        s = s + "\n"
                        for j in range(depth):
                            s = s + (" "*(len_nodes) + "|" if j+1 in tlines else " "*(len_nodes+1))
                            if j < depth-1:
                                s = s + " "*(len_arrows+7)
                s = s + self.recursive_str_diagram(sub[kk],k,depth=depth+1,nodes=nodes,arrows=arrows,len_nodes=len_nodes,len_arrows=len_arrows,lines=tlines if i+1 != len(no_extra(sub[kk])) else lines)
            return s
        else:
                return "---" + tran+ "--> " + node 