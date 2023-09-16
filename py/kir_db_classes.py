#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  6 23:43:14 2023

@author: doreen nixdorf
"""

import csv
import re
from unidecode import unidecode
import kir_prepare_verbs as kv
import kir_string_depot as sd
import kir_helper2 as kh


def load_dbkirundi():
    """returns lists sorted more or less by part of speech:
    verbs, nouns, adjectives, pronouns,
    (prepositions, adverbs, conjunctions and interjections) together,
    (prefixes and phrases) together, all stems
    """
    verbs = []
    nouns = []
    adjectivs = []
    pronouns = []
    unchanging_words = []
    rests = []
    stems = []
    stems = set(stems)
    with open(sd.ResourceNames.fn_db, encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=";")
        line_count = 0
        for row in csv_reader:
            # attention: column numbers still valid?
            # first row is column names
            if line_count > 0:
                if row[8] == "0":
                    if row[13] and row[15]:
                        # there is also an alternative spelling
                        row_a = kv.prepare_verb_alternativ(row)
                        verb = kv.Verb(row_a)
                        verbs.append(verb)
                        row[0] = str(row[0]) + "_0"  # 0 id
                        row[13] = ""                  # alternatives
                    verb = kv.Verb(row)
                    verbs.append(verb)
                elif row[8] == "1":
                    nouns.append(Noun(row))
                elif row[8] == "2":
                    adjectivs.append(Adjectiv(row))
                elif row[8] == "5":
                    pronouns.append(Pronoun(row))
                # prepositions, adverbs, conjunctions, interjections
                elif row[8] == "3" or row[8] == "6" or row[8] == "7" \
                        or row[8] == "8":
                    unchanging_words.append(kv.Lemma(row))
                # prefixes, phrases
                else:
                    rests.append(kv.Lemma(row))
                # stems as set
                stems.add(unidecode(row[4]).lower())
            line_count += 1
    kh.OBSERVER.notify(
        kh._('{} entries of the dictionary prepared.').format(line_count))
    csv_file.close()
    verbs = kv.filter_proverbs_out(verbs)
    verbs = kv.filter_passiv_out(verbs)
    stems = list(stems)
    return (verbs, nouns, adjectivs, pronouns, unchanging_words, rests, stems)


def load_ne():
    """reads file Named Entites and foreign words
    returns list of objects"""
    namedentities = []
    loc = []
    per = []
    lng = []
    foreign = []
    with open(sd.ResourceNames.fn_namedentities, encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=";")
        for row in csv_reader:
            if row[2] == "F":
                foreign.append(Foreign(row))
            elif row[2] == "PROPN_LOC":
                loc.append(NamedEntities(row))
            elif row[2] == "PROPN_PER":
                per.append(NamedEntities(row))
            elif row[2] == "PROPN_LNG":
                lng.append(NamedEntities(row))
            else:
                enti = NamedEntities(row)
                enti.questions = enti.alternatives
                namedentities.append(enti)
    csv_file.close()
    # build and sort more locations, languages, persons
    for i in loc:
        if i.alternatives[0][:3] == "ubu":
            i.alternatives.pop(0)
    check_entries_location_person_language(lng, per)
    check_entries_location_person_language(loc, lng, "lang")
    check_entries_location_person_language(loc, per)

    # set questions for existing language entries
    for i in lng:
        i.set_languages()
        i.questions = i.lang
        del i.row
    # set questions for existing person entries
    for i in per:
        i.set_persons()
        i.questions = i.persons
        del i.row
    # set questions for location entries and
    # make language and person entries if doesn't exist yet
    set_person_language_out_of_location(loc, per, lng)
    for i in loc:
        del i.row
    # TODO check if first line is head or entry
    return namedentities+foreign+lng+loc+per


class Foreign:
    """sets PoS and question for string-search
    """

    def __init__(self, row):
        columns = [0,  # entry0-lemma
                   2]  # entry1-PoS
        entry = [unidecode(row[x].strip().lower()) for x in columns]
        self.lemma = entry[0].strip()
        self.dbid = ""
        self.pos = entry[1].strip().upper()
        self.questions = [self.lemma,]

    def __str__(self):
        return f"lemma= {self.lemma}, PoS={self.pos}"

    def __repr__(self):
        return f"lemma= {self.lemma}, PoS={self.pos}"


class NamedEntities:
    """sets PoS, alternative spellings and
    questions for string-search
    """

    def __init__(self, row):
        columns = [0,  # entry0-lemma
                   2,  # entry1-PoS
                   4]  # entry2-alternatives
        entry = [unidecode(row[x].strip().lower()) for x in columns]
        self.row = row
        self.dbid = ""
        self.lemma = entry[0].strip()
        self.pos = entry[1].strip().upper()
        if entry[2]:
            self.alternatives = [i.strip() for i in entry[2].split(";")]
        else:
            self.alternatives = []
        self.alternatives.insert(0, self.lemma)
        self.persons = []
        self.lang = []
        self.questions = []

    def __str__(self):
        return f"lemma= {self.lemma},  "\
             + f"alternatives= {self.alternatives}, PoS={self.pos}, "\
             + f"lang={self.lang}, persons={self.persons}, "\
             + f"questions={self.questions}"

    def __repr__(self):
        return f"lemma={self.lemma}, alternatives={self.alternatives}, "\
              + f"PoS= {self.pos}, lang='{self.lang}', "\
              + f"persons={self.persons}, questions={self.questions}"

    def set_persons(self):
        """set regex for persons
        """
        # if self.lemma[:5] == "umuny" :
        #     for alt in self.alternatives:
        #         self.persons += [r"umuny[ae]"+alt,r"abany[ae]"+alt]
        if self.lemma[:3] == "umw":
            for alt in self.alternatives:
                self.persons += ["umw"+alt, "ab"+alt,
                                 "umuny"+alt, "abany"+alt]
        elif self.lemma[:3] == "umu":
            for alt in self.alternatives:
                self.persons += [r"umu(ny[ae])?"+alt, r"aba(ny[ae])?"+alt]
        for i in self.persons:
            self.questions += [
                r"^"+sd.NounPrepositions.qu_nta+"?"+i[1:]+"(kazi)?$",
                r"^"+sd.NounPrepositions.qu_ca_vowel+"?"+i+"(kazi)?$"
                ]

    def set_languages(self):
        """set regex for languages
        """
        if self.lemma[:5] == "ikiny":
            for i in self.alternatives:
                self.lang.append("ikiny"+i)
        elif self.lemma[:3] == "iki":
            for i in self.alternatives:
                self.lang.append("iki"+i)
        elif self.lemma[:3] == "igi":
            for i in self.alternatives:
                self.lang.append("igi"+i)
        if self.lemma[:2] == "ic":
            for i in self.alternatives:
                self.lang.append("ic"+i)
        for i in self.lang:
            self.questions += [r"^"+i+"$", r"^"+i[1:]+"$"]


def check_entries_location_person_language(
        propn_list1, propn_list2, lang_or_per="per"):
    """check if there are extra entries for location, person, language,
    if so, we put together all alternativ spellings
    """
    for propn1 in propn_list1:
        done = False
        set1 = set(propn1.alternatives)
        for propn2 in propn_list2:
            set2 = set(propn2.alternatives)
            if set1.intersection(set2):
                propn2.alternatives = set(
                    propn2.alternatives+propn1.alternatives)
                propn1.alternatives = set(
                    propn2.alternatives+propn1.alternatives)
                done = True
                break
            if propn1.lemma[:3] == "ubu" \
                    and propn1.lemma[3:] == \
                    propn2.lemma[3:][-(len(propn1.lemma)-3):]:
                done = True
                break
        if done:
            if lang_or_per == "lang":
                propn1.lang = "done"
            else:
                propn1.persons = "done"


def set_person_language_out_of_location(loc, per, lng):
    """appends not yet existing entries to PROPN_PER and PROPN_LANG lists
    based on PROPN_LOC
    """
    for i in loc:
        # only countries which start with ubu need ubu also in their variants
        if i.lemma[:3] == "ubu":
            for location in i.alternatives:
                i.questions += [
                    r"^"+sd.NounPrepositions.qu_nta+"?bu"+location+"$",
                    r"^"+sd.NounPrepositions.qu_ca_vowel+"?ubu"+location+"$"
                    ]
                if sd.sortletter(i.lemma[4]) == "weak_consonant":
                    langname = "iki"+i.lemma[3:]
                elif sd.sortletter(i.lemma[4]) == "hard_consonant":
                    langname = "igi"+i.lemma[3:]
                # add alternative forms without ubu
                i.questions += [
                    r"^"+sd.NounPrepositions.qu_nta+"?"+location+"$",
                    r"^"+sd.NounPrepositions.qu_ca_konsonant+"?"+location+"$"
                    ]
                pername = "umu"+i.lemma[3:]
        elif i.lemma[:3] in "ubw":
            for location in i.alternatives:
                i.questions += [
                    r"^"+sd.NounPrepositions.qu_nta+"?bw"+location+"$",
                    r"^"+sd.NounPrepositions.qu_ca_vowel+"?ubw"+location+"$"
                    ]
                langname = "ic"+i.lemma[3:]
                pername = "umw"+i.lemma[3:]
        # locations without ubu/ubw
        else:
            langname = "ikinya_"+i.lemma
            pername = "umunya_"+i.lemma
            # location name starts with vowel
            if sd.sortletter(i.lemma[0]) == "vowel":
                for location in i.alternatives:
                    i.questions += [
                        r"^"+sd.NounPrepositions.qu_nta+"?"+location+"$",
                        r"^"+sd.NounPrepositions.qu_ca_vowel+"?"+location+"$"
                        ]
            # location name starts with consonant
            else:
                for location in i.alternatives:
                    i.questions += [
                        r"^"+sd.NounPrepositions.qu_nta+"?"+location+"$",
                        r"^"+sd.NounPrepositions.qu_ca_konsonant+"?"+location+"$"
                        ]

        if i.lang != "done":
            i.row[0] = langname
            new = NamedEntities(i.row)
            new.pos = "PROPN_LNG"
            new.alternatives = i.alternatives
            new.set_languages()
            if new.lang:
                new.questions = new.lang
                lng.append(new)

        if i.persons != "done":
            i.row[0] = pername
            new = NamedEntities(i.row)
            new.pos = "PROPN_PER"
            new.alternatives = i.alternatives
            new.set_persons()
            if new.questions:
                per.append(new)


class Noun(kv.Lemma):
    """sets db-ID, lemma, stem, PoS, singular, plural, alternative spellings
    and questions for regex-search
    """

    def __init__(self, row):
        super().__init__(row)
        self.questions = []
        self.coll = []
        self._set_questions(row)

    def __str__(self):
        return f"lemma={self.lemma}, ID={self.dbid}, POS= {self.pos}, "\
               + f"all variants={self.coll}, "\
               + f"questions: {len(self.questions)}"

    def __repr__(self):
        return f"lemma={self.lemma}, dbid={self.dbid}, POS= {self.pos}, "\
                   + f"coll={self.coll}, "\
                   + f"len(questions)={len(self.questions)}"

    def _possibilities(self, variant):
        """more variants if nouns are written inclusive prepositions without
        apostrophe
        """
        # noun starts with vowel
        if variant[0] in "aeiuu":
            qu_0 = r"^"+sd.NounPrepositions().qu_nta+"?"+variant[1:]+"$"
            qu_1 = r"^"+sd.NounPrepositions().qu_ca_vowel+"?"+variant+"$"
        # noun starts with consonant
        else:
            qu_0 = r"^"+sd.NounPrepositions().qu_nta+"?"+variant+"$"
            qu_1 = r"^"+sd.NounPrepositions().qu_ca_konsonant+variant+"$"
        return [qu_0, qu_1]

    def _set_questions(self, row):
        """takes row from dbkirundi
        sets singular, plural with and without augment and also for
        spelling variations
        """
        columns = [3,   # entry0-prefix_sg
                   7,   # entry1-prefix_pl
                   14,  # entry2-alternative prefix_sg
                   21]  # entry3-plural irregular
        entry = [unidecode(row[x]).strip().lower() for x in columns]
        # add plural
        # plural is irregular (amaso)
        if entry[3]:
            coll = [self.lemma, entry[3]]
        # there is plural and it's different from singular
        elif entry[1] not in ("", entry[0]):
            coll = [self.lemma, sd.breakdown_consonants(entry[1]+self.stem)]
        # there is no plural
        else:
            coll = [self.lemma, ]
        # add alternatives
        # there is at least one alternativ
        if self.alternatives:
            for i in self.alternatives:
                coll.append(i)
                # add plural of alternativ
                # begin of alternativ is same like sg-prefix of lemma
                if entry[0] == "" or i[:(len(entry[2]))] == entry[0]:
                    # use plural-prefix for alternativ
                    coll.append(
                        sd.breakdown_consonants(entry[1]+i[len(entry[0]):]))
        for i in coll:
            self.questions += self._possibilities(i)
        self.coll = coll


def collect_nouns(db_substantive, freq_d, before_verbs=False):
    """maps nouns to lemmata in dbkirundi
    takes frequency-dictionary and list of nouns
    returns list with columns:
                lemma, id, PoS, sum of frequency of all forms, counted forms,
                all forms found ([form, frequency] per column)
            and changed frequency-dictionary {'found_noun':0}
    """
    # freqSubs = {str(n[0]):n[1] for n in freq_d[:29290]}
    freq_subs = {x: y for x, y in freq_d.items() if y != 0}
    collection = []
    subs_ukg = []
    points = int(len(db_substantive)/50)
    lemma_count = 0
    for noun in db_substantive:
        # collect nouns that could be verbs, inspect them after verbs
        if before_verbs is True \
           and noun.lemma[:2] in ["uk", "ug"] \
           and noun.lemma[-1] == "a":
            subs_ukg.append(noun)
            # skip to next lemma
            continue
        found = regex_search(noun, freq_subs)
        if found:
            collection.append(found)
        if before_verbs is True:
            # progress bar ;-)
            lemma_count += 1
            if lemma_count % points == 0:
                print('.', end="")

    if collection:
        # result: first most wordforms, with high freq first
        collection.sort(key=lambda x: x[3], reverse=True)
        collection.sort(key=lambda x: x[4], reverse=True)

    # if before_verbs == True :
    #     # Wörter, die zum Wörterbuch gemappt wurden sind 0
    #     save_dict(freq_subs,"keine4_subst.csv")
    #     # Wörter, die im Korpus vorkommen
    #     kh.save_list(collection,"found4_subst.csv",";")
    #     # Dictionary-Einträge, fdist ausgedünnt, später zu untersuchende Substantive
    # else :
    #     save_dict(freq_subs,"keine7_subst.csv")
    #     kh.save_list(collection,"found7_subst.csv",";")
    return (collection, freq_subs, subs_ukg)


class Adjectiv(kv.Lemma):
    """sets db-ID, lemma, stem, PoS, alternative spellings and
    questions for regex-search
    """

    def __init__(self, row):
        super().__init__(row)
        self.coll = [self.stem,]
        self.questions = []
        if self.alternatives:
            for i in self.alternatives:
                self.coll.append(i.strip("-"))
        # add prefix-regex depending on first letter of stem of variant
        self.set_qu(self.coll)

    def __str__(self):
        return f"lemma={self.lemma}, ID={self.dbid}, POS= {self.pos}, "\
               + f"stem={self.stem}, alternatives={self.alternatives}, "\
               + f"all variants {self.coll}: {len(self.questions)}"

    def __repr__(self):
        return f"lemma={self.lemma}, dbid={self.dbid}, POS= {self.pos}, "\
               + f"stem={self.stem}, alternatives={self.alternatives}, "\
               + f"coll={self.coll}, len(questions)={len(self.questions)}"

    def set_qu(self, coll):
        """sets regex-questions for fishing adjectivs out of
        requency distribution
        """
        # prefixes1 = ["ba","ka","ma","ha","aya",
        #              "bi","ki","mi","ri","yi","zi",\
        #              "bu","ku","mu","ru","tu","uyu","uwu","n"]
        pre_kgregex = r"^((a?[bgkmhy]?a)|(i?[bgkmryz]?i)|(u?[bgkmrdtwy]?u)|[mn])(%s)$"
        # prefixes2 = ["bw","kw","mw","rw","tw","ny","ry","vy","y","n","z",\
        #                b","k","c","h"]
        pre_aregex = r"^((u?[bkmrt]?w)|(i?[nrv]?y)|a?[bkh]|i?[cz]|n)(%s)$"
        # prefixes4 = ["b","k","c","h","z","y","ry","vy","nz"\
        #        "bw","kw","mwo","mwe",rwo","rwe","two","twe"]
        pre_oregex = r"^(((u?[bkmrt]?w)[oe])|((i?[rv]?y|nz|a?[bkh]|i?[cz])o))(%s)$"
        #prefixes3 = [be,ke,me,he, bwi,kwi,mwi,rwi,twi, myi,nyi,vyi,nzi,bi,ci]
        pre_iregex = r"^((a?[bkmh]e)|(u?[bkmrt]?w[i]+)|(i?[mnrv]?yi|n?zi|[bc]i))(%s)$"

        # aba aka aya aha ibi iki iyi iri izi ubu uku uwu uru utu
        #     aga       ivy igi ic ny iry  nz ubw ugu ukw  urw udu utw
        #  be  ke ma me he         y mi my n m        mu mw w  twe
        #  bo  ko   yo  ho  vyo co      ryo  zo  bwo kwo wo rwo two
        # i- n- nk- ni-o  -ari-o -a-o i-ya nta-o na-o
        for variant in coll:
            teil = variant.split("-")
            if variant[0] == "a":
                quest = pre_aregex % (teil[0])
            elif variant[0] == "i":
                quest = pre_iregex % (teil[0][1:])
            elif variant[0] == "o":
                quest = pre_oregex % (teil[0][1:])
            else:
                quest = pre_kgregex % (teil[0])
            # ??? to do: what about ki-co ...
            # in case it's an adjective with two hyphen (e.g. -re-re)
            if len(teil) == 2:
                if teil[1][0] == "a":
                    quest = quest[:-1]+pre_aregex[1:] % (teil[1])
                elif teil[1][0] == "o":
                    quest = quest[:-1]+pre_oregex[1:] % (teil[1])
                else:
                    quest = quest[:-1]+pre_kgregex[1:] % (teil[1])
            self.questions.append(quest)


def collect_adjs(db_adjektive, freq_d):
    """maps adjectivs to lemmata in dbkirundi
    takes frequency-dictionary and list of adjectives
    returns list with columns:
                lemma, id, PoS, sum of frequency of all forms, counted forms,
                all forms found ([form, frequency] per column)
            and changed frequency-dictionary {'found_adjectiv':0}
    """
    collection = []
    # kommt freq als liste oder dict? (vorher sammle_subst?)
    # freqText = {freq[x][0]:freq[x][1] for x in freq if freqfreq[x][1] != 0}
    freq_adj = {x: y for x, y in freq_d.items() if y != 0}
    for adj in db_adjektive:
        found = regex_search(adj, freq_adj)
        if found:
            collection.append(found)
    collection.sort(key=lambda x: x[3], reverse=True)
    collection.sort(key=lambda x: x[4], reverse=True)

    # mapped types now have 0 in simplefreq
    # save_dict(freq_adj,"keine5_adj.csv")
    # all adjectives
    # kh.save_list(collection,"found5_adj.csv",";")
    return (collection, freq_adj)


class Pronoun(kv.Lemma):
    """sets db-ID, lemma, stem, PoS, alternative spellings and
    questions for string-search
    """

    def __init__(self, row):
        super().__init__(row)
        if self.alternatives:
            for i in self.alternatives:
                self.questions.append(i.strip())

    def __str__(self):
        return f"lemma= {self.lemma}, ID={ self.dbid}, stem={self.stem}, "\
                + f"alternatives= {self.alternatives}, PoS={self.pos}, "\
                + f"questions={self.questions}"

    def __repr__(self):
        return f"lemma={self.lemma}, dbid={self.dbid}, stem={self.stem}, "\
                + f"alternatives={self.alternatives}, PoS= {self.pos} "\
                + f"questions={self.questions}"


def collect_pronouns(db_pronouns, freq_d):
    """maps pronouns to lemmata of db and also builds other combinations
    takes frequency-dictionary and list of pronouns
    returns list with columns:
                lemma, id, PoS, sum of frequency of all forms, counted forms,
                all forms found ([form, frequency] per column)
            and changed frequency-dictionary {'found_pronouns':0}
    """
    collection = []
    freq_prn = {x: y for x, y in freq_d.items() if y != 0}

    regex_prn_c_a = r"(([bkrt]w|[rv]?y|[bchkwz]))"
    regex_prn_c_o = r"([bkrt]?w|[rv]?y|[bchkz])"
    regex_prn_ic_o = r"(a[bhky]|i([cz]|([rv]?)y)|u(([bkrt]?w?)|y))"
    regex_prn_gi = r"([bghm]a|[bgmirz]i|n|[bdgmr]u)"
    regex_prn_i_ki = r"((a?[bhk]a|i?[bkrz]i|u?[bkrt]u)|[aiu])"
    regex_prn_kiw = r"(([bhky]a|[bkryz]i|[bkrtw]u))"
    regex_prn_poss = r"((u|kub)|("+regex_prn_ic_o+"|"+regex_prn_c_o+")?i)w"
    regex_prn_igki = r"(a[bhgkmy]a|i(v?y|[bgkmrz])i|u[bgkmrdtwy]u)"
    regex_prn_je = r"(([jw]|[mt]w)e)"

    # lemma, question, marker if regex needs Variable,
    #                                 db_id (or new id given here), -lemma-
    prns_made_here = [  # one lemma, one question
            [["nk-o",], [r"nk"+regex_prn_ic_o+"o",], 0, 3281, ""],
            [["-rtyo",], [regex_prn_gi+r"(r?tyo)",], 0, 7145, ""],
            [["-a-o",], [regex_prn_c_a+"a"+regex_prn_c_o+"o", ], 0, 40000, ""],
            [["_-o",], [regex_prn_ic_o+"o?",], 0, 40001, ""],
            [["-a",], [regex_prn_c_a+"a?",], 0, 7778, ""],
            [["-o",], [regex_prn_c_o+"o?",], 0, 40002, ""],
            [["n_",], [r"((n[ai]t?we)|n)",], 0, 40003, ""],
            # list of lemmata, list of questions
            [["anje", "awe", "iwe", "acu", "anyu", "abo"],
                [r"^" + regex_prn_poss + "%s$",
                 r"^" + regex_prn_c_o + "%s$"],
                1, [112, 174, 2326, 7490, 133, 8098], "-x"],
            # list of lemmata, one question
            [["ni", "nki", "na", "nka", "nta", "atari", "ari",
              "ukwa", "si", "hari"],
                [r"^%s" + regex_prn_c_o + "o?$",],
                1,
                [40004, 40005, 40005, 40007, 40008, 40009, 40010, 40011,
                 40012, 40013],
                "x-"
             ],
            [["riya", "rya", "ryo", "no"],
                [r"^"+regex_prn_i_ki+"%s$"],
                1, [7320, 6510, 40014, 1458], "-x"],
            # one lemma, list of questions
            [["-ari-o",],
                ["uwariwo", "iyariyo", "iryariryo", "ayariyo", "icarico",
                 "ivyarivyo", "izarizo", "urwarirwo", "akariko", "utwaritwo",
                 "ubwaribwo", "ukwarikwo", "ihariho"],
                0, 40015, ""
             ],
            [["-o-o",],
                ["wowo", "bobo", "yoyo", "ryoryo", "coco", "vyovyo", "zozo",
                 "rworwo", "koko", "twotwo", "bwobwo", "kwokwo", "hoho"],
                0, 40016, ""],
            [["nyene",],
                [r"^(na)?("+regex_prn_je+"|"+regex_prn_c_o+"o)%s$",
                 r"^%s"+regex_prn_c_o+"o$",
                 r"^"+regex_prn_ic_o+"o%s$",
                 r"^"+regex_prn_igki+"%s$",
                 ],
                1, [3402,], "-x"],
            [["ndi",],
                [r"^([an]ta|[km]u|nka)"+regex_prn_kiw+"%s$",
                 r"^n?"+regex_prn_igki+"%s$",
                 r"^wawu%s$", r"^a?baba%s$", r"^yiyi%s$", r"^ryari%s$",
                 r"^yaya%s$", r"^caki%s$", r"^vyabi%s$", r"^zazi%s$",
                 r"^kaka%s$", r"^twatu%s$", r"^rwaru%s$", r"^bwabu%s$",
                 r"^kwaku%s$", r"^haha%s$",
                 ],
                1, [3218,], "-x"]
            ]
    for quest in prns_made_here:
        # list of lemma
        for i in range(len(quest[0])):
            freqsum = 0
            found = []
            # set lemma
            if quest[4] == "-x":
                qu4 = "-"+quest[0][i]
            elif quest[4] == "x-":
                qu4 = quest[0][i]+"-"
            else:
                qu4 = quest[0][i]
            # set list of questions
            for qu1 in quest[1]:
                if quest[2] == 0:
                    question = r"^"+qu1+"$"
                    qu3 = quest[3]
                elif quest[2] == 1:
                    question = qu1 % quest[0][i]
                    qu3 = quest[3][i]
                # search
                for freqs, num in freq_prn.items():
                    if num != 0 and re.search(question, freqs) is not None:
                        freqsum += num
                        found.append([freqs, num])
                        freq_prn.update({freqs: 0})
                        continue  # next qu1
            if freqsum > 0:
                found.sort()
                found = [qu4, qu3, "PRON", freqsum, len(found)] + found
                collection.append(found)

    # for all other pronouns we didn't made here
    for lemma in db_pronouns:
        found = string_search(lemma, freq_prn)
        if found:
            collection.append(found)
    # put same IDs together
    collection.sort(key=lambda x: int(x[1]))
    coll = []
    run_next = True
    for i in range(1, len(collection)):
        if run_next is True:
            if int(collection[i][1]) == int(collection[i-1][1]):
                collection[i][3] += collection[i-1][3]
                collection[i][4] += collection[i-1][4]
                coll.append(collection[i]+collection[i-1][5:])
                run_next = False
            else:
                coll.append(collection[i])
        else:
            # skip only one
            run_next = True
    coll.sort(key=lambda x: x[3], reverse=True)
    coll.sort(key=lambda x: x[4], reverse=True)
    # # Wörter, die zum Wörterbuch gemappt wurden, sind jetzt auf 0
    # save_dict(freq_prn,"keine3_pron.csv")
    # # Wörter, die im Korpus vorkommen
    # kh.save_list(collection,"found3_pron.csv",";")
    return (coll, freq_prn)


def filter_names_out(names_and_foreign_words, freq_list):
    """maps named entities and foreign words
    takes frequency-list and NE-object list
    returns list with columns:
                lemma, id, frequency, counted form =1,
                [form, frequency]
            and a frequency-dictionary {'found_word':0}
    """
    collection = []
    freq_names = dict(freq_list)
    points = int(len(names_and_foreign_words)/50)
    lemma_count = 0
    for name in names_and_foreign_words:
        if name.pos in ["PROPN_PER", "PROPN_LOC"]:
            found = regex_search(name, freq_names)
        else:
            found = string_search(name, freq_names)
        if found:
            collection.append(found)
        lemma_count += 1
        # progress bar
        if lemma_count % points == 0:
            print('.', end="")
    collection.sort(key=lambda x: x[3], reverse=True)
    return (collection, freq_names)


def collect_adv_plus(db_advplus, freq_d):
    """maps prepositions, adverbs, conjunctions and interjections to lemma in db
    takes frequency-dictionary and list of lemmata
    returns list with columns:
                lemma, id, sum of frequency of all forms, counted forms,
                all forms found ([form, frequency] per column)
            and a frequency-dictionary {'found_word':0}
    """
    collection = []
    freq_unchangable = {x: y for x, y in freq_d.items() if y != 0}
    for lemma in db_advplus:
        found = string_search(lemma, freq_unchangable)
        if found:
            collection.append(found)
    collection.sort(key=lambda x: x[3], reverse=True)
    # # Wörter, die zum Wörterbuch gemappt wurden, sind jetzt auf 0
    # save_dict(freq_unchangable,"keine2_div.csv")
    # # Wörter, die im Korpus vorkommen
    # kh.save_list(collection,"found2_div.csv",";")

    return (collection, freq_unchangable)


# #TODO
# class Exclamations:
#     def __init__(self, row):
#         super().__init__(row)
#         if self.alternatives:
#             for i in self.alternatives:
#                 self.questions.append(i.strip())
#     def __str__(self):
#         return f"lemma={self.lemma}, ID={self.dbid}, "\
#                +f"alternatives={self.alternatives}, "\
#                #+f"all alternatives {self.coll}: {self.questions}"
#     def __repr__(self):
#         return f"lemma={self.lemma}, dbid={self.dbid}, "\
#                    +f"alternatives={self.alternatives}, "\
#                    +f"coll={self.coll}, len(questions)={len(self.questions)}"


def collect_exclamations(db_rest, freq_d):
    """maps exclamations to a list of regex made here and all the rest
    of entries in the db
    takes frequency-dictionary and list of lemmata
    returns list with columns:
                lemma, id, sum of frequency of all forms, counted forms,
                all forms found ([form, frequency] per column)
            and a frequency-dictionary {'found_word':0}
    """
    collection = []
    freq_exc = {x: y for x, y in freq_d.items() if y != 0}
    regex_exc_ego = r"^(y?e+go+|e+h?|y?ee+)$"
    regex_exc_oya = r"^(oya+)$"
    regex_exc_ha = r"^(ha)+$"
    regex_exc_la = r"^(la)+$"
    regex_exc_ah = r"^([au]+h|aa+|y?uu+|ah[ao]+|hu+)$"
    regex_exc_yo = r"^(y?o+h?|o+ho+|oh+)$"
    regex_exc_mh = r"^(m+h+|hu+m+|hm+|mm+|uu+m)$"
    regex_exc_he = r"^(e?he+)$"
    regex_exc_kye = r"^(kye+)+$"
    regex_exc_luya = r"^(h?al+e+l+u+[iy]a+)$"
    # exclamations not in the original db get IDs from 30000
    ecxl_made_here = [["ego", regex_exc_ego, 818],  # db_id
                      ["oya", regex_exc_oya, 3556],
                      ["ha", regex_exc_ha, 30000],
                      ["la", regex_exc_la, 30001],
                      ["aah", regex_exc_ah, 30002],
                      ["ooh", regex_exc_yo, 30003],
                      ["mh", regex_exc_mh, 30004],
                      ["hee", regex_exc_he, 30005],
                      ["kyee", regex_exc_kye, 30006],
                      ["alleluia", regex_exc_luya, 30007],
                      ]
    for excl in ecxl_made_here:
        freqsum = 0
        found = []
        db_id = excl[2]
        for freqs, num in freq_exc.items():
            if num != 0 and re.search(excl[1], freqs) is not None:
                freqsum += num
                found.append([freqs, num])
                freq_exc.update({freqs: 0})
                continue  # next qu1
        if freqsum > 0:
            found.sort()
            found = [excl[0], db_id, "INTJ", freqsum, len(found)] + found
            collection.append(found)

    # for all exclamation we didn't made here and the rest of db_dict
    for lemma in db_rest:
        freqsum = 0
        found = []
        for variant in lemma.alternatives:
            variant = variant.strip("-")
            for freqs, num in freq_exc.items():
                if num != 0 and variant == freqs:
                    freqsum += num
                    found.append([freqs, num])
                    freq_exc.update({freqs: 0})
        if freqsum > 0:
            found.sort()
            # entry, id, PoS, frequency lemma, number of variants,
            #   list(variante, frequency)
            found = [lemma.lemma, lemma.dbid, "INTJ", freqsum,
                     len(found)] + found
            collection.append(found)
            freq_exc.update({freqs: 0})

    collection.sort(key=lambda x: x[3], reverse=True)
    collection.sort(key=lambda x: x[4], reverse=True)
    # # Wörter, die zum Wörterbuch gemappt wurden, sind jetzt auf 0
    # save_dict(freq_exc,"keine8_excl_div2.csv")
    # # Wörter, die im Korpus vorkommen
    # kh.save_list(collection,"found8_excl_div2.csv",";")
    return (collection, freq_exc)


def regex_search(word, freq_dict):
    """compares type to regex of lemma
    """
    freqsum = 0
    found = []
    for quest in word.questions:
        for freqtype, num in freq_dict.items():
            if num != 0 and re.search(quest, freqtype) is not None:
                freqsum += num
                found.append([freqtype, num])
                freq_dict.update({freqtype: 0})
    if freqsum > 0:
        found.sort()
        # lemma,id,PoS,Summe, different forms, all[form alphabetical,frequency]
        found = [word.lemma, word.dbid, word.pos, freqsum, len(found)] + found
    return found


def string_search(word, freq_dict):
    """compares type to string of lemma
    """
    freqsum = 0
    found = []
    for quest in word.questions:
        for freqtype, num in freq_dict.items():
            if num != 0 and quest == freqtype:
                freqsum += num
                found.append([freqtype, num])
                freq_dict.update({freqtype: 0})
    if freqsum > 0:
        found.sort()
        # lemma,id,PoS,Summe, different forms, all[form alphabetical,frequency]
        found = [word.lemma, word.dbid, word.pos, freqsum, len(found)] + found
    return found
