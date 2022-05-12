from deep_translator import * 
source_lang='en'
target_lang='en'
while True:
    print("Text: ",end="")
    to_translate = input()
    print()
    for lang in ["de","fr","es"]:
        for t in [  GoogleTranslator,
                    #PonsTranslator,
                    #LingueeTranslator,
                    MyMemoryTranslator,
                    #DeeplTranslator,
        ]:
            print(t(source=lang, target=target_lang).translate(t(source=source_lang, target=lang).translate(to_translate)))
