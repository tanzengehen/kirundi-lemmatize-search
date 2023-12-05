#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  6 23:43:14 2023

@author: doreen nixdorf
"""

import csv
import re
from unidecode import unidecode
try:
    import kir_prepare_verbs as kv
    import kir_string_depot as sd
    import kir_helper2 as kh
except ImportError:
    from ..lemmatize_search import kir_prepare_verbs as kv
    from ..lemmatize_search import kir_string_depot as sd
    from ..lemmatize_search import kir_helper2 as kh


def read_db_kirundi(filename=sd.ResourceNames.fn_db):
    """reads db_kirundi"""
    rows = []
    with open(filename, encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=";")
        for entry in csv_reader:
            rows.append(kv.RundiDictEntry(entry))
    return rows


def read_named_entities(filename=sd.ResourceNames.fn_named_entities):
    """reads names and foreign words"""
    rows = []
    with open(filename, encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=";")
        for entry in csv_reader:
            rows.append(EnEntry(entry))
    return rows


def get_resources(rundi_file=sd.ResourceNames.fn_db,
                  names_file=sd.ResourceNames.fn_named_entities):
    """load Named Entities and db_kirundi
    """
    # read db
    database_rundi = read_db_kirundi(rundi_file)
    # map db
    db_rundi = map_db_kirundi(database_rundi)
    # read named entities
    database_names = read_named_entities(names_file)
    # map named entities
    db_names = map_ne(database_names)
    db_rundi.update({"names": complete_location_language_person(db_names)})
    return db_rundi


class EnEntry:
    """single Named-Entity entry mapped"""

    def __init__(self, ne_entry):
        self.row = {}
        self.read_ne_entry(ne_entry)

    def __str__(self):
        return f"lemma: '{self.row.get('lemma')}', "\
                + f"pos: '{self.row.get('pos')}',\n"\
                + f"alternatives: '{self.row.get('alternatives')}"

    def __repr__(self):
        return f"lemma: '{self.row.get('lemma')}', "\
                + f"pos: '{self.row.get('pos')}',\n"\
                + f"alternatives: '{self.row.get('alternatives')}'"

    def read_ne_entry(self, ne_entry):
        """dao ne_kirundi"""
        ne_rundi_map = [['lemma', 'entry'],
                        ['pos', 'PoS'],
                        ['alternatives', 'alternatives']]
        for i in ne_rundi_map:
            if ne_entry.get(i[1]):
                my_value = unidecode(ne_entry.get(i[1]).strip())
            else:
                # None or ""
                my_value = ne_entry.get(i[1])
            self.row.update({i[0]: my_value})


def map_db_kirundi(rows):
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
    for entry in rows:
        row = entry.row
        if row.get('pos') == "VERB":
            if row.get('alternatives') or row.get('alternative_stem'):
                # there is also an alternative spelling
                row_a = kv.prepare_verb_alternativ(row)
                verb = kv.Verb(row_a)
                verbs.append(verb)
                row.update({'alternative': "x"})
            verb = kv.Verb(row)
            verbs.append(verb)
        elif row.get('pos') == "NOUN":
            nouns.append(Noun(row))
        elif row.get('pos') == "ADJ":
            adjectivs.append(Adjectiv(row))
        elif row.get('pos') == "PRON":
            pronouns.append(kv.Lemma(row))
        # prepositions, adverbs, conjunctions, interjections
        elif row.get('pos') in ["PREP", "ADV", "CONJ", "INTJ"]:
            unchanging_words.append(kv.Lemma(row))
        # prefixes, phrases
        else:
            rests.append(kv.Lemma(row))
        # stems as set
        stems.add(unidecode(row.get('stem').lower()))
    # kh.OBSERVER.notify(
    #     kh._('{} entries of the dictionary prepared.\n').format(line_count))

    # set questions only for verbs we will use
    # skip proverbs and lemma with passiv
    verbs = kv.filter_proverbs_out(verbs)
    verbs = kv.filter_passiv_out(verbs)
    for verb in verbs:
        verb.set_questions()

    # divide nouns: to be searched before or after verbs
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


def map_ne(rows):
    """reads file Named Entites and foreign words
    returns list of objects"""
    namedentities = []
    loc = []
    per = []
    lng = []
    foreign = []
    # print('in load ne: rows0=', rows[:5])
    for entry in rows:
        row = entry.row
        if row.get('pos') == "F":
            foreign.append(Foreign(row))
        elif row.get('pos') == "PROPN_LOC":
            loc.append(NamedEntities(row))
        elif row.get('pos') == "PROPN_PER":
            per.append(NamedEntities(row))
        elif row.get('pos') == "PROPN_LNG":
            lng.append(NamedEntities(row))
        else:
            enti = NamedEntities(row)
            enti.questions = enti.alternatives
            namedentities.append(enti)
    ne_dict = {"names": namedentities,
               'loc': loc,
               'per': per,
               'lng': lng,
               'foreign': foreign}
    return ne_dict


def complete_location_language_person(ne_dict):
    """add constructed languages, persons to ne_dict"""
    loc = ne_dict.get('loc')
    per = ne_dict.get('per')
    lng = ne_dict.get('lng')
    # assumed that alternative-list contains also stem of lemma
    for local in loc:
        local.alternatives = [i for i in local.alternatives
                              if i[:3] != "ubu"]
    for person in per:
        person.alternatives = [i for i in person.alternatives
                               if i[:3] not in ["umu", "umw"]]
    for language in lng:
        language.alternatives = [i for i in language.alternatives
                                 if i[:3] not in ["iki", "igi"]]

    # collect and share all alternative-spellings to all three lists
    check_entries_location_person_language(loc, per)
    check_entries_location_person_language(loc, lng, "lang")
    check_entries_location_person_language(lng, per)

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
    # create language and person entries if doesn't exist yet
    for i in loc:
        new_lang, new_per = i.set_location_and_create_person_language_out_of_it()
        if new_lang:
            lng.append(new_lang)
        if new_per:
            per.append(new_per)
        del i.row
    # TODO check if first line is head or entry
    return ne_dict.get('names') + ne_dict.get('foreign') + loc + per + lng


def check_entries_location_person_language(
        propn_list1, propn_list2, lang_or_per="per"):
    """check if there are different alternatives of stems in
    location, person, language;
    if so, we collect all alternativ spellings
    """
    for propn1 in propn_list1:
        done = False
        set1 = set(propn1.alternatives)
        for propn2 in propn_list2:
            set2 = set(propn2.alternatives)
            if set1.intersection(set2):
                propn2.alternatives = set(list(set2)+list(set1))
                propn1.alternatives = set(list(set2)+list(set1))
                done = True
                break
        if done:
            if lang_or_per == "lang":
                propn1.lang = "done"
            else:
                # lang_or_per is "per"
                propn1.persons = "done"
    return propn_list1, propn_list2


class Foreign:
    """sets PoS and question for string-search
    """

    def __init__(self, row):
        self.lemma = unidecode(row.get('lemma')).strip().lower()
        self.dbid = ""
        self.pos = row.get('pos').strip().upper()
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
        self.row = row
        self.dbid = ""
        self.lemma = unidecode(row.get('lemma')).strip().lower()
        self.pos = row.get('pos').strip().upper()
        if row.get('alternatives'):
            self.alternatives = [unidecode(i).strip().lower() for i in row.get(
                'alternatives').split(";")]
        else:
            self.alternatives = []
        self.alternatives.insert(0, self.lemma)
        # sometimes an alternative is after unidecode() the same word as lemma
        self.alternatives = list(set(self.alternatives))
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
        if not self.alternatives:
            if self.lemma[:3] == "umu":
                self.persons += [self.lemma, "aba"+self.lemma[3:]]
            else:
                self.persons += [r"(umuny[ae]?)?"+self.lemma,
                                 r"(abany[ae]?)?"+self.lemma]
        else:  # if self.alternatives:
            pref = "u"
            if self.lemma[:5] == "umuny":
                pref = "nya"

            for alt in self.alternatives:
                if pref == "u":
                    if alt[0] in sd.Letter.vowel:
                        self.persons += ["umw"+alt, "ab"+alt]
                    else:
                        self.persons += ["umu"+alt, "aba"+alt]
                else:
                    if alt[0] in sd.Letter.vowel:
                        self.persons += ["umuny"+alt, "abany"+alt]
                    else:
                        self.persons += ["umuny[ae]"+alt, "abany[ae]"+alt]

        for i in self.persons:
            self.questions += [
                r"^"+sd.NounPrepositions.qu_nta+"?"+i[1:]+"(kazi)?$",
                r"^"+sd.NounPrepositions.qu_ca_vowel+"?"+i+"(kazi)?$"
                ]

    def set_languages(self):
        """set questios for languages
        """
        if not self.alternatives:
            if self.lemma[:2] in ["ik", "ig", "ic"]:
                self.questions = [self.lemma, self.lemma[1:]]
            else:
                self.questions = [self.lemma, ]
                self.alternatives = [self.lemma, ]
                pref = "nya"

        if self.alternatives:
            pref = "i"
            if self.lemma[:5] == "ikiny":
                pref = "nya"

            for alt in self.alternatives:
                if pref == "i":
                    if alt[0] in sd.Letter.hard_consonant:
                        self.questions += ["gi"+alt, "igi"+alt]
                    elif alt[0] in sd.Letter.weak_consonant:
                        self.questions += ["ki"+alt, "iki"+alt]
                    else:
                        self.questions += ["c"+alt, "ic"+alt]
                else:
                    if alt[0] in sd.Letter.vowel:
                        self.questions += ["kiny"+alt, "ikiny"+alt]
                    else:
                        self.questions += ["kinya"+alt, "ikinya"+alt]

    def perla_from_ub(self):
        """creates lemma-names for related language and person
        of locations which start with ubu/ubw"""
        pername, langname = "", ""
        if self.pos == "PROPN_LOC":
            if self.lemma[2] == "u":
                # ubu
                pername = "umu"+self.lemma[3:]
                if self.lemma[3] in sd.Letter.weak_consonant:
                    langname = "iki"+self.lemma[3:]
                else:
                    langname = "igi"+self.lemma[3:]
            else:
                # ubw   only ubwongereza
                pername = "umw"+self.lemma[3:]
                langname = "ic"+self.lemma[2:]
        return pername, langname

    def create_new_lang(self, langname):
        """creates new language instance from location-data
        takes lemma_name"""
        new = None
        if self.pos == "PROPN_LOC":
            self.row.update({'lemma': langname})
            new = NamedEntities(self.row)
            new.pos = "PROPN_LNG"
            new.alternatives = self.alternatives
            new.set_languages()
        return new

    def create_new_person(self, pername):
        """creates new person instance from location-data
        takes lemma_name"""
        new = None
        if self.pos == "PROPN_LOC":
            self.row.update({'lemma': pername})
            new = NamedEntities(self.row)
            new.pos = "PROPN_PER"
            new.alternatives = self.alternatives
            new.set_persons()
        return new

    def set_location_and_create_person_language_out_of_it(self):
        """sets questions for location and returns not yet existing entries
        of PROPN_PER and PROPN_LANG based on that PROPN_LOC
        """
        new_lang = None
        new_per = None
        if self.pos == "PROPN_LOC":
            if self.lemma[:2] == "ub":
                # language- and person-lemma for locations with ubu/ubw
                pername, langname = self.perla_from_ub()

                # only countries with a name that starts with ubu/ubw
                #   get also in their variants ubu/ubw
                for location in self.alternatives:
                    if location[0] in sd.Letter.vowel:
                        self.questions += [
                            r"^"+sd.NounPrepositions.qu_nta+"?bw"+location+"$",
                            r"^"+sd.NounPrepositions.qu_ca_vowel+"?ubw"+location+"$"
                            ]
                    else:
                        self.questions += [
                            r"^"+sd.NounPrepositions.qu_nta+"?bu"+location+"$",
                            r"^"+sd.NounPrepositions.qu_ca_vowel+"?ubu"+location+"$"
                            ]
            # names for locations without ubu/ubw
            else:
                langname = "ikinya_"+self.lemma
                pername = "umunya_"+self.lemma

            # all locations (and their variants) get questions without ubu/ubw
            for location in self.alternatives:
                # location name starts with vowel
                if self.lemma[0] in sd.Letter.vowel:
                    self.questions += [
                        # ??? r"^"+sd.NounPrepositions.qu_nta+"?"+location+"$",
                        r"^"+sd.NounPrepositions.qu_ca_vowel+"?"+location+"$"
                        ]
                # location name starts with consonant
                else:
                    self.questions += [
                        r"^"+sd.NounPrepositions.qu_nta+"?"+location+"$",
                        r"^"+sd.NounPrepositions.qu_ca_konsonant+"?"+location+"$"
                        ]
            if self.lang != "done":
                new_lang = self.create_new_lang(langname)
            if self.persons != "done":
                new_per = self.create_new_person(pername)
        return new_lang, new_per


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
        sg_prefix = unidecode(row.get('prefix')).strip().lower()
        pl_prefix = unidecode(row.get('prefix_plural')).strip().lower()
        sg_alternative_prefix = unidecode(
            row.get('alternative_singular')).strip().lower()
        pl_irregular = unidecode(row.get('plural_irregular')).strip().lower()
        # add plural
        # plural is irregular (amaso)
        if pl_irregular:
            coll = [self.lemma, unidecode(pl_irregular)]
        # there is plural and it's different from singular
        elif pl_prefix not in ("", sg_prefix):
            coll = [self.lemma, sd.breakdown_consonants(pl_prefix+self.stem)]
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
                if sg_prefix == "" \
                   or i[:(len(sg_alternative_prefix))] == sg_prefix:
                    # use plural-prefix of lemma also for alternative
                    coll.append(
                        sd.breakdown_consonants(pl_prefix+i[len(sg_prefix):]))
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
    points = 0
    lemma_count = 0
    for noun in db_substantive:
        # print("noun", noun.questions)
        found = regex_search(noun, freq_subs)
        if found:
            collection.append(found)
        points, lemma_count = kh.show_progress(points,
                                               lemma_count,
                                               len(db_substantive))
    if collection:
        # result: most wordforms first, with high freq first
        collection.sort(key=lambda x: x[3], reverse=True)
        collection.sort(key=lambda x: x[4], reverse=True)
    freq_uncollected = {x: y for x, y in freq_subs.items() if y != 0}
    return (collection, freq_uncollected)


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
        self.set_questions(self.coll)

    def __str__(self):
        return f"lemma={self.lemma}, ID={self.dbid}, POS= {self.pos}, "\
               + f"stem={self.stem}, alternatives={self.alternatives}, "\
               + f"all variants {self.coll}: {len(self.questions)}"

    def __repr__(self):
        return f"lemma={self.lemma}, dbid={self.dbid}, POS= {self.pos}, "\
               + f"stem={self.stem}, alternatives={self.alternatives}, "\
               + f"coll={self.coll}, len(questions)={len(self.questions)}"

    def set_questions(self, coll):
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


def collect_adjs(db_adjektive, freq_simple_dict):
    """maps adjectivs to lemmata in dbkirundi
    takes frequency-dictionary and list of adjectives
    returns list with columns:
                lemma, id, PoS, sum of frequency of all forms, counted forms,
                all forms found ([form, frequency] per column)
            and changed frequency-dictionary {'found_adjectiv':0}
    """
    collection = []
    freq_uncollected = freq_simple_dict.copy()
    for adj in db_adjektive:
        found = regex_search(adj, freq_uncollected)
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
                        freq_uncollected.update({ftype: foundtype[1]})
                        found[4] -= 1
                        found[3] -= foundtype[1]
                    found = found[:5]+new
                collection.append(found)
            else:
                collection.append(found)
    if collection:
        collection.sort(key=lambda x: x[3], reverse=True)
        collection.sort(key=lambda x: x[4], reverse=True)
    freq_uncollected = {x: y for x, y in freq_uncollected.items() if y != 0}

    # save_dict(freq_adj,"keine5_adj.csv")
    # all adjectives
    # kh.save_list(collection,"found5_adj.csv",";")
    return (collection, freq_uncollected)


def build_pronouns():
    """make pronouns out of combinations"""

    prns_made_here = []
    # lemma, question, db_id (or new id given here)
    # one lemma, one question
    one_lemma_one_question = [
        ["nk-o", [r"^nk"+sd.PrnRgx.ic_o+"o$",], 3281, "PRON"],
        ["-rtyo", [r"^"+sd.PrnRgx.gi+r"(r?tyo)$",], 7145, "PRON"],
        ["-a-o", [r"^"+sd.PrnRgx.c_a+"a"+sd.PrnRgx.c_o+"o$", ], 40000, "PRON"],
        ["_-o", [r"^"+sd.PrnRgx.ic_o+"o?$",], 40001, "PRON"],
        ["-a", [r"^"+sd.PrnRgx.c_a+"a?$",], 7778, "PRON"],
        ["-o", [r"^"+sd.PrnRgx.c_o+"o?$",], 40002, "PRON"],
        ["n_", [r"^((n[ai]t?we)|n)$",], 40003, "PRON"]
        ]
    for row in one_lemma_one_question:
        prn = kv.WordBuild()
        prn.set_questions_simple(row)
        prns_made_here.append(prn)

    # one lemma, list of questions
    lem_loq = [
            ["-ari-o",
                ["uwariwo", "iyariyo", "iryariryo", "ayariyo", "icarico",
                 "ivyarivyo", "izarizo", "urwarirwo", "akariko", "utwaritwo",
                 "ubwaribwo", "ukwarikwo", "ihariho"],
                40015, "PRON"],
            ["-o-o",
                ["wowo", "bobo", "yoyo", "ryoryo", "coco", "vyovyo", "zozo",
                 "rworwo", "koko", "twotwo", "bwobwo", "kwokwo", "hoho"],
                40016, "PRON"],
            ["nyene",
                [r"^(na)?("+sd.PrnRgx.je+"|"+sd.PrnRgx.c_o+"o)nyene$",
                 r"^nyene"+sd.PrnRgx.c_o+"o$",
                 r"^"+sd.PrnRgx.ic_o+"onyene$",
                 r"^"+sd.PrnRgx.igki+"nyene$",
                 ],
                3402, "PRON"],
            ["ndi",
                [r"^([an]ta|[km]u|nka)"+sd.PrnRgx.kiw+"ndi$",
                 r"^n?"+sd.PrnRgx.igki+"ndi$",
                 r"^wawundi$", r"^a?babandi$", r"^yiyindi$", r"^ryarindi$",
                 r"^yayandi$", r"^cakindi$", r"^vyabindi$", r"^zazindi$",
                 r"^kakandi$", r"^twatundi$", r"^rwarundi$", r"^bwabundi$",
                 r"^kwakundi$", r"^hahandi$",
                 ],
                3218, "PRON"]
            ]
    for row in lem_loq:
        prn = kv.WordBuild()
        prn.set_questions_simple(row)
        prns_made_here.append(prn)

    # list of lemmata, same question, at start of lemma: ?+x
    lol_q_start = [
            ["riya", "rya", "ryo", "no"],
            [r"^"+sd.PrnRgx.i_ki+"%s$"],
            [7320, 6510, 40014, 1458],
            ]
    for i in range(len(lol_q_start[0])):
        build_p = kv.WordBuild()
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
        build_p = kv.WordBuild()
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
        build_p = kv.WordBuild()
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
    returns * list with columns:
                lemma, id, PoS, sum of frequency of all forms, counted forms,
                all forms found ([form, frequency] per column)
            * and changed frequency-dictionary {found pronouns are removed}
    """
    collection = []
    freq_prn = freq_d.copy()

    # pronouns made with regex
    prns_made_here = build_pronouns()
    for prn in prns_made_here:
        found = regex_search(prn, freq_prn)
        if found:
            collection.append(found)
    if collection:
        freq_prn = {x: y for x, y in freq_prn.items() if y != 0}

    # pronouns with entry in db
    for lemma in db_pronouns:
        found = string_search(lemma, freq_prn)
        if found:
            collection.append(found)
    if collection:
        # sort to make sure that lemma is: '-no' and not: 'hano'
        collection.sort(key=lambda x: x[0])
        collection = kv.put_alternatives_of_same_id_together(collection)
    freq_uncollected = {x: y for x, y in freq_prn.items() if y != 0}

    # save_dict(not_collected, "keine3_pron.csv")
    # # Wörter, die im Korpus vorkommen
    # kh.save_list(collection,"found3_pron.csv",";")
    return (collection, freq_uncollected)


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
    points = 0
    lemma_count = 0
    for name in names_and_foreign_words:
        if name.pos in ["PROPN_PER", "PROPN_LOC"]:
            # persons and locations have RegEx for their possibilities
            found = regex_search(name, freq_names)
        else:
            # all possibilities are already readable strings
            found = string_search(name, freq_names)
        if found:
            collection.append(found)
        # progress bar
        points, lemma_count = kh.show_progress(points,
                                               lemma_count,
                                               len(names_and_foreign_words))
    if collection:
        collection.sort(key=lambda x: x[3], reverse=True)
    freq_uncollected = {x: y for x, y in freq_names.items() if y != 0}

    return (collection, freq_uncollected)


