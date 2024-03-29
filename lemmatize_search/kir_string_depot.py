#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  6 15:10:18 2023

@author: doreen nixdorf
"""

import os
import time
import gettext
# import sys


class ResourceNames:
    """pathames for resource files
    """

#     print(sys.path)
    sep = os.path.sep
    long_root = os.getcwd().split(sep)
    for i, part in enumerate(long_root):
        if part == "rundi_lemmatize_search":
            relative = i
            break
    root = sep.join(os.getcwd().split(sep)[:relative+1])

    fn_i18n = root+sep+"i18n"
    fn_help = root+sep+"resources"+sep+"help_"  # +LANG".html"
    fn_corpuslist = root+sep+"resources"+sep+"verzeichnis.txt"
    fn_named_entities = root+sep+"resources"+sep+"extern.csv"
    fn_freqfett = root+sep+"resources"+sep+"freq_fett.csv"
    fn_db_newest = root+sep+"resources"+sep+"db_kirundi.csv"
    fn_db_cox20 = root+sep+"resources"+sep+"db_cox.csv"
    fn_dates = root+sep+"resources"+sep+"dates.txt"
    # fn_db depends on supplied resource
    if os.path.exists(fn_db_newest):
        fn_db = fn_db_newest
        tic = os.path.getmtime(fn_db_newest)
        # tic_object = time.strptime(time.ctime(tic))
        tic_object = time.localtime(tic)
        tic_date = time.strftime("%y%m%d", tic_object)
        # version saved in tag__text
        db_version = 'fn_db_'+tic_date
    else:
        fn_db = fn_db_cox20
        db_version = 'fn_db_cox20'
    dir_tagged = root+sep+"results"+sep+"tagged"+sep
    dir_searched = root+sep+"results"+sep+"searched"+sep

    def __str__(self):
        return f"root={self.root}, fn_namedentities={self.fn_named_entities},"\
            + f" n_freqfett={self.fn_freqfett}, fn_db={self.fn_db}, "\
            + f"fn_dates={self.fn_dates}, dir_tagged={self.dir_tagged}, "\
            + f"dir_searched={self.dir_searched}, fn_i18n={self.fn_i18n}"

    def __repr__(self):
        return f"root={self.root}, fn_namedentities={self.fn_named_entities},"\
            + f" n_freqfett={self.fn_freqfett}, fn_db={self.fn_db}, "\
            + f"fn_dates={self.fn_dates}, dir_tagged={self.dir_tagged}, "\
            + f"dir_searched={self.dir_searched}, fn_i18n={self.fn_i18n}"


def short_input_filename(filename):
    """extracts from path/to/file.end the 'file' part and if necessary cuts
    the starting 'tag__' off"""
    myname = filename.split(ResourceNames.sep)[-1]
    if myname.startswith("tag__"):
        myname = myname[5:]
    short = myname.rfind(".")
    fn_short = myname[:short]
    return fn_short


def find_relative_path(name="rundi_lemmatize_search"):
    """finds the relative path from the current working directory to where
    the Rundi Lemmatizer is installed"""
    # not used now, goes up too far even it's nearby
    print("momentchen...")
    sep = os.path.sep
    for dirpath, dirname, filename in os.walk(sep, topdown=False):
        if name in dirname:
            # print(dirpath, dirname, filename)
            install_path = dirpath
            break
    rel_path = os.path.relpath(install_path) + os.sep + name
    return rel_path


language_dialog = {"rn": {'title': "Guhindura ururimi turavugana",
                          'message_l': "Incuro iza kwugurura iki \
urashobora kubikoresha mu kirundi.\nZima ubu co guhindura",
                          'ok': "Kuzima",
                          'cancel': "Oya, kubandanya"},
                   "fr": {'title': "Passer au français",
                          'message_l': "Pour que le passage au \
français soit effectif, veuillez redémarrer l'application.",
                          'ok': "Fermer l'appli",
                          'cancel': "Non, continuer"},
                   "en": {'title': "Change user interface to English",
                          'message_l': "With next start of the App \
we'll communicate in English.\nClose now to apply the change.",
                          'ok': "Close",
                          'cancel': "No, continue"},
                   "de": {'title': "Programmsprache wechseln",
                          'message_l': "Beim nächsten Mal, startet das \
Programm auf deutsch.\nFür diese Änderung jetzt bitte schließen.",
                          'ok': "Schliessen",
                          'cancel': "Nein, danke."}
                   }


encodings = [
    # which charSets may work
    # "ascii",
    # "big5",
    # "big5hkscs",
    # "cp037",
    # "cp424",
    # "cp437",
    # "cp500",
    # "cp720",
    # "cp737",
    # "cp775",
    # "cp850",
    # "cp852",
    # "cp855",
    # "cp856",
    # "cp857",
    # "cp858",
    # "cp860",
    # "cp861",
    # "cp862",
    # "cp863",
    # "cp864",
    # "cp865",
    # "cp866",
    # "cp869",
    # "cp874",
    # "cp875",
    # "cp932",
    # "cp949",
    # "cp950",
    # "cp1006",
    # "cp1026",
    # "cp1140",
    # "cp1250",
    # "cp1251",
    # "cp1252",
    # "cp1253",
    # "cp1254",
    # "cp1255",
    # "cp1256",
    # "cp1257",
    # "cp1258",
    # "euc_jp",
    # "euc_jis_2004",
    # "euc_jisx0213",
    # "euc_kr",
    # "gb2312",
    # "gbk",
    # "gb18030",
    # "hz",
    # "iso2022_jp",
    # "iso2022_jp_1",
    # "iso2022_jp_2",
    # "iso2022_jp_2004",
    # "iso2022_jp_3",
    # "iso2022_jp_ext",
    # "iso2022_kr",
    # "latin_1",
    # "iso8859_2",
    # "iso8859_3",
    # "iso8859_4",
    # "iso8859_5",
    # "iso8859_6",
    # "iso8859_7",
    # "iso8859_8",
    # "iso8859_9",
    # "iso8859_10",
    # "iso8859_13",
    # "iso8859_14",
    # "iso8859_15",
    # "iso8859_16",
    # "johab",
    # "koi8_r",
    # "koi8_u",
    # "mac_cyrillic",
    # "mac_greek",
    # "mac_iceland",
    # "mac_latin2",
    # "mac_roman",
    # "mac_turkish",
    # "ptcp154",
    # "shift_jis",
    # "shift_jis_2004",
    # "shift_jisx0213",
    # "utf_32",
    # "utf_32_be",
    # "utf_32_le",
    "utf_16",
    # "utf_16_be",
    # #"utf_16_le",
    # "utf_7",
    # "utf_8",
    # "utf_8_sig",
]


# categories of corpus from University
corpus_categories = ['1920s', '1940s', '1950s', '1960s', '1970s', '1980s',
                     '1990s', '2000s', '2010s', 'ORAL', 'WRITTEN', 'Chansons',
                     'Poésie', 'Théâtre', 'Contes', 'Romans', 'Magazines',
                     'Nouvelles', 'Informations', 'Culture_traditionnelle',
                     'Éducation', 'Santé', 'Société', 'Écologie', 'Paix',
                     'Lois', 'Politique', 'Histoire', 'Religion']


# Part-of-Speech tags used by the program
possible_tags = ["ADJ", "ADV", "CONJ", "EMAIL", "F", "INTJ", "NI", "NOUN",
                 "NUM", "NUM_ROM", "PRON", "PROPN", "PROPN_CUR", "PROPN_LOC",
                 "PROPN_NAM", "PROPN_ORG", "PROPN_PER", "PROPN_REL",
                 "PROPN_SCI", "PROPN_THG", "PROPN_VEG", "PREP", "SYMBOL",
                 "UNK", "VERB", "WWW"]


class NounPrepositions:
    """more variants if nouns are written inclusive prepositions without
    apostrophe
    """
    qu_nta = r"([na]ta|[mk]u|s?i)"
    qu_ca_vowel = r"([bkmrt]?w|[rv]?y|[nsckzbh])"
    qu_ca_konsonant = r"([nckzbh]|[bkmrt]?w|[rv]?y)[ao]"

    def __str__(self):
        return f"nta,ata,si,mu etc.: {self.qu_nta}, qu_ca_vowel = "\
            + f"{self.qu_ca_vowel}, qu_ca_konsonant = {self.qu_ca_konsonant}"

    def __repr__(self):
        return f"qu_nta = {self.qu_nta}, qu_ca_vowel = {self.qu_ca_vowel}, "\
            + f"qu_ca_konsonant = {self.qu_ca_konsonant}"


class PrnRgx:
    """regex for building pronouns by combination"""
    c_a = r"(([bkrt]w|[rv]?y|[bchkwz]))"
    c_o = r"([bkrt]?w|[rv]?y|[bchkz])"
    ic_o = r"(a[bhky]|i([cz]|([rv]?)y)|u(([bkrt]?w?)|y))"
    gi = r"([bghm]a|[bgmirz]i|n|[bdgmr]u)"
    i_ki = r"((a?[bhk]a|i?[bkrz]i|u?[bkrt]u)|[aiu])"
    kiw = r"(([bhky]a|[bkryz]i|[bkrtw]u))"
    poss = r"((u|kub)|(" + ic_o + "|" + c_o + ")?i)w"
    igki = r"(a[bhgkmy]a|i(v?y|[bgkmrz])i|u[bgkmrdtwy]u)"
    je = r"(([jw]|[mt]w)e)"


class ExclRgx:
    """regex for building exclamation"""
    ego = r"^(y?e+go+|e+h?|y?ee+)$"
    oya = r"^(oya+)$"
    ha = r"^(ha)+$"
    la = r"^(la)+$"
    ah = r"^([au]+h|aa+|y?uu+|ah[ao]+|hu+)$"
    yo = r"^(y?o+h?|o+ho+|oh+)$"
    mh = r"^(m+h+|hu+m+|hm+|mm+|uu+m)$"
    he = r"^(e?(he+)+)$"
    kye = r"^(kye+)+$"
    luya = r"^(h?al+e+l+u+[iy]a+)$"
    alo = r"^(alo+)$"
    euh = r"^(e+uh)$"


def column_names_lemmafreq():
    """headline for lemmafreq.csv
    """
    first_line = "lemma;id;PoS;tokens;types;forms"
    return first_line


def punctuation():
    """returns string of punctuationmarks etc.
    does not include currency signs
    """
    return ',.;:!?(){}[]\'"´`#%&+-*/<=>@\\^°_|~'


# for tagging we replace some characters because they will disorganise the
# structure of our csv files
replaced_symbols = {'semikolon': ';',
                    'quotation': '"',
                    'deg': '°'}


def replace_worded_symbols_back(word):
    """replace worded symbols back to symbols"""
    if word in replaced_symbols:
        return replaced_symbols.get(word)
    return word


class Letter:
    """group letters for class marker variants
    """
    # iki
    weak_consonant = "bdgjlmnrvwyz"
    # igi
    hard_consonant = "cfhkpst"
    # ic
    vowel = "aeiou"
    # foreign
    not_in_use = "qx"


def breakdown_consonants(mystring):
    """returns changed consonants in case of some combinations of letters
    """
    for i in range(len(mystring)-1):
        if mystring[i] == "n":
            if mystring[i+1] in r"[bpvf]":
                mystring = mystring.replace(mystring[i], "m")
    mystring = mystring.replace(
        "nr", "nd").replace("nh", "mp").replace("mh", "mp")\
        .replace("nn", "n").replace(r"[nm]m", "m")
    return mystring


class Search:
    """query and filenames for result, frequency distributions and tagged text
    """

    def __init__(self, fn_in, query):
        self.query = query
        self.fn_search = self.set_fnsearch(fn_in, query)

    def __str__(self):
        return f"query={self.query}, fn_search={self.fn_search}"

    def __repr__(self):
        return f"query={self.query}, fn_search={self.fn_search}"

    def set_fnsearch(self, fn_in, query):
        """combine filename of analysed file and search-terms for making
        a filename to store the search results
        """
        fn_short = short_input_filename(fn_in)
        search = ""
        # query format: list of tuples (yes/no, lemma/tag/word/wildcard, word)
        # print("in sd.set_fn_search query", query)
        for i in query:
            yesno = i[0]
            wtl = i[1]
            searchword = i[2]
            if wtl == "token":
                question = searchword+"(exact)"+"_"
            elif wtl == "lemma":
                question = searchword+"(lemma)"+"_"
            else:
                question = searchword+"_"
            if yesno == "n":
                search += "!"+question
            else:
                search += question
        fn_search = ResourceNames.dir_searched+fn_short+"__"+search+".txt"
        return fn_search


# TODO check with TextMeta.set_corpuscategories
# Achtung: "Culture traditionnelle" und "Culture traditionelle"
# 1. Schreibfehler, 2. Leerzeichen im Begriff !
def collect_corpuscategories():
    """collects different parts of pathnames of kirundi corpus as a list
    """
    paths_list = ResourceNames.fn_corpuslist
    categories = []
    for i in paths_list:
        elements = i.split("/")
        for element in elements[:-1]:
            if element.strip() not in categories:
                categories.append(element)
    for uninteresting in ["Constantin", "Ernest", "Ferdinand", "Doreen",
                          "Manoah", "Yvette", "G-MdS"]:
        categories.remove(uninteresting)
    return categories
