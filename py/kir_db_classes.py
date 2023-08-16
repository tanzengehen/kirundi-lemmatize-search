#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  6 23:43:14 2023

@author: doreen
"""

import csv
import re
from unidecode import unidecode
import kir_prepare_verbs as kv
import kir_string_depot as sd


class Noun(kv.Lemma):
    """sets db-ID, lemma, stem, POS, singular, plural, alternative spellings and
    questions for lemma search
    """
    def __init__(self, row):
        super().__init__(row)
        self.questions = []
        self.coll = []
        self._set_questions(row)
        # add prefix-regex depending on first letter of stem of variant
    def __str__(self):
        return f"lemma={self.lemma}, ID={self.dbid}, POS= {self.pos}, "\
               +f"all variants={self.coll}, "\
               +f"questions: {len(self.questions)}"
    def __repr__(self):
        return f"lemma={self.lemma}, dbid={self.dbid}, POS= {self.pos}, "\
                   +f"coll={self.coll}, "\
                   +f"len(questions)={len(self.questions)}"
    def _possibilities(self, variant):
        """more variants if nouns are written inclusive prepositions without apostrophe
        """
        # noun starts with vowel
        if variant[0] in ["a","e","i","u"] :
            qu_0 = r"^([na]ta|[mk]u|i)?"+variant[1:]+"$"
            qu_1 = r"^([bkmrt]?w|[rv]?y|[nsckzbh])?"+variant+"$"
         # noun starts with consonant
        else :
            qu_0 = r"^([na]ta|[mk]u|s?i)?"+variant+"$"
            qu_1 = r"^([nckzbh]|[bkmrt]?w|[rv]?y)[ao]"+variant+"$"
        return [qu_0, qu_1]
    def _set_questions(self, row):
        """takes row from dbkirundi
        sets singular, plural and spelling variations with and without augment 
        """
        columns = [3,  # entry0-prefix_sg
                   7,  # entry1-prefix_pl
                   14, # entry2-alternative prefix
                   21] # entry3-plural irregular 
        entry = [unidecode(row[x]).strip().lower() for x in columns]
        # plural is not regular (amaso)
        if entry[3]:
            coll = [self.lemma, entry[3]]
        # there is plural and it's different from singular
        elif entry[1] not in ("" , entry[0]) :
            coll = [self.lemma, sd.breakdown_consonants(entry[1]+self.stem)]
        # there is no plural
        else :
            coll = [self.lemma, ]
        # there is at least one alternativ
        if self.alternatives :
            for i in self.alternatives :
                if entry[2] == entry[0]:
                # gleiche Präfix Klasse wie Sg -> auch gleiche Pluralbildung
                    coll.append(sd.breakdown_consonants(entry[1]+i[len(entry[0]):]))
        for i in coll:
            self.questions += self._possibilities(i)
        self.coll = coll

def collect_nouns(db_substantive, freq_d, before_verbs =True):
    """sortiert Substantive auf bekannte Lemmas im kirundi Dictionary
    liest fdist als dict ein und gibt auch dict zurück"""
    #freqSubs = {str(n[0]):n[1] for n in freq_d[:29290]}
    freq_subs = {x:y for x,y in freq_d.items() if y != 0}
    #print ("untersuche",len(freqSubs),"freqs")
    collection = []
    subs_kgu = [] # collect nouns that could be verbs, inspect them after verbs
    points = int(len(db_substantive)/50)
    lemma_count = 0
    for noun in db_substantive :
        if before_verbs is True and noun.lemma[:2] in ["uk","ug"] and noun.lemma[-1] == "a" :
            subs_kgu.append(noun)
            # gleich zum nächsten lemma
            continue
        found= lemma_search(noun, freq_subs, "NOUN")
        if found:
            # if len(found)<4:
            #     print("collect nouns",(found))
            collection.append(found)
        if before_verbs is True :
            # Fortschrittsbalken ;-)
            lemma_count +=1
            if lemma_count%points == 0 :
                print('.',end = "")

    # result: first most wordforms, there most freqs first
    collection.sort(key=lambda x: x[3], reverse = True)
    collection.sort(key=lambda x: x[4], reverse = True)
    collection.insert(0,["lemma;id;noun;count;counted forms;forms",])

    # if before_verbs == True :
    #     # Wörter, die zum Wörterbuch gemappt wurden sind 0
    #     save_dict(freq_subs,"keine4_subst.csv")
    #     # Wörter, die im Korpus vorkommen
    #     kh.save_list(collection,"found4_subst.csv",";")
    #     # Dictionary-Einträge, fdist ausgedünnt, später zu untersuchende Substantive
    # else :
    #     save_dict(freq_subs,"keine7_subst.csv")
    #     kh.save_list(collection,"found7_subst.csv",";")
    return (collection, freq_subs, subs_kgu)




class Adjectiv(kv.Lemma):
    """sets db-ID, lemma, stem, POS, alternative spellings and
    questions for lemma search
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
        return f"lemma={self.lemma}, ID={self.dbid}, POS= {self.pos}, stem={self.stem}, "\
               +f"alternatives={self.alternatives}, "\
               +f"all variants {self.coll}: {len(self.questions)}"
    def __repr__(self):
        return f"lemma={self.lemma}, dbid={self.dbid}, POS= {self.pos}, stem={self.stem}, "\
                   +f"alternatives={self.alternatives}, "\
                   +f"coll={self.coll}, len(questions)={len(self.questions)}"
    def set_qu(self, coll):
        """sets regex-questions for fishing nouns out of frequency distribution
        """
        #prefixes1 = ["ba","ka","ma","ha","aya","bi","ki","mi","ri","yi","zi",\
        #        "bu","ku","mu","ru","tu","uyu","uwu","n"]
        pre_kgregex = r"^((a?[bgkmhy]?a)|(i?[bgkmryz]?i)|(u?[bgkmrdtwy]?u)|[mn])(%s)$"
        #prefixes2 = ["bw","kw","mw","rw","tw","ny","ry","vy","y","n","z",\
        #        b","k","c","h"]
        pre_aregex = r"^((u?[bkmrt]?w)|(i?[nrv]?y)|a?[bkh]|i?[cz]|n)(%s)$"
        #prefixes4 = ["b","k","c","h","z","y","ry","vy","nz"\
        #        "bw","kw","mwo","mwe",rwo","rwe","two","twe"]
        pre_oregex = r"^(((u?[bkmrt]?w)[oe])|((i?[rv]?y|nz|a?[bkh]|i?[cz])o))(%s)$"
        #prefixes3 = [be,ke,me,he, bwi,kwi,mwi,rwi,twi, myi,nyi,vyi,nzi,bi,ci]
        pre_iregex = r"^((a?[bkmh]e)|(u?[bkmrt]?w[i]+)|(i?[mnrv]?yi|n?zi|[bc]i))(%s)$"

        # aba aka aya aha ibi iki iyi iri izi ubu uku uwu uru utu
        #     aga       ivy igi ic ny iry  nz ubw ugu ukw  urw udu utw
        #  be ke ma me he         y mi my n m        mu mw w  twe
        # bo ko   yo  ho  vyo co      ryo  zo  bwo kwo wo rwo two
        # i- n- nk- ni-o  -ari-o -a-o i-ya nta-o na-o
        for variant in coll:
            teil = variant.split("-")
            if variant[0] == "a" :
                quest = pre_aregex % (teil[0])
            elif variant[0] == "i" :
                quest = pre_iregex % (teil[0][1:])
            elif variant[0] == "o" :
                quest = pre_oregex % (teil[0][1:])
            else :
                quest = pre_kgregex % (teil[0])
            #??? to do: what about ki-co ...
            # in case it's an adjective with two hyphen (e.g. -re-re)
            if len(teil) == 2 :
                if teil[1][0] == "a" :
                    quest = quest[:-1]+pre_aregex[1:] % (teil[1])
                    #print (question)
                elif teil[1][0] == "o" :
                    quest = quest[:-1]+pre_oregex[1:] % (teil[1])
                    #print (question)
                else :
                    quest = quest[:-1]+pre_kgregex[1:] % (teil[1])
                    #print (question)
            self.questions.append(quest)

