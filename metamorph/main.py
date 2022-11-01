#!/usr/bin/python3
import argparse
import sys
# readline might not be available on all platforms
try:
    import readline
except ImportError:
    pass
# colorama might not be available on all platforms
try:
    import colorama
    from metamorph.util import get_edits_string
except ImportError:
    get_edits_string = lambda old, new: new

import metamorph
from metamorph.config import Config
from metamorph.handler import generate_alternatives




def __main__():
    """
    Main function.
    """
    parser = argparse.ArgumentParser(description='Metamorph-' + str(metamorph.version) + ' text by passing through several translators.')
    parser.add_argument("-gs","--goal-start",type=str, help="initial and final language", default="en")
    parser.add_argument("-g","--goal",type=str, help="final language", default=None)
    parser.add_argument("-s","--start",type=str, help="initial language", default=None)
    parser.add_argument("-t","--translator", type=str,help="default translator (from deep_translator: GoogleTranslator, PonsTranslator, LingueeTranslator, MyMemoryTranslator, DeeplTranslator, ... )",default="GoogleTranslator")
    parser.add_argument("-l","--languages",type=str,nargs='+', help="list of intermediate languages (for more variation choose inherently different languages).", default=["de","fr","es"])

    parser.add_argument("-i","--interactive",action='store_true',help="Enable interactive mode. Will prompt for input.",default=True)
    parser.add_argument("-ni","--non-interactive",action='store_false',help="Parse stdin, without input prompts.",dest="interactive")
    parser.add_argument("-a","--all-in-one",action='store_true', help="Instead of parsing input line by line, parse all text at once",default=False)

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
        
    if args.interactive and (args.show_diagrams or args.show_diagram_init):
        print("Loaded translation diagram:")
        print(conf.str_diagram(nodes="language" ,arrows="translator_short"))

    if args.interactive:
        try:
            while True:
                print("Text:")
                to_translate = input()
                s = generate_alternatives(to_translate, conf)
                for tmp_text in s:
                    if args.colour:
                        print(get_edits_string(to_translate,tmp_text))
                    else:
                        print(tmp_text)
                print()
                if args.show_diagrams or args.show_diagram_result:
                    print("Diagram:")
                    print(conf.str_diagram(nodes="result",arrows="language"))
        except KeyboardInterrupt:
            sys.exit(0)
    else:
        lines = sys.stdin.readlines()
        if args.all_in_one:
            lines = ["".join(lines)]
        results = None
        for line in lines:
            s = generate_alternatives(line, conf)
            if results is None:
                results = [""]*len(s)
            for i,tmp_text in enumerate(s):
                results[i] = results[i] + tmp_text + "\n"
        for tmp_text in results:
            print(tmp_text)


if __name__ == "__main__":
    __main__()
