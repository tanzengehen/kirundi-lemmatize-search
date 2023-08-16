#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 29 10:13:10 2023

@author: doreen
"""

from unidecode import unidecode
import re
import kir_string_depot as sd


REGEX_SUFFIX = r"((([hyk]|mw)o)?$)"

class Lemma:
    """sets: db-ID, lemma, stem, POS, alternative spellings
    """
    def __init__(self, row):
        columns = [0,  # entry0-id
                   1,  # entry1-lemma
                   4,  # entry2-stem
                   8,  # entry3-POS
                   13] # entry4-list with alternatives
        entry = [unidecode(row[x].strip().lower()) for x in columns]
        pos_dict = {"0":"VERB", "1":"NOUN", "2":"ADJ", "3":"PREP", "5":"PRON",
                    "6":"ADV", "7":"CONJ", "8":"INTJ", "9":"PHRASE", "10":"PREFIX"}
        self.dbid = entry[0]
        self.lemma = entry[1]
        self.pos = pos_dict.get(entry[3])
        if entry[2]:
            self.stem = entry[2]
        else:
            print(f"lemma has no stem in database: ID{self.dbid}")
            self.stem = "xxx"
        if entry[4]:
            self.alternatives = entry[4].split(";")
        else:
            self.alternatives =""
        self.questions = [self.lemma,]
    def __str__(self):
        return f"lemma= {self.lemma}, ID={ self.dbid}, POS= {self.pos}, stem= {self.stem}, "\
               +f"alternatives= {self.alternatives} "\
               +f"questions: {self.questions}"
    def __repr__(self):
        return f"lemma={self.lemma}, dbid={self.dbid}, POS= {self.pos}, stem= {self.stem}, "\
                   +f"alternatives={self.alternatives}, "\
                   +f"len(questions)={len(self.questions)}"


def regex_prfx_autonom_subjects_verbs():
    """ regex for autonomous verbform
    """
    ####### autonom subjects ########

    #time3 (only possibility for time in this forms) uwu-ta-:
    #    uwa, uwara, uwuta, uwutara, uwo, uwuto, uwuzo, !uwutazo,
    #, uwuki, uwutaki, uwuka?
    #       uwagira, uwagize / uwaragira, uwaragize
    #       uwutagira, uwutagize / uwutaragira, uwutaragize
    #       uwogira, uwogize / uwutogira, uwutogize
    #       uwuzokora, uwuzokoze / uwutazogira, uwutazogize
    #       () / ()
    #       uwukigira, uwukigize / uwutakigira, uwutakigize

    #that means:
    #uwO, uwA, uwAra, uwuTa, uwuTara, uwuTaki, uwuKi, uwuTo, uwuZo
    #abo, aba, abara, abata, abatara, abataki, abaki, abato, abazo
    #ivyo, ivya, ivyara, ibita, ibitara, ibitaki, ibiki, ibito, ibizo
    #uwandika, ubwandika, ivyiruka, iryiruka, abandika, iciruka
    #       +stem or perfektive
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
        regex_atn_negtime_gu +")|"+regex_ibi_gu+")"
    regex_ay_ibi_infx_kw = r"(("+regex_ivy_kw+"((o(kw)?)|(a(ra)?))?)|("+\
        regex_ibi_ku + regex_atn_negtime_kw +"))"
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
    #ay_ku
    for i in [subj_ku_a, subj_ku_y]:
        i.append(r"("+re_all_class_subj+"ka(na)?)")
    #ay_gu
    for i in [subj_gu_a, subj_gu_y]:
        i.append(r"("+re_all_class_subj+"kana|"+re_all_class_subj+"ga)")
    #ay_kw
    for i in [subj_kw_a, subj_kw_y]:
        i.append( r"("+re_all_class_subj+"k(an)?)")

    ##################################################################
    ###### n time_1 for stem-ends aey #########
    # after n may change next letter
        # vor gu_tkcsz,ku_dgjy, obj_norm(tkzdgy):
    # nda(ca)- ndaka- na- nara- (si)na- (si)no- (si)nzo- (si)nda-
    for i in [subj_ku_a, subj_ku_e, subj_ku_y,
              subj_gu_a, subj_gu_e, subj_gu_y]:
        #aey_kgo
        i.append("((si)?)")
        #aey_kg
        i.append(r"((nda([ckg]a)?)|nara|((si)?n([ao]|zo)))")

    # before kw_aeiou instead of a may come kw,y
    #aey_kw
    for i in [subj_kw_a, subj_kw_e, subj_kw_y]:
        i.append(r"(nd(a[ck])?|nar|((si)?n((a?y)|((a|(z?o))(kw)?))))")

    '''regex_aey_sin = r")"
    # n disappears, if n is last letter before   ku_mn, guh
    # n will be asked with only_stem 
    regex_aey_sin_mnhr  = r"(si)?" '''

    #only for stem_end e: ndaka- sinka- sinkana- ni-
    #e_ku
    subj_ku_e.append(r"(ndaka|sinka(na)?|nin)")
    regex_e_n_mnh = r"(ndaka|sinka(na)?|ni)" #??? noch eintragen !!
    #e_gu
    subj_gu_e.append(r"(ndaga|sin(g|kan)a|nin)")
    #e_kw
    subj_kw_e.append(r"(ndak|sink(an)?|nin)")
    # ndandika tse / ndakandika tse
    # narandika tse / sinandika tse
    # nandika tse / nandika tse
    # nokwandika tse / nzokwandika  nzokwanditse
    # ncandika tse / sincandika tse
    # sinzokwandika, sinokwandika tse,

    # insert kw also with kwi- or kwo-verb
    #kwoza nokwoza, nokwogeje   nzokwoza
    #kwiruka nokwiruka nokwirutse nzokiruka

    # ndamira tse / ndakamira tse
    # naramira tse / sinamira tse
    # mira mize / namira tse                 #collect mira with imperatives, mize!!
    # nomira tse / nzomira  nzomiye
    # (for all ab n-) sinzomira, sinomira tse,

    # ndagira ze / ndakagira (ze not)
    # naragira tse / sinagira ze
    # ngira ze / nagira ze
    # nogira ze / nzogira  nzogize
    # sinzogira, sinogira ze

    ####### time1 after ntu: ntiwa, ntura for stem-ends ae, ntiwo, ntuzo, ntuki #######

    # for stem-end e:
    # ntuka- ntukana- nu-      for gu,guh,  ku,kur,kum/n  kw
    #nu for: höfl.Imperativ, na will be asked with (si)?na
    #ka for: du sollst niemals... +e
    #e_ku
    subj_ku_e.append(r"((nt[aiu]ka(na)?)|n[ui])")
    #e_gu
    subj_gu_e.append(r"(nt[aiu](ga|kana)|n[ui])")
    #e_kw
    subj_kw_e.append(r"((nt[aiu]k(an)?)|n(uw|[ai]y))")
    # ntugakore, ntukagire, ntukandike, ntukoze, ntukiruke
    # nukore, nugire, nuwandika, niyoze, nayiruke

    # for stem-ends aey
    # (nt)u- (nt)uzo-           for gu,guh,ku,kur,kumn,kw
    #aey_kg
    for i in [subj_ku_a, subj_ku_e, subj_ku_y,
              subj_gu_a, subj_gu_e, subj_gu_y]:
        i.append(r"((nt)?[uai](zo)?)")
    #aey_kw
    for i in [subj_kw_a, subj_kw_e, subj_kw_y]:
        i.append(r"((nt)?(i([wy]|(z(okw)?))|[ua](z(okw)?)))")

    # for stem-ends ay
    # else rak will be asked before ra-kw
    #ay_kw
    for i in [subj_kw_a, subj_kw_y]:
        i.append(r"([uai]ra[ktr]w?)")
    # wara- (nti)wa- (nti)wo- (nt)ura- ukazo-
    #ay_kg
    for i in [subj_ku_a, subj_ku_y,
              subj_gu_a, subj_gu_y]:
        i.append(r"([wy]ara|(nti)?[wy][ao]|(nt)?[uai](ra)|[uai]kazo)")
    # kw will be asked with bi_kw

    # for stem-end a
    # uraka-
    #a_kg
    for i in [subj_ku_a, subj_gu_a]:
        i.append(r"([uai]raka)")
    # kw with ay, else rak will be asked before ra-kw

    #time1
    # for stem-end e:       ntibika-  n(t)ibi-
    #e_ku
    subj_ku_e.append(r"((nti"+regex_bi_ku+"(ka)?)|(ni"+regex_bi_ku+"))") #ntibi(ka)gende, nimugende
    #e_gu
    subj_gu_e.append(r"((nti"+regex_bi_ku+"ga)|(nt?i"+regex_bi_gu+"))")  #ntitugakore, n(t)idukore
    #e_kw
    subj_kw_e.append(r"((nti"+regex_bi_ku+"k)|(nt?i"+regex_bi_kw+"))")   #ntukandike, n(t)ukiruke

    # for stem-ends aey:    (nti)bi, (nti)bizo, (nti)vya
    #aey_ku
    for i in [subj_ku_a, subj_ku_e, subj_ku_y]:
        i.append(r"((nti)?"+regex_bi_ku+"(zo)?|("+regex_bi_kw+"a))")
    #aey_gu
    for i in [subj_gu_a, subj_gu_e, subj_gu_y]:
        i.append(r"((nti)?("+regex_bi_gu+"|"+regex_bi_ku+"zo|"+regex_bi_kw+"a(kw)?))")
    #aey_kw
    for i in [subj_kw_a, subj_kw_e, subj_kw_y]:
        i.append(r"((nti)?("+regex_bi_kw+"(ay)?|"+regex_bi_ku+"(z(okw)?)))")
    # for stem-ends ay:     vyara (nti)vyo (nti)bira bikazo
    #ay_kg
    for i in [subj_ku_a, subj_ku_y,
              subj_gu_a, subj_gu_y]:
        i.append(r"("+regex_bi_kw+"ara|(nti)?("+regex_bi_kw+"o|"+\
                 regex_bi_ku+"ra)|"+regex_bi_ku+"kazo)")
    #ay_kw
    for i in [subj_kw_a, subj_kw_y]:
        i.append(r"("+regex_bi_kw+"ar|(nti)?("+regex_bi_kw+"o(kw)?|"+\
                 regex_bi_ku+"[rc])|"+regex_bi_ku+"kaz(okw)?)")
    #a_kw
    subj_kw_a.append(r"("+regex_bi_ku+"ra[ktr]w?|sind)")
    # for stem-end a:       biraka
    #a_ku
    subj_ku_a.append(r"("+regex_bi_ku+"raka|sinda)")
    #a_gu
    subj_gu_a.append(r"("+regex_bi_ku+"raga|sinda)")
       # kw also with y because of object

    #time1 after nti:
    #kugenda
    #       bigendae, bigiye / ntibigendae, ntibigiye
    #       bizogendae, bizogiye / ntibizogendae, ntibizogiye
    #       ((vyagenda, vyagiye)) /ntivyagenda, ntivyagiye
    #       ((vyogenda, vyogiye)) /  ntivyogenda, ntivyogiye
    #       ((vyaragenda, vyaragiye)) /()
    #       ((biragenda, biragiye)) / ntibiragenda, ntibiragiye
    #       bikazogenda, bikazogiye

    #time2
    # ra raca raka ta tara!!! taki tazo ki zo to
    # n, u bi
    #aey_ku
    for i in [subj_ku_a, subj_ku_e, subj_ku_y]:
        i.append(r"(n((da([ck]a)?)|ta(ra|ki|zo)?|ki|zo|to))")
        i.append(r"(("+regex_bi_ku+"|[uai])((ra([ck]a)?)|ta(ra|ki|zo)?|ki|zo|to))")
    #aey_gu
    for i in [subj_gu_a, subj_gu_e, subj_gu_y]:
        i.append(r"(n((da([ck]a)?)|da|((ta)?(ra|ki|zo))|to))")
        i.append(r"(("+regex_bi_ku+"|[uai])((ra([ck]a)?)|da|((ta)?(ra|ki|zo))|to))")
    #aey_kw
    for i in [subj_kw_a, subj_kw_e, subj_kw_y]:
        i.append(r"(n((d(a[ck]?))|((ta)?(r|c|([zt](okw)?)))))")
        i.append(r"(("+regex_bi_ku+"|[uai])((ra[ck])|r|((ta)?([rc]|([zt](okw)?))))?)")

    # plus the regex for autonom forms
    (regex_ay_ibi_infx_ku,
     regex_ay_ibi_infx_gu,
     regex_ay_ibi_infx_kw) = regex_prfx_autonom_subjects_verbs()
    #ay_ku
    for i in [subj_ku_a, subj_ku_y]:
        i.append(regex_ay_ibi_infx_ku)
    #ay_gu
    for i in [subj_gu_a, subj_gu_y]:
        i.append(regex_ay_ibi_infx_gu)
    #ay_kw
    for i in [subj_kw_a, subj_kw_y]:
        i.append(regex_ay_ibi_infx_kw)

#??? aey sortieren nach nächstem Durchlauf, mal sehen, was kommt
# problem with kw: single krt here, will not search for kw,rw,tw in object !

    #time2 with u-ta-: ((wa)), ((wara)), ((wo)), ((ura)),        ((=asked above))
    #       uta, utara!, uto, utazo!, uraca, uraka!, utaki, uki!, uka
    #       bita, bitara, bito, bitazo, biraca, biraka, bitaki, biki
    #kugira:
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
    #       ((wo:  wokwiruka, wokwirutse)) /  utazo: utaziruka, utazokwiruka, utazokwirutse
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

    obj_ku.append(r"(" +n_norm_ku +"(ha)?)")
    obj_gu.append(r"(n" +norm_gu +")")
    obj_kw.append(r"(n" +norm_kw +")")

    obj_gu.append(r"(" +n_norm_ku +"ha)")
    obj_kw.append(r"(" +n_norm_ku +"h)")

    # exception2: ba bi bu
    b_kg = r"(b[aiu])"
    b_kw = r"(bw|vy|b)"
    nb_kg = r"(mb[aiu])"
    for i in [obj_ku, obj_gu]:
        i.append(r"(" +nb_kg +"(ha)?)")
    obj_kw.append(r"(m(bw|vy|b))" )   # problem: sorts bivuga to kwivuga(ba), instead to kuvuga(bi)
    obj_kw.append(r"(" +nb_kg +"h)")

    # exception3: ri ru
    r_kg = r"(r[iu])"
    r_kw = r"(r[yw])"
    nr_kg = r"(nd[iu])"
    for i in [obj_ku, obj_gu]:
        i.append(r"("+nr_kg+"(ha)?)")
    obj_kw.append(r"(nd[yw])")       #ba-n-ru-andika ba-n-ri-andika
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
    obj_all_ku = r"(" +b_kg+"|"+r_kg+"|mu|ha|"+norm_ku+")"
    obj_ku.append(obj_all_ku)
    obj_ku.append(r"(" +obj_all_ku +"{1,2}(ha)?)")
    for i in [obj_ku, obj_gu]:
        i.append(r"(" +obj_all_ku + obj_nh_kg +")")
    obj_all_gu = r"(" +b_kg+"|"+r_kg+"|mu|ha|"+norm_gu+")"
    obj_gu.append(obj_all_gu)
    obj_gu.append(r"(" +obj_all_ku +"?" +obj_all_gu +")")
    obj_gu.append(r"(" +obj_all_ku +"{1,2}ha)")

    obj_all_kw = r"(" +b_kw+"|"+r_kw+"|mu|ha|"+norm_kw+")"
    obj_kw.append(obj_all_kw)
    obj_kw.append(r"(" +obj_all_ku +"?" +obj_all_kw +")")
    obj_kw.append(r"(" +obj_all_ku +"{1,2}h)")
    obj_kw.append(r"(" +obj_all_ku + obj_nh_kw +")")

    #obj_all_n = r"(" +obj_all_ku +"n)"        #??? wird durch n_end erledigt
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
        self.perfective = unidecode(row[5].strip().lower())
        self.set_qu()

    def __str__(self):
        return f"lemma={self.lemma}, ID={self.dbid}, POS= {self.pos}, stem='{self.stem}', "\
               +f"perfective= -{self.perfective}, alternatives={self.alternatives}, "\
               +f"comb_set={self.comb is not None}"#": {len(self.comb)}"
    def __repr__(self):
        return f"lemma={self.lemma}, dbid={self.dbid}, "\
                   +"POS= {self.pos},\t-{self.stem} / -{self.perfective},\t"\
                   +f"alternatives={self.alternatives}, "\
                   +f"comb_set={self.comb is not None}"#, len(comb)={len(self.comb)}"
    def mark_proverb(self):
        """ mark verbs with ' ' in lemma as proverb 
        and accept at stem and perfective only first part
        """
        # lemma has more than one part
        if self.lemma.find(" ") > -1 :
            #save full lemma for later
            self.proverb = True
            # first part is hopefully verb-part
            if self.stem.find(" ") :
                self.stem = self.stem.split()[0]
            # cut also perfective
            if self.perfective.find(" ") :
                self.perfective = self.perfective.split()[0]
        if self.perfective is None :
            print("perfective is lost: ", self.lemma)
        else :
            self.perfective = self.perfective.strip()
        # if perfective is unclear
        if self.perfective.find("?") > -1 :
            print(self.lemma+": perfective?", self.perfective, ".")
            self.unclear.append([self.lemma, "perfective unclear:", self.perfective])
            self.perfective = None
    def mark_passiv(self):
        if self.lemma[-2] =="w":
            self.passiv = True
    def _set_end_of_ends(self):
        """sets regex-strings for three possible endforms of the verb including passiv, subjunctiv,
        perfective, perfective passive and each with direction-suffixes
        these are: end_a, end_e, end_y (each is string)
        """
        # add passiv to indikativ: end_a
        self._end_a = self.stem[:-1] +r"(w?a)" + REGEX_SUFFIX
        # make subjunctiv: end_e
        self._end_e = self.stem[:-1]+"e" + REGEX_SUFFIX
        # add passiv to perfective: end_y
        if self.perfective == "" :
            perfp = ""
        else :
            if len(self.perfective) > 3 and self.perfective [-2] == "y" :
                if self.perfective [-3] in ["m","n"] :
                    perfp= self.perfective[:-1]+r"(w?e)"
                elif self.perfective [-3] in ["a","i","e","o"] :
                    perfp = self.perfective[:-2]+r"([yw]e)"
                elif self.perfective [-3] == "u" :
                    perfp = self.perfective[:-2]+r"(ye|((ri)?we))"
                elif self.perfective [-3] == "v" :
                    perfp = self.perfective[:-3]+r"(vye|bwe)"
                else :
                    self.unclear.append(["perfective: unexpected letter before [y] ",\
                                         self.lemma, self.perfective])
                    print("unk vor y", self.lemma, self.perfective)
                    perfp = self.perfective
            elif len(self.perfective) > 3 and self.perfective[-2] in ["j","z","s","h","w"] :
                perfp = self.perfective[:-1]+r"((w)?e)"
            else :
                self.unclear.append(["perfective: unexpected letter before last letter:",
                                     self.lemma, self.perfective])
                #print("unk -2", self.lemma, self.perfective)
                perfp = self.perfective
        if perfp =="" :
            self._end_y =""
        else:
            self._end_y = perfp + REGEX_SUFFIX

        # special cases
        if self.stem == "ti" :
            self._end_a = self.stem + REGEX_SUFFIX
            self._end_e, self._end_y = "", ""
            self._qu_obj = ""
        elif self.stem == "ri" :
            self._end_a = self.stem + REGEX_SUFFIX
            self._n_end_a = "ndi" + REGEX_SUFFIX
            self._end_e, self._end_y = "", ""
            self._qu_obj = "ha"
        elif self.stem == "zi" :
            self._end_a = "zw?i"+ REGEX_SUFFIX
            self._end_e, self._end_y = "", ""
        elif self.stem in ["fise","fitiye"] :
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
        if self.stem[0] in r"[bdgjmnrvyz]" :
            # each is list of strings
            self._qu_a = SUBJ_KU_A
            self._qu_e = SUBJ_KU_E
            self._qu_y = SUBJ_KU_Y
            self._qu_obj = OBJ_KU
            stem_consonant = {"r":"nd", "b":"mb", "v":"mv", "m":"m", "n":"n"}
            # ends are strings
            if self.stem[0] in stem_consonant.keys() :
                self._n_end_a = stem_consonant.get(self.stem[0])+self._end_a[1:]
                self._n_end_e = stem_consonant.get(self.stem[0])+self._end_e[1:]
                self._n_end_y = stem_consonant.get(self.stem[0])+self._end_y[1:]
            else :
                self._n_end_a = r"n" +self._end_a
                self._n_end_e = r"n" +self._end_e
                self._n_end_y = r"n" +self._end_y
        # == "gu" :
        elif self.stem[0] in r"[cfhkpst]" :
            self._qu_a = SUBJ_GU_A
            self._qu_e = SUBJ_GU_E
            self._qu_y = SUBJ_GU_Y
            self._qu_obj = OBJ_GU
            stem_consonant = {"p":"mp", "f":"mf", "h":"mp"}
            # breakdown rules for gu-
            if self.stem[0] in stem_consonant.keys() :
                self._n_end_a = stem_consonant.get(self.stem[0])+self._end_a[1:]
                self._n_end_e = stem_consonant.get(self.stem[0])+self._end_e[1:]
                self._n_end_y = stem_consonant.get(self.stem[0])+self._end_y[1:]
            else :
                self._n_end_a = r"n" +self._end_a
                self._n_end_e = r"n" +self._end_e
                self._n_end_y = r"n" +self._end_y
        # == "kw" :
        elif self.stem[0] in r"[aeiou]" :
            self._qu_a = SUBJ_KW_A
            self._qu_e = SUBJ_KW_E
            self._qu_y = SUBJ_KW_Y
            self._qu_obj = OBJ_KW
            self._n_end_a = r"ny?" +self._end_a
            self._n_end_e = r"ny?" +self._end_e
            self._n_end_y = r"ny?" +self._end_y


    def set_qu(self):
        """ combines beginnning-possibilities to it's equivalent end
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
        for subject_regex in self._qu_a :
            coll_end_a.append(r"^"+subject_regex+"$")
        for object_regex in self._qu_obj:
            coll_end_a.append(r"^"+object_regex+"$")
            for subject_regex in SUBJ_KU_A :
                coll_end_a.append(r"^"+subject_regex + object_regex+"$")

        coll_end_e = []
        for subject_regex in self._qu_e :
            coll_end_e.append(r"^"+subject_regex+"$")
        for object_regex in self._qu_obj:
            coll_end_e.append(r"^"+object_regex+"$")
            for subject_regex in SUBJ_KU_E :
                coll_end_e.append(r"^"+subject_regex + object_regex+"$")

        coll_end_y = []
        for subject_regex in self._qu_y :
            coll_end_y.append(r"^"+subject_regex+"$")
        for object_regex in self._qu_obj:
            coll_end_y.append(r"^"+object_regex+"$")
            for subject_regex in SUBJ_KU_Y :
                coll_end_y.append(r"^"+subject_regex + object_regex+"$")

        coll_end_na =[]
        for subject_regex in SUBJ_KU_A :
            coll_end_na.append(r"^"+subject_regex+"$")
            coll_end_na.append(r"^"+subject_regex + OBJ_ALL_KU+"$")
        coll_end_na.append(r"^"+OBJ_ALL_KU+"$")

        coll_end_ne =[]
        for subject_regex in SUBJ_KU_E :
            coll_end_ne.append(r"^"+subject_regex+"$")
            coll_end_ne.append(r"^"+subject_regex + OBJ_ALL_KU+"$")

        coll_end_ny =[]
        for subject_regex in SUBJ_KU_Y :
            coll_end_ny.append(r"^"+subject_regex+"$")
            coll_end_ny.append(r"^"+subject_regex + OBJ_ALL_KU+"$")

        # map to each of six end-string it's list of possibilities
        coll_comb = []
        if self._end_a != "" :
            coll_comb.append([self._n_end_a, coll_end_na])
            coll_comb.append([self._end_a, coll_end_a])
        if self._end_e != "" :
            coll_comb.append([self._n_end_e, coll_end_ne])
            coll_comb.append([self._end_e, coll_end_e])
        if self.perfective != "" :
            coll_comb.append([self._n_end_y, coll_end_ny])
            coll_comb.append([self._end_y, coll_end_y])
        self.comb=coll_comb

    def get(self, attribut):
        """give back attributes"""
        if attribut == "dbid" :
            return self.dbid
        if attribut == "lemma" :
            return self.lemma
        if attribut == "stem" :
            return self.stem
        if attribut == "perfective" :
            return self.perfective
        if attribut == "alternatives" :
            return self.alternatives
        if attribut == "comb" :
            return self.comb
        if attribut == "proverb" :
            return self.proverb
        if attribut == "unclear" :
            return self.unclear
        return "Hm, does class Verb has this feature?"