def lemma_search(word, freq_dict, pos):
    """checks type and regex per lemma
    """
    freqsum = 0
    found = []
    for quest in word.questions:
        for freqtype, num in freq_dict.items() :
            if num != 0  and re.search(quest,freqtype) is not None:
                freqsum += num
                found.append( [freqtype,num] )
                freq_dict.update({freqtype:0})
    if freqsum > 0 :
        found.sort()
        #             lemma,     id,   PoS,Summe, different forms, all[form alphabetical,frequency]
        found = [word.lemma, word.dbid, pos, freqsum, len(found)]+ found
    return found

def collect_adjs(db_adjektive, freq_d):
    """takes fdist as dict and returns dict
    """
    collection = []
    # kommt freq als liste oder dict? (vorher sammle_subst?)
    #freqText = {freq[x][0]:freq[x][1] for x in freq if freqfreq[x][1] != 0}
    freq_adj = {x:y for x,y in freq_d.items() if y != 0}
    for adj in db_adjektive :
        found= lemma_search(adj, freq_adj, "ADJ")
        if found:
            collection.append(found)
    collection.sort(key=lambda x: x[3], reverse = True)
    collection.sort(key=lambda x: x[4], reverse = True)
    collection.insert(0,["lemma;id;adj;count;counted forms;forms",])
    # mapped types now have 0 in simplefreq
    #save_dict(freq_adj,"keine5_adj.csv")
    # all adjectives
    #kh.save_list(collection,"found5_adj.csv",";")
    return (collection, freq_adj)


