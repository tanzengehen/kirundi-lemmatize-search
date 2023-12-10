#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 07:39:44 2023

@author: doreen nixdorf
"""

import re
import datetime
from nltk.text import FreqDist
from nltk.corpus import PlaintextCorpusReader
from unidecode import unidecode
try:
    import kir_string_depot as sd
    import kir_db_classes as dbc
    import kir_prepare_verbs as kv
except ImportError:
    from ..lemmatize_search import kir_string_depot as sd
    from ..lemmatize_search import kir_db_classes as dbc
    from ..lemmatize_search import kir_prepare_verbs as kv
# import kir_helper2 as kh


class TextMeta:
    """statistics
    """

    def __init__(self, fn_in=None):
        self.fileid = None
        self.fn_in = fn_in
        self.raw = ""
        self.categories = ""
        # for results
        self.text = ""
        self.nodds = ""
        self.nchars = None
        self.fn_short = ""
        self.fn_tag = ""
        self.fn_freqlemma = ""
        if fn_in:
            self.set_fn_tag_and_lemma()

    def __str__(self):
        textset = bool(self.text)
        return f"FileMeta: fileid={self.fileid}, pathname={self.fn_in}, "\
               f"text_prepared={textset}, mistakes while "\
               f"loaded={self.nodds}, characters={self.nchars}"

    def __repr__(self):
        textset = bool(self.text)
        return f"FileMeta: fileid={self.fileid}, pathname={self.fn_in}, "\
               f"text={textset}, nodd={self.nodds},"\
               f" nchar={self.nchars}, fn_tag={self.fn_tag}"

    def set_corpuscategories(self, pathname):
        """extracts categories from filenames of files in university-corpus
        """
        if pathname is not None:
            elements = pathname.split("/")[-5:-1]
            self.categories = \
                [x for x in elements if x in sd.CorpusCategories.cc]

    def update_pathslist(self, corpus_root):
        """updates the filenames we have ito a corpus
        """
        wordlists = PlaintextCorpusReader(corpus_root, '.*')
        paths_list = wordlists.fileids()
        with open(corpus_root+"verzeichnisNeu.txt", "w",
                  encoding="utf-8") as file:
            for i in paths_list:
                file.write(i+"\n")
        return paths_list

    def replace_strangeletters(self):
        """replaces odd characters from bad OCR
        take: string
        set: text, nodds, nchars
        """
        strangethings = str(self.raw.encode(encoding="utf-8",
                                            errors="backslashreplace"))[2:-1]
        mistakes = re.findall(r"(\\x[a-f0-8]{2}){2}", strangethings)
        n_mistakes = len(mistakes)
        strange_list = [("\\xe1\\xba\\xad", "ậ"),
                        ("\\xe1\\xba\\xb7", "ặ"),
                        ("\\xe1\\xbb\\x82", "Ể"),  # E mit circonflex und hook
                        ("\\xe1\\xbb\\x83", "ể"),  # e mit circonflex und hook
                        ("\\xe1\\xbb\\x87", "ệ"),
                        ("\\xe1\\xbb\\xa9", "ú"),
                        ("\\xe1\\xbe\\xb0", "Ᾰ"),
                        ("\\xe1\\xbe\\xb8", "Ᾰ"),  # A combininb breve
                        # ("\\xe2\\x80\\xa", " "),  #
                        # ("\\xe2\\x80\\x9", " "),  #
                        ("\\xe2\\x80\\x98", "'"),
                        ("\\xe2\\x80\\x91", "-"),    # non breaking hyphen
                        ("\\xe2\\x80\\x99", "'"),  # right single quotation mark
                        ("\\xe2\\x80\\xa6", "..."),  # horizontal ellipsis
                        ("\\xe2\\x80\\x9d", '"'),
                        ("\\xe2\\x80\\x9c", '"'),
                        ("\\xe2\\x80\\x83", ""),
                        ("\\xe2\\x80\\x88", "."),
                        ("\\xe2\\x80\\x93", "-"),  # schmaler Gedankenstrich (n)
                        ("\\xe2\\x80\\x94", "-"),  # breiter Gedankenstrich (m)
                        ("\\xe2\\x80\\x9a", ","),
                        ("\\xe2\\x80\\x9e", '"'),
                        ("\\xe2\\x80\\xa2", "·"),
                        ("\\xe2\\x80\\xb9", '"'),    # ‹
                        ("\\xe2\\x80\\xba", '"'),    # ›
                        ("\\xe2\\x82\\xac", "€"),
                        ("\\xe2\\x96\\xa0", "-"),    # ■
                        ("\\xe2\\x96\\xba", "-"),    # ►
                        ("\\xe2\\x97\\x8f", "-"),    # ●
                        ("\\xe2\\x99\\xa6", "-"),    # ♦
                        ("\\xe2\\x9d\\x96", "-"),    # ❖
                        ("\\xe2\\x9e\\xa2", ">"),    # ➢ 3D-Pfeil
                        ("\\xef\\x80\\xa1", "???"),    # chinesisch
                        ("\\xef\\x80\\xaa", "???"),  # Nr 1034 chinese
                        ("\\xef\\x80\\xad", "???"),  # 846 chinese
                        ("\\xef\\x81\\x84", "???"),  # 1034 chinese
                        ("\\xef\\x81\\xb6", "???"),  # 1106 chinese
                        ("\\xef\\x81\\x89", "???"),  # 1308 chinese
                        ("\\xef\\x82\\xa7", "???"),  # 1106 chinese
                        ("\\xef\\x82\\xae", "???"),    # 846 !?  chinese
                        ("\\xef\\x82\\xaf", "???"),  # 846? chinese
                        ("\\xef\\x83\\xa8", ""),   # 846 seems empty
                        ("\\xef\\x83\\xbc", "-"),  # 1391 Aufzählung chinese
                        ("\\xef\\x83\\x98", "???"),  # chinese
                        ("\\xef\\xb4\\xbe", "("),  # 1031, 1032 dekorierteKLammer U+FD3E
                        ("\\xef\\xbb\\xbf", ""),  # 294 zero width no-break-space
                        ("\\xef\\xbf\\xbd", " "),  # diverse in Nr.369 replacement: ? im Rhombus
                    #    ("\\xc3\\xa"," "),      #
                        ("\\xc2\\x92", "'"),   # ' privat use (komma oben)
                        ('\\xc2\\xa0', ' '),   # no break space
                        ('\\xc2\\xa1', '¡'),
                        ('\\xc2\\xa2', '¢'),
                        ('\\xc2\\xa3', '£'),
                        ('\\xc2\\xa4', '¤'),
                        ('\\xc2\\xa5', '¥'),
                        ('\\xc2\\xa6', '¦'),
                        ('\\xc2\\xa7', '§'),
                        ('\\xc2\\xa8', '¨'),
                        ('\\xc2\\xa9', '©'),
                        ('\\xc2\\xaa', 'ª'),
                        ('\\xc2\\xab', '"'),    # « left pointing double quotation mark
                        ('\\xc2\\xac', '¬'),
                        ('\\xc2\\xad', '-­'),    # soft hyphen
                        ('\\xc2\\xae', '®'),    # ® registered
                        ('\\xc2\\xaf', '¯'),
                        # ('\\xc2\\xb', '»'),
                        ('\\xc2\\xb0', '°'),
                        ('\\xc2\\xb1', '±'),
                        ('\\xc2\\xb2', '²'),
                        ('\\xc2\\xb3', '³'),
                        ('\\xc2\\xb4', "'"),   # ´ Acute accent ´
                        ('\\xc2\\xb5', 'µ'),
                        ('\\xc2\\xb6', '¶'),
                        ('\\xc2\\xb7', '.'),   # · mittlerer Punkt
                        ('\\xc2\\xb8', ','),   # ¸ cedilla
                        ('\\xc2\\xb9', '¹'),
                        ('\\xc2\\xba', '°'),   # º männlich
                        ('\\xc2\\xbb', '"'),   # » right pointing double quotation mark
                        ('\\xc2\\xbc', '¼'),
                        ('\\xc2\\xbd', '½'),
                        ('\\xc2\\xbe', '¾'),
                        ('\\xc2\\xbf', '¿'),
                        ('\\xc3\\x80', 'À'),
                        ('\\xc3\\x81', 'Á'),
                        ('\\xc3\\x82', 'Â'),
                        ('\\xc3\\x83', 'Ã'),
                        ('\\xc3\\x84', 'Ä'),
                        ('\\xc3\\x85', 'Å'),
                        ('\\xc3\\x86', 'Æ'),
                        ('\\xc3\\x87', 'Ç'),
                        ('\\xc3\\x88', 'È'),
                        ('\\xc3\\x89', 'É'),
                        ('\\xc3\\x8a', 'Ê'),
                        ('\\xc3\\x8b', 'Ë'),
                        ('\\xc3\\x8c', 'Ì'),
                        ('\\xc3\\x8d', 'Í'),
                        ('\\xc3\\x8e', 'Î'),
                        ('\\xc3\\x8f', 'Ï'),
                        ('\\xc3\\x90', 'Ð'),
                        ('\\xc3\\x91', 'Ñ'),
                        ('\\xc3\\x92', 'Ò'),
                        ('\\xc3\\x93', 'Ó'),
                        ('\\xc3\\x94', 'Ô'),
                        ('\\xc3\\x95', 'Õ'),
                        ('\\xc3\\x96', 'Ö'),
                        ('\\xc3\\x97', '×'),
                        ('\\xc3\\x98', 'Ø'),
                        ('\\xc3\\x99', 'Ù'),
                        ('\\xc3\\x9a', 'Ú'),
                        ('\\xc3\\x9b', 'Û'),
                        ('\\xc3\\x9c', 'Ü'),
                        ('\\xc3\\x9d', 'Ý'),
                        ('\\xc3\\x9e', 'Þ'),
                        ('\\xc3\\x9f', 'ß'),
                        ('\\xc3\\xa0', 'à'),
                        ('\\xc3\\xa1', 'á'),
                        ('\\xc3\\xa2', 'â'),
                        ('\\xc3\\xa3', 'ã'),
                        ('\\xc3\\xa4', 'ä'),
                        ('\\xc3\\xa5', 'å'),
                        ('\\xc3\\xa6', 'æ'),
                        ('\\xc3\\xa7', 'ç'),
                        ('\\xc3\\xa8', 'è'),
                        ('\\xc3\\xa9', 'é'),
                        ('\\xc3\\xaa', 'ê'),
                        ('\\xc3\\xab', 'ë'),
                        ('\\xc3\\xac', 'ì'),
                        ('\\xc3\\xad', 'í'),
                        ('\\xc3\\xae', 'î'),
                        ('\\xc3\\xaf', 'ï'),
                        ('\\xc3\\xb0', 'ð'),
                        ('\\xc3\\xb1', 'ñ'),
                        ('\\xc3\\xb2', 'ò'),
                        ('\\xc3\\xb3', 'ó'),
                        ('\\xc3\\xb4', 'ô'),
                        ('\\xc3\\xb5', 'õ'),
                        ('\\xc3\\xb6', 'ö'),
                        ('\\xc3\\xb7', '÷'),
                        ('\\xc3\\xb8', 'ø'),
                        ('\\xc3\\xb9', 'ù'),
                        ('\\xc3\\xba', 'ú'),
                        ('\\xc3\\xbb', 'û'),
                        ('\\xc3\\xbc', 'ü'),
                        ('\\xc3\\xbd', 'ý'),
                        ('\\xc3\\xbe', 'þ'),
                        ('\\xc3\\xbf', 'ÿ'),
                        ('\\xc4\\xb0', 'İ'),
                        ('\\xc4\\xb1', 'ı'),
                        ('\\xc4\\x83', 'ă'),
                        ('\\xc4\\x9f', 'ğ'),
                        ('\\xc4\\xab', 'ī'),
                        ('\\xc5\\x84', 'ń'),
                        ('\\xc5\\x93', 'œ'),
                        ('\\xc5\\x9e', 'Ş'),
                        ('\\xc5\\x9f', 'ş'),
                        ('\\xc5\\xab', 'ū'),
                        ('\\xc5\\xad', 'ŭ'),
                        ('\\xc5\\xb8', 'Ÿ'),
                        ('\\xc7\\x94', 'ǔ'),
                        ('\\xc7\\x99', 'Ǚ'),
                        ('\\xc7\\x9a', 'ǚ'),
                        ('\\xc8\\x8f', 'ô'),
                        ('\\xca\\xbc', "'"),  # modifier apostroph
                        ('\\xca\\xbe', "'"),  # ' modifier letter, right half ring
                        ('i\\xcc\\x87', 'İ'),
                        ('\\xcc\\x8b', '"'),  # combining double Acute Accent
                        ('\\xcc\\x8f', '"'),  # combining double Grave Accent
                        ('\\xce\\xaf', 'ί'),
                        ('\\xcf\\x8c', 'ό'),
                        ('\\xd1\\x97', ':'),
                        ('\\xd7\\x83', 'ï'),
                        ('\\x0c', ' '),  # Form Feed
                        ('\\x7f', ' '),  # Enter
                        ('\\t', ' '),    # tab
                        ("\\'", "'"),    # \' wird zu '
                        ("\\ ", " "),
                        ]
        for strange in strange_list:
            text2 = strangethings.replace(strange[0], strange[1])
            strangethings = text2
        # all whitespaces become only one blank
        text2 = re.sub(r"\s+", " ", text2)
        self.text = text2
        self.nodds = n_mistakes
        self.nchars = len(self.text)

    def set_fn_tag_and_lemma(self):
        """set path to filenames where lemma-frequency-distribution and
        tagged text will later be stored
        lemmafreq in csv-format, tagged text in json-format
        """
        root_tagg = sd.ResourceNames.dir_tagged
        myname = self.fn_in.split("/")[-1]
        short = myname.find(".")
        self.short = myname[:short]
        self.fn_tag = root_tagg+"tag__"+self.short+".csv"
        self.fn_freqlemma = root_tagg+"fl__"+self.short+".csv"

    def set_fn_corpus(self, corpus_name):
        """set filenames for results in corpus mode
        """
        self.fn_tag = sd.ResourceNames.dir_tagged + \
            corpus_name + "/tag__" + self.short + ".json"
        self.fn_freqlemma = sd.ResourceNames.dir_tagged + \
            corpus_name + "/fl__" + self.short + ".csv"


class FreqSimple:
    """frequency distribution of types
    """

    def __init__(self, blanktext):
        self.ntypes = None
        self.n_one = None
        self.pathname = None
        self.fileid = None
        self.freq = None
        self.blanktext = ""
        self.ntokens = None
        self.__make_simplefreq_fromtext__(blanktext)

    def __str__(self):
        return f"origin='{self.pathname}', fileid={self.fileid}, "\
                + f"Anzahl Types={self.ntypes}"

    def __repr__(self):
        return f"pathname='{self.pathname}', fileid={self.fileid}, " \
            + "ntypes={self.ntypes}\nask .blanktext for analysed words "\
            + "and .freq for the frequency distribution"

    def __f_dist__(self, blanktext):
        """returns frequency list from list of words,
            reverse-sorted by frequency"""
        fdist = FreqDist(blanktext.split())
        freq = sorted(fdist.items(), key=lambda x: x[1], reverse=True)
        return freq

    def __make_simplefreq_fromtext__(self, blanktext):
        """schreibt alles klein, zupft Akzente ab, entfernt Zeilenumbrüche,
        schmeißt Zeichensetzung und Leerzeichen raus
        liefert: simple_freq
        """
        # replace linebreaks and diacritics and lower
        cleaned1 = unidecode(blanktext.lower()).replace("\\n", " ")
        longpunctuation = '.´`\',;:!?"-()0123456789*+/<=>[\\]^_{|}~@$€«»#%&'
        for p in longpunctuation:
            cleaned2 = cleaned1.replace(p, " ")
            cleaned1 = cleaned2
        # reduce the new whitespaces
        self.blanktext = re.sub(r"\s+", " ", cleaned2)
        self.ntokens = len(self.blanktext.split())
        # frequency distribution
        self.freq = self.__f_dist__(self.blanktext)
        self.ntypes = len(self.freq)


class Collection:
    """collects types in PoS lists
    """

    def __init__(self, simple_freq_list):
        self.names = []
        self.advs = []
        self.pronouns = []
        self.nouns = []
        self.adjs = []
        self.verbs = []
        self.unk = dict(simple_freq_list)
        self.known = []

    def __str__(self):
        return f"names={len(self.names)}, adv={len(self.advs)}, "\
                + f"prn={len(self.pronouns)}, nouns={len(self.nouns)}, "\
                + f"adj={len(self.adjs)}, verbs={len(self.verbs)}, "\
                + f"unk={len(self.unk)}, known={len(self.known)}"

    def __repr__(self):
        return f"names={len(self.names)}, adv={len(self.advs)}, "\
                + f"prn={len(self.pronouns)}, nouns={len(self.nouns)}, "\
                + f"adj={len(self.adjs)}, verbs={len(self.verbs)}, "\
                + f"unk={len(self.unk)}, known={len(self.known)}"

    def put_known(self):
        """ returns a list of all types which found a lemma,
        sorted by lemma frequency
        """
        known = self.names \
            + self.pronouns \
            + self.nouns \
            + self.adjs \
            + self.verbs \
            + self.advs
        # print("in put_known:",  len(known))
        for i in known:
            # lemma,id,PoS,count,n-wordforms,found forms: count should be int
            # for debugging only
            if len(i) < 4:
                # print(i)
                known.remove(i)
        ########
        for i in known:
            if isinstance((i[3]), int) is False:
                print(f"{i[0]}, {i[3]} type of 'count': {type(i[3])}")
        # sort by count of lemma
        known.sort(key=lambda x: x[3], reverse=True)
        self.known = known

    def all_in(self):
        """returns a list of all types sorted by frequency of lemma
        or frequency of themselves if they didn't match a lemma
        """
        all_in = self.known+self.unk
        all_in.sort(key=lambda x: x[3], reverse=True)
        return all_in

    def collect_names(self, names):
        """collects names"""
        self.names, self.unk = dbc.collect_names(names, self.unk)

    def collect_adverbs(self, db_adverbs):
        """collects adverbs"""
        self.advs, self.unk = dbc.collect_adv_plus(db_adverbs, self.unk)

    def collect_pronouns(self, db_pronouns):
        """collects pronouns"""
        self.pronouns, self.unk = dbc.collect_pronouns(db_pronouns, self.unk)

    def collect_nouns(self, db_nouns):
        """collect nouns"""
        # attention: adds found nouns because we do it twice
        found_here, self.unk = dbc.collect_nouns(db_nouns, self.unk)
        self.nouns += found_here

    def collect_verbs(self, db_verbs):
        """collects verbs"""
        self.verbs, self.unk = kv.collect_verbs(db_verbs, self.unk)

    def collect_adjectives(self, db_adjectives):
        """collects adjectives"""
        self.adjs, self.unk = dbc.collect_adjs(db_adjectives, self.unk)

    def collect_exclamations(self, db_rest):
        """collects exclamations and put together with adverbs"""
        # attention: adds found exclamations because some are mapped to adverbs
        found_here, self.unk = dbc.collect_exclamations(db_rest, self.unk)
        self.advs += found_here
        self.adv = kv.put_alternatives_of_same_id_together(self.advs)


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
            if i[3] == 1:
                self.n_one += 1
            if i[2] == "UNK":
                self.n_unk += 1
            elif i[2] in ["ADJ", "ADV", "CONJ", "INTJ", "NI", "NOUN",
                          "PRON", "PREP", "VERB"]:
                self.n_lemma += 1
            elif i[2] == "F":
                self.n_extern += 1
            elif i[2][:5] == "PROPN":
                # PROPN, PROPN_CUR, PROPN_LOC, PROPN_NAM, PROPN_ORG,
                # PROPN_PER, PROPN_REL, PROPN_SCI, PROPN_THG, PROPN_VEG, ...
                self.n_ne += 1

    def __str__(self):
        return f"length of lemmafreq={self.length}, "\
                + f"found lemmata={self.n_lemma}, unknown to db={self.n_unk},"\
                + f" singletons= {self.n_one}, NamedEntities={self.n_ne}, "\
                + f"foreign words={self.n_extern}"

    def __repr__(self):
        return f"length={self.length}, n_lemma={self.n_lemma}, "\
                + f" n_unk={self.n_unk}, n_one= {self.n_one}, "\
                + f"n_ne={self.n_ne}, n_extern={self.n_extern}"


class Token:
    """a word in a text with its lemma and PoS-tag and
    its position in text and sentence
    """

    def __init__(self, token, pos="UNK", lemma=None):
        self.id_token = None
        self.id_char = None
        self.id_sentence = None
        self.id_tokin_sen = None
        self.id_para = None
        self.token = token
        self.pos = pos
        if not lemma:
            self.lemma = token
        else:
            self.lemma = lemma

    def __str__(self):
        return f"'{self.token}', PoS-tag={self.pos}, lemma='{self.lemma}', " \
                + f"id_token={self.id_token}"

    def __repr__(self):
        return f"Token ({self.token}/{self.pos}/{self.lemma},"\
                + f"\n\t\tchar={self.id_char}, token={self.id_token}, "\
                + f"sentence={self.id_sentence}, "\
                + f"word_in_sentence={self.id_tokin_sen}, "\
                + f"paragraph={self.id_para}"

    def set_nrs(self, isentence, iword_in_sentence, itoken, ichar, ipara):
        """stores position of the token"""
        self.id_sentence = isentence
        self.id_tokin_sen = iword_in_sentence
        self.id_token = itoken
        self.id_char = ichar
        self.id_para = ipara

    def get(self, tag_str="lemma"):
        """call the tags when not knowing before which one to call"""
        if tag_str == "token":
            return self.token
        if tag_str == "pos":
            return self.pos
        return self.lemma


class TokenMeta:
    """list of all tokens in a text
    """

    def __init__(self, tagged_list):
        self.tokens = tagged_list
        self.datetime = datetime.datetime.now()
        self.n_tokensbond = 0
        self.n_tokenscut = 0
        self.n_unk = 0
        self.percent_unk = None
        self.n_types = len({i.token for i in self.tokens})
        self.n_lemmata = len({i.lemma for i in self.tokens})
        self._count_tokens()

    def __str__(self):
        return f"Tokens={self.n_tokensbond} Tokens(cut)={self.n_tokenscut} "\
             + f"Types={self.n_types} Lemmata={self.n_lemmata}"

    def __repr__(self):
        return f"n_tokenscut={self.n_tokenscut} n_types={self.n_types} "\
             + f"n_lemmata={self.n_lemmata}"

    def _count_tokens(self):
        """counts tokens, cut_tokens, unknowns
        """
        bond, cut, unk = 0, 0, 0
        for i, tok in enumerate(self.tokens[1:], 1):
            if tok.id_token != self.tokens[i-1].id_token:
                bond += 1
            if tok.pos != "SYMBOL":
                cut += 1
        self.n_tokensbond = bond
        self.n_tokenscut = cut
        for i in self.tokens:
            unk += 1
        self.n_unk = unk

    def lemmasoup(self):
        """replaces tokens in the text by its lemma if known,
        marks unknown types with '?'
        (skips SYMBOL)
        """
        lemmasoup = ""
        for i in self.tokens:
            if i.pos == "UNK":
                lemmasoup += "?"+i.lemma+" "
            elif i.pos == "SYMBOL":
                if i.lemma in sd.replaced_symbols.keys():
                    lemmasoup += sd.replaced_symbols.get(i)+" "
            else:
                lemmasoup += i.lemma+" "
        return lemmasoup.strip()

    def tokensoup(self):
        """deletes tokens with PoS 'SYMBOL'
        """
        tokensoup = ""
        for i in self.tokens:
            if i.pos != "SYMBOL":
                tokensoup += i.token+" "
        return tokensoup.strip()

    def possoup(self):
        """replaces tokens in an text by its PoS-tag if known
        """
        possoup = ""
        for i in self.tokens:
            possoup += i.pos+" "
        return possoup.strip()

    def remake_text(self):
        """makes out of json the text again
        """
        text = self.tokens[0].token
        for i, tok in enumerate(self.tokens[1:], 1):
            # end of line
            if tok.id_para > self.tokens[i-1].id_para:
                text += "\n" + tok.token
            # put tokens with apostrophe in it together again
            elif self.tokens[i-1].id_tokin_sen == tok.id_tokin_sen:
                text += tok.token
            else:
                text += " " + tok.token
        return text
