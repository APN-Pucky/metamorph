import yaml
import requests


def dot_to_ascii(dot: str, fancy: bool = True):

    url = 'https://dot-to-ascii.ggerganov.com/dot-to-ascii.php'
    boxart = 0

    # use nice box drawing char instead of + , | , -
    if fancy:
        boxart = 1

    params = {
        'boxart': boxart,
        'src': dot,
    }

    response = requests.get(url, params=params).text

    if response == '':
        raise SyntaxError('DOT string is not formatted correctly')

    return response



# TODO add api key option
# TODO handle same languages follow case
class Config:
    def __init__(self,file:str=None, start = "en", goal = "en" , flow = None,):
        self.goal = goal
        self.start = start
        self.flow = flow
        if file is not None:
            self.load_file(file)

    def load_file(self,file:str):
        with open(file, 'r') as file:
            conf = yaml.safe_load(file)
            self.goal = conf['goal']
            self.start = conf['start']
            self.flow = conf['flow']

    def print_diagram(self):
        recursive_print_diagram({self.start : self.flow})
def recursive_print_diagram(sub,depth=0):
    if sub is not None:
        for k in sub.keys():
            if sub[k] is not None:
                s = ""
                s = s + k + " -> { rank = same;"
                for ss in sub[k]:
                    s = s + ss + " "
                s = s + "}"
                print(s)
        for k in sub.keys():
            if sub[k] is not None:
                recursive_print_diagram(sub[k])
c = Config('config.yml')
print(c.__dict__)
c.print_diagram()