def load_dbkirundi():
    """returns lists sorted more or less by part of speech
    """
    verbs = []
    nouns = []
    adjectivs = []
    pronouns =[]
    unchanging_words = []
    rests = []
    stems = []
    stems = set(stems)
    with open(sd.RessourceNames().fn_db, encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = ";")
        line_count = 0
        for row in csv_reader:
            # attention: column numbers still valid?
            if line_count > 0 :
                if row[8] == "0" :
                    if row[13] and row[15]:
                        # there is also an alternative spelling
                        row_a = kv.prepare_verb_alternativ(row)
                        verb = kv.Verb(row_a)
                        verbs.append(verb)
                        row[0] =  str(row[0])+"_0"  # 0 id
                        row[13] = ""                # alternatives
                    verb = kv.Verb(row)
                    verbs.append(verb)
                elif row[8] == "1" :
                    nouns.append(Noun(row))
                elif row[8] == "2" :
                    adjectivs.append(Adjectiv(row))
                elif row[8] == "5" :
                    pronouns.append(kv.Lemma(row))
                #prepositions, adverbs, conjunctions, interjections (incl POS-tag)
                elif row[8] == "3" or row[8] == "6" or row[8] == "7" \
                or row[8] == "8":
                    unchanging_words.append(kv.Lemma(row))
                #exclamation, emphasis, prefixes, phrases and all without "!?..." (inkl POS-tag)
                else :
                    rests.append(kv.Lemma(row))
                #stems as set
                stems.add(unidecode(row[4]).lower())
            line_count += 1
    print(f'{line_count} entries of the dictionary prepared.')
    csv_file.close()
    verbs = kv.filter_proverbs_out(verbs)
    verbs =  kv.filter_passiv_out(verbs)
    
    stems = list(stems)
    return (verbs, nouns, adjectivs, pronouns, unchanging_words, rests, stems)


def filter_names_out(names_and_foreign_words, freq_list):
    """takes simplefreq as list (not as dict), but returns dict
    returns list of names and simplefreq with zeros, where names are taken out"""
    collection = []
    freq_names = dict(freq_list)
    points = int(len(names_and_foreign_words)/50)
    lemma_count = 0
    for names in names_and_foreign_words :
        for word,num in freq_names.items():
            if names[0] == word:
                # Eintrag, Anzahl
                collection.append([word,"",names[1],num,1,[word,num]])
                freq_names.update({word:0})
        lemma_count +=1
        # progress bar
        if lemma_count%points == 0 :
            print('.',end = "")
    collection.sort(key=lambda x: x[3], reverse = True)
    collection.insert(0,"lemma;;names;count",)
    return(collection,freq_names)

#TODO
class Exclamations:
    def __init__(self, lemma, dbid=None, alternatives =None):
        self.dbid = dbid
        self.lemma = lemma
        self.alternatives = alternatives
        self.questions = []
    def __str__(self):
        return f"lemma={self.lemma}, ID={self.dbid}, "\
               +f"alternatives={self.alternatives}, "\
               #+f"all alternatives {self.coll}: {self.questions}"
    def __repr__(self):
        return f"lemma={self.lemma}, dbid={self.dbid}, "\
                   +f"alternatives={self.alternatives}, "\
                   #+f"coll={self.coll}, len(questions)={len(self.questions)}"


