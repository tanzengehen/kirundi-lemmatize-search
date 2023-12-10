#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  3 22:31:05 2023

@author: doreen nixdorf

it's only auxilliary for the IDE,
Sebastian Lisken was working on the website interface'
"""

from sys import exit as sysexit
try:
    import kir_string_depot as sd
    import kir_helper2 as kh
    import kir_tag_search as ts
    import kir_db_classes as dbc
except ImportError:
    from ..lemmatize_search import kir_string_depot as sd
    from ..lemmatize_search import kir_helper2 as kh
    from ..lemmatize_search import kir_tag_search as ts
    from ..lemmatize_search import kir_db_classes as dbc


def input_fnin():
    """get the path to a raw Kirundi text or already tagged text
    allows txt and json
    """
    while True:
        fnin = input("  : ")
        if fnin[-4:] not in [".txt", ".csv"]:
            if fnin == "q":
                sysexit()
            if fnin in ["c", "C"]:
                # for debugging only
                fnin = "c"
                break
            # Translators: terminal only
            kh.OBSERVER.notify(kh._("txt or csv file or 'q' for 'quit'"))
            continue
        if not kh.check_file_exits(fnin):
            kh.OBSERVER.notify(kh._("""This file doesn't exist. {}
Try again""").format(fnin))
            continue
        break
    return fnin


def input_searchterm():
    """get a query string of search terms
    returns list of strings, allows (!)words, (!)tags, *
    """
    while True:
        searchterm = input("  : ")
        searchterm = searchterm.strip()
        searchterm = searchterm.strip("*")
        if searchterm == "":
            # Translators: terminal only
            kh.OBSERVER.notify(kh._("please give me a searchterm"))
            continue
        searchterm = searchterm.split()
        for i in searchterm:
            # check if '*' is inside of a word
            if len(i) > 1 and "*" in i:
                kh.OBSERVER.notify(kh._("""'*' only for words, not for letters.
Write searchterm again please"""))
                again = True
                break
            again = False
        if again is True:
            continue  # next input
        break
    return searchterm


def figure_out_query(which_words):
    """figure the searchterm out
    return list of tuples:
    (to exclude or not, word/tag/lemma/wildcard, searchword)"""
    quest = []
    show = ""
    for interest in which_words:
        whichtag = ""
        # discard this word/tag/lemma
        if interest[0] == "!":
            yesno = "n"
            interest = interest[1:]
            show += "all except "
        else:
            yesno = "y"
        # exact word
        if interest[0] == "/":
            interest = interest[1:]
            whichtag = "token"
            show += "(exact)" + interest + " + "
        # wildcard
        if interest == "*":
            whichtag = "?"
            show += "anything + "
        # pos-tag
        elif interest.upper() in sd.PossibleTags.pt:
            whichtag = "pos"
            show += interest + " + "
        # lemma
        elif whichtag == "":
            whichtag = "lemma"
            show += "(lemma)" + interest + " + "
        quest.append((yesno, whichtag, interest))
    kh.OBSERVER.notify(kh._(show[:-3]))
    return quest


if __name__ == "__main__":
    kh.OBSERVER = kh.PrintConsole()
    # kh.SINGLE = True
    db_rundi = dbc.get_resources()
    kh.OBSERVER.notify("""Ubu nyene ururimi rw'igikoresho ni kirundi.
Pfyonda ENTER canke andika 'de', 'en' canke 'fr' iyo urashaka ko turaganira mu
rundi rurimi.
    (Default UI-language is Rundi. Just press ENTER for OK or change it.
    Die UI-Sprache ist auf kirundi voreingestellt, du kannst aber auch wechseln.
    Au moment l'interface utilisateur est rundi, mais tu peux l'échanger.
deutsch, english, français)
'de', 'en', 'fr' ,'rn'""")
    while True:
        locale = input('  : ')
        lang = kh.set_ui_language(locale)
        if lang == "not":
            continue
        break
    lang.install()
    kh._ = lang.gettext
    kh.OBSERVER.notify(kh._("\nSelect the Rundi text you want to inspect."))
    # Translators: terminal only
    # kh.OBSERVER.notify(kh._("\tc\t\t\t\t= whole tagged corpus"))
    # Translators: terminal only
    kh.OBSERVER.notify(kh._("Prefer the tagged file, if there is one already."))
    # kh.OBSERVER.notify(kh._("path/to/file\t\t= a single file (txt or csv)"))
    kh.OBSERVER.notify(kh._("path/to/file (txt or csv)"))
    # corpus or file, if file: ist it txt?
    f_in = input_fnin()

    if f_in == "c":
        # f_in = sd.ResourceNames.root+"resources/meta_bbc.txt"
        f_in = sd.ResourceNames.dir_tagged+"bbc/tag__bbcall.json"
        if f_in[-12:] == "meta_bbc.txt":
            ts.tag_multogether(f_in, db_rundi)
            sysexit()
    else:
        tagged = ts.tag_or_load_tags(f_in, db_rundi)
    # Translators: terminal only
    kh.OBSERVER.notify(kh._("""\nWhat are you looking for?
    Divide searchterms with space characters.
    You can put a '!' before a !word or !tag, if you want to exclude it.
    You can place a separate '*' to set one token as wildcard.
    You can place a '/' before a /word, if you want to find exact this word,
    else the word will be taken as a lemma and all wordforms will be found.

    You can use these tags:
        [ADJ, ADV, CONJ, EMAIL, F(foreign word), INTJ, NI, NOUN,
        NUM, NUM_ROM (roman number), PRON (pronouns), PROPN,
        PROPN_CUR, PROPN_LOC (geographical place),
        PROPN_NAM (personal name), PROPN_ORG,
        PROPN_PER (group of persons), PROPN_REL, PROPN_SCI,
        PROPN_THG, PROPN_VEG, PRP (prepositions), SYMBOL,
        UNK (unkwon to dictionary), VERB, WWW (webaddress)]
Now enter our searchterm"""))
    query = input_searchterm()
#     kh.OBSERVER.notify(
#         kh._("\tOK, you are looking for a {}-gram.\n").format((len(query))))
#     # Translators: terminal only
#     kh.OBSERVER.notify(kh._("""For distinction between type, tag and lemma
# chose for each part of the searchterm a letter..."""))
#     # Translators: terminal only
#     kh.OBSERVER.notify(kh._("""\t\tW = this type
# \t\tL = all types of this lemma
# \t\tT = Part of Speech-tag
# \t\t? = wildcard"""))
#     wtl = input_wtl(len(query))
#     nots, quterms = check_search_wtl(wtl, query)

    kh.OBSERVER.notify(kh._(
        "\tOK, you are looking for a {}-gram.\n").format((len(query))))
    search = figure_out_query(query)
    # ts.search_or_load_search(f_in, wtl, nots, quterms, kh.SINGLE, tagged.tokens)
    ts.search_or_load_search(f_in, search, kh.SINGLE, tagged.tokens)
