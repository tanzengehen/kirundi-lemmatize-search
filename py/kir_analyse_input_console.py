#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  3 22:31:05 2023

@author: doreen nixdorf

it's only auxilliary for the IDE,
Sebastian Lisken is working on the website interface'
"""

from sys import exit as sysexit
import kir_string_depot as sd
import kir_helper2 as kh
import kir_tag_search as ts
import kir_db_classes as dbc
# # nur vorübergehend
# import gettext


def input_fnin():
    """get the path to a raw Kirundi text or already tagged text
    allows txt and json
    """
    while True:
        fnin = input("  : ")
        if fnin[-4:] != ".txt" and fnin[-5:] != ".json":
            if fnin == "q":
                sysexit()
            if fnin in ["c", "C"]:
                # for debugging only
                fnin = "c"
                break
            # Translators: terminal only
            kh.OBSERVER.notify(kh._("txt or json file or 'q' for 'quit'"))
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


def input_wtl(lengths):
    """specify if a word in the searchstring should be seen as
    word, tag or lemma
    """
    while True:
        short = input("  : ")
        short = short.replace(" ", "").lower()
        if not short:
            # Translators: terminal only
            kh.OBSERVER.notify(
                kh._("""please enter the 'wtl' combination for your
searchterms or 'q' for 'quit'"""))
            continue
        if short == 'q':
            sysexit()
        for i in short:
            if i not in "wlt?":
                # Translators: terminal only
                kh.OBSERVER.notify(
                    kh._("\tonly 'w', '!w', 't', '!t', 'l', '!l' or '?'"))
                again = True
                break
            again = False
        if again is True:
            continue
        if len(short) != lengths:
            # Translatorse: terminal only
            kh.OBSERVER.notify(
                kh._("Hm, not as many as searchterms... Please again."))
            continue
        break
    kind_of_search = {"w": "token", "t": "pos", "l": "lemma", "?": "?"}
    tags = [kind_of_search.get(i) for i in short]
    return tags


def check_search_wtl(whichtags, whichwords):
    """check if searchterm and wtl match in length and possibilities
    """
    possible = sd.PossibleTags
    search = []
    notss = []
    show = ""
    for i, interest in enumerate(whichtags):
        # wildcard
        if interest == "?":
            notss.append("y")
            search.append("?")
            # Translators: terminal only
            show += kh._("all + ")
            if whichwords[i] != '*':
                # it should be * but we don't ask again, only warn
                # Translators: terminal only
                kh.OBSERVER.notify(kh._("mismatch: wildcard {}.").format(i+1))
                # Translators: terminal only
                yesno = input(kh._("I go with the wildcard. Y/N : "))
                # Translators: terminal only
                if yesno not in kh._("yY"):
                    # Translators: terminal only
                    kh.OBSERVER.notify(kh._("Start again"))
                    sysexit()
        # not wildcard
        else:
            # not this word, tag or lemma
            if whichwords[i][0] == "!":
                notss.append("!")
                show += kh._("all except ")
                whichwords[i] = whichwords[i].strip("!")
            else:
                notss.append("y")
            # tag
            if interest == "pos":
                # PoS tags always in uppercase
                whichwords[i] = whichwords[i].upper()
                if whichwords[i] in possible.pt:
                    search.append(whichwords[i])
                    show += whichwords[i]+" + "
                else:
                    # Translators: terminal only
                    kh.OBSERVER.notify(
                        kh._("Invalid tag: {}. There will be no result.")
                        .format(whichwords[i]))
                    sysexit()
            # word or lemma
            else:
                search.append(whichwords[i])
                # lemma
                if interest == "lemma":
                    show += whichwords[i]+"(lemma) + "
                # word
                else:
                    show += whichwords[i]+" + "
    kh.OBSERVER.notify("\n"+kh._("Query = {}\n").format(show[:-3]))
    return notss, search


def get_resources():
    """load Named Entities and db_kirundi
    """
    # read db
    database_rundi = dbc.AllRundiRows(sd.ResourceNames.fn_db)
    # map db
    db_rundi = dbc.load_db_kirundi(database_rundi.rows)
    # read named entities
    database_names = dbc.AllNeRows(sd.ResourceNames.fn_named_entities)
    # map named entities
    db_names = dbc.load_ne(database_names.rows)
    db_rundi.update({"names": dbc.complete_location_language_person(db_names)})
    return db_rundi


if __name__ == "__main__":
    kh.OBSERVER = kh.PrintConsole()
    # kh.SINGLE = True
    db_rundi = get_resources()
    kh.OBSERVER.notify("""Ubu nyene ururimi rw'igikoresho ni kirundi.
Pfyonda ENTER canke andika 'de', 'en' canke 'fr' iyo urashaka ko turaganira mu
rundi rurimi.
    (Default UI-language is Rundi. Just press ENTER for OK or change it.
    Die UI-Sprache ist auf kirundi voreingestellt, du kannst aber auch wechseln.
    Au moment l'interface utilisateur est rundi, mais tu peux l'échanger.
deutsch, english, français)
'de', 'en', 'fr' ,'rn'""")
    while True:
        locale = input("  : ")
        lang = kh.set_ui_language(locale)
        if lang == "not":
            continue
        break
    lang.install()
    kh._ = lang.gettext
    kh.OBSERVER.notify(kh._("\nSelect the Rundi text you want to inspect:"))
    # Translators: terminal only
    kh.OBSERVER.notify(kh._("\tc\t\t\t\t= whole tagged corpus"))
    # Translators: terminal only
    kh.OBSERVER.notify(kh._("\tpath/to/file\t\t= a single file (txt or json)"))
    kh.OBSERVER.notify(kh._("Prefer the tagged file, if there is one already.\n"))
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
    You can place a separate '*' for a wildcard.

    Possible PoS-tags:
        [ADJ, ADV, CONJ, EMAIL, F(foreign word), INTJ, NI, NOUN,
        NUM, NUM_ROM (roman number), PRON (pronouns), PROPN,
        PROPN_CUR, PROPN_LOC (geographical place),
        PROPN_NAM (personal name), PROPN_ORG,
        PROPN_PER (group of persons), PROPN_REL, PROPN_SCI,
        PROPN_THG, PROPN_VEG, PRP (prepositions), SYMBOL,
        UNK (unkwon to dictionary), VERB, WWW (webaddress)]
Your searchterm"""))
    query = input_searchterm()
    kh.OBSERVER.notify(
        kh._("\tOK, you are looking for a {}-gram.\n").format((len(query))))
    # Translators: terminal only
    kh.OBSERVER.notify(kh._("""For distinction between type, tag and lemma
chose for each part of the searchterm a letter..."""))
    # Translators: terminal only
    kh.OBSERVER.notify(kh._("""\t\tW = this type
\t\tL = all types of this lemma
\t\tT = Part of Speech-tag
\t\t? = wildcard"""))
    wtl = input_wtl(len(query))
    nots, quterms = check_search_wtl(wtl, query)

    ts.search_or_load_search(f_in, wtl, nots, quterms, kh.SINGLE, tagged.tokens)