def collect_exclamations(db_rest,freq_d) :
    """collects exclamations and their variants"""
    collection = []
    freq_exc = {x:y for x,y in freq_d.items() if y != 0}
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
    ecxl_made_here = [["ego",regex_exc_ego,818], #db_id
            ["oya",regex_exc_oya,3556],
            ["ha",regex_exc_ha,30000],
            ["la",regex_exc_la,30001],
            ["aah",regex_exc_ah,30002],
            ["ooh",regex_exc_yo,30003],
            ["mh",regex_exc_mh,30004],
            ["hee",regex_exc_he,30005],
            ["kyee",regex_exc_kye,30006],
            ["alleluia",regex_exc_luya,30007],
        ]
    for excl in ecxl_made_here :
        freqsum = 0
        found = []
        db_id = excl[2]

        for freqs, num in freq_exc.items() :
            if num !=0 and re.search(excl[1],freqs) is not None :
                freqsum += num
                found.append( [freqs,num] )
                freq_exc.update({freqs:0})
                continue # next qu1
        if freqsum > 0 :
            found.sort()
            found = [excl[0], db_id, "INTJ", freqsum, len(found)] + found
            collection.append(found)

    # for all exclamation we didn't made here and the rest of db_dict
    for lemma in db_rest :
        freqsum = 0
        found = []
        for variant in lemma.alternatives:
            variant = variant.strip("-")
            for freqs, num in freq_exc.items() :
                if num !=0 and variant == freqs:
                    freqsum += num
                    found.append( [freqs,num] )
                    freq_exc.update({freqs:0})
        # Eintrag, id, POS, Summe Häufigkeit, Anzahl Varianten, Liste(Variante, Häufigkeit)
        if freqsum > 0 :
            found.sort()
            found = [lemma.lemma, lemma.dbid, "INTJ", freqsum, len(found)]+ found
            collection.append(found)
            freq_exc.update({freqs:0})


    collection.sort(key=lambda x: x[3], reverse = True)
    collection.sort(key=lambda x: x[4], reverse = True)
    collection.insert(0,"keyword;id;exclamation;count;counted forms;forms",)
    # # Wörter, die zum Wörterbuch gemappt wurden, sind jetzt auf 0
    # save_dict(freq_exc,"keine8_excl_div2.csv")
    # # Wörter, die im Korpus vorkommen
    # kh.save_list(collection,"found8_excl_div2.csv",";")
    return (collection, freq_exc)



def sammle_kleine_woerter(db_advplus, freq_d):
    """liest fdist als dict ein und gibt auch dict zurück"""
    collection = []
    freq_unchangable = {x:y for x,y in freq_d.items() if y != 0}

    for lemma in db_advplus :
        for freqs,num in freq_unchangable.items():
            if lemma.lemma == freqs:
                # Eintrag, id, Anzahl
                collection.append([freqs,lemma.dbid,lemma.pos,num,1,[freqs,num]])
                freq_unchangable.update({freqs:0})
                #??? Varianten einbauen: nk, mur

    collection.sort(key=lambda x: x[3], reverse = True)
    collection.insert(0,"lemma;id;div;count",)
    # # Wörter, die zum Wörterbuch gemappt wurden, sind jetzt auf 0
    # save_dict(freq_unchangable,"keine2_div.csv")
    # # Wörter, die im Korpus vorkommen
    # kh.save_list(collection,"found2_div.csv",";")

    return(collection, freq_unchangable)

#TODO
class Pronouns(kv.Lemma):
    def __init__(self, row):
        super().__init__(row)
    def __str__(self):
        return f"lemma= {self.lemma}, ID={ self.dbid}, stem= {self.stem}, "\
               +f"alternatives= {self.alternatives}, POS= {self.pos}"\
               #+f"all alternatives {self.coll}: {self.questions}"
    def __repr__(self):
        return f"lemma={self.lemma}, dbid={self.dbid}, stem= {self.stem}, "\
                   +f"alternatives={self.alternatives}, POS= {self.pos}"