def prepare_verb_alternativ(row):
    """takes: id,lemma,alternative_stem,alternativ_perfectif
    returns row for the alternatively spelled verb
    """
    row_a = [i for i in row]
    stem_a = row[15]
    perf_a = row[16]
    lemma = row[1]
    perfective_a = ""
    if perf_a != "" :
        if len(stem_a) > len(perf_a)+1:
        # only short version of perfective is given
            # find the last vowel before the ending a:
            for count_back in range(len(stem_a)-2,0,-1):
                if stem_a[count_back] in ["a","e","i","o","u"] :
                    perfective_a = stem_a[:count_back+1]+perf_a
                    break
            # stem_a has only 2 vocals: the very first letter and the ending a :
            if perfective_a == "" and stem_a[0] in ["a","e","i","o","u"] :
                perfective_a = stem_a[:1]+perf_a
        else:
        # long version of perfective is already given
            perfective_a = perf_a
    else : perfective_a = ""
    # suppose the first letter of stem and stem_a is always the same:
    lemma_a = lemma[:2]+stem_a
    row_a[0] = str(row[0])+"_a"     #  0 id
    row_a[1] = lemma_a              #  1 lemma
    row_a[4] = stem_a               #  4 stem
    row_a[5] = perfective_a         #  5 perfectiv
    row_a[13] = ""                  # 13 alternatives
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
        verb.mark_proverb()
        try:
            if verb.proverb is False:
                new_list.append(verb)
                pur_stems.append(verb.stem)
                continue
            # verb-part of proverb maybe already as pure infinitiv in the list?
            if verb.stem in pur_stems :
                # we can skip it
                continue
            # there is no pure version in the list, we take it
            new_list.append(verb)
            pur_stems.append(verb.stem)
        except Exception:
            print("filter proverbs klappt nicht:", verb)
    return new_list

