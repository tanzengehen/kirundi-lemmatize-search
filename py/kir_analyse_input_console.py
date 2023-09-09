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
from kir_tag_search import search_or_load_search


def check_fnin(fn_in):
    """checks filename of txt ending"""
    if fn_in == "":
        kh.observer.notify("Kubera ko ataco watoye nahejeje.")
        sysexit()
    if fn_in in "cC":
        return "c"
    if fn_in[-4:] not in [".txt", ".json"]:
        kh.observer.notify(f"Hariho ikosa n'ifishi: ' {f_in}"
                           "'\nNdashobora gukoresha ifishi ifise impera "
                           "'.txt' canke '.json' gusa")
        sysexit()
    return "f"


def check_interest(interest0):
    """checks kind of search: word, tag, lemma or joker
    returns list with indices for tag-parts:
    [1,1,2] for tag, tag, lemma"""
    interest = interest0.replace(" ", "").lower()
    interest_nojoker = interest0.replace("?", "")
    if interest == "":
        # nothing picked
        kh.observer.notify("Kubera ko ataco watoye nahejeje.")
        sysexit()
    elif interest_nojoker == "":
        # '?' on all positions
        kh.observer.notify("nonosora ukurondera kwawe")  # specify your search
        sysexit()
    elif len(interest_nojoker) == 1:
        # only one is no '?'
        interest = interest_nojoker
    for i in interest:
        if i not in "wlt?":
            # wrong character picked
            kh.observer.notify("hari ikosa: no valid search criteria:"
                               "gusa 'w', 't' , 'l' canke '?'")
            sysexit()
    kind_of_search = {"w": "token", "t": "pos", "l": "lemma", "?": "?"}
    interest1 = [kind_of_search.get(i) for i in interest]
    return interest1


def specify_search(interest0):
    """takes exact searchword, searchtag or searchlemma"""
    kind_of_search = {"token": "Ijambo ririhe? (Which word?) : ",
                      "pos": "Amajambo yose afise indanzi (all words with tag) : ",
                      "lemma": "Amajambo yose y'itsitso ririhe? (all words of lemma) : "}
    search = []
    notss = []
    give = ""
    kh.observer.notify(f"Urashaka gutora {len(interest0)}-gram "
                       f"(You are looking for a {len(interest0)}-gram)")
    if len(interest0) > 1:
        kh.observer.notify("\n    now specify each part \n(you can put a '!' "
                           "before it, if you want to exclude this word or tag)")
        # for printing confirmation later
        count = "    igice "
    else:
        count = "    "
    for i, interest in enumerate(interest0):
        if interest == "?":
            kh.observer.notify(f"{i+1} : kira jambo rirakunda")
            search.append("?")
        else:
            take = input(count+str(i+1)+": " + kind_of_search.get(interest))
            if take[0] == "!":
                notss.append("!")
                give += "alles außer "
                take = take.strip("!")
            else:
                notss.append("y")
            possible = sd.PossibleTags
            if interest == "pos":
                # PoS tags always in uppercase
                take = take.upper()
                if take in possible.pt:
                    search.append(take)
                    give += take+" + "
                else:
                    kh.observer.notify(f"indanzi {take} ntiriho")  # =no tag
                    sysexit()
            # word, lemma
            elif take != "":
                search.append(take)
                give += take+" + "
            else:
                search.append(take)
    kh.observer.notify(f"\nNdarondera: {give[:-3]}")
    if not search:
        kh.observer.notify("Kubera ko ataco watoye nahejeje.")
        sysexit()
    return notss, search


if __name__ == "__main__":
    kh.observer = kh.PrintConsole()
    f_in = input(r"""Tora ifishi ushaka kwihweza
      c                      = tagged korpus yose
      inzira/ku/fishi.txt    = ifishi rimwe (tora variante tagged iyo ufise)
      (filename please)
     : """)
    # corpus or file, if file: ist it txt?
    MULTIPLE = bool(check_fnin(f_in) == "c")
    kh.observer.notify(r"""
    Ushaka kurondera iki mu gisomwa?
            - for Bigrams or Trigrams use a combination of two respectively three letters
            - Possible PoS-tags:
               ADJ, ADV, CONJ, EMAIL, F(foreign words), INTJ, NI, NOUN,
               NUM, NUM_ROM (roman numbers), PRON (pronouns),
               PROPN, PROPN_CUR, PROPN_LOC (geographical places),
               PROPN_NAM (personal names), PROPN_ORG , PROPN_PER, PROPN_REL,
               PROPN_SCI, PROPN_THG, PROPN_VEG, PRP (prepositions),
               SYMBOL, UNK (unkwon to dictionary), VERB, WWW (webaddresses)

    Tora indome muri (chose letters from)""")

    # word/tag/lemma/?
    wtl = input(r"""        W = exact word
        L = all wordforms of a lemma
        T = part of speech-tag
        ? = wildcard
    : """)
    wtl = check_interest(wtl)
    # specify the wtl or exclude a wtl (word/tag/lemma)
    nots, quterms = specify_search(wtl)
    search_or_load_search(f_in, wtl, nots, quterms, MULTIPLE)
