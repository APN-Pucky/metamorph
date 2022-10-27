import deep_translator
from deep_translator import *
from metamorph.config import is_end, no_extra
import sys


def generate_alternatives(text,conf):
    """
    Generate alternatives for ``text`` using Config ``conf``.

    :param text: Text to generate alternatives for.
    :param conf: Config to use.
    :return: List of alternatives.

    Example::
	>>> from metamorph.config import Config
        >>> "Hello World!" in generate_alternatives("Hallo world!",Config(flow={"de":None,"fr":None,"es":None}))
	True
        >>> "Hallo Welt!" in generate_alternatives("Hello world!",Config(start="de",goal="de",flow={"en":None,"fr":None,"es":None}))
	True
        >>> "Hello World!" in generate_alternatives("Hallo world!",Config("configs/default_config.yaml"))
	True
    """
    s =[]
    for k in no_extra(conf.flow):
	# We set the extra of the start node to the text we want to translate.
        conf.flow[k]["extra"]["result"] = text
        s = s + recursive_translate(conf,conf.flow,k)
    return s


def recursive_translate(conf,sub,kk):
    """
    Recursively translate ``sub`` using Config ``conf``.
    """
    ret = []
    # We recurse over everything except the end nodes.
    if not is_end(sub[kk]):
        text = sub[kk]["extra"]["result"]
        source = sub[kk]["extra"]["language"]
	# Iterate elements of subnodes
        for _,k in enumerate(no_extra(sub[kk])):
            target = sub[kk][k]["extra"]["language"]
        # get translator
            translator = sub[kk][k]["extra"]["translator"]
	    # infer deep_translator from string
            try:
                t = getattr(sys.modules[__name__], translator)
            except AttributeError:
                print("Translator " + translator + " not found. Did you mean " + translator + "Translator?")
                sys.exit(1)
	    # save the translated text in the extra field of the node
            sub[kk][k]["extra"]["result"] = translate(t,source ,target,text,api_key=conf.get_api_key(translator),proxies = conf.proxies)
	    # append result to the list of results from end nodes
            ret = ret + recursive_translate(conf,sub[kk],k)
        return ret
    else:
	# Return the result of the end node.
        return [sub[kk]["extra"]["result"]]

def translate(translator,source,target,text,api_key=None,proxies=None,quiet=False,verbose=True):
    """
    Translate ``text`` from ``source`` language to ``target`` language using translator ``translator``.
    :param translator: Translator to use (from :mod:`deep_translator`).

    :param source: Source language.
    :param target: Target language.
    :param text: Text to translate.
    :param quiet: If ``True``, don't print anything.
    :param verbose: If ``True``, print error messages.

    :return: Translated text.

    Example::
        >>> translate(GoogleTranslator, "en", "de", "Hello world!")
	'Hallo Welt!'
    """
    try:
        return translator(source=source,target=target,api_key=api_key,proxies=proxies).translate(text)
    except deep_translator.exceptions.LanguageNotSupportedException as e:
        if not quiet:
            print(e)
    except Exception as e:
        if verbose:
            print(e)
    return ""