def filter_passiv_out(verb_list):
    # sort by length of lemma to have proverbs later than pur verbs
    verbs = sorted(verb_list, key=lambda x: len(x.lemma))
    pur_stems = []
    new_list = []
    for verb in verbs:
        verb.mark_passiv()
        try:
            if verb.passiv is False:
                new_list.append(verb)
                pur_stems.append(verb.stem)
                continue
            # verb without passiv maybe already as pure infinitiv in the list?
            if verb.stem in pur_stems :
                # we can skip it
                continue
            # there is no pure version in the list, we take it
            new_list.append(verb)
            pur_stems.append(verb.stem)
        except Exception:
            print("filter passiv klappt nicht:", verb)
    return new_list

def sammle_verben(db_verben, freq_d):
    """sorts verbforms to their stem
    takes fdist as a dict and returns also dict"""

    freq_verb = {x:y for x,y in freq_d.items() if y != 0}
    #freqVerb = {x:y for x,y in freq_d if y != 0}

    collect_unclear_things =["things that didn't match\n",]
    # sort by length of stem, for better hits
    verben = sorted(db_verben,key=lambda x: len(x.stem),reverse=True)
    points = int(len(verben)/50)
    collection = []
    collection_a =[]

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
    
    
    gukora:                        subj_ba,uwu         obj              sinkora,kirakora
    kumeneka,kunegura:             sin,                obj              simanuka
    kugira:                        subj_ba,uwu         obj    
    kwandika,kwoza,kwiheruka:      subj_ba,subj_u,uwu  obj, time 
    guha:                          sin,                obj,     trunk   urampa
    kureka:                                                     trunk   ndeka
    '''

    lemma_count = 0
    for verb in verben :
        freqsum = 0
        found = []

        # ((%zeit1+subj|%subj+zeit2) %obj? (%stem[:-1]wae, %perfw) | %stem_only))(ho yo ko mwo))
        '''
        1. ends with end_aey or n_end_aey ?
        2. if yes: analyse all before
        3. if it ends but we don't have yet a box for it: 
            collect for later analysis
        '''
        # for short verbs
        # for including kuba, -ri but excluding hari, kuhaba
        if len(verb.stem) == 2   and verb.lemma[0] in "gk-"   and len(verb.lemma) < 5 :
            #print ("stem2 :", lemma, inf, stem)
            qu_list_for_short_freqs = [sd.breakdown_consonants(x + verb.stem) for x in ["naiu"]]
            if len(verb.lemma) == 4 :
                qu_list_for_short_freqs.append(verb.stem)
             #coll_comb = [x for x in coll_comb if x[0] not in [n_end_a, n_end_e]]
        else : qu_list_for_short_freqs = []

        for freqs, num in freq_verb.items() :
            #for short freqs
            if num != 0 and len(freqs) < 4 and qu_list_for_short_freqs :
                for i in qu_list_for_short_freqs :
                    if freqs == i :
                        freqsum += num
                        found.append( [freqs,num] )
                        freq_verb.update({freqs:0})
                        num = 0
                        break #next freq
            # for n/end_a, n/end_e, n/end_y
            ask_begin = False
            # comb is list of 6 elements [end, questions for this end]
            for end_aey in verb.comb :
                if num == 0 :
                    break #next freq
                end = end_aey[0]
                # freq ends like verb
                if re.search(end,freqs) is not None :
                    ask_begin = True
                    # check begin
                    part1 = re.sub(re.search(end,freqs).group(),"",freqs)
                    #there is nothing else
                    if part1 == "" :
                        #is pure Imperativ
                        freqsum += num
                        found.append( [freqs,num] )
                        freq_verb.update({freqs:0})
                        num = 0
                        ask_begin = False # no break here, die end_Schlaufe
                        #muss weitergehen, wird oben bei num==0 abgebrochen
                    else :
                        #check each question
                        for qu in end_aey[1]:
                            if re.search(qu,part1) is not None:
                                freqsum += num
                                found.append( [freqs,num] )
                                freq_verb.update({freqs:0})
                                num = 0
                                ask_begin = False
                                break # next end/ dann oben gleich break >> next freq
                if ask_begin is True :
                    collect_unclear_things.append([verb.lemma,end,freqs])
                    ask_begin = False

        if freqsum > 0 :
            #alphabetisch
            found.sort()
            #head of line
            found = [verb.lemma, verb.dbid, "VERB", freqsum, len(found)]+ found
            if len(verb.lemma) >2 and verb.lemma[-2] == "_" :
                # id has two variants of writing the verb, collect all of those verbs here
                collection_a.append(found)
            else :
                collection.append(found)
        # Fortschrittsbalken ;-)
        if lemma_count%points == 0 :
            print('.',end = "")
        lemma_count +=1

    # map both variants of verbs to one id and add this to the big collection
    # sort by id, so the variants become neighbours with id_0 before id_a
    collection_b = sorted(collection_a,key=lambda x: x[3])
    if len(collection_b) > 1:
        # also the last element needs a next element to compare with
        collection_b.append([";",""])
        i = 0
        head_0 = collection_b[i][:5]
        while i < len(collection_b)-1 :
            if collection_b[i][0] != ";" :
                head_a = collection_b[i+1][:5]
                if str(head_0[1])[:-2] == str(head_a[1])[:-2] :
                    # same id but: id_0 bzw id_a
                    forms = collection_b[i][5:]+collection_b[i+1][5:]
                    forms.sort()
                    # the head for the sum of both variants of this id
                    forms = [head_0[0], head_0[1][:-2], "VERB", \
                        int(head_0[3])+int(head_a[3]), int(head_0[4])+int(head_a[4]) ] \
                        + forms
                    collection.append(forms)
                    # next element is used already, we can skip it
                    i += 2
                    head_0 = collection_b[i]
                else :
                    # cut _0/_a from id
                    #head_0[1] = head_0[1][:-2]
                    collection_b[i][1] = str(collection_b[i][1])[:-2]
                    collection.append(collection_b[i])
                    head_0 = head_a
                    i += 1


    # Eintrag,id,Anzahl verschiedener Formen,Summe aller Formen,
    #      nach Variantenreichtum sortiert (Form,Anzahl - hier alphabetisch)
    collection.sort(key=lambda x: x[3], reverse = True)
    collection.sort(key=lambda x: x[4], reverse = True)
    collection.insert(0,"lemma;id;verb;count;counted forms;forms",)
    #else : sammlung1 = []

    #kh.save_list(collection, "found6_verbs.csv", ";")
    #save_dict(freqVerb, "keine6_verbs.csv")

    #kh.save_list(unk_verbform, "unk_verbform.csv")
    #kh.save_list(unk_perf, "unk_perfective.csv")
    return (collection,freq_verb)
