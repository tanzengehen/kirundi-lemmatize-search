#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  6 15:10:18 2023

@author: doreen nixdorf
"""

import os


class ResourceNames:
    """pathames for resource files
    """
    root = "/".join(os.getcwd().split("/")[:-1])
    fn_i18n = root+"/i18n"
    fn_corpuslist = root+"/resources/verzeichnis.txt"
    fn_namedentities = root+"/resources/extern.csv"
    fn_freqfett = root+"/resources/freq_fett.csv"
    fn_db = root+"/resources/db_kirundi.csv"
    fn_dates = root+"/resources/dates.txt"
    dir_tagged = root+"/results/tagged/"
    dir_searched = root+"/results/searched/"

    def __str__(self):
        return f"root={self.root}, fn_namedentities={self.fn_namedentities}, "\
            + f"n_freqfett={self.fn_freqfett}, fn_db={self.fn_db}, "\
            + f"fn_dates={self.fn_dates}, dir_tagged={self.dir_tagged}, "\
            + f"dir_searched={self.dir_searched}"

    def __repr__(self):
        return f"root={self.root}, fn_namedentities={self.fn_namedentities}, "\
            + f"n_freqfett={self.fn_freqfett}, fn_db={self.fn_db}, "\
            + f"fn_dates={self.fn_dates}, dir_tagged={self.dir_tagged}, "\
            + f"dir_searched={self.dir_searched}"


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


class CorpusCategories:
    """categories of corpus from University
    """
    cc = ['1920s', '1940s', '1950s', '1960s', '1970s',
          '1980s', '1990s', '2000s', '2010s', 'ORAL', 'WRITTEN',
          'Chansons', 'Poésie', 'Théâtre', 'Contes', 'Romans', 'Magazines',
          'Nouvelles', 'Informations', 'Culture_traditionnelle',
          'Éducation', 'Santé', 'Société', 'Écologie', 'Paix', 'Lois',
          'Politique', 'Histoire', 'Religion']

    def __str__(self):
        return f"categories = {self.cc}"

    def __repr__(self):
        return f"cc = {self.cc}"


class PossibleTags:
    """Part-of-Speech tags the program uses
    """
    pt = ["ADJ", "ADV", "CONJ", "EMAIL", "F", "INTJ", "NI", "NOUN",
          "NUM", "NUM_ROM", "PRON", "PROPN", "PROPN_CUR", "PROPN_LOC",
          "PROPN_NAM", "PROPN_ORG", "PROPN_PER", "PROPN_REL", "PROPN_SCI",
          "PROPN_THG", "PROPN_VEG", "PREP", "SYMBOL", "UNK", "VERB", "WWW"]

    def __str__(self):
        return f"tags = {self.pt}"

    def __repr__(self):
        return f"pt = {self.pt}"


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

    def __init__(self, f_in, wtl, nots, quterms):
        self.fn_in = f_in
        self.wtl = wtl
        self.nots = nots
        self.questions = quterms
        self.short = ""
        self.fn_search = self.set_fnsearch()

    def __str__(self):
        return f"wtl={self.wtl}, questions={self.questions}, \
            nots={self.nots}, short={self.short}"

    def __repr__(self):
        return f"wtl={self.wtl}, questions={self.questions}, \
            nots={self.nots}, short={self.short}"

    def set_fnsearch(self):
        """combine filename of analysed file and search-terms for making
        a filename to store the search results
        """
        search = ""
        for i, quest in enumerate(self.questions):
            if self.wtl[i] == "lemma":
                que = "(l)"+quest
            else:
                que = quest
            if self.nots[i] == "!":
                search += "!"+que+"_"
            else:
                search += que+"_"
        myname = self.fn_in.split("/")[-1]
        short = myname.find(".")
        self.short = myname[:short]
        fn = ResourceNames.dir_searched+self.short+"__"+search+".txt"
        return fn


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