def collect_adv_plus(db_advplus, freq_d):
    """maps prepositions, adverbs, conjunctions and interjections
    to lemma in db
    takes frequency-dictionary and list of lemmata
    returns list with columns:
                lemma, id, sum of frequency of all forms, counted forms,
                all forms found ([form, frequency] per column)
            and a frequency-dictionary {found words are removed}
    """
    collection = []
    freq_unchangable = freq_d
    for lemma in db_advplus:
        found = string_search(lemma, freq_unchangable)
        if found:
            collection.append(found)
    if collection:
        collection.sort(key=lambda x: x[3], reverse=True)
    freq_uncollected = {x: y for x, y in freq_unchangable.items() if y != 0}
    return (collection, freq_uncollected)


def build_exclamations():
    """make exclamation lemmata with regex questions"""
    excl_made_here = []
    # exclamations not in the original db get IDs from 30000
    one_lemma_one_question = [
        ["ego", [sd.ExclRgx.ego,], 818, "INTJ"],
        ["oya", [sd.ExclRgx.oya,], 3556, "INTJ"],
        ["ha", [sd.ExclRgx.ha,], 30000, "INTJ"],
        ["la", [sd.ExclRgx.la,], 30001, "INTJ"],
        ["aah", [sd.ExclRgx.ah,], 30002, "INTJ"],
        ["ooh", [sd.ExclRgx.yo,], 30003, "INTJ"],
        ["mh", [sd.ExclRgx.mh,], 30004, "INTJ"],
        ["hee", [sd.ExclRgx.he,], 30005, "INTJ"],
        ["kyee", [sd.ExclRgx.kye,], 30006, "INTJ"],
        ["alleluia", [sd.ExclRgx.luya,], 30007, "INTJ"],
        ["alo", [sd.ExclRgx.alo,], 3008, "INTJ"],
        ["euh", [sd.ExclRgx.euh,], 3009, "INTJ"]
    ]
    for row in one_lemma_one_question:
        excl = kv.WordBuild()
        excl.set_questions_simple(row)
        excl_made_here.append(excl)
    return excl_made_here


def collect_exclamations(db_rest, freq_d):
    """maps exclamations to a list of regex made here and all the rest
    of entries in the db
    takes frequency-dictionary and list of lemmata
    returns list with columns:
                lemma, id, sum of frequency of all forms, counted forms,
                all forms found ([form, frequency] per column)
            and a frequency-dictionary {found words are removed}
    """
    collection = []
    freq_exc = freq_d

    # exclamations made with regex
    excl_made_here = build_exclamations()
    for excl in excl_made_here:
        found = regex_search(excl, freq_exc)
        if found:
            collection.append(found)
    if collection:
        freq_exc = {x: y for x, y in freq_exc.items() if y != 0}

    # exclamations with entry in db
    for lemma in db_rest:
        found = string_search(lemma, freq_exc)
        if found:
            collection.append(found)
    if collection:
        collection = kv.put_alternatives_of_same_id_together(collection)
    freq_uncollected = {x: y for x, y in freq_exc.items() if y != 0}
    # print("in dbc coll_excl:", collection[:2])
    return (collection, freq_uncollected)


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
