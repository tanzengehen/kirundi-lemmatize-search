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
from kir_tag_search import search_or_load_search

def check_fnin(fn_in):
    """checks filename of txt ending"""
    if fn_in == "":
        print("Kubera ko ataco watoye nahejeje.")
        sysexit()
    if fn_in in "cC":
        return "c"
    if fn_in[-4:] not in [".txt",".json"] :
        print("Hariho ikosa n'ifishi: '"+f_in
              +"'\nNdashobora gukoresha ifishi ifise impera '.txt' canke '.json' gusa")
        sysexit()
    return "f"

def check_interest(interest0):
    """checks kind of search: word, tag, lemma or joker 
    returns list with indices for tag-parts:
    [1,1,2] for tag, tag, lemma"""
    interest = interest0.replace(" ","").lower()
    interest_nojoker = interest0.replace("?","")
    if interest == "":
        # nothing picked
        print("Kubera ko ataco watoye nahejeje.")
        sysexit()
    elif interest_nojoker == "":
        # '?' on all positions
        print("nonosora ukurondera kwawe") # specify your search
        sysexit()
    elif len(interest_nojoker) == 1:
        # only one is no '?'
        interest = interest_nojoker
    for i in interest:
        if i not in "wlt?":
            # wrong character picked
            print("hari ikosa: no valid search criteria: gusa 'w', 't' , 'l' canke '?'")
            sysexit()
    kind_of_search = {"w":"token","t":"pos","l":"lemma","?":"?"}
    print(interest)
    interest1 = [kind_of_search.get(i) for i in interest]
    return interest1

def specify_search(interest0):
    """takes exact searchword, searchtag or searchlemma"""
    kind_of_search = {"token": "Ijambo ririhe? : ",
                      "pos": "Amajambo yose afise indanzi: ",
                      "lemma": "Amajambo yose y'itsitso ririhe? : "} #itsitsu -Wurzel
    search =[]
    if len(interest0) > 1 :
        print("Urashaka gutora "+str(len(interest0))+"-gram")
        count = "igice " # for printing confirmation later
    else :
        count = ""
    for i,interest in enumerate(interest0):
        if interest == "?" :
            print(str(i+1),": kira jambo rirakunda")
            search.append("?")
        else:
            take =input(count+str(i+1)+": "+kind_of_search.get(interest))
            possible= sd.PossibleTags()
            if interest == "pos" :
                # PoS tags always in uppercase
                take = take.upper()
                if take in possible.pt1 or take in possible.pt2 :
                    search.append(take)
                else:
                    print("indanzi",take,"ntiriho") # gibt's nicht
                    sysexit()
            # word, lemma
            elif take != "" :
                search.append(take)
    for i in search[:-1] :
        print (i, end = " + ") #??? wofür end?
    print(search[-1])
    if not search:
        print("Kubera ko ataco watoye nahejeje.")
        sysexit()
    return search


f_in = input(r"""Tora ifishi ushaka kwihweza
  c                      = tagged korpus yose
  inzira/ku/fishi.txt    = ifishi rimwe (tora variante tagged iyo ufise)
 : """)
# corpus or file, if file: ist it txt?
MULTIPLE = bool(check_fnin(f_in) == "c")

print(r"""
Ushaka kurondera iki mu gisomwa? 
        - for Bigrams or Trigrams use a combination of two respectively three letters
        - Possible POS-tags: 
           ADJ, ADV, CONJ, EMAIL, F(foreign words), INTJ, NI, NOUN, 
           NUM, NUM_ROM (roman numbers), 
           PHRASE, PRON (pronouns), PROPN, PROPN_CUR", PROPN_LOC (geographical places), 
           PROPN_NAM (personal names), PROPN_ORG , PROPN_PER, PROPN_REL, PROPN_SCI
           PROPN_THG, PROPN_VEG, PRP (prepositions),
           SYMBOL, UNK (unkwon to dictionary), VERB, WWW (webaddresses)
           and this: ,.:!?(){}[]'"
    
Tora indome""")

# word/tag/lemma/?
wtl = input(r"""    W = exact word
    L = all wordforms of a lemma 
    T = part of speech-tag
    ? = wildcard
 : """)
wtl = check_interest(wtl)
# which word/tag/lemma
questions = specify_search(wtl)
search_or_load_search(f_in, wtl, questions, MULTIPLE)
