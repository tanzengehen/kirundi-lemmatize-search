#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 13:12:22 2023

@author: doreen
"""

# import csv  # json
from unittest import TestCase
# import kir_db_classes as dbc
import kir_prepare_verbs as kv
# import kir_string_depot as sd


# nosetests --with-spec --spec-color --with-coverage --cover-erase
# coverage report -m

DB_DATA = []
NE_DATA = []
FREQ_SIM = {}


###############################################################
#       TEST   V E R B S                                      #
###############################################################
class TestNoun(TestCase):
    """Test cases for Verb and its alternatives
    in time, mode, negation, ...
    subjects, objects, ku/gu/kw
    """

    # @classmethod
    # def setUpClass(cls):
    #     """ Connect and load data needed by tests """
    #     global DB_DATA
    #     global FREQ_SIM
    #     # with open("bsp.csv") as csv_data:
    #     #     DB_DATA = csv.reader(csv_data, delimiter=";")

    def setUp(self):
        global DB_DATA
        global FREQ_SIM
        DB_DATA = [
            # 0 short, ku
            kv.Verb(['180', 'kuba', 'kubá',
                     'ku', 'ba', 'baye', 'baye',
                     '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                     '', '', '', '', '', '0', '', '0', '', 'NULL']),
            # 1
            kv.Verb(['8895', 'kwibonera', '',
                     'kw', 'ibonera', 'iboneye', 'ye',
                     '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                     '', '', '', '', '', '0', '', '0', '', 'NULL']),
            # 2 kw-a
            kv.Verb(['83', 'kwandika', 'kwaandika',
                     'kw', 'andika', 'anditse', 'tse',
                     '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                     '', '', '', '', '', '0', '', '0', '', 'NULL']),
            # 3 kw-o
            kv.Verb(['3562', 'kwoza', 'kwoóza',
                     'kw', 'oza', 'ogeje', 'geje',
                     '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                     '', '', '', '', '', '0', '', '0', '', 'NULL']),
            # 4 kw-i
            kv.Verb(['2236', 'kwiruka', 'kwiíruka',
                     'kw', 'iruka', 'irutse', 'tse',
                     '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                     '', '', '', '', '', '0', '', '0', '', 'NULL']),
            # 5 m-stem
            kv.Verb(['3120', 'kumira', 'kumira',
                     'ku', 'mira', 'mize', 'ze',
                     '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                     '', '', '', '', '', '0', '', '0', '', 'NULL']),
            # 6 n-stem
            kv.Verb(['3209', 'kunanirana', 'kunanirana',
                     'ku', 'nanirana', 'naniranye', 'nye',
                     '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                     '', '', '', '', '', '0', '', '0', '', 'NULL']),
            # 7 ku
            kv.Verb(['2795', 'gukora', '',
                     'gu', 'kora', 'koze', 'ze',
                     '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                     '', '', '', '', '', '0', '', '0', '', 'NULL']),
            # 8 same lemma, different perfective/meaning like no7
            kv.Verb(['2796', 'gukora', 'gukoora',
                     'gu', 'kora', 'koye', 'ye',
                     '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                     '', '', '', '', '', '0', '', '0', '', 'NULL']),
            # 9 with alternative (in perfective)
            kv.Verb(['1814', 'guhuhuta', '',
                     'gu', 'hūhūta', 'hūhūse', 'se',
                     '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                     'guhuhuta', '', 'huhuta', 'hūhūshe',
                     '', '0', '', '0', '', 'NULL']),
            # 10 passiv and with alternatives (clean infinitiv: no17)
            kv.Verb(['4229', 'gusabwa', 'gusabwa',
                     'gu', 'sabwa', 'sabwe', 'bwe',
                     '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                     'gusabga', '', 'sabga', 'bge',
                     '', '0', '', '0', '', 'NULL']),
            # 11 proverb (solo verb not in list)
            kv.Verb(['6988', 'gukoma amashi', 'gukóma amashí',
                     'gu', 'koma amashi', 'komye', '',
                     '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                     '', '', '', '', '', '0', '', '0', '', 'NULL']),
            # 12 proverb (solo verb already in list: no16)
            kv.Verb(['7161', 'kugira amazinda', 'kugira amaziinda',
                     'ku', 'gira amazinda', 'gize', 'gize',
                     '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                     '', '', '', '', '', '0', '', '0', '', 'NULL']),
            # 13 perfective defect
            kv.Verb(['9999', 'kurararara', '',
                     'ku', 'rararara', 'raye?', '?',
                     '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                     '', '', '', '', '', '0', '', '0', '', 'NULL']),
            # 14 no perfective
            kv.Verb(['9999', 'kurururura', '',
                     'ku', 'rururura', '', '',
                     '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                     '', '', '', '', '', '0', '', '0', '', 'NULL']),
            # 15 perfective with u
            kv.Verb(['5585', 'gupfa', '',
                     'gu', 'pfa', 'pfūye', 'pfūye',
                     '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                     '', '', '', '', '', '0', '', '0', '', 'NULL']),
            # 16 gu (and reference to no12)
            kv.Verb(['1223', 'kugira', 'kugira',
                     'ku', 'gira', 'gize', 'gize ',
                     '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                     '', '', '', '', '', '0', '', '0', '', 'NULL']),
            # 17 clean infinitiv as reference to no.10)
            kv.Verb(['4222', 'gusaba', 'gusaba',
                     'gu', 'saba', 'savye', 'vye',
                     '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                     '', '', '', '', '', '0', '', '0', '', 'NULL']),
            # 18 passiv with infinitive already in list: no5
            kv.Verb(['3124', 'kumirwa', 'kumirwa',
                     'ku', 'mirwa', 'mizwe', 'zwe',
                     '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                     '', '', '', '', '', '0', '', '0', '', 'NULL']),
            # 19 passiv without infinitive already in list
            kv.Verb(['467', 'kuborerwa', 'kuborerwa',
                     'ku', 'borerwa', 'borewe', 'we',
                     '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                     '', '', '', '', '', '0', '', '0', '', 'NULL']),
            # 20 r-stem
            kv.Verb(['3984', 'kurima', 'kurima',
                     'ku', 'rima', 'rimye', 'mye',
                     '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                     '', '', '', '', '', '0', '', '0', '', 'NULL']),
            # 21 h-stem
            kv.Verb(['6364', 'guhagarara', 'guhágarara',
                     'gu', 'hagarara', 'hagaraze', 'ze',
                     '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                     '', '', '', '', '', '0', '', '0', '', 'NULL']),
            # 22
            kv.Verb(['1135', 'kugenda', '',
                     'ku', 'gēnda', 'giye', 'giye',
                     '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                     '', '', '', '', '', '0', '', '0', '', 'NULL']),
            # 23 short stem
            kv.Verb(['1406', 'guha', '',
                     'gu', 'ha', 'haye', 'haye',
                     '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                     '', '', '', '', '', '0', '', '0', '', 'NULL']),
        ]
        FREQ_SIM = {
            'wagira': 3, 'wagize': 3, 'waragira': 3, 'waragize': 3,
            'wogira': 3, 'wogize': 3, 'uragira': 3, 'uragize': 3,
            'utagira': 3, 'utagize': 3, 'utaragira': 3, 'utogira': 3,
            'utogize': 3, 'utazogira': 3, 'utazogize': 3, 'uracagira': 3,
            'uracagize': 3, 'urakagira': 3, 'urakagize': 3, 'ukigira': 3,
            'ukigize': 3, 'utakigira': 3, 'utakigize': 3, 'ukagira': 3,
            'ukagize': 3,
            'ndagira': 3, 'ndagize': 3, 'ndakagira': 3, 'ndakagize': 404,
            'naragira': 3, 'naragize': 3, 'sinagira': 3, 'sinagize': 3,
            'ngira': 3, 'ngize': 3, 'nagira': 3, 'nagize': 3,
            'nogira': 3, 'nogize': 3, 'nzogira': 3, 'nzogize': 3,
            'sinzogira': 3, 'sinogira': 3, 'sinogize': 3,

            'wandika': 3, 'wanditse': 3, 'warandika': 3, 'waranditse': 3,
            'utandika': 3, 'utanditse': 3, 'utarandika': 3, 'wokwandika': 3,
            'wokwanditse': 3, 'utazokwandika': 3, 'utazokwanditse': 3,
            'uracandika': 3, 'uracanditse': 3, 'urandika': 3, 'uranditse': 3,
            'urakandika': 3, 'ucandika': 3, 'ucanditse': 3,
            'utacandika': 3, 'utacanditse': 3, 'ukandika': 3, 'ukanditse': 3,
            'ndandika': 3, 'ndanditse': 3, 'ndakandika': 3, 'ndakanditse': 3,
            'narandika': 3, 'naranditse': 3, 'sinandika': 3, 'sinanditse': 3,
            'nandika': 3, 'nanditse': 3, 'nokwandika': 3, 'nokwanditse': 3,
            'nzokwandika': 3, 'nzokwanditse': 3,
            'ncandika': 3, 'ncanditse': 3, 'sincandika': 3, 'sincanditse': 3,
            'sinzokwandika': 3, 'sinokwandika': 3, 'sinokwanditse': 3,

            'woza': 3, 'wogeje': 3, 'waroza': 3, 'warogeje': 3,
            'utoza': 3, 'utogeje': 3, 'utaroza': 3, 'wokwoza': 3,
            'wokwogeje': 3, 'utazokwoza': 3, 'utazokwogeje': 3,
            'uracoza': 3, 'uracogeje': 3, 'uroza': 3, 'urogeje': 3,
            'urakwoza': 3, 'urakwogeje': 3, 'ukwoza ': 3,
            'utacoza': 3, 'utacogeje': 3,
            'nokwoza': 3, 'nokwogeje': 3, 'nzokwoza': 3,

            'wiruka': 3, 'wirutse': 3, 'wariruka': 3, 'warirutse': 3,
            'utiruka': 3, 'utirutse': 3, 'utariruka': 3,
            'wokwiruka': 3, 'wokwirutse': 3, 'utaziruka': 3, 'utazokwiruka': 3,
            'utazokwirutse': 3, 'uraciruka': 3, 'uracirutse': 3,
            'uriruka': 3, 'urirutse': 3, 'urakiruka': 3, 'urakirutse': 3,
            'uciruka': 3, 'utaciruka': 3, 'utacirutse': 3,
            'ukiruka': 3, 'ukirutse': 3,
            'nokwiruka': 3, 'nokwirutse': 3, 'nzokiruka': 3,

            'bigenda': 3, 'bigende': 3, 'bigiye': 3, 'ntibigenda': 3,
            'ntibigende': 3, 'ntibigiye': 3, 'bizogenda': 3, 'bizogende': 3,
            'bizogiye': 3, 'ntibizogenda': 3, 'ntibizogende': 3,
            'ntibizogiye': 3, 'vyagenda': 3, 'vyagiye': 3, 'ntivyagenda': 3,
            'ntivyagiye': 3, 'vyogenda': 3, 'vyogiye': 3, 'ntivyogenda': 3,
            'ntivyogiye': 3, 'vyaragenda': 3, 'vyaragiye': 3,
            'biragenda': 3, 'biragiye': 3, 'ntibiragenda': 3, 'ntibiragiye': 3,
            'bikazogenda': 3, 'bikazogiye': 3,

            'ndamira': 3, 'ndamize': 3, 'ndakamira': 3, 'ndakamize': 3,
            'naramira': 3, 'naramize': 3, 'sinamira': 3, 'sinamize': 3,
            'mira': 3, 'mize': 3, 'namira': 3, 'namize ': 3,
            'nomira': 3, 'nomize ': 3, 'nzomira': 3, 'nzomize': 3,
            'sinzomira': 3, 'sinomira': 3, 'sinomize': 3,

            'ntugakore': 3, 'ntukagire': 3, 'ntukandike': 3, 'ntukoze': 3,
            'ntukiruke': 3,
            'nukore': 3, 'nugire': 3, 'nuwandika': 3, 'niyoze': 3,
            'nayiruke': 3,
            'uwagira': 3, 'uwagize': 3, 'uwaragira': 3, 'uwaragize': 3,
            'uwutagira': 3, 'uwutagize': 3, 'uwutaragira': 3, 'uwutaragize': 3,
            'uwogira': 3, 'uwogize': 3, 'uwutogira': 3, 'uwutogize': 3,
            'uwuzokora': 3, 'uwuzokoze': 3, 'uwutazogira': 3, 'uwutazogize': 3,
            'uwukigira': 3, 'uwukigize': 3, 'uwutakigira': 3, 'uwutakigize': 3,
            'uwandika': 3, 'ubwandika': 3, 'ivyiruka': 3, 'iryiruka': 3,
            'abandika': 3, 'iciruka': 3,
            'mpa': 3, 'wahuhuse': 3, 'wahuhushe': 3
            }

    # @classmethod
    # def tearDownClass(cls):
    #     """Disconnect from database"""
    #     global DB_DATA
    #     DB_DATA = None

    def tearDown(self):
        global DB_DATA
        DB_DATA = []

    def test_init_simple(self):
        """Test direct initializations"""
        data = DB_DATA[0]
        self.assertEqual(data.lemma, "kuba")
        self.assertEqual(data.dbid, "180")
        self.assertEqual(data.pos, "VERB")
        self.assertEqual(data.stem, "ba")
        self.assertEqual(data.perfective, "baye")
        data = DB_DATA[13]
        self.assertEqual(data.perfective, "raye?")
        data = DB_DATA[9]
        self.assertEqual(data.lemma, "guhuhuta")
        self.assertEqual(data.dbid, "1814")
        self.assertEqual(data.alternatives, ['guhuhuta'])
        self.assertEqual(data.comb, None)

    def test_set_end_of_verbs(self):
        """Test built verb endings"""
        data = DB_DATA[5]
        data._set_end_of_ends()
        self.assertEqual(data.lemma, "kumira")
        self.assertEqual(data._end_a, 'mir(w?a)((([hyk]|mw)o)?$)')
        self.assertEqual(data._end_e, 'mire((([hyk]|mw)o)?$)')
        self.assertEqual(data._end_y, 'miz((w)?e)((([hyk]|mw)o)?$)')
        data = DB_DATA[15]
        data._set_end_of_ends()
        self.assertEqual(data.lemma, "gupfa")
        self.assertEqual(data.perfective[-3], "u")
        self.assertEqual(
            data._end_y, 'pfu(ye|((ri)?we))((([hyk]|mw)o)?$)')
        # test exceptions for perfectives
        data = DB_DATA[13]
        data.perfective = "cafye"
        data._set_end_of_ends()
        self.assertEqual(
            data._end_y, 'capuwe((([hyk]|mw)o)?$)')
        data.stem = "zi"
        data._set_end_of_ends()
        self.assertEqual(data._end_y, '')
        self.assertEqual(data._end_a, 'zw?i((([hyk]|mw)o)?$)')
        data.stem = "fise"
        data._set_end_of_ends()
        self.assertEqual(data._end_y, 'fise((([hyk]|mw)o)?$)')
        data.perfective = "calye"
        data._set_end_of_ends()
        self.assertIn(['perfective: unexpected letter before [y] ',
                       'kurararara', 'calye'],
                      data.unclear)

    def test_get(self):
        """Test get attributes"""
        self.assertEqual(DB_DATA[3].get('lemma'), 'kwoza')
        self.assertEqual(DB_DATA[4].get('dbid'), '2236')
        self.assertEqual(DB_DATA[6].get('stem'), 'nanirana')
        self.assertEqual(DB_DATA[7].get('perfective'), 'koze')
        self.assertEqual(DB_DATA[8].get(
            'alternative'), 'Hm, does class Verb has this feature?')
        self.assertEqual(DB_DATA[8].get('alternatives'), '')
        self.assertEqual(DB_DATA[9].get('comb'), None)
        self.assertEqual(DB_DATA[10].get('proverb'), False)
        self.assertEqual(DB_DATA[11].get('unclear'), [])

    def test_prepare_verb_alternativ(self):
        """Test prepare_verb_alternativ"""
        row_alt = kv.prepare_verb_alternativ(
            ['1814', 'guhuhuta', '',
             'gu', 'hūhūta', 'hūhūse', 'se',
             '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
             'guhuhuta', '', 'huhuta', 'hūhūshe',
             '', '', '0', '', '0', '', 'NULL'])
        self.assertEqual(row_alt[0], '1814_a')
        self.assertEqual(row_alt[1], 'guhuhuta')
        self.assertEqual(row_alt[4], 'huhuta')
        self.assertEqual(row_alt[5], 'hūhūshe')
        # test short perfective given
        row_alt = kv.prepare_verb_alternativ(
            ['4229', 'gusabwa', 'gusabwa',
             'gu', 'sabwa', 'sabwe', 'bwe',
             '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
             'gusabga', '', 'sabga', 'bge',
             '', '0', '', '0', '', 'NULL'])
        self.assertEqual(row_alt[0], '4229_a')
        self.assertEqual(row_alt[4], 'sabga')
        self.assertEqual(row_alt[5], 'sabge')
        self.assertEqual(row_alt[13], '')

    def test_mark_proverb(self):
        """Test mark proverb
        is preparation for 'filter proverbs out'"""
        data = [DB_DATA[i] for i in [11, 12, 13, 16]]
        for verb in data:
            verb.mark_proverb()
        self.assertEqual(data[0].lemma, "gukoma amashi")
        self.assertEqual(data[0].proverb, True)
        self.assertEqual(data[1].lemma, "kugira amazinda")
        self.assertEqual(data[1].proverb, True)
        self.assertEqual(data[2].lemma, "kurararara")
        self.assertEqual(
            data[2].unclear,
            [['kurararara', 'perfective unclear:', 'raye?']])
        self.assertEqual(data[3].lemma, "kugira")
        self.assertEqual(data[3].proverb, False)

    def test_filter_proverbs_out(self):
        """Test filter proverbs out:
        take only verb from stem and only if there's no same solo form"""
        # prepare
        data = [DB_DATA[x] for x in [0, 1, 11, 12, 16]]
        lemma_before = [i.lemma for i in data]
        for i in ["kugira", "kugira amazinda", "gukoma amashi"]:
            self.assertIn(i, lemma_before)
        self.assertNotIn("gukoma", lemma_before)
        # test
        new_list = kv.filter_proverbs_out(data)
        lemma_after, stems = [], []
        for i in new_list:
            lemma_after.append(i.lemma)
            stems.append(i.stem)
        self.assertTrue(len(new_list) == len(data)-1)
        self.assertIn("koma", stems)
        self.assertIn("gira", stems)
        self.assertNotIn("gira amazinda", stems)
        self.assertNotIn("koma amashi", stems)
        self.assertIn("gukoma amashi", lemma_after)
        self.assertNotIn("kugira amazinda", lemma_after)

    def test_mark_passiv(self):
        """Test mark passiv:
        is preparation for 'filter passiv out'"""
        data = [DB_DATA[i]for i in [8, 10]]
        for verb in data:
            verb.mark_passiv()
        self.assertEqual(data[0].lemma, "gukora")
        self.assertEqual(data[0].passiv, False)
        self.assertEqual(data[1].lemma, "gusabwa")
        self.assertEqual(data[1].passiv, True)

    def test_filter_passiv_out(self):
        """Test filter passiv out:
        skip passiv-lemma if there's already same lemma without passiv"""
        data = [DB_DATA[i] for i in [4, 5, 10, 17, 18, 19]]
        lemma_before = [i.lemma for i in data]
        for i in ["gusabwa", "gusaba", "kuborerwa", "kumira", "kumirwa"]:
            self.assertIn(i, lemma_before)
        self.assertNotIn("kuborera", lemma_before)
        # test
        new_list = kv.filter_passiv_out(data)
        stems = [i.stem for i in new_list]
        self.assertTrue(len(new_list) == len(data)-2)
        self.assertIn("saba", stems)
        self.assertIn("mira", stems)
        self.assertIn("borerwa", stems)
        self.assertNotIn("sabwa", stems)
        self.assertNotIn("kmirwa", stems)

    def test_set_qu(self):
        """Test set regEx"""
        data = DB_DATA[0]
        self.assertEqual(data.lemma, "kuba")
        data.set_qu()
        self.assertEqual(len(data.comb), 6)
        self.assertEqual(len(data.comb[0][0]), 24)
        self.assertEqual(len(data.comb[0][1]), 25)
        self.assertEqual(len(data.comb[1][0]), 23)
        self.assertEqual(len(data.comb[1][1]), 116)
        self.assertEqual(len(data.comb[2][0]), 20)
        self.assertEqual(len(data.comb[2][1]), 18)
        self.assertEqual(len(data.comb[3][0]), 19)
        self.assertEqual(len(data.comb[3][1]), 89)
        self.assertEqual(len(data.comb[4][0]), 27)
        self.assertEqual(len(data.comb[4][1]), 20)
        self.assertEqual(len(data.comb[5][0]), 26)
        self.assertEqual(len(data.comb[5][1]), 98)
        data = DB_DATA[2]
        self.assertEqual(data.lemma, "kwandika")
        data.set_qu()
        self.assertEqual(len(data.comb[0][0]), 30)
        self.assertEqual(len(data.comb[0][1]), 25)
        self.assertEqual(len(data.comb[1][0]), 27)
        self.assertEqual(len(data.comb[1][1]), 166)
        self.assertEqual(len(data.comb[2][0]), 26)
        self.assertEqual(len(data.comb[2][1]), 18)
        self.assertEqual(len(data.comb[3][0]), 23)
        self.assertEqual(len(data.comb[3][1]), 128)
        self.assertEqual(len(data.comb[4][0]), 33)
        self.assertEqual(len(data.comb[4][1]), 20)
        self.assertEqual(len(data.comb[5][0]), 30)
        self.assertEqual(len(data.comb[5][1]), 141)
        data = DB_DATA[4]
        data.set_qu()
        self.assertEqual(data.lemma, "kwiruka")
        self.assertEqual(data.comb[0][0], "ny?iruk(w?a)((([hyk]|mw)o)?$)")
        self.assertEqual(len(data.comb[0][1]), 25)
        self.assertEqual(data.comb[1][0], "iruk(w?a)((([hyk]|mw)o)?$)")
        self.assertEqual(len(data.comb[1][1]), 166)
        self.assertEqual(data.comb[2][0], "ny?iruke((([hyk]|mw)o)?$)")
        self.assertEqual(len(data.comb[2][1]), 18)
        self.assertEqual(data.comb[3][0], "iruke((([hyk]|mw)o)?$)")
        self.assertEqual(len(data.comb[3][1]), 128)
        self.assertEqual(data.comb[4][0], "ny?iruts((w)?e)((([hyk]|mw)o)?$)")
        self.assertEqual(len(data.comb[4][1]), 20)
        self.assertEqual(data.comb[5][0], "iruts((w)?e)((([hyk]|mw)o)?$)")
        self.assertEqual(len(data.comb[5][1]), 141)
        data = DB_DATA[5]
        data.set_qu()
        self.assertEqual(data.lemma, "kumira")
        self.assertEqual(data.comb[0][0], "mir(w?a)((([hyk]|mw)o)?$)")
        self.assertEqual(len(data.comb[0][1]), 25)
        self.assertEqual(data.comb[1][0], "mir(w?a)((([hyk]|mw)o)?$)")
        self.assertEqual(len(data.comb[1][1]), 116)
        self.assertEqual(data.comb[2][0], 'mire((([hyk]|mw)o)?$)')
        self.assertEqual(len(data.comb[2][1]), 18)
        self.assertEqual(data.comb[3][0], "mire((([hyk]|mw)o)?$)")
        self.assertEqual(len(data.comb[3][1]), 89)
        self.assertEqual(data.comb[4][0], "miz((w)?e)((([hyk]|mw)o)?$)")
        self.assertEqual(len(data.comb[4][1]), 20)
        self.assertEqual(data.comb[5][0], "miz((w)?e)((([hyk]|mw)o)?$)")
        self.assertEqual(len(data.comb[5][1]), 98)
        data = DB_DATA[7]
        data.set_qu()
        self.assertEqual(data.lemma, "gukora")
        self.assertEqual(data.comb[0][0], "nkor(w?a)((([hyk]|mw)o)?$)")
        self.assertEqual(len(data.comb[0][1]), 25)
        self.assertEqual(data.comb[1][0], "kor(w?a)((([hyk]|mw)o)?$)")
        self.assertEqual(len(data.comb[1][1]), 142)
        self.assertEqual(data.comb[2][0], 'nkore((([hyk]|mw)o)?$)')
        self.assertEqual(len(data.comb[2][1]), 18)
        self.assertEqual(data.comb[3][0], "kore((([hyk]|mw)o)?$)")
        self.assertEqual(len(data.comb[3][1]), 109)
        self.assertEqual(data.comb[4][0], "nkoz((w)?e)((([hyk]|mw)o)?$)")
        self.assertEqual(len(data.comb[4][1]), 20)
        self.assertEqual(data.comb[5][0], "koz((w)?e)((([hyk]|mw)o)?$)")
        self.assertEqual(len(data.comb[5][1]), 120)
        data = DB_DATA[20]
        data.set_qu()
        self.assertEqual(data.lemma, "kurima")
        self.assertEqual(data.comb[0][0], "ndim(w?a)((([hyk]|mw)o)?$)")
        self.assertEqual(len(data.comb[0][1]), 25)
        self.assertEqual(data.comb[1][0], "rim(w?a)((([hyk]|mw)o)?$)")
        self.assertEqual(len(data.comb[1][1]), 116)
        self.assertEqual(data.comb[2][0], 'ndime((([hyk]|mw)o)?$)')
        self.assertEqual(len(data.comb[2][1]), 18)
        self.assertEqual(data.comb[3][0], "rime((([hyk]|mw)o)?$)")
        self.assertEqual(len(data.comb[3][1]), 89)
        self.assertEqual(data.comb[4][0], "ndimy(w?e)((([hyk]|mw)o)?$)")
        self.assertEqual(len(data.comb[4][1]), 20)
        self.assertEqual(data.comb[5][0], "rimy(w?e)((([hyk]|mw)o)?$)")
        self.assertEqual(len(data.comb[5][1]), 98)
        data = DB_DATA[21]
        data.set_qu()
        self.assertEqual(data.lemma, "guhagarara")
        self.assertEqual(data.comb[0][0], "mpagarar(w?a)((([hyk]|mw)o)?$)")
        self.assertEqual(len(data.comb[0][1]), 25)
        self.assertEqual(data.comb[1][0], "hagarar(w?a)((([hyk]|mw)o)?$)")
        self.assertEqual(len(data.comb[1][1]), 142)
        self.assertEqual(data.comb[2][0], 'mpagarare((([hyk]|mw)o)?$)')
        self.assertEqual(len(data.comb[2][1]), 18)
        self.assertEqual(data.comb[3][0], "hagarare((([hyk]|mw)o)?$)")
        self.assertEqual(len(data.comb[3][1]), 109)
        self.assertEqual(data.comb[4][0], "mpagaraz((w)?e)((([hyk]|mw)o)?$)")
        self.assertEqual(len(data.comb[4][1]), 20)
        self.assertEqual(data.comb[5][0], "hagaraz((w)?e)((([hyk]|mw)o)?$)")
        self.assertEqual(len(data.comb[5][1]), 120)

    def test_collect_verbs(self):
        """Test collect verbs"""
        # skip proverbs, passives, incorrects
        data = DB_DATA[0:10]+DB_DATA[15:18]+DB_DATA[20:]
        # add alternative
        data[9].dbid = "1814_0"
        data.append(kv.Verb(['1814_a', 'guhuhuta', '',
                             'gu', 'hūhūta', 'hūhūshe', '',
                             '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                             '', '', '', '',
                             '', '0', '', '0', '', 'NULL']))
        for i in data:
            i.set_qu()
        freq = FREQ_SIM
        collection, freq_verbs = kv.collect_verbs(data, freq)
        for i in freq_verbs:
            print(i)
        # TODO check if they should be collected:
        # ukwoza, namize, nomize, nuwandika
        # TODO should not be collected: ndakagize
        self.assertEqual(len(freq_verbs), 4)
        for i in collection:
            print(i)
        self.assertEqual(len(collection), 9)
        types = 0
        for i in collection:
            types += i[4]
            print(i)
        self.assertEqual(len(freq_verbs), len(freq)-types)
        self.assertEqual(collection[0][0], 'kugira')
        self.assertEqual(collection[0][4], 64)
        self.assertEqual(collection[1][0], 'kwandika')
        self.assertEqual(collection[1][4], 47)
        self.assertEqual(collection[2][0], 'kwiruka')
        self.assertEqual(collection[2][4], 31)
        self.assertEqual(collection[3][0], 'kugenda')
        self.assertEqual(collection[3][4], 28)
        self.assertEqual(collection[4][0], 'kwoza')
        self.assertEqual(collection[4][4], 23)
        self.assertEqual(collection[5][0], 'kumira')
        self.assertEqual(collection[5][4], 17)
        self.assertEqual(collection[6][0], 'gukora')
        self.assertEqual(collection[6][4], 5)
        self.assertEqual(collection[7][0], 'guhuhuta')
        self.assertEqual(collection[7][4], 2)
        self.assertEqual(collection[8][0], 'guha')
        self.assertEqual(collection[8][4], 1)
        # test: only alternative hits
        data1 = [DB_DATA[9], DB_DATA[23],]
        # add alternative
        data1[0].dbid = "1114_0"
        data1.append(kv.Verb(['1114_a', 'guhuhuta', '',
                              'gu', 'hūhūta', 'hūhūshe', '',
                              '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                              '', '', '', '',
                              '', '0', '', '0', '', 'NULL']))
        for i in data1:
            i.set_qu()
        freq1 = {'abandika': 3, 'iciruka': 3,
                 'mpa': 3, 'wahuhushe': 3}
        collection, freq_verbs = kv.collect_verbs(data1, freq1)
        for i in collection:
            print(i)
        self.assertEqual(len(freq_verbs), 2)
        self.assertEqual(len(collection), 2)


