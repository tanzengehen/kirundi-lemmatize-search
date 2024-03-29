#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 29 10:13:10 2023

@author: doreen nixdorf
"""

import re
from abc import abstractmethod
from unidecode import unidecode
try:
    import kir_string_depot as sd
    import kir_helper2 as kh
except ImportError:
    from ..lemmatize_search import kir_string_depot as sd
    from ..lemmatize_search import kir_helper2 as kh


REGEX_SUFFIX = r"((([hyk]|mw)o)?$)"


class RundiDictEntry:
    """single db_kirundi entry mapped"""

    def __init__(self, db_entry):
        self.row = {}
        self.read_db_entry(db_entry)

    def __str__(self):
        return f"lemma: '{self.row.get('lemma')}', "\
                + f"dbid: '{self.row.get('dbid')}', "\
                + f"pos: '{self.row.get('pos')}',\n"\
                + f"prefix: '{self.row.get('prefix')}', "\
                + f"stem: '{self.row.get('stem')}', "\
                + f"perfective: '{self.row.get('perfective')}', "\
                + f"prefix_plural: '{self.row.get('prefix_plural')}', "\
                + f"plural_irregular: '{self.row.get('plural_irregular')}', "\
                + f"alternatives: '{self.row.get('alternatives')}', "\
                + "alternative_singular: "\
                + f"'{self.row.get('alternative_singular')}', "\
                + f"alternative_stem: '{self.row.get('alternative_stem')}', "\
                + "alternative_perfective: "\
                + f"'{self.row.get('alternative_perfective')}'"

    def __repr__(self):
        return f"lemma: '{self.row.get('lemma')}', "\
                + f"dbid: '{self.row.get('dbid')}', "\
                + f"pos: '{self.row.get('pos')}',\n"\
                + f"prefix: '{self.row.get('prefix')}', "\
                + f"stem: '{self.row.get('stem')}', "\
                + f"perfective: '{self.row.get('perfective')}', "\
                + f"prefix_plural: '{self.row.get('prefix_plural')}', "\
                + f"plural_irregular: '{self.row.get('plural_irregular')}', "\
                + f"alternatives: '{self.row.get('alternatives')}', "\
                + "alternative_singular: "\
                + f"'{self.row.get('alternative_singular')}', "\
                + f"alternative_stem: '{self.row.get('alternative_stem')}', "\
                + "alternative_perfective: "\
                + f"'{self.row.get('alternative_perfective')}'"

    def read_db_entry(self, db_entry):
        """dao db_kirundi"""
        pos_dict = {"0": "VERB", "1": "NOUN", "2": "ADJ", "3": "PREP",
                    "5": "PRON", "6": "ADV", "7": "CONJ", "8": " INTJ",
                    "9": "PHRASE", "10": "PREFIX"}
        if int(db_entry.get('type')) in [0, 1, 2, 3, 5, 6, 7, 8, 9, 10]:
            pos = pos_dict.get(db_entry.get('type')).strip()
        else:
            pos = "UNK"
        self.row.update({'pos': pos})
        db_rundi_map = [['dbid', 'id'],
                        ['lemma', 'kirundi0'],
                        ['prefix', 'prefix'],
                        ['stem', 'stem'],
                        ['perfective', 'stem_perf'],
                        ['prefix_plural', 'plural'],
                        ['plural_irregular', 'pluralFull'],
                        ['alternatives', 'kirundi0_a'],
                        ['alternative_singular', 'prefix_a'],
                        ['alternative_stem', 'stem_a'],
                        ['alternative_perfective', 'stem_perf_a']]
        for i in db_rundi_map:
            if db_entry.get(i[1]):
                my_value = unidecode(db_entry.get(i[1]).strip())
            else:
                # None or ""
                my_value = db_entry.get(i[1])
            self.row.update({i[0]: my_value})


class WordBuild:
    """lemma-entry made by the program"""
    @abstractmethod
    def __init__(self):
        self.dbid = ''
        self.lemma = ''
        self.pos = ''
        self.stem = ''
        self.alternatives = []
        self.questions = []

    def __str__(self):
        return f"lemma= {self.lemma}, ID={ self.dbid}, PoS= {self.pos}, "\
                + f"stem= {self.stem}, alternatives= {self.alternatives} "\
                + f"questions: {self.questions}"

    def __repr__(self):
        return f"lemma={self.lemma}, dbid={self.dbid}, PoS= {self.pos}, "\
                    + f"stem= {self.stem}, alternatives={self.alternatives}, "\
                    + f"len(questions)={len(self.questions)}"

    def set_questions_simple(self, row):
        """set questions"""
        self.lemma = row[0]
        self.questions = row[1]
        self.dbid = row[2]
        self.pos = row[3]


class Lemma:
    """sets: db-ID, lemma, stem, POS, alternative spellings
    """

    def __init__(self, row):
        # print(type(row), row)
        self.dbid = row.get('dbid')
        self.lemma = row.get('lemma')
        self.pos = row.get('pos')
        if row.get('stem'):
            self.stem = row.get('stem')
        else:
            # Translators: (debug) check dictionary new entry
            kh.OBSERVER.notify_error(
                kh._("lemma has no stem in database: ID {}").format(self.dbid))
            self.stem = "xxx"
        # self.questions = [self.lemma,]
        if row.get('alternatives'):
            self.alternatives = [i.strip() for i in row.get('alternatives').split(";")]
            self.questions = [i.strip() for i in row.get('alternatives').split(";")]
        else:
            self.alternatives = ""
            self.questions = []
        self.questions.insert(0, self.lemma)

    def __str__(self):
        return f"lemma= {self.lemma}, ID={ self.dbid}, PoS= {self.pos}, "\
               + f"stem= {self.stem}, alternatives= {self.alternatives} "\
               + f"questions: {self.questions}"

    def __repr__(self):
        return f"lemma={self.lemma}, dbid={self.dbid}, PoS= {self.pos}, "\
                   + f"stem= {self.stem}, alternatives={self.alternatives}, "\
                   + f"len(questions)={len(self.questions)}"


def regex_prfx_autonom_subjects_verbs():
    """ regex for autonomous verbform
    """
    # ###### autonom subjects ########

    # time3 (only possibility for time in this forms) uwu-ta-:
    #    uwa, uwara, uwuta, uwutara, uwo, uwuto, uwuzo, !uwutazo,
    #    uwuki, uwutaki, uwuka?
    #       uwagira, uwagize / uwaragira, uwaragize
    #       uwutagira, uwutagize / uwutaragira, uwutaragize
    #       uwogira, uwogize / uwutogira, uwutogize
    #       uwuzokora, uwuzokoze / uwutazogira, uwutazogize
    #       () / ()
    #       uwukigira, uwukigize / uwutakigira, uwutakigize

    # that means:
    # uwO, uwA, uwAra, uwuTa, uwuTara, uwuTaki, uwuKi, uwuTo, uwuZo
    # abo, aba, abara, abata, abatara, abataki, abaki, abato, abazo
    # ivyo, ivya, ivyara, ibita, ibitara, ibitaki, ibiki, ibito, ibizo
    # uwandika, ubwandika, ivyiruka, iryiruka, abandika, iciruka
    #       +stem or +perfektive
    regex_ibi_ku = r"((a[bkhy]a)|(i[bkryz]i)|(u[bkrtw]u))"
    regex_ibi_gu = r"((a[bhgy]a)|(i[bgryz]i)|(u[bgrdw]u))"
    regex_ivy_kw = r"((a[bkhy])|(i([cz]|([vr]?y)))|(u[bkrt]?w))"

    regex_atn_negtime_ku = "(ta(ra|ki|zo)?|ki|([zt]?o))"
    regex_atn_negtime_gu = "(da|ta(ra|gi|zo)|gi|([zt]?o))"  # ibitogira > ibitokora
    regex_atn_negtime_kw = "(ta[rc]|[tz]okw|[tcz])"   # uwuziruka or uwuzokwiruka both is ok
                                                      # uwutaciruka ok
    # without objects
    regex_ay_ibi_infx_ku = r"("+regex_ivy_kw+"(o|(a(ra)?))|("+regex_ibi_ku +\
        "("+regex_atn_negtime_ku+")?))"
    regex_ay_ibi_infx_gu = r"("+regex_ivy_kw+"(o|(a(ra)?))|("+regex_ibi_ku +\
        regex_atn_negtime_gu+")|"+regex_ibi_gu+")"
    regex_ay_ibi_infx_kw = r"(("+regex_ivy_kw+"((o(kw)?)|(a(ra)?))?)|(" +\
        regex_ibi_ku+regex_atn_negtime_kw+"))"
    return regex_ay_ibi_infx_ku, regex_ay_ibi_infx_gu, regex_ay_ibi_infx_kw


def regex_prfx_subj_times_verbs():
    """prepares regex for prefixes of subject-classes combined with
    times, negation, conditional
    """
    subj_ku_a, subj_ku_e, subj_ku_y = [], [], []
    subj_gu_a, subj_gu_e, subj_gu_y = [], [], []
    subj_kw_a, subj_kw_e, subj_kw_y = [], [], []

    ##################################################################
    ####### subject-prefix ##########
    # pre-subjects (only classes, with 2 letters as "bi")
    # bi-       for ku,kur,kum/n and gu,guh
    regex_bi_ku = r"([bkh]a|[bkrz]i|[bkmrt]u)"
    regex_bi_gu = r"([bgh]a|[bgrz]i|[bgmrd]u)"
    # vy- w-    for kw_aeiou:
    regex_bi_kw = r"(([vr]?y)|[bchz]|([bkmrt]?w)|[bkmrt]?uny)"
    # subjects for all classes
    re_all_class_subj = r"([nuai]|"+regex_bi_ku+")"

    ##################################################################
    # n,u,bi for stem-ends a und y : nka nkana, uka ukana, bika bikana
    # ay_ku
    for i in [subj_ku_a, subj_ku_y]:
        i.append(r"("+re_all_class_subj+"ka(na)?)")
    # ay_gu
    for i in [subj_gu_a, subj_gu_y]:
        i.append(r"("+re_all_class_subj+"kana|"+re_all_class_subj+"ga)")
    # ay_kw
    for i in [subj_kw_a, subj_kw_y]:
        i.append(r"("+re_all_class_subj+"k(an)?)")

    ##################################################################
    ###### n time_1 for stem-ends aey #########
    # after n may change next letter
        # vor gu_tkcsz,ku_dgjy, obj_norm(tkzdgy):
    # nda(ca)- ndaka- na- nara- (si)na- (si)no- (si)nzo- (si)nda-
    for i in [subj_ku_a, subj_ku_e, subj_ku_y,
              subj_gu_a, subj_gu_e, subj_gu_y]:
        # aey_kgo
        i.append("((si)?)")
        # aey_kg
        i.append(r"((nda([ckg]a)?)|nara|((si)?n([ao]|zo)))")

    # before kw_aeiou instead of a may come kw,y
    # aey_kw
    for i in [subj_kw_a, subj_kw_e, subj_kw_y]:
        i.append(r"(nd(a[ck])?|nar|((si)?n((a?y)|((a|(z?o))(kw)?))))")

    '''regex_aey_sin = r")"
    # n disappears, if n is last letter before   ku_mn, guh
    # n will be asked with only_stem
    regex_aey_sin_mnhr  = r"(si)?" '''

    # only for stem_end e: ndaka- sinka- sinkana- ni-
    # e_ku
    subj_ku_e.append(r"(ndaka|sinka(na)?|nin)")
    regex_e_n_mnh = r"(ndaka|sinka(na)?|ni)"  # ??? noch eintragen !!
    # e_gu
    subj_gu_e.append(r"(ndaga|sin(g|kan)a|nin)")
    # e_kw
    subj_kw_e.append(r"(ndak|sink(an)?|nin)")
    # ndandika tse / ndakandika tse
    # narandika tse / sinandika tse
    # nandika tse / nandika tse
    # nokwandika tse / nzokwandika  nzokwanditse
    # ncandika tse / sincandika tse
    # sinzokwandika, sinokwandika tse,

    # insert kw also with kwi- or kwo-verb
    # kwoza nokwoza, nokwogeje   nzokwoza
    # kwiruka nokwiruka nokwirutse nzokiruka

    # ndamira tse / ndakamira tse
    # naramira tse / sinamira tse
    # mira mize / namira tse            #collect mira with imperatives, mize!!
    # nomira tse / nzomira  nzomiye
    # (for all ab n-) sinzomira, sinomira tse,

    # ndagira ze / ndakagira (ze not)
    # naragira ze / sinagira ze
    # ngira ze / nagira ze
    # nogira ze / nzogira  nzogize
    # sinzogira, sinogira ze

    # *******************************************************************
    # time1 after ntu: ntiwa, ntura for stem-ends ae, ntiwo, ntuzo, ntuki

    # for stem-end e:
    # ntuka- ntukana- nu-      for gu,guh,  ku,kur,kum/n  kw
    # nu for: höfl.Imperativ, na will be asked with (si)?na
    # ka for: du sollst niemals... +e
    # e_ku
    subj_ku_e.append(r"((nt[aiu]ka(na)?)|n[ui])")
    # e_gu
    subj_gu_e.append(r"(nt[aiu](ga|kana)|n[ui])")
    # e_kw
    subj_kw_e.append(r"((nt[aiu]k(an)?)|n(uw|[ai]y))")
    # ntugakore, ntukagire, ntukandike, ntukoze, ntukiruke
    # nukore, nugire, nuwandika, niyoze, nayiruke

    # for stem-ends aey
    # (nt)u- (nt)uzo-           for gu,guh,ku,kur,kumn,kw
    # aey_kg
    for i in [subj_ku_a, subj_ku_e, subj_ku_y,
              subj_gu_a, subj_gu_e, subj_gu_y]:
        i.append(r"((nt)?[uai](zo)?)")
    # aey_kw
    for i in [subj_kw_a, subj_kw_e, subj_kw_y]:
        i.append(r"((nt)?(i([wy]|(z(okw)?))|[ua](z(okw)?)))")

    # for stem-ends ay
    # else rak will be asked before ra-kw
    # ay_kw
    for i in [subj_kw_a, subj_kw_y]:
        i.append(r"([uai]ra[ktr]w?)")
    # wara- (nti)wa- (nti)wo- (nt)ura- ukazo-
    # ay_kg
    for i in [subj_ku_a, subj_ku_y,
              subj_gu_a, subj_gu_y]:
        i.append(r"([wy]ara|(nti)?[wy][ao]|(nt)?[uai](ra)|[uai]kazo)")
    # kw will be asked with bi_kw

    # for stem-end a
    # uraka-
    # a_kg
    for i in [subj_ku_a, subj_gu_a]:
        i.append(r"([uai]raka)")
    # kw with ay, else rak will be asked before ra-kw

    # time1
    # for stem-end e:       ntibika-  n(t)ibi-
    # e_ku -- ntibi(ka)gende, nimugende
    subj_ku_e.append(r"((nti"+regex_bi_ku+"(ka)?)|(ni"+regex_bi_ku+"))")
    # e_gu -- ntitugakore, n(t)idukore
    subj_gu_e.append(r"((nti"+regex_bi_ku+"ga)|(nt?i"+regex_bi_gu+"))")
    # e_kw -- ntukandike, n(t)ukiruke
    subj_kw_e.append(r"((nti"+regex_bi_ku+"k)|(nt?i"+regex_bi_kw+"))")

    # for stem-ends aey:    (nti)bi, (nti)bizo, (nti)vya
    # aey_ku
    for i in [subj_ku_a, subj_ku_e, subj_ku_y]:
        i.append(r"((nti)?("+regex_bi_ku+"(zo)?|("+regex_bi_kw+"a)))")
    # aey_gu
    for i in [subj_gu_a, subj_gu_e, subj_gu_y]:
        i.append(r"((nti)?("+regex_bi_gu+"|"+regex_bi_ku+"zo|" +
                 regex_bi_kw+"a(kw)?))")
    # aey_kw
    for i in [subj_kw_a, subj_kw_e, subj_kw_y]:
        i.append(r"((nti)?("+regex_bi_kw+"(ay)?|"+regex_bi_ku+"(z(okw)?)))")
    # for stem-ends ay:     vyara (nti)vyo (nti)bira bikazo
    # ay_kg
    for i in [subj_ku_a, subj_ku_y,
              subj_gu_a, subj_gu_y]:
        i.append(r"("+regex_bi_kw+"ara|(nti)?("+regex_bi_kw+"o|" +
                 regex_bi_ku+"ra)|"+regex_bi_ku+"kazo)")
    # ay_kw
    for i in [subj_kw_a, subj_kw_y]:
        i.append(r"("+regex_bi_kw+"ar|(nti)?("+regex_bi_kw+"o(kw)?|" +
                 regex_bi_ku+"[rc])|"+regex_bi_ku+"kaz(okw)?)")
    # a_kw
    subj_kw_a.append(r"("+regex_bi_ku+"ra[ktr]w?|sind)")
    # for stem-end a:       biraka
    # a_ku
    subj_ku_a.append(r"("+regex_bi_ku+"raka|sinda)")
    # a_gu
    subj_gu_a.append(r"("+regex_bi_ku+"raga|sinda)")
    # kw also with y because of object

    # time1 after nti:
    # kugenda
    #       bigendae, bigiye / ntibigendae, ntibigiye
    #       bizogendae, bizogiye / ntibizogendae, ntibizogiye
    #       ((vyagenda, vyagiye)) /ntivyagenda, ntivyagiye
    #       ((vyogenda, vyogiye)) /  ntivyogenda, ntivyogiye
    #       ((vyaragenda, vyaragiye)) /()
    #       ((biragenda, biragiye)) / ntibiragenda, ntibiragiye
    #       bikazogenda, bikazogiye

    # time2
    # ra raca raka ta tara!!! taki tazo ki zo to
    # n, u bi
    # aey_ku
    for i in [subj_ku_a, subj_ku_e, subj_ku_y]:
        i.append(r"(n((da([ck]a)?)|ta(ra|ki|zo)?|ki|zo|to))")
        i.append(r"(("+regex_bi_ku +
                 "|[uai])((ra([ck]a)?)|ta(ra|ki|zo)?|ki|zo|to))")
    # aey_gu
    for i in [subj_gu_a, subj_gu_e, subj_gu_y]:
        i.append(r"(n((da([ck]a)?)|da|((ta)?(ra|ki|zo))|to))")
        i.append(r"(("+regex_bi_ku +
                 "|[uai])((ra([ck]a)?)|da|((ta)?(ra|ki|zo))|to))")
    # aey_kw
    for i in [subj_kw_a, subj_kw_e, subj_kw_y]:
        i.append(r"(n((d(a[ck]?))|((ta)?(r|c|([zt](okw)?)))))")
        i.append(r"(("+regex_bi_ku +
                 "|[uai])((ra[ck])|r|((ta)?([rc]|([zt](okw)?))))?)")

    # plus the regex for autonom forms
    (regex_ay_ibi_infx_ku,
     regex_ay_ibi_infx_gu,
     regex_ay_ibi_infx_kw) = regex_prfx_autonom_subjects_verbs()
    # ay_ku
    for i in [subj_ku_a, subj_ku_y]:
        i.append(regex_ay_ibi_infx_ku)
    # ay_gu
    for i in [subj_gu_a, subj_gu_y]:
        i.append(regex_ay_ibi_infx_gu)
    # ay_kw
    for i in [subj_kw_a, subj_kw_y]:
        i.append(regex_ay_ibi_infx_kw)

# ??? aey sortieren nach nächstem Durchlauf, mal sehen, was kommt
# problem with kw: single krt here, will not search for kw,rw,tw in object !

    # time2 with u-ta-: ((wa)), ((wara)), ((wo)), ((ura)),     ((=asked above))
    #       uta, utara!, uto, utazo!, uraca, uraka!, utaki, uki!, uka
    #       bita, bitara, bito, bitazo, biraca, biraka, bitaki, biki
    # kugira
    #       ((wagira, wagize))/ ((waragira, waragize))
    #       ((wogira, wogize)) / ((uragira, uragize))
    #       utagira, utagize / utaragira, ()
    #       utogira, utogize       ?? /utazogira, utazogize
    #       uracagira, uracagize / urakagira, urakagize(?)
    #       ukigira, ukigize     / utakigira, utakigize
    #       ukagira, ukagize
    # kwandika
    #       ((wandika, wanditse))/ ((warandika, waranditse))
    #       utandika, utanditse, utarandika ()
    #       ((wokwandika, wokwanditse)), utazokwandika , utazokwanditse
    #       uracandika, uracanditse, ((urandika, uranditse))
    #       urakandika, (), ucandika , ucanditse
    #       utacandika, utacanditse, ukandika, ukanditse
    # kwoza
    #       ((woza, wogeje))/ ((waroza, warogeje))
    #       utoza, utogeje, utaroza ()
    #       ((wokwoza, wokwogeje)), utazokwoza, utazokwogeje
    #       uracoza, uracogeje / ((uroza, urogeje))
    #       urakwoza, urakwogeje / ukwoza ()
    #       utacoza, utacogeje
    # kwiruka
    #       ((wa:  wiruka, wirutse))/ ((wara: wariruka, warirutse))
    #       uta: utiruka, utirutse  / utara: utariruka ()
    #       ((wo:  wokwiruka, wokwirutse)) / utazo: utaziruka, utazokwiruka, utazokwirutse
    #       uraca: uraciruka, uracirutse / ((ura: uriruka, urirutse))
    #       uraka: urakiruka, urakirutse(?) / uki: uciruka ()
    #       utaki: utaciruka, utacirutse / uka: ukiruka, ukirutse

    return (subj_ku_a, subj_ku_e, subj_ku_y,
            subj_gu_a, subj_gu_e, subj_gu_y,
            subj_kw_a, subj_kw_e, subj_kw_y)


def regex_prfx_obj_verbs():
    """
    prepares regex-lists for objects depending on first letter of stem of verb
    """
    obj_ku = []
    obj_gu = []
    obj_kw = []
    # subj may end with n (=special cases obj_b_r_m_h) or not (=norm)
    # obj may end with n (=special cases stem_bv_pf_mn_r_h) or not (=ku_gu_kw)
    # obj_n never comes after subj_n or other obj_n   (thank goddess!)

    # subj        up to 3 objects, possible combinations:            variants of stem behind
    # list         n ki h?           : n norm h?                             k g w
    # list         n b h?            : mb h?                                 kg w
    # list         n r h?            : nd h?                                 kg w
    # list         n m h?            : m h?                                  kg w
    # list         n h               : n h                                   kg w
    # list         all n? h          : (b|r|m|h|norm) n? h                   kg w
    # list         all n             : (b|r|m|h|norm) n                      bvpf mn r h
    # sin, list    ohne_n? ohne_n h? : (b|r|m|h|norm)?  ((b|r|m|h)|norm) h?  k g w
    # sin, list                         -no object -                         k g w
    # si, list                          -no object -                         bv pf mn r h
    #def set_obj(self):
    # normal1: ka ya ki yi zi ku mu tu wu
    norm_ku = r"(([ky]a)|([kyz]i)|([kmtw]u))"
    norm_gu = r"(([gy]a)|([gyz]i)|([gmdw]u))"
    norm_kw = r"(([kmt]?w)|[kycz])"
    n_norm_ku = r"(n"+norm_ku+")"

    obj_ku.append(r"("+n_norm_ku+"(ha)?)")
    obj_gu.append(r"(n"+norm_gu+")")
    obj_kw.append(r"(n"+norm_kw+")")

    obj_gu.append(r"("+n_norm_ku+"ha)")
    obj_kw.append(r"("+n_norm_ku+"h)")

    # exception2: ba bi bu
    b_kg = r"(b[aiu])"
    b_kw = r"(bw|vy|b)"
    nb_kg = r"(mb[aiu])"
    for i in [obj_ku, obj_gu]:
        i.append(r"("+nb_kg+"(ha)?)")
    obj_kw.append(r"(m(bw|vy|b))")   # problem?: sorts bivuga to kwivuga(ba), instead to kuvuga(bi)
    obj_kw.append(r"("+nb_kg+"h)")

    # exception3: ri ru
    r_kg = r"(r[iu])"
    r_kw = r"(r[yw])"
    nr_kg = r"(nd[iu])"
    for i in [obj_ku, obj_gu]:
        i.append(r"("+nr_kg+"(ha)?)")
    obj_kw.append(r"(nd[yw])")       # ba-n-ru-andika ba-n-ri-andika
    obj_kw.append(r"("+nr_kg+"h)")

    # exception4: mu
    #    obj_nm_kgw = r"m[uw]" # n vor m fällt weg, also nmh = mh
    for i in [obj_ku, obj_gu]:
        i.append(r"(mu(ha)?)")
    obj_kw.append(r"(m(w|uh))")     # mw|muh
    # exception5: ha
    obj_nh_kg = r"((mp|h)a)"
    for i in [obj_ku, obj_gu]:
        i.append(obj_nh_kg)
    obj_nh_kw = r"(mp|h)"
    obj_kw.append(obj_nh_kw)

    # "all" means: all obj except n
    obj_all_ku = r"("+b_kg+"|"+r_kg+"|mu|ha|"+norm_ku+")"
    obj_ku.append(obj_all_ku)
    obj_ku.append(r"("+obj_all_ku+"{1,2}(ha)?)")
    for i in [obj_ku, obj_gu]:
        i.append(r"("+obj_all_ku + obj_nh_kg+")")
    obj_all_gu = r"("+b_kg+"|"+r_kg+"|mu|ha|"+norm_gu+")"
    obj_gu.append(obj_all_gu)
    obj_gu.append(r"("+obj_all_ku+"?"+obj_all_gu+")")
    obj_gu.append(r"("+obj_all_ku+"{1,2}ha)")

    obj_all_kw = r"("+b_kw+"|"+r_kw+"|mu|ha|"+norm_kw+")"
    obj_kw.append(obj_all_kw)
    obj_kw.append(r"("+obj_all_ku+"?"+obj_all_kw+")")
    obj_kw.append(r"("+obj_all_ku+"{1,2}h)")
    obj_kw.append(r"("+obj_all_ku+obj_nh_kw+")")

    # obj_all_n = r"(" +obj_all_ku +"n)"    #??? wird durch n_end erledigt
                                            # außer kw! n > ny
    return obj_ku, obj_gu, obj_kw, obj_all_ku


(SUBJ_KU_A, SUBJ_KU_E, SUBJ_KU_Y,
 SUBJ_GU_A, SUBJ_GU_E, SUBJ_GU_Y,
 SUBJ_KW_A, SUBJ_KW_E, SUBJ_KW_Y) = regex_prfx_subj_times_verbs()
OBJ_KU, OBJ_GU, OBJ_KW, OBJ_ALL_KU = regex_prfx_obj_verbs()


class Verb(Lemma):
    """sets id, lemma, stem, perfective, questions-regex, proverb,
    initializes an alternative instance if there is a spelling variant
    """

    def __init__(self, row):
        super().__init__(row)
        self._end_a = ""
        self._end_e = ""
        self._end_y = ""
        self._qu_a = ""
        self._n_end_a = ""
        self._qu_e = ""
        self._n_end_e = ""
        self._qu_y = ""
        self._n_end_y = ""
        self._qu_obj = ""
        self.comb = None
        self.unclear = []
        self.proverb = False
        self.passiv = False
        self.perfective = unidecode(row.get('perfective').strip().lower())
        self.check_perfective()

    def __str__(self):
        return f"lemma={self.lemma}, ID={self.dbid}, POS= {self.pos}, "\
                + f"stem='{self.stem}', perfective= -{self.perfective}, "\
                + f"alternatives={self.alternatives}, "\
                + f"comb_set={self.comb is not None}"  # ": {len(self.comb)}"

    def __repr__(self):
        return f"lemma={self.lemma}, dbid={self.dbid}, "\
                   + f"POS= {self.pos},\t-{self.stem} / -{self.perfective},\t"\
                   + f"alternatives={self.alternatives}, "\
                   + f"comb_set={self.comb is not None}"  # , len(comb)={len(self.comb)}"

    def check_perfective(self):
        """sort out unclear perfective"""
        if self.perfective.find("?") > -1:
            # (debug) check new entries of rundi dictionary
            # Translators: for debugging only
            kh.OBSERVER.notify_error(
                kh._("{}: perfective? -{}").format(self.lemma, self.perfective))
            self.unclear.append(
                [self.lemma, "perfective unclear:", self.perfective])
            self.perfective = ''

    def mark_proverb(self):
        """ mark verbs with ' ' in lemma as proverb
        and accept at stem and perfective only first part
        """
        # lemma has more than one part
        if self.lemma.find(" ") > -1:
            # save full lemma for later
            self.proverb = True
            # first part is hopefully verb-part
            if self.stem.find(" "):
                self.stem = self.stem.split()[0]
            # cut also perfective
            if self.perfective.find(" "):
                self.perfective = self.perfective.split()[0].strip()

    def mark_passiv(self):
        """marks passiv form of verb
        """
        if self.lemma[-2] == "w":
            self.passiv = True

    def _set_end_of_ends(self):
        """sets regex-strings for three possible endforms of the
        verb including passiv, subjunctiv, perfective, perfective-passive and
        each with direction-suffixes these are:
        end_a, end_e, end_y (each is string)
        """
        # add passiv to indikativ: end_a
        self._end_a = self.stem[:-1]+r"(w?a)"+REGEX_SUFFIX
        # make subjunctiv: end_e
        self._end_e = self.stem[:-1]+"e"+REGEX_SUFFIX
        # add passiv to perfective: end_y
        if self.perfective == "":
            perfective_passiv = ""
        else:
            if len(self.perfective) > 3 and self.perfective[-2] == "y":
                if self.perfective[-3] in ["m", "n"]:
                    perfective_passiv = self.perfective[:-1]+r"(w?e)"
                elif self.perfective[-3] in "aeio":
                    perfective_passiv = self.perfective[:-2]+r"([yw]e)"
                elif self.perfective[-3] == "u":
                    perfective_passiv = self.perfective[:-2]+r"(ye|((ri)?we))"
                elif self.perfective[-3] == "v":
                    perfective_passiv = self.perfective[:-3]+r"(vye|bwe)"
                elif self.perfective[-3] == "f":
                    perfective_passiv = self.perfective[:-3]+"puwe"
                else:
                    self.unclear.append(
                        ["perfective: unexpected letter before [y] ",
                         self.lemma, self.perfective])
                    # Translators: (debug) check dictionary new entry
                    kh.OBSERVER.notify_error(f"\t{self.lemma} -{self.perfective}:"
                                       + kh._("""\n\t\ttried to add passiv to
