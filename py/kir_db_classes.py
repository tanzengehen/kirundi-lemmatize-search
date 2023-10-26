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
                        row[13] = ""                 # alternatives
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
    # kh.OBSERVER.notify(
    #     kh._('{} entries of the dictionary prepared.\n').format(line_count))
    csv_file.close()
    verbs = kv.filter_proverbs_out(verbs)
    verbs = kv.filter_passiv_out(verbs)
    nouns_one, nouns_two = noun_partition(nouns)
    stems = list(stems)
    dbrundi = {"verbs": verbs,
               "nouns1": nouns_one,
               "nouns2": nouns_two,
               "adjectives": adjectivs,
               "pronouns": pronouns,
               "unchanging_words": unchanging_words,
               "rests": rests,
               "stems": stems}
    return dbrundi


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
        # only countries with a name that starts with ubu
        #   need ubu also in their variants
        if i.lemma[:3] == "ubu":
            for location in i.alternatives:
                i.questions += [
                    r"^"+sd.NounPrepositions.qu_nta+"?bu"+location+"$",
                    r"^"+sd.NounPrepositions.qu_ca_vowel+"?ubu"+location+"$"
                    ]
                # if sd.sortletter(i.lemma[4]) == "weak_consonant":
                if i.lemma[4] in sd.Letter.weak_consonant:
                    langname = "iki"+i.lemma[3:]
                elif i.lemma[4] in sd.Letter.hard_consonant:
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
            if i.lemma[0] in sd.Letter.vowel:
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
        # print(self.coll)

    def __str__(self):
        return f"lemma={self.lemma}, ID={self.dbid}, POS= {self.pos}, "\
               + f"all variants={self.coll}, "\
               + f"n_questions: {len(self.questions)}"

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
        # there is at least one alternative
        if self.alternatives:
            for i in self.alternatives:
                coll.append(i)
                # add plural of alternative
                # alternative starts with same letters as sg-prefix of lemma
                if entry[0] == "" or i[:(len(entry[2]))] == entry[0]:
                    # use plural-prefix of lemma also for alternative
                    coll.append(
                        sd.breakdown_consonants(entry[1]+i[len(entry[0]):]))
        for i in coll:
            self.questions += self._possibilities(i)
        self.coll = coll


def noun_partition(db_substantive):
    """devide nouns into analysed before or after verbs and adjectives
    because otherwise they could produce many false positives"""
    part_one = []
    part_two = []
    for noun in db_substantive:
        if noun.lemma[:2] in ["uk", "ug"] or noun.stem in ["se", "inshi"]:
            part_two.append(noun)
        else:
            part_one.append(noun)
    return part_one, part_two