def sammle_pronouns(db_pronouns,freq_d):
    """liest fdist als dict ein und gibt auch dict zurück"""
    collection = []
    freq_prn = {x:y for x,y in freq_d.items() if y != 0}
    regex_prn_c_a = r"(([bkrt]w|[rv]?y|[bchkwz]))"
    regex_prn_c_o = r"([bkrt]?w|[rv]?y|[bchkz])"
    regex_prn_ic_o = r"(a[bhky]|i([cz]|([rv]?)y)|u(([bkrt]?w?)|y))"
    regex_prn_gi = r"([bghm]a|[bgmirz]i|n|[bdgmr]u)"
    regex_prn_i_ki = r"((a?[bhk]a|i?[bkrz]i|u?[bkrt]u)|[aiu])"
    regex_prn_kiw = r"(([bhky]a|[bkryz]i|[bkrtw]u))"
    regex_prn_poss = r"((u|kub)|("+regex_prn_ic_o+"|"+regex_prn_c_o+")?i)w"
    regex_prn_igki = r"(a[bhgkmy]a|i(v?y|[bgkmrz])i|u[bgkmrdtwy]u)"
    regex_prn_je = r"(([jw]|[mt]w)e)"


    # lemma, qu, marker if regex needs Variable, (dict_id #??? unused)
    prns_made_here = [#lemma,qu
            [["nk-o",],[r"nk"+regex_prn_ic_o+"o",], 0, 3281],
            [["rtyo",],[regex_prn_gi+r"(r?tyo)",], 0, 7145],
            [["-a-o",],[regex_prn_c_a+"a"+regex_prn_c_o+"o",], 0],
            [["_-o",],[regex_prn_ic_o+"o?",], 0],
            [["-a",],[regex_prn_c_a+"a?",], 0, 7778],
            [["-o",],[regex_prn_c_o+"o?",], 0],
            [["n_",],[r"((n[ai]t?we)|n)",], 0],
            #list,list
            [["anje","awe","iwe","acu","anyu","abo"], \
                 [r"^"+regex_prn_poss+"%s$", r"^"+regex_prn_c_o+"%s$"], \
                 1, [112, 174, 2326, 7490, 133, 8098]],
            # list,qu
            [["ni","nki","na","nka","nta","atari","ari","ukwa","si","hari"], \
                 [r"^%s"+regex_prn_c_o+"o?$",], 1],
            [["riya","rya","ryo","no"], \
                 [r"^"+regex_prn_i_ki+"%s$"], 1, [7320, 6510, "", 1458]],
            # lemma,list
            [["-ari-o",],["uwariwo","iyariyo","iryariryo","ayariyo","icarico", \
                     "ivyarivyo","izarizo","urwarirwo", "akariko","utwaritwo", \
                     "ubwaribwo","ukwarikwo","ihariho"], 0],
            [["-o-o",],["wowo","bobo","yoyo","ryoryo","coco","vyovyo","zozo", \
                     "rworwo","koko","twotwo","bwobwo","kwokwo","hoho"], 0],
            [["nyene",],[r"^(na)?("+regex_prn_je+"|"+regex_prn_c_o+"o)%s$", \
                         r"^%s"+regex_prn_c_o+"o$", r"^"+regex_prn_ic_o+"o%s$", \
                         r"^"+regex_prn_igki+"%s$", ],1, 3402],
            [["ndi"],[r"^([an]ta|[km]u|nka)"+regex_prn_kiw+"%s$",
                     r"^n"+regex_prn_igki+"%s$",
                     r"^wawu%s$", r"^a?baba%s$", r"^yiyi%s$", r"^ryari%s$",
                     r"^yaya%s$", r"^caki%s$", r"^vyabi%s$", r"^zazi%s$",
                     r"^kaka%s$", r"^twatu%s$", r"^rwaru%s$", r"^bwabu%s$",
                     r"^kwaku%s$", r"^haha%s$", ], 1, 3218]    ]

    for quest in prns_made_here :
        for qu0 in quest[0]:
            freqsum = 0
            found = []
            for qu1 in quest[1] :
                if quest[2] == 0 :
                    question = r"^"+qu1+"$"
                if quest[2] == 1 :
                    question = qu1 %qu0
                #print (question)
                for freqs, num in freq_prn.items() :
                    if num !=0 and re.search(question,freqs) is not None :
                        freqsum += num
                        found.append( [freqs,num] )
                        freq_prn.update({freqs:0})
                        continue # next qu1
            if freqsum > 0 :
                found.sort()
                found = [qu0, "", "PRON", freqsum, len(found)] + found
                collection.append(found)

    # for all pronouns we didn't made here
    for lemma in db_pronouns :
        freqsum = 0
        found = []
        for variant in lemma.alternatives:
            for freqs, num in freq_prn.items() :
                if num !=0 and variant == freqs:
                    freqsum += num
                    found.append( [freqs,num] )
                    freq_prn.update({freqs:0})
        # Eintrag, id, Anzahl
        if freqsum > 0 :
            found.sort()
            found = [lemma.lemma, lemma.dbid, "PRON", freqsum, len(found)]+ found
            collection.append(found)
            freq_prn.update({freqs:0})

    collection.sort(key=lambda x: x[3], reverse = True)
    collection.sort(key=lambda x: x[4], reverse = True)
    collection.insert(0,"lemma;id;pron;count;counted forms;forms",)
    # # Wörter, die zum Wörterbuch gemappt wurden, sind jetzt auf 0
    # save_dict(freq_prn,"keine3_pron.csv")
    # # Wörter, die im Korpus vorkommen
    # kh.save_list(collection,"found3_pron.csv",";")
    return (collection, freq_prn)