perfective but unknown letter before y"""))
                    perfective_passiv = self.perfective
            elif len(self.perfective) > 3 and self.perfective[-2] in "jzshw":
                perfective_passiv = self.perfective[:-1]+r"((w)?e)"
            else:
                self.unclear.append(
                    ["perfective: unexpected letter before last letter:",
                     self.lemma, self.perfective])
                perfective_passiv = self.perfective
        if perfective_passiv == "":
            self._end_y = ""
        else:
            self._end_y = perfective_passiv + REGEX_SUFFIX

        # special cases
        if self.stem == "ti":
            self._end_a = self.stem + REGEX_SUFFIX
            self._end_e, self._end_y = "", ""
            self._qu_obj = ""
        elif self.stem == "ri":
            self._end_a = self.stem + REGEX_SUFFIX
            self._n_end_a = "ndi"+REGEX_SUFFIX
            self._end_e, self._end_y = "", ""
            self._qu_obj = "ha"
        elif self.stem == "zi":
            self._end_a = "zw?i"+REGEX_SUFFIX
            self._end_e, self._end_y = "", ""
        elif self.stem in ["fise", "fitiye"]:
            self._end_a = self.stem + REGEX_SUFFIX
            self._end_y = self.stem + REGEX_SUFFIX

    def _set_begins_and_n_end(self):
        """depending on first consonant of stem it
        sets regex-possibilities of beginings and
        sets variant for first letter of stem if begining-regex ends with 'n'
        following breakdown rules
        now we have 6 end-strings and four regex-lists for beginnings
        """
        # == "ku" :
        if self.stem[0] in r"[bdgjmnrvyz]":
            # each is list of strings
            self._qu_a = SUBJ_KU_A
            self._qu_e = SUBJ_KU_E
            self._qu_y = SUBJ_KU_Y
            self._qu_obj = OBJ_KU
            stem_consonant = {"r": "nd", "b": "mb", "v": "mv", "m": "m",
                              "n": "n"}
            # ends are strings
            if self.stem[0] in stem_consonant:
                self._n_end_a = stem_consonant.get(self.stem[0])+self._end_a[1:]
                self._n_end_e = stem_consonant.get(self.stem[0])+self._end_e[1:]
                self._n_end_y = stem_consonant.get(self.stem[0])+self._end_y[1:]
            else:
                self._n_end_a = r"n"+self._end_a
                self._n_end_e = r"n"+self._end_e
                self._n_end_y = r"n"+self._end_y
        # == "gu" :
        elif self.stem[0] in r"[cfhkpst]":
            self._qu_a = SUBJ_GU_A
            self._qu_e = SUBJ_GU_E
            self._qu_y = SUBJ_GU_Y
            self._qu_obj = OBJ_GU
            stem_consonant = {"p": "mp", "f": "mf", "h": "mp"}
            # breakdown rules for gu-
            if self.stem[0] in stem_consonant:
                self._n_end_a = stem_consonant.get(self.stem[0])+self._end_a[1:]
                self._n_end_e = stem_consonant.get(self.stem[0])+self._end_e[1:]
                self._n_end_y = stem_consonant.get(self.stem[0])+self._end_y[1:]
            else:
                self._n_end_a = r"n"+self._end_a
                self._n_end_e = r"n"+self._end_e
                self._n_end_y = r"n"+self._end_y
        # == "kw" :
        elif self.stem[0] in r"[aeiou]":
            self._qu_a = SUBJ_KW_A
            self._qu_e = SUBJ_KW_E
            self._qu_y = SUBJ_KW_Y
            self._qu_obj = OBJ_KW
            self._n_end_a = r"ny?"+self._end_a
            self._n_end_e = r"ny?"+self._end_e
            self._n_end_y = r"ny?"+self._end_y

    def set_questions(self):
        """ combines beginning-possibilities to it's equivalent end
        subject/object/time/negation/... with Indikativ/Subjunctiv/Perfectiv
        inkl. first letter of stem differences
        only the last part before end_aey has to decide kgw
        list with 6 elements: [end, questions for this end]

        collection of combinations :
        questions = {end_a   : each subj_ku_a with each qu_obj(kgw),
                               each qu_a solo(kgw),
                               each qu_obj solo(kgw),
                               stem solo(kgw)
                     end_e   : each qu_e(kgw),
                               each subj_ku_e with each qu_obj(kgw),
                     end_y   : each qu_y(kgw),
                               each subj_ku_y with each qu_obj,

                     n_end_a : each subj_ku with each obj_all_n -- for last obj is n
                               each subj_ku                     -- for obj is only n
                               #r"(si)?"
                               each obj_all_n                   -- imperativ
                     n_end_e : each qu_e with each obj_all_n,
                               each subj_ku
                     n_end_y : each qu_y with each obj_all_n,
                               each subj_ku
                               #r"(si)?")}
        """
        # three ends
        self._set_end_of_ends()
        # six ends, 4 begin-lists
        self._set_begins_and_n_end()
        # collect subj-obj-combination-possibilities for each end
        coll_end_a = []
        for subject_regex in self._qu_a:
            coll_end_a.append(r"^"+subject_regex+"$")
        for object_regex in self._qu_obj:
            coll_end_a.append(r"^"+object_regex+"$")
            for subject_regex in SUBJ_KU_A:
                coll_end_a.append(r"^"+subject_regex + object_regex+"$")

        coll_end_e = []
        for subject_regex in self._qu_e:
            coll_end_e.append(r"^"+subject_regex+"$")
        for object_regex in self._qu_obj:
            coll_end_e.append(r"^"+object_regex+"$")
            for subject_regex in SUBJ_KU_E:
                coll_end_e.append(r"^"+subject_regex + object_regex+"$")

        coll_end_y = []
        for subject_regex in self._qu_y:
            coll_end_y.append(r"^"+subject_regex+"$")
        for object_regex in self._qu_obj:
            coll_end_y.append(r"^"+object_regex+"$")
            for subject_regex in SUBJ_KU_Y:
                coll_end_y.append(r"^"+subject_regex + object_regex+"$")

        coll_end_na = []
        for subject_regex in SUBJ_KU_A:
            coll_end_na.append(r"^"+subject_regex+"$")
            coll_end_na.append(r"^"+subject_regex + OBJ_ALL_KU+"$")
        coll_end_na.append(r"^"+OBJ_ALL_KU+"$")

        coll_end_ne = []
        for subject_regex in SUBJ_KU_E:
            coll_end_ne.append(r"^"+subject_regex+"$")
            coll_end_ne.append(r"^"+subject_regex + OBJ_ALL_KU+"$")

        coll_end_ny = []
        for subject_regex in SUBJ_KU_Y:
            coll_end_ny.append(r"^"+subject_regex+"$")
            coll_end_ny.append(r"^"+subject_regex + OBJ_ALL_KU+"$")

        # map to each of six end-string it's list of possibilities
        coll_comb = []
        if self._end_a != "":
            coll_comb.append([self._n_end_a, coll_end_na])
            coll_comb.append([self._end_a, coll_end_a])
        if self._end_e != "":
            coll_comb.append([self._n_end_e, coll_end_ne])
            coll_comb.append([self._end_e, coll_end_e])
        if self.perfective != "":
            coll_comb.append([self._n_end_y, coll_end_ny])
            coll_comb.append([self._end_y, coll_end_y])
        self.comb = coll_comb

    def get(self, attribut):
        """give back attributes"""
        if attribut == "dbid":
            return self.dbid
        if attribut == "lemma":
            return self.lemma
        if attribut == "stem":
            return self.stem
        if attribut == "perfective":
            return self.perfective
        if attribut == "alternatives":
            return self.alternatives
        if attribut == "comb":
            return self.comb
        if attribut == "proverb":
            return self.proverb
        if attribut == "unclear":
            return self.unclear
        return "Hm, does class Verb has this feature?"


def prepare_verb_alternativ(row):
    """takes: id,lemma,alternative_stem,alternativ_perfectif
    returns row for the alternatively spelled verb
    """
    row_a = row.copy()
    stem_a = row.get('alternative_stem')
    perf_a = row.get('alternative_perfective')
    # lemma = row.get('lemma')
    perfective_a = ""
    if perf_a != "":
        if len(stem_a) > len(perf_a)+1:
            # only short version of perfective is given
            # find the last vowel before the ending a:
            for count_back in range(len(stem_a)-2, 0, -1):
                if stem_a[count_back] in "aeiou":
                    perfective_a = stem_a[:count_back+1]+perf_a
                    break
            # stem_a has only 2 vowels: the very first letter and the ending a
            if perfective_a == "" and stem_a[0] in "aeiou":
                perfective_a = stem_a[:1]+perf_a
        else:
            # long version of perfective is already given
            perfective_a = perf_a
    else:
        perfective_a = ""
    # suppose the first letter of stem and stem_alternative is always the same:
    # lemma_a = lemma[:2]+stem_a
    row_a.update({# 'lemma': lemma_a,
                  'stem': stem_a,
                  'perfective': perfective_a,
                  'alternatives': "x"})
    return row_a


def filter_proverbs_out(verb_list):
    """
    only verbs without blank pass to the list
    """
    # sort by length of lemma to have proverbs later than pur verbs
    verbs = sorted(verb_list, key=lambda x: len(x.lemma))
    pur_stems = []
    new_list = []
    for verb in verbs:
        try:
            verb.mark_proverb()
            if verb.proverb is False:
                new_list.append(verb)
                pur_stems.insert(0, verb.stem)
                continue
            # verb-part of proverb maybe already as pure infinitiv in the list?
            if verb.stem in pur_stems:
                # we can skip it
                continue
            # there is no pure version in the list, we take it
            new_list.append(verb)
            pur_stems.append(verb.stem)
        except Exception:
            # Translators: (debug) check dictionary new entry
            kh.OBSERVER.notify_error(kh._(
                "Attention: filter proverbs out doesn't work with '{}'. Check "
                + "also its alternatives in the database.").format(verb.lemma))
    return new_list


def filter_passiv_out(verb_list):
    """because it's not really a lemma and will be asked with its base form
    """
    # sort by length of lemma to have passiv later than base form
    verbs = sorted(verb_list, key=lambda x: x.lemma)
    baseforms = []
    new_list = []
    for verb in verbs:
        verb.mark_passiv()
        try:
            if verb.passiv is False:
                new_list.append(verb)
                baseforms.insert(0, verb.stem)
                continue
            # base form is already in the list?
            if verb.stem[:-2]+"a" in baseforms:
                # kunywa is not passiv of kunya
                if verb.lemma == "kunywa":
                    new_list.append(verb)
                # we can skip the others
                continue
            # there is no base form in the list, we take it
            new_list.append(verb)
            baseforms.append(verb.stem)
        except Exception:
            # Translators: (debug) check dictionary new entry
            kh.OBSERVER.notify_error(
                kh._("filter passiv out doesn't work': {}").format(verb.lemma))
    return new_list


def collect_verbs(db_verbs, freq_simple_dict):
    """sorts verbforms to their stem
    takes fdist as a dict and returns also dict"""

    freq_uncollected = freq_simple_dict.copy()
    collect_unclear_things = ["things that didn't match\n",]
    # sort by length of stem, for better hits
    verben = sorted(db_verbs, key=lambda x: len(x.stem), reverse=True)
    points = 0
    lemma_count = 0
    collection = []
    collection_x = []

    # to exclude faster:
    # check first the stem of verbs and afterwards the prefixes
    # variants of ends are:
    #   |      a         |     e     |        y         |   stem   |
    # (((passiv,infinitiv,subjunctiv),passiv,perfective), imperativ)

    # all prefix-regex
    #         subj_ku_a, subj_ku_e, subj_ku_y,
    #         subj_gu_a, subj_gu_e, subj_gu_y,
    #         subj_kw_a, subj_kw_e, subj_kw_y
    # obj_ku, obj_gu, obj_kw, obj_all_ku = regex_prfx_obj_verbs()

    # (((passiv+indikativ,subjunctiv),perfective+passiv), imperativ) + Suffix

    '''
    1. sin            +obj?  +trunk [kw|gu|ku|r|h|mn] xx

    2. nt? u|ba              +trunk [kw|gu|ku]        x
    3. nt? u|ba        +obj  +trunk [kw|gu|ku|r|h|mn] xx
    4. nt? u|ba +time1       +trunk [kw]
    5. nt? u|ba +time1 +obj  +trunk [kw|gu|ku|r|h|mn] xx
    6.     u|ba +time2       +trunk [kw]
    7.     u|ba +time2 +obj  +trunk [kw|gu|ku|r|h|mn] xx

     8.    uwu               +trunk [kw|gu|ku]        xx
     9.    uwu         +obj  +trunk [kw|gu|ku|r|h|mn] xx
    10.    uwu  +time3       +trunk [kw|gu|ku]        xx
    11     uwu  +time3 +obj  +trunk [kw|gu|ku|r|h|mn] xx


    gukora:                        subj_ba,uwu         obj             sinkora,kirakora
    kumeneka,kunegura:             sin,                obj             simanuka
    kugira:                        subj_ba,uwu         obj
    kwandika,kwoza,kwiheruka:      subj_ba,subj_u,uwu  obj, time
    guha:                          sin,                obj,    trunk   urampa
    kureka:                                                    trunk   ndeka
    '''

    for verb in verben:
        freqsum = 0
        found = []

        # ((%time1+subj|%subj+time2) %obj? (%stem[:-1]wae, %perfw) | %stem_only))(ho yo ko mwo))
        '''
        1. ends with end_aey or n_end_aey ?
        2. if yes: analyse all before
        3. if it ends but we don't have yet a box for it:
            collect for later analysis
        '''
        # for short verbs
        # to include kuba, -ri
        # but excluding hari ('h' not in 'gk-'), kuhaba (len 6)

        if len(verb.stem) == 2 \
            and verb.lemma[0] != 'h' \
                and len(verb.lemma) < 5:
            qu_list_for_short_freqs = \
                [sd.breakdown_consonants(x + verb.stem) for x in "naiu"]
            if len(verb.lemma) == 4:
                qu_list_for_short_freqs.append(verb.stem)
        # coll_comb = [x for x in coll_comb if x[0] not in [n_end_a, n_end_e]]
        else:
            qu_list_for_short_freqs = []

        for freqtype, num in freq_uncollected.items():
            # for short freqtypes
            if num != 0 and len(freqtype) < 4 and qu_list_for_short_freqs:
                for quest in qu_list_for_short_freqs:
                    if freqtype == quest:
                        freqsum += num
                        found.append([freqtype, num])
                        freq_uncollected.update({freqtype: 0})
                        num = 0
                        break  # next freqtype
            # for n/end_a, n/end_e, n/end_y
            ask_begin = False
            # comb is list of 6 elements, each: [end, questions for this end]
            for end_aey in verb.comb:
                if num == 0:
                    break  # next freqtype
                end = end_aey[0]
                # freq ends like verb ends?
                if re.search(end, freqtype) is not None:
                    ask_begin = True
                    # check begin
                    part1 = re.sub(re.search(end, freqtype).group(), "", freqtype)
                    # is there nothing else?
                    if part1 == "":
                        # is pure Imperative
                        freqsum += num
                        found.append([freqtype, num])
                        freq_uncollected.update({freqtype: 0})
                        num = 0
                        ask_begin = False  # no break here, the end_loop
                        # has to go on, it will break above with num==0
                    # there is at least one letter before the end
                    else:
                        # check each question of this end
                        for qu in end_aey[1]:
                            if re.search(qu, part1) is not None:
                                freqsum += num
                                found.append([freqtype, num])
                                freq_uncollected.update({freqtype: 0})
                                num = 0
                                ask_begin = False
                                break  # next end/ loop breaks above >> next freqtype
                if ask_begin is True:
                    collect_unclear_things.append([verb.lemma, end, freqtype])
                    ask_begin = False

        if freqsum > 0:
            # alphabetical
            found.sort()
            # head of line
            found = [verb.lemma, verb.dbid, "VERB", freqsum, len(found)]+found
            if verb.alternatives == ["x"]:
                # id has two variants of writing the verb,
                # collect all of those verbs here
                collection_x.append(found)
            else:
                collection.append(found)

        # progress bar ;-)
        points, lemma_count = kh.show_progress(points,
                                               lemma_count, len(verben))

    collection_x = put_alternatives_of_same_id_together(collection_x)
    collection += collection_x

    # lemma, id, PoS, sum of all ocurrences, number of different types, types
    #     collection sorted: 1. sum of types 2. by numbers of different types
    #     per lemma: types sorted alphabetically
    if collection:
        collection.sort(key=lambda x: x[3], reverse=True)
        collection.sort(key=lambda x: x[4], reverse=True)
        freq_uncollected = {
            x: y for x, y in freq_uncollected.items() if y != 0}

    # kh.save_list(collection, "found6_verbs.csv", ";")
    # save_dict(freqVerb, "keine6_verbs.csv")

    # kh.save_list(unk_verbform, "unk_verbform.csv")
    # kh.save_list(unk_perf, "unk_perfective.csv")
    return (collection, freq_uncollected)


def put_alternatives_of_same_id_together(collection):
    """sums up and adds found types of variants to same ID
    """
    # put both variants of lemma together and add this to the big collection
    coll = []
    # sort by id, so the variants become neighbours
    collection.sort(key=lambda x: str(x[1]))
    # create an element to have something to compare the first element with
    collection.insert(0, ["some data", "-1", "to compare with first element"])
    for i in range(1, len(collection)):
        if collection[i][1] == collection[i-1][1]:
            # add sums (or should we count them again?)
            collection[i-1][3] += collection[i][3]
            # add numbers of types
            collection[i-1][4] += collection[i][4]
            # discard i-1
            coll.pop(-1)
            # replace it with sum of both
            coll.append(collection[i-1] + collection[i][5:])
        # only one of id_0 or its id_a found something
        else:
            coll.append(collection[i])
    return coll