def collect_nouns(db_substantive, freq_d):
    """maps nouns to lemmata in dbkirundi
    takes frequency-dictionary and list of nouns
    returns list with columns:
                lemma, id, PoS, sum of frequency of all forms, counted forms,
                all forms found ([form, frequency] per column)
            and changed frequency-dictionary {'found_noun':0}
    """
    freq_subs = freq_d
    collection = []
    if len(db_substantive) < 50:
        points = False
    else:
        points = int(len(db_substantive)/50)
    lemma_count = 0
    for noun in db_substantive:
        # print("noun", noun.questions)
        found = regex_search(noun, freq_subs)
        if found:
            collection.append(found)
        lemma_count += 1
        if points and lemma_count % points == 0:
            kh.OBSERVER.notify_cont('.')
    if collection:
        freq_subs = {x: y for x, y in freq_subs.items() if y != 0}
        # result: most wordforms first, with high freq first
        collection.sort(key=lambda x: x[3], reverse=True)
        collection.sort(key=lambda x: x[4], reverse=True)
    return (collection, freq_subs)


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
        frequency distribution
        """
        # prefixes1 = ["ba","ka","ma","ha","aya",
        #              "bi","ki","mi","ri","yi","zi",\
        #              "bu","ku","mu","ru","tu","uyu","uwu","n"]
        pre_kgregex = r"^((a?[bgkmhy]?a)|(i?[bgkmryz]?i)|(u?[bgkmrdtwy]?u)|[mn])(%s)$"
        # TODO make separated g- and k-regex
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
                if variant[0] == "r":
                    self.questions.append("ndende")
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
    freq_adj = freq_d
    for adj in db_adjektive:
        found = regex_search(adj, freq_adj)
        if found:
            teil = found[0].strip("-").split("-")
            # filter wrong positivs out: ibirebire yes, but not abarekure
            if len(teil) == 2 and teil[0] == teil[1]:
                new = []
                for foundtype in found[5:]:
                    ftype = foundtype[0]
                    # print(ftype)
                    # find both syllables
                    first_end = ftype.find(teil[0])
                    second_end = ftype.rfind(teil[0])
                    first = ftype[:first_end]
                    second = ftype[first_end + len(teil[0]):second_end]
                    if second in [first, first[1:]]:
                        new.append(foundtype)
                    else:
                        # was wrong positiv, roll back
                        freq_adj.update({ftype: foundtype[1]})
                        found[4] -= 1
                        found[3] -= foundtype[1]
                    found = found[:5]+new
                collection.append(found)
            else:
                collection.append(found)
    if collection:
        freq_adj = {x: y for x, y in freq_adj.items() if y != 0}
        collection.sort(key=lambda x: x[3], reverse=True)
        collection.sort(key=lambda x: x[4], reverse=True)

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

    def __str__(self):
        return f"lemma= {self.lemma}, ID={ self.dbid}, stem={self.stem}, "\
                + f"alternatives= {self.alternatives}, PoS={self.pos}, "\
                + f"questions={self.questions}"

    def __repr__(self):
        return f"lemma={self.lemma}, dbid={self.dbid}, stem={self.stem}, "\
                + f"alternatives={self.alternatives}, PoS= {self.pos} "\
                + f"questions={self.questions}"


def put_same_ids_together(collection):
    """sums up and adds found types of same ID,
    for interjections + adverbs and pronouns
    because some of them are made with regex and not listed in db"""
    collection.sort(key=lambda x: int(x[1]))
    coll = []
    for i in range(1, len(collection)):
        if int(collection[i][1]) == int(collection[i-1][1]):
            collection[i][3] += collection[i-1][3]
            collection[i][4] += collection[i-1][4]
            coll.append(collection[i] + collection[i-1][5:])
        else:
            coll.append(collection[i])
    coll.sort(key=lambda x: x[3], reverse=True)
    coll.sort(key=lambda x: x[4], reverse=True)
    return coll


def build_pronouns():
    """make pronouns out of combinations"""

    prns_made_here = []
    # lemma, question, db_id (or new id given here)
    # one lemma, one question
    one_lemma_one_question = [
        ["nk-o", [r"^nk"+sd.PrnRgx.ic_o+"o$",], 3281],
        ["-rtyo", [r"^"+sd.PrnRgx.gi+r"(r?tyo)$",], 7145],
        ["-a-o", [r"^"+sd.PrnRgx.c_a+"a"+sd.PrnRgx.c_o+"o$", ], 40000],
        ["_-o", [r"^"+sd.PrnRgx.ic_o+"o?$",], 40001],
        ["-a", [r"^"+sd.PrnRgx.c_a+"a?$",], 7778],
        ["-o", [r"^"+sd.PrnRgx.c_o+"o?$",], 40002],
        ["n_", [r"^((n[ai]t?we)|n)$",], 40003]
        ]
    for prn in one_lemma_one_question:
        build_p = kv.Word()
        build_p.lemma = prn[0]
        build_p.dbid = prn[2]
        build_p.pos = "PRON"
        build_p.questions = prn[1]
        prns_made_here.append(build_p)

    # one lemma, list of questions
    lem_loq = [
            ["-ari-o",
                ["uwariwo", "iyariyo", "iryariryo", "ayariyo", "icarico",
                 "ivyarivyo", "izarizo", "urwarirwo", "akariko", "utwaritwo",
                 "ubwaribwo", "ukwarikwo", "ihariho"],
                40015],
            ["-o-o",
                ["wowo", "bobo", "yoyo", "ryoryo", "coco", "vyovyo", "zozo",
                 "rworwo", "koko", "twotwo", "bwobwo", "kwokwo", "hoho"],
                40016],
            ["nyene",
                [r"^(na)?("+sd.PrnRgx.je+"|"+sd.PrnRgx.c_o+"o)nyene$",
                 r"^nyene"+sd.PrnRgx.c_o+"o$",
                 r"^"+sd.PrnRgx.ic_o+"onyene$",
                 r"^"+sd.PrnRgx.igki+"nyene$",
                 ],
                3402],
            ["ndi",
                [r"^([an]ta|[km]u|nka)"+sd.PrnRgx.kiw+"ndi$",
                 r"^n?"+sd.PrnRgx.igki+"ndi$",
                 r"^wawundi$", r"^a?babandi$", r"^yiyindi$", r"^ryarindi$",
                 r"^yayandi$", r"^cakindi$", r"^vyabindi$", r"^zazindi$",
                 r"^kakandi$", r"^twatundi$", r"^rwarundi$", r"^bwabundi$",
                 r"^kwakundi$", r"^hahandi$",
                 ],
                3218]
            ]
    for i in lem_loq:
        build_p = kv.Word()
        build_p.lemma = i[0]
        build_p.dbid = i[2]
        build_p.pos = "PRON"
        build_p.questions = i[1]
        prns_made_here.append(build_p)

    # list of lemmata, same question, at start of lemma: ?+x
    lol_q_start = [
            ["riya", "rya", "ryo", "no"],
            [r"^"+sd.PrnRgx.i_ki+"%s$"],
            [7320, 6510, 40014, 1458],
            ]
    for i in range(len(lol_q_start[0])):
        build_p = kv.Word()
        build_p.lemma = "-" + lol_q_start[0][i]
        build_p.dbid = lol_q_start[2][i]
        build_p.pos = "PRON"
        build_p.questions = [r"^" + sd.PrnRgx.i_ki + lol_q_start[0][i] + "$",]
        prns_made_here.append(build_p)

    # list of lemmata, same question at end of lemma: x+?
    lol_q_end = [
            ["ni", "nki", "na", "nka", "nta", "atari", "ari",
                "ukwa", "si", "hari"],
            [r"^%s" + sd.PrnRgx.c_o + "o?$",],
            [40004, 40005, 40005, 40007, 40008, 40009, 40010, 40011,
                40012, 40013],
            ]
    for i in range(len(lol_q_end[0])):
        build_p = kv.Word()
        build_p.lemma = lol_q_end[0][i] + "-"
        build_p.dbid = lol_q_end[2][i]
        build_p.pos = "PRON"
        build_p.alternatives = []
        build_p.questions = [r"^" + lol_q_end[0][i] + sd.PrnRgx.c_o + "o?$",]
        prns_made_here.append(build_p)

    # list_of_lemmata, list_of_questions at start of lemma: ?+x
    lol_loq = [
            ["anje", "awe", "iwe", "acu", "anyu", "abo"],
            [r"^" + sd.PrnRgx.poss + "%s$",  r"^" + sd.PrnRgx.c_o + "%s$"],
            [112, 174, 2326, 7490, 133, 8098]
            ]
    for i in range(len(lol_loq[0])):
        build_p = kv.Word()
        build_p.lemma = "-" + lol_loq[0][i]
        build_p.dbid = lol_loq[2][i]
        build_p.pos = "PRON"
        build_p.alternatives = []
        build_p.questions = [r"^" + sd.PrnRgx.poss + lol_loq[0][i]+"$",
                             r"^" + sd.PrnRgx.c_o + lol_loq[0][i]+"$"]
        prns_made_here.append(build_p)

    return prns_made_here


def collect_pronouns(db_pronouns, freq_d):
    """maps pronouns to lemmata of db and also builds pronouns with
    combinations
    takes frequency-dictionary and list of pronouns
    returns list with columns:
                lemma, id, PoS, sum of frequency of all forms, counted forms,
                all forms found ([form, frequency] per column)
            and changed frequency-dictionary {found pronouns are removed}
    """
    collection = []
    freq_prn = freq_d
    # for all pronouns with entry in db
    for lemma in db_pronouns:
        # print("lemma quest:", lemma)
        found = string_search(lemma, freq_prn)
        if found:
            collection.append(found)
    if collection:
        freq_prn = {x: y for x, y in freq_prn.items() if y != 0}
    # pronouns made out of regex
    prns_made_here = build_pronouns()
    for prn in prns_made_here:
        found = regex_search(prn, freq_prn)
        if found:
            collection.append(found)
    if collection:
        collection.sort(key=lambda x: x[0])
        print(collection)
        collection = put_same_ids_together(collection)
        freq_prn = {x: y for x, y in freq_prn.items() if y != 0}

    # save_dict(freq_prn,"keine3_pron.csv")
    # # Wörter, die im Korpus vorkommen
    # kh.save_list(collection,"found3_pron.csv",";")
    return (collection, freq_prn)


def collect_names(names_and_foreign_words, freq_list):
    """maps named entities and foreign words;
    takes frequency-list and NE-object list;
    returns list with columns:
                lemma, id, frequency, counted form =1,
                [form, frequency]
            and a frequency-dictionary {found words are removed}
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
        # kh.progress(int(lemma_count/maxi)*100)
        # progress bar
        if lemma_count % points == 0:
            # print('.', end="")
            kh.OBSERVER.notify_cont('.')
    if collection:
        collection.sort(key=lambda x: x[3], reverse=True)
        freq_names = {x: y for x, y in freq_names.items() if y != 0}
    return (collection, freq_names)


