#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 07:39:44 2023

@author: doreen nixdorf
"""

import re
from nltk.text import FreqDist
from nltk.corpus import PlaintextCorpusReader
from unidecode import unidecode
import kir_string_depot as sd
import kir_helper2 as kh


class TextMeta:
    """statistics
    """
    def __init__(self, raw, pathname=None, fileid= None):
        self.fileid = fileid
        self.pathname = pathname
        self.categories = ""
        self.raw = raw
        # for results
        self.text, self.nodds = self.replace_strangeletters(self.raw)
        self.nchars = len(self.text)
    def __str__(self):
        if self.text:
            textset=True
        return f"FileMeta: fileid={self.fileid}, pathname={self.pathname},"\
            +f" text_prepared={textset}, mistakes while loaded={self.nodds}, "\
              +f" characters={self.nchars}"
    def __repr__(self):
        if self.raw:
            textset="set"
        return f"FileMeta: fileid={self.fileid} pathname={self.pathname} text={textset} " \
                +f"nodd={self.nodds}"\
              +f" nchar={self.nchars}"
    def set_corpuscategories(self, pathname):
        """extracts categories from filenames of files in university-corpus
        """
        if pathname is not None:
            elements = pathname.split("/")[-5:-1]
            self.categories = [x for x in elements if x in sd.CorpusCategories.cc]
    def update_pathslist(self, corpus_root):
        """updates the filenames we have in this corpus
        """
        wordlists = PlaintextCorpusReader(corpus_root, '.*')
        paths_list = wordlists.fileids()
        with open(corpus_root+"verzeichnisNeu.txt","w",encoding="utf-8") as file:
            for i in paths_list :
                file.write(i+"\n")
        return paths_list
    def replace_strangeletters(self,raw_text):
        """replaces odd characters from bad OCR
        takes string
        returns list [corrected string, mistakes]
        """
        strangethings = str(raw_text.encode(encoding="utf-8",errors="backslashreplace"))[2:-1]
        mistakes = re.findall(r"(\\x[a-f0-8]{2}){2}",strangethings)
        n_mistakes = len(mistakes)
        strange_list =[("\\xe1\\xba\\xad","ậ"),
                        ("\\xe1\\xba\\xb7","ặ"),
                        ("\\xe1\\xbb\\x82","Ể"), # E mit circonflex und hook
                        ("\\xe1\\xbb\\x83","ể"), # e mit circonflex und hook
                        ("\\xe1\\xbb\\x87","ệ"),
                        ("\\xe1\\xbb\\xa9","ú"),
                        ("\\xe1\\xbe\\xb0","Ᾰ"),
                        ("\\xe1\\xbe\\xb8","Ᾰ"), # A combininb breve
                       # ("\\xe2\\x80\\xa"," "), #
                       # ("\\xe2\\x80\\x9"," "), #
                        ("\\xe2\\x80\\x98","'"),
                        ("\\xe2\\x80\\x91","-"),    # non breaking hyphen
                        ("\\xe2\\x80\\x99","'"),    # right single quotation mark
                        ("\\xe2\\x80\\xa6","..."),  # horizontal ellipsis
                        ("\\xe2\\x80\\x9d",'"'),
                        ("\\xe2\\x80\\x9c",'"'),
                        ("\\xe2\\x80\\x83",""),
                        ("\\xe2\\x80\\x88","."),
                        ("\\xe2\\x80\\x93","-"),    # schmaler Gedankenstrich (n)
                        ("\\xe2\\x80\\x94","-"),    # breiter Gedankenstrich (m)
                        ("\\xe2\\x80\\x9a",","),
                        ("\\xe2\\x80\\x9e",'"'),
                        ("\\xe2\\x80\\xa2","·"),
                        ("\\xe2\\x80\\xb9",'"'),    # ‹
                        ("\\xe2\\x80\\xba",'"'),    # ›
                        ("\\xe2\\x82\\xac","€"),
                        ("\\xe2\\x96\\xa0","-"),    # ■
                        ("\\xe2\\x96\\xba","-"),    # ►
                        ("\\xe2\\x97\\x8f","-"),    # ●
                        ("\\xe2\\x99\\xa6","-"),    # ♦
                        ("\\xe2\\x9d\\x96","-"),    # ❖
                        ("\\xe2\\x9e\\xa2",">"),    # ➢ 3D-Pfeil
                        ("\\xef\\x80\\xa1","???"),    # chinesisch
                        ("\\xef\\x80\\xaa","???"),  # Nr 1034 chinesisch
                        ("\\xef\\x80\\xad","???"),  # 846 chinesisch
                        ("\\xef\\x81\\x84","???"),  # 1034 149x chinesisch
                        ("\\xef\\x81\\xb6","???"),  # 1106 4x chinesisch
                        ("\\xef\\x81\\x89","???"),  # 1308 2x chinesisch
                        ("\\xef\\x82\\xa7","???"),  # 1106 6x chinesisch
                        ("\\xef\\x82\\xae","???"),    # 846 !?  chinesisch
                        ("\\xef\\x82\\xaf","???"),  # 846? chinesisch
                        ("\\xef\\x83\\xa8",""),   # 846 sieht leer aus
                        ("\\xef\\x83\\xbc","-"),  # 1391 13x Aufzählung chinesisch
                        ("\\xef\\x83\\x98","???"),# chinesisch
                        ("\\xef\\xb4\\xbe","("),  # 1031, 1032 dekorierteKLammer U+FD3E
                        ("\\xef\\xbb\\xbf",""), #294 zero width no-break-space
                        ("\\xef\\xbf\\xbd"," "),  #diverse in Nr.369 replacement: ? im Rhombus
                    #    ("\\xc3\\xa"," "),      #
                        ("\\xc2\\x92","'"),   # ' privat use (komma oben)
                        ('\\xc2\\xa0',' '), #no break space
                        ('\\xc2\\xa1','¡'),
                        ('\\xc2\\xa2','¢'),
                        ('\\xc2\\xa3','£'),
                        ('\\xc2\\xa4','¤'),
                        ('\\xc2\\xa5','¥'),
                        ('\\xc2\\xa6','¦'),
                        ('\\xc2\\xa7','§'),
                        ('\\xc2\\xa8','¨'),
                        ('\\xc2\\xa9','©'),
                        ('\\xc2\\xaa','ª'),
                        ('\\xc2\\xab','"'),     # «
                        ('\\xc2\\xac','¬'),
                        ('\\xc2\\xad','-­'),    # soft hyphen
                        ('\\xc2\\xae','®'),     # ® registered
                        ('\\xc2\\xaf','¯'),
                    #    ('\\xc2\\xb','»'),
                        ('\\xc2\\xb0','°'),
                        ('\\xc2\\xb1','±'),
                        ('\\xc2\\xb2','²'),
                        ('\\xc2\\xb3','³'),
                        ('\\xc2\\xb4',"'"),     # ´ Acute accent ´
                        ('\\xc2\\xb5','µ'),
                        ('\\xc2\\xb6','¶'),
                        ('\\xc2\\xb7','.'),   # · mittlerer Punkt
                        ('\\xc2\\xb8',','),   # ¸ cedilla
                        ('\\xc2\\xb9','¹'),
                        ('\\xc2\\xba','°'),    # º männlich
                        ('\\xc2\\xbb','"'),    # »
                        ('\\xc2\\xbc','¼'),
                        ('\\xc2\\xbd','½'),
                        ('\\xc2\\xbe','¾'),
                        ('\\xc2\\xbf','¿'),
                        ('\\xc3\\x80','À'),
                        ('\\xc3\\x81','Á'),
                        ('\\xc3\\x82','Â'),
                        ('\\xc3\\x83','Ã'),
                        ('\\xc3\\x84','Ä'),
                        ('\\xc3\\x85','Å'),
                        ('\\xc3\\x86','Æ'),
                        ('\\xc3\\x87','Ç'),
                        ('\\xc3\\x88','È'),
                        ('\\xc3\\x89','É'),
                        ('\\xc3\\x8a','Ê'),
                        ('\\xc3\\x8b','Ë'),
                        ('\\xc3\\x8c','Ì'),
                        ('\\xc3\\x8d','Í'),
                        ('\\xc3\\x8e','Î'),
                        ('\\xc3\\x8f','Ï'),
                        ('\\xc3\\x90','Ð'),
                        ('\\xc3\\x91','Ñ'),
                        ('\\xc3\\x92','Ò'),
                        ('\\xc3\\x93','Ó'),
                        ('\\xc3\\x94','Ô'),
                        ('\\xc3\\x95','Õ'),
                        ('\\xc3\\x96','Ö'),
                        ('\\xc3\\x97','×'),
                        ('\\xc3\\x98','Ø'),
                        ('\\xc3\\x99','Ù'),
                        ('\\xc3\\x9a','Ú'),
                        ('\\xc3\\x9b','Û'),
                        ('\\xc3\\x9c','Ü'),
                        ('\\xc3\\x9d','Ý'),
                        ('\\xc3\\x9e','Þ'),
                        ('\\xc3\\x9f','ß'),
                        ('\\xc3\\xa0','à'),
                        ('\\xc3\\xa1','á'),
                        ('\\xc3\\xa2','â'),
                        ('\\xc3\\xa3','ã'),
                        ('\\xc3\\xa4','ä'),
                        ('\\xc3\\xa5','å'),
                        ('\\xc3\\xa6','æ'),
                        ('\\xc3\\xa7','ç'),
                        ('\\xc3\\xa8','è'),
                        ('\\xc3\\xa9','é'),
                        ('\\xc3\\xaa','ê'),
                        ('\\xc3\\xab','ë'),
                        ('\\xc3\\xac','ì'),
                        ('\\xc3\\xad','í'),
                        ('\\xc3\\xae','î'),
                        ('\\xc3\\xaf','ï'),
                        ('\\xc3\\xb0','ð'),
                        ('\\xc3\\xb1','ñ'),
                        ('\\xc3\\xb2','ò'),
                        ('\\xc3\\xb3','ó'),
                        ('\\xc3\\xb4','ô'),
                        ('\\xc3\\xb5','õ'),
                        ('\\xc3\\xb6','ö'),
                        ('\\xc3\\xb7','÷'),
                        ('\\xc3\\xb8','ø'),
                        ('\\xc3\\xb9','ù'),
                        ('\\xc3\\xba','ú'),
                        ('\\xc3\\xbb','û'),
                        ('\\xc3\\xbc','ü'),
                        ('\\xc3\\xbd','ý'),
                        ('\\xc3\\xbe','þ'),
                        ('\\xc3\\xbf','ÿ'),
                        ('\\xc4\\xb0','İ'),
                        ('\\xc4\\xb1','ı'),
                        ('\\xc4\\x83','ă'),
                        ('\\xc4\\x9f','ğ'),
                        ('\\xc4\\xab','ī'),
                        ('\\xc5\\x84','ń'),
                        ('\\xc5\\x93','œ'),
                        ('\\xc5\\x9e','Ş'),
                        ('\\xc5\\x9f','ş'),
                        ('\\xc5\\xab','ū'),
                        ('\\xc5\\xad','ŭ'),
                        ('\\xc5\\xb8','Ÿ'),
                        ('\\xc7\\x94','ǔ'),
                        ('\\xc7\\x99','Ǚ'),
                        ('\\xc7\\x9a','ǚ'),
                        ('\\xc8\\x8f','ô'),
                        ('\\xca\\xbc',"'"), # modifier apostroph
                        ('\\xca\\xbe',"'"), # ' modifier letter, right half ring
                        ('i\\xcc\\x87','İ'),
                        ('\\xcc\\x8b','"'), # combining double Acute Accent
                        ('\\xcc\\x8f','"'), # combining double Grave Accent
                        ('\\xce\\xaf','ί'),
                        ('\\xcf\\x8c','ό'),
                        ('\\xd1\\x97',':'),
                        ('\\xd7\\x83','ï'),
                        ('\\x0c',' '),  # Form Feed
                        ('\\x7f',' '),  #Enter
                        ('\\t',' '),    #tab
                        ("\\'","'"),    # \' wird zu '
                        ("\\ "," "),
          ]
        for strange in strange_list:
            text2 = strangethings.replace(strange[0],strange[1])
            strangethings = text2
        # all whitespaces become only one blank
        text2 = re.sub(r"\s+"," ",strangethings)
        return text2,n_mistakes


class FreqSimple:
    """frequency distribution of types
    """
    def __init__(self, blanktext):
        self.ntypes = None
        self.n_unk = None
        self.n_one = None
        self.pathname = None
        self.fileid = None
        self.freq = None
        self.blanktext = blanktext
        self.ntokens = None
        self.__make_simplefreq_fromtext__(self.blanktext)
    def __str__(self):
        return f"origin='{self.pathname}', fileid={self.fileid}, Anzahl Types={self.ntypes}"
    def __repr__(self):
        return f"pathname='{self.pathname}', fileid={self.fileid}, ntypes={self.ntypes}" \
            +"\nask .blanktext for analysed words and .simple for the frequency distribution"
    def __f_dist__(self, blanktext):
        """returns frequency list from list of words, 
            reverse-sorted by frequency"""
        fdist = FreqDist(blanktext.split())
        freq = sorted(fdist.items(), key = lambda x: x[1], reverse = True)
        return freq
    def __make_simplefreq_fromtext__(self, blanktext) :
        """schreibt alles klein, zupft Akzente ab, entfernt Zeilenumbrüche,
        schmeißt Zeichensetzung und Leerzeichen raus
        liefert: simple_freq
        """
        #replace linebreaks and diacritics and lower
        cleaned1 = unidecode(blanktext.lower()).replace("\n"," ")
        longpunctuation = '´`\'!"#$€%&()*+,-/:<=>?[\\]^_{|}~;.@0123456789'
        for p in longpunctuation:
            cleaned2 = cleaned1.replace(p," ")
            cleaned1 = cleaned2
        # reduce the new whitespaces
        blanktext = re.sub(r"\s+"," ",cleaned2)
        self.ntokens = len(blanktext.split())
        # frequency distribution
        self.freq = self.__f_dist__(blanktext)
        self.ntypes = len(self.freq)
        kh.messages.new("\nvocabulary: "+str(self.ntokens)+" tokens\n"+11*" "\
                        +str(self.ntypes)+" types\n")

class Collection:
    """collects types in PoS lists
    """
    def __init__(self,simple_freq_list):
        self.names = []
        self.advs = []
        self.pronouns = []
        self.nouns = []
        self.adjs = []
        self.verbs = []
        self.exclams = []
        self.unk = []
    def known(self):
        """ returns a list of all types which found a lemma
        sorted by lemma
        """
        known = self.names \
            +self.advs \
            +self.pronouns \
            +self.nouns \
            +self.adjs \
            +self.verbs \
            +self.exclams
        for i in known:
            if type(i[3]) is not int:
                kh.messages.new(i+" type [3]: "+type(i[3]))
        known.sort(key=lambda x: x[3], reverse = True)
        return known
    def all_in(self):
        """returns a list of all types sorted by lemma or themselves if they didn't match
        a lemma
        """
        all_in = self.known()+self.unk
        all_in.sort(key=lambda x: x[3], reverse = True)
        return all_in


class FreqMeta:
    """some statistics of the frequency distributions
    """
    def __init__(self, lemmafreq):
        self.freq = lemmafreq
        self.length = len(lemmafreq)
        self.n_lemma = 0
        self.n_unk = 0
        self.n_one = 0
        self.n_ne = 0
        self.n_extern = 0
        for i in lemmafreq:
            if i[3] == 1 :
                self.n_one += 1
            if i[2] == "UNK" :
                self.n_unk += 1
            elif i[2] in [
                "ADJ", "ADV", "CONJ", "INTJ", "NI", "NOUN", 
                 "PRON","PREP", "VERB"] :
                self.n_lemma += 1
            elif i[2] == "F":
                self.n_extern += 1
            elif i[2] in [
                "PROPN","PROPN_CUR","PROPN_LOC","PROPN_NAM","PROPN_ORG",
                "PROPN_PER", "PROPN_REL","PROPN_SCI","PROPN_THG",
                "PROPN_VEG"] :
                self.n_ne += 1
    def __str__(self):
        return f"length of lemmafreq={self.length}, found lemmata={self.n_lemma}, "\
                +f" unknown to db={self.n_unk}, singletons= {self.n_one}, "\
                +f"NamedEntities={self.n_ne}, foreign words={self.n_extern}"
    def __repr__(self):
        return f"length={self.length}, n_lemma={self.n_lemma}, "\
                +f" n_unk={self.n_unk}, n_one= {self.n_one}, "\
                +f"n_ne={self.n_ne}, n_extern={self.n_extern}"


class Token:
    """a word in a text with its lemma and PoS-tag and
    diverse numbers for its positions in text and sentence
    """
    def __init__(self, token, pos="UNK", lemma=None):
        self.id_token = None
        self.id_char = None
        self.id_sentence = None
        self.id_tokin_sen = None
        self.token = token
        self.pos = pos
        if not lemma:
            self.lemma = token
        else:
            self.lemma = lemma
    def __str__(self):
        return f"'{self.token}', POS-tag={self.pos}, lemma='{self.lemma}'"
    def __repr__(self):
        return f"Token( {self.token}/{self.pos}/{self.lemma},"\
               +f"\n\t\tchar={self.id_char}, token={self.id_token}, "\
               +f"sentence={self.id_sentence}, word_in_sentence={self.id_tokin_sen})"
    def set_nrs(self, isentence, iword_in_sentence, itoken, ichar):
        """stores position of the token"""
        self.id_sentence = isentence
        self.id_tokin_sen = iword_in_sentence
        self.id_token = itoken
        self.id_char = ichar
    # to get the right item when we don't know which one we need
    def get(self, tag_str="lemma"):
        """call the tags"""
        if tag_str == "token" :
            return self.token
        if tag_str == "pos" :
            return self.pos
        return self.lemma



class TokenList:
    """list of all tokens in a text
    """
    def __init__(self,tagged_list):
        self.tokens = tagged_list
        self.ntokens = len(self.tokens)
        self.ntypes = len({i.token for i in self.tokens})
        self.nlemmata = len({i.lemma for i in self.tokens})
        self.lemmasoup=""
        for i in self.tokens:
            self.lemmasoup += i.lemma+" "
        self.lemmasoup= self.lemmasoup.strip()
        self.tokensoup =""
        self.possoup=""
    def __str__(self):
        return f"ntokens={self.ntokens} ntypes={self.ntypes} nlemmata={self.nlemmata}"
    def __repr__(self):
        return f"ntokens={self.ntokens} ntypes={self.ntypes} nlemmata={self.nlemmata}"
    def make_tokensoup(self):
        """replaces tokens in an text by its lemma if known
        """
        for i in self.tokens:
            self.tokensoup += i.token+" "
        self.tokensoup= self.tokensoup.strip()
    def make_possoup(self):
        """replaces tokens in an text by its PoS-tag if known
        """
        for i in self.tokens:
            self.possoup += i.token+" "
        self.possoup= self.possoup.strip()