###############################################################
#       TEST   HELPER                                         #
###############################################################
class TestHelper(TestCase):
    """Test helper functions for PoS classes"""

    def test_put_same_ids_together(self):
        """Test merging variants of lemmata with same ID
        (spelling variants or built with RegEx)"""
        collection = [
            ['hano', '1458', 'PRON', 1048, 1,
                ['hano', 1048]],
            ['iki', '8274', 'PRON', 6373, 1, ['iki', 6373]],
            ['-no', '1458', 'PRON', 4918, 18,
                ['ahano', 4], ['akano', 5], ['ano', 139], ['bano', 290],
                ['bino', 111], ['buno', 481], ['ino', 1193],
                ['irino', 5], ['kano', 155], ['kino', 657], ['kuno', 59],
                ['rino', 77], ['runo', 55], ['tuno', 8], ['ubuno', 1],
                ['uno', 1611], ['utuno', 1], ['zino', 66]]
        ]
        collection.sort(key=lambda x: x[0])
        collection.sort(key=lambda x: x[1])
        collection = kv.add_same_ids_up(collection)
        self.assertEqual(len(collection), 2)
        self.assertEqual(collection[0][0], '-no')
        self.assertIn(['hano', 1048], collection[0])
        self.assertIn(['rino', 77], collection[0])
        self.assertEqual(collection[0][3], 1048+4918)
        self.assertEqual(collection[0][4], 1+18)