def collect_adv_plus(db_advplus, freq_d):
    """maps prepositions, adverbs, conjunctions and interjections
    to lemma in db
    takes frequency-dictionary and list of lemmata
    returns list with columns:
                lemma, id, sum of frequency of all forms, counted forms,
                all forms found ([form, frequency] per column)
            and a frequency-dictionary {'found_word':0}
    """
    collection = []
    freq_unchangable = freq_d
    for lemma in db_advplus:
        found = string_search(lemma, freq_unchangable)
        if found:
            collection.append(found)
    if collection:
        collection.sort(key=lambda x: x[3], reverse=True)
        freq_unchangable = {x: y for x, y in freq_unchangable.items() if y != 0}
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
    freq_exc = freq_d
    regex_exc_ego = r"^(y?e+go+|e+h?|y?ee+)$"
    regex_exc_oya = r"^(oya+)$"
    regex_exc_ha = r"^(ha)+$"
    regex_exc_la = r"^(la)+$"
    regex_exc_ah = r"^([au]+h|aa+|y?uu+|ah[ao]+|hu+)$"
    regex_exc_yo = r"^(y?o+h?|o+ho+|oh+)$"
    regex_exc_mh = r"^(m+h+|hu+m+|hm+|mm+|uu+m)$"
    regex_exc_he = r"^(e?(he+)+)$"
    regex_exc_kye = r"^(kye+)+$"
    regex_exc_luya = r"^(h?al+e+l+u+[iy]a+)$"
    regex_exec_alo = r"^(alo+)$"
    regex_exec_euh = r"^(e+uh)$"
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
                      ["alo", regex_exec_alo, 3008],
                      ["euh", regex_exec_euh, 3009]
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

    if collection:
        freq_exc = {x: y for x, y in freq_exc.items() if y != 0}
        collection = put_same_ids_together(collection)
        # collection.sort(key=lambda x: x[3], reverse=True)
        # collection.sort(key=lambda x: x[4], reverse=True)

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
