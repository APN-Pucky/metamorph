import re
import sys

# colorama might not be available on all platforms
try:
    import colorama

    from metamorph.util import get_edits_string
except ImportError:
    get_edits_string = lambda old, new: new

from smpl_io import io as sio

from metamorph.config import Config
from metamorph.handler import generate_alternatives

try:
    import readline

    __readline = True
except ImportError:
    __readline = False


def rlinput(prompt, prefill=""):
    # check if readline is available
    if __readline:
        readline.set_startup_hook(lambda: readline.insert_text(prefill))
    try:
        return input(prompt)  # or raw_input in Python 2
    finally:
        if __readline:
            readline.set_startup_hook()


def input_loop(args, conf: Config):
    try:
        while True:
            print("Text:")
            to_translate = input()
            s = generate_alternatives(to_translate, conf)
            for tmp_text in s:
                if args.colour:
                    print(
                        get_edits_string(
                            to_translate,
                            tmp_text,
                            conf.color,
                            conf.on_color if args.background_colour else None,
                        )
                    )
                else:
                    print(tmp_text)
            print()
            if args.show_diagrams or args.show_diagram_result:
                print("Diagram:")
                print(conf.str_diagram(nodes="result", arrows="language"))
    except KeyboardInterrupt:
        sys.exit(0)
    except EOFError:
        sys.exit(0)


def merge(args, conf: Config):
    lines = sio.read(args.input).split("\n")
    rets = [""] * len(lines)
    l = 0
    while l < len(lines):
        to_translate = lines[l]
        print(f"[0]: {to_translate}")
        s = generate_alternatives(to_translate, conf)
        for i, tmp_text in enumerate(s):
            out_text = ""
            if args.colour:
                out_text = get_edits_string(
                    to_translate,
                    tmp_text,
                    conf.color,
                    conf.on_color if args.background_colour else None,
                )
            else:
                out_text = f"[{i+1}]: {tmp_text}"
            print(f"[{i+1}]: {out_text}")
        trans = [to_translate] + s
        # let the user choose the translation
        regex = f"(({'|'.join(str(k) for k in range(len(trans)))})e?|b|f)"
        matched = None
        response = ""
        while not matched:
            response = input(f"Pick, [e]dit, [b]ack, [f]orward; /{regex}/: ")
            # check if response matches the regex
            matched = re.match(regex, response)
        if "b" in response:
            l = max(l - 1, 0)
            continue
        elif "f" in response:
            l = min(l + 1, len(lines) - 1)
            continue
        elif "e" in response:
            j = int(response.replace("e", ""))
            rets[l] = rlinput("", trans[j])
            l += 1
        else:
            j = int(response)
            rets[l] = trans[j]
            l += 1
    sio.write(args.output, "\n".join(rets))
