import json
import yaml
import re

def is_end(dic):
    """
    Returns True if dictionary is an end node.
    """
    b = dic is None or (len(dic.keys()) == 1 and 'extra' in dic.keys())
    return b

def no_extra(dic):
    """
    Returns keys of dictionary that are not 'extra'.
    """
    r = []
    for k in dic.keys():
        if k != "extra":
            r = r + [k]
    return r

def remove_lower(text:str):
    """
    Remove lowercase letters from ``text``.

    :param text: Text to remove lowercase letters from.
    :return: Text without lowercase letters.

    Example::
        >>> remove_lower("GoogleTranslate")
        'GT'
        >>> remove_lower({"GoogleTranslate":"XXX"})
        {'GT': 'XXX'}
    """
    if type(text) is dict:
        r = {}
        for k,v in text.items():
            r[remove_lower(k)] = v
        return r
    return re.sub('[a-z]', '', text)

class Config:
    """
    Defines the language flow to generate alternative texts.
    """
    def __init__(self,file:str = None, start = "en", goal = "en",translator = "GoogleTranslator",proxies = None, api_keys=None, flow = None,):
        if goal is not None:
            self.goal = goal
        if start is not None:
            self.start = start
        if flow is not None:
            self.flow = flow
        if translator is not None:
            self.translator = translator
        if api_keys is not None:
            self.api_keys = api_keys
        else:
            self.api_keys = {}
        self.proxies = proxies
        if file is not None:
            self.load_file(file)

        self.flow = {self.start : self.flow}
        self.fill_missing(self.flow)
        #print(json.dumps(self.flow,indent=4))

    def get_api_key(self,translator):
        """
        Returns the api key for ``translator``.
        """
        if translator in self.api_keys:
            return self.api_keys[translator]
        #print("No api key for translator " + translator + " found.")
        return None

    def load_file(self,file:str):
        """
        Loads a configuration file.
        """
        with open(file, 'r') as file:
            conf = yaml.safe_load(file)
            self.translator= conf['translator']
            if 'api_keys' in conf:
                self.api_keys = conf['api_keys']
            if 'proxies' in conf:
                self.proxies = conf['proxies']
            self.flow = conf['flow']
            if 'goal' in conf:
                self.goal = conf['goal']
            if 'start' in conf:
                self.start = conf['start']

    def default_extra(self,direct,k):
        """
        Adds default keys to dictionary at ``direct[k]``.
        """
        if "extra" not in direct[k]:
            direct[k]["extra"] = {}
        if "translator" not in direct[k]["extra"]:
            #print("overwritte",k,direct[k],direct[k]["extra"] )
            direct[k]["extra"]["translator"] = self.translator
        if "translator_short" not in direct[k]["extra"]:
            direct[k]["extra"]["translator_short"] = remove_lower(direct[k]["extra"]["translator"])
        if "language" not in direct[k]["extra"]:
            direct[k]["extra"]["language"] =  k
        if "result" not in direct[k]["extra"]:
            direct[k]["extra"]["result"] =  ""
 

    def fill_missing(self,direct):
        """
        Sets default extras for missing elements in dictionary.
        """
        for k in no_extra(direct):
            if is_end(direct[k]):
                if self.goal is not None:
                    if direct[k] is None:
                        direct[k] = {}
                    direct[k][self.goal] = {}
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
        """
        Prints a diagram of the language flow.
        """
        s = ""
        for k in no_extra(self.flow):
            s = s + self._recursive_str_diagram(self.flow,k,nodes=nodes,arrows=arrows) + "\n\n"
        return s

    def _recursive_get_str_max_length(self,sub,key):
        ret = len(sub["extra"][key])
        for k in no_extra(sub):
            m = self._recursive_get_str_max_length(sub[k],key)
            if m > ret:
                ret =m
        return ret


    def _recursive_str_diagram(self,sub,kk,depth=1,lines=None,nodes="language",arrows=None,len_nodes=None,len_arrows=None):
        if lines is None:
            lines = []
        if len_arrows is None:
            len_arrows =0
            if  arrows is not None:
                len_arrows = self._recursive_get_str_max_length(sub[kk],arrows)
            else:
                len_arrows = 0
        if len_nodes is None:
            len_nodes = self._recursive_get_str_max_length(sub[kk],nodes)
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
                    s = s + "|"
                else:
                    for _ in range(2):
                        s = s + "\n"
                        for j in range(depth):
                            s = s + (" "*(len_nodes) + "|" if j+1 in tlines else " "*(len_nodes+1))
                            if j < depth-1:
                                s = s + " "*(len_arrows+7)
                s = s + self._recursive_str_diagram(sub[kk],k,depth=depth+1,nodes=nodes,arrows=arrows,
                    len_nodes=len_nodes,len_arrows=len_arrows,lines=tlines if i+1 != len(no_extra(sub[kk])) else lines)
            return s
        else:
                return "---" + tran+ "--> " + node
