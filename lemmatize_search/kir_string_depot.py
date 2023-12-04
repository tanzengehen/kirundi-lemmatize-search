#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  6 15:10:18 2023

@author: doreen nixdorf
"""

import os
# import sys


class ResourceNames:
    """pathames for resource files
    """

    sep = os.path.sep
    long_root = os.getcwd().split(sep)
#     print(sys.path)
    for i, part in enumerate(long_root):
        if part == "rundi_lemmatize_search":
            relative = i
            break
    root = sep.join(os.getcwd().split(sep)[:relative+1])
    fn_i18n = root+sep+"i18n"
    fn_corpuslist = root+sep+"resources"+sep+"verzeichnis.txt"
    fn_named_entities = root+sep+"resources"+sep+"extern.csv"
    fn_freqfett = root+sep+"resources"+sep+"freq_fett.csv"
    # fn_db = root+sep+"resources"+sep+"db_kirundi.csv"
    # fn_db = root+"/tests/test_lemmata.csv"
    fn_db = root+"/resources/db_cox.csv"
    fn_dates = root+sep+"resources"+sep+"dates.txt"
    dir_tagged = root+sep+"results"+sep+"tagged"+sep
    dir_searched = root+sep+"results"+sep+"searched"+sep

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


test_text = "1710 || amakuru-49975817 || 2019-10-08 || ABAGORE || (93+2849)" +\
    "Abagore babiri barwaye kanseri y’ibere batanguje ishirahamwe " +\
    "ry’ugufasha abandi barwayi nkabo Abagore babiri barwaye kanseri " +\
    "y'ibere idakira bashinze ishirahamwe bise Secondary Sisters " +\
    " kugira ngo bafashe abandi, ni inyuma y'aho baronkeye ibipimo " +\
    "vyabaciye umutima. Abongerezakazi Nicky Newman na Laura " +\
    "Middleton-Hughes, bompi b'imyaka 31, bafise kanseri igeze ku " +\
    "rugero rugira kane. Bisigura ko igeze ku rugero rwo gukwiragira " +\
    "mu bindi bice vy'umubiri nk'amagufa, amahaha, igitigu (canke " +\
    "umwijima mu Kinyarwanda) canke ubwonko. Igihe Nicky wo mu karere ka " +\
    "Guildford yabwirwa ko kanseri yiwe idashobora gukira kubera " +\
    "yari igeze ku rugero rwo hejuru, avuga ko vyatumye " +\
    "agira ""ubwoba budasanzwe"". Abo bagore bompi bizeye ko iryo " +\
    "shirahamwe ryabo rikorera ku rubuga ngurukanabumenyi rizofasha " +\
    "abandi bazoronka inkuru mbi nk'iyi guhangana nayo. Laura ava i " +\
    "Norwich avuga ko gushinga iryo shirahamwe vyabahaye ""akaryo keza " +\
    "k'ukuganira ku vyerekeye kanseri yacu"". Ati: ""Twempi tubona ko " +\
    "dufise kazoza kadatomoye, ariko turafise kazoza kandi tuzobaho " +\
    "uko nyene"". ""Rero mu gihe twoshobora gufasha n'umuntu n'umwe " +\
    "gusa kwumva amahoro, akumva ko ari umuntu nk'abandi, ico " +\
    "kirahagije"". Abo bagore bompi, bakorana n'umugambi wiswe " +\
    "Stand Up To Cancer. Ni umugambi w'isekeza ry'ukwegeranya amahera " +\
    "watunganijwe n'ikigo co mu Bwongereza ca Cancer Research UK kijejwe " +\
    "kurwanya kanseri, hamwe na televiziyo Channel 4. Nicky yagiye " +\
    "kumenya ko afise ikivyimba mw'ibere igihe yari yagiye kwivuza ari " +\
    "kumwe n'umugabo wiwe. Avuga ko yari yavyiketse n'imbere y'uko " +\
    "abimubwira, aravye ingene muganga yahindutse mu maso. Mu gihe " +\
    "yariko arapimwa, yavuze ko yumva ababara mu mugongo, ariho yaca " +\
    "arungikwa ku muhinga afotora mu mubiri. Ati: ""Umuganga yambwiye " +\
    "ati: 'Sha nta kundi, ntaco nshobora kugufasha'. Vyaciye bintera " +\
    "ubwoba bwinshi"". Ariko, yaciye amuha umuti witwa Palbociclib " +\
    "wari uherutse kwemerwa n'ikigo NHS kijejwe amagara y'abantu mu " +\
    "Bwongereza. Imiti bariko barafata ishobora kuba yaratumye iyo " +\
    "ndwara itabandanya ikwiragira mu mubiri, ariko ikaba yatumye " +\
    "batazigera bavyara. Nicky avuga ko igihe yava kwa muganga, yari " +\
    "ababajwe cane n'uko atazoronka akaryo ko kwitwa umuvyeyi gusumba " +\
    "kurwara kanseri. Mugenziwe Laura yagiye kumenya ko arwaye kanseri " +\
    "yo mw'ibere mu mwaka wa 2014 mu gihe yari mu karuhuko bakamutora " +\
    "ikivyimba. Baciye bamukura ibere rimwe baranamuvura, kandi " +\
    "arakira neza. Hagati aho, mu kwezi kwa kane 2016, niho yumva " +\
    "ububabare ku rutugu i buryo bwaguma bwongerekana, baca " +\
    "bamurungika gucishwa mu cuma agapimwa. Niho basanga afise " +\
    "ikivyimba ku mutwe w'igufa bita 'humerus' rifatanya urutugu " +\
    "n'inkokora. Ati: ""Nagize ubwoba budasanzwe, 2016 wambereye " +\
    "umwaka mubi, umwaka mubi n'ukuri!"" Laura afise ibimenyetso vya " +\
    "kanseri y'amabere vyakwiragiye mu ruti rw'umugongo, mu magufa " +\
    "afatanye narwo no mu gice c'urukenyerero n'amayunguyungu. Avuga " +\
    "ati: ""Hagati aho, ndashima ko imiti ndiko ndafata iriko iramfasha " +\
    "kubandanya mbaho""."''

test_text2 = "Bavuga 'ko hariho ayandi majambo mu Kitabu Kitakatifu, " +\
    "ahakana ubukuru bwa B. Mariya. (Inj·ili ya Yohani II. 3-4) . Yezu " +\
    "na Mariya bari batumiwe mu bukwe i Kana. Imvinyu irangiye. " +\
    "nyina wa Yezu amubwira ati: 'Nta mvinyu bakigira.' Yezu " +\
    "aramwishura ati : 'Mbega mugore twe na we tubisinzikayekoiki?'"
