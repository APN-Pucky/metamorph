#!/usr/bin/python3
import deep_translator
from deep_translator import * 
from termcolor import colored
import difflib
import colorama
import argparse
import sys
import pkg_resources as pkg

from metamorph.config import Config, is_end, no_extra

package = "metamorph"

try:
    version = pkg.require(package)[0].version
except pkg.DistributionNotFound:
    version = "dirty"


def get_edits_string(old, new):
    result = ""
    codes = difflib.SequenceMatcher(a=old, b=new).get_opcodes()
    for code in codes:
        if code[0] == "equal": 
            result += old[code[1]:code[2]]
            #result += white(old[code[1]:code[2]])
        #elif code[0] == "delete":
            #result += red(old[code[1]:code[2]])
        elif code[0] == "insert":
            result += colored(new[code[3]:code[4]],'green')
        elif code[0] == "replace":
            #result += red(old[code[1]:code[2]]) 
            result += colored(new[code[3]:code[4]],'green')
    return result

def __main__():
    parser = argparse.ArgumentParser(description='Metamorph-' + str(version) + ' text by passing through several translators.')
    parser.add_argument("-gs","--goal-start",type=str, help="initial and final language", default="en")
    parser.add_argument("-g","--goal",type=str, help="final language", default=None)
    parser.add_argument("-s","--start",type=str, help="initial language", default=None)
    parser.add_argument("-t","--translator", type=str,help="default translator (from deep_translator: GoogleTranslator, PonsTranslator, LingueeTranslator, MyMemoryTranslator, DeeplTranslator, ... )",default="GoogleTranslator")
    parser.add_argument("-l","--languages",type=str,nargs='+', help="list of intermediate languages (for more variation choose inherently different languages).", default=["de","fr","es"])

    parser.add_argument("-c","--config", type=str,help="load config from a file",default=None)
    parser.add_argument("-v","--verbose", type=bool,help="print error messages instead of skipping them",default=False)
    parser.add_argument("-q","--quiet", type=bool,help="suppress error messages",default=False)

    parser.add_argument("--colour",action='store_true' ,help="show coloured differences",default=True)
    parser.add_argument("-nc","--no-colour",dest='colour',action='store_false' ,help="don't show coloured differences")
    parser.add_argument("-sd", "--show-diagrams", action='store_true', help="print all diagrams",default=False )
    parser.add_argument("-sdi", "--show-diagram-init", action='store_false', help="print the diagram translation flow",default=True)
    parser.add_argument("-hdi", "--hide-diagram-init", dest='show_diagram_init',action='store_false', help="don't print the diagram translation flow")
    parser.add_argument("-sdr", "--show-diagram-result", action='store_true', help="print the diagram including intermediate translations",default=False )

    args = parser.parse_args()
    if args.colour:
        colorama.init()
    goal = args.goal_start
    start = args.goal_start 
    if args.goal is not None:
        goal = args.goal
    if args.start is not None:
        start= args.start

    conf = None
    if args.config is not None:
        conf = Config(args.config, goal=goal,start= start,translator=args.translator)
    else:
        conf = Config(flow={l:None for l in args.languages }, goal=goal,start= start,translator=args.translator)
        
    if args.show_diagrams or args.show_diagram_init:
        print("Loaded translation diagram:")
        print(conf.str_diagram(nodes="language" ,arrows="translator_short"))
    
    while True:
        print("Text:")
        to_translate = input()
        s =[]
        for k in no_extra(conf.flow):
            conf.flow[k]["extra"]["result"] = to_translate
            s = s + recursive_translate(conf,conf.flow,k)
        for tmp_text in s:
            if args.colour:
                print(get_edits_string(to_translate,tmp_text))
            else:
                print(tmp_text)
        print()
        if args.show_diagrams or args.show_diagram_result:
            print("Diagram:")
            print(conf.str_diagram(nodes="result",arrows="language"))

def translate(trans,source,target,text,quiet=False,verbose=True):
    try:
        return trans(source=source,target=target).translate(text)
    except deep_translator.exceptions.LanguageNotSupportedException as e:
        if not quiet:
            print(e)
    except Exception as e:
        if verbose:
            print(e)
        pass
    return ""

def recursive_translate(conf,sub,kk):
    ret = []
    if not is_end(sub[kk]):
        text = sub[kk]["extra"]["result"]
        source = sub[kk]["extra"]["language"]
        for i,k in enumerate(no_extra(sub[kk])):
            target = sub[kk][k]["extra"]["language"]
            t = getattr(sys.modules[__name__], sub[kk][k]["extra"]["translator"])
            sub[kk][k]["extra"]["result"] = translate(t,source ,target,text)
            ret = ret + recursive_translate(conf,sub[kk],k)
        return ret
    else:
        return [sub[kk]["extra"]["result"]]


__main__()


