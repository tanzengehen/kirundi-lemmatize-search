#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 13:12:22 2023

@author: doreen
"""

import csv  # json
from unittest import TestCase
import kir_db_classes as dbc
import kir_prepare_verbs as kv
import kir_string_depot as sd


# nosetests --with-spec --spec-color --with-coverage --cover-erase
# coverage report -m

DB_DATA = []
NE_DATA = []
FREQ_SIM = {}


###############################################################
#       TEST   V E R B S                                      #
###############################################################
class TestNoun(TestCase):
    """Test cases for Verb
    and alternatives in time, mode, negation, ...
    subjects, objects, ku/gu/kw
    """

    @classmethod
    def setUpClass(cls):
        """ Connect and load data needed by tests """
        global DB_DATA
    #     global FREQ_SIM
    #     # with open("bsp.csv") as csv_data:
    #     #     DB_DATA = csv.reader(csv_data, delimiter=";")

    # def setUp(self):
    #     global DB_DATA
        DB_DATA = [
            kv.Verb(['180', 'kuba', 'kubá',
                     'ku', 'ba', 'baye', 'baye',
                     '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                     '', '', '', '', '', '0', '', '0', '', 'NULL']),
        #     kv.Verb(['326', 'kubera', 'kubéera',
        #              'ku', 'bera', 'bereye', 'bereye',
        #              '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
        #              '', '', '', '', '180', '0', '', '0	', '', 'NULL']),
        #     kv.Verb(['542', 'guca', 'gucá',
        #              'gu', 'ca', 'keye', 'keye',
        #              '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
        #              '', '', '', '', '', '0', '', '0', '', 'NULL']),
        #     kv.Verb(['896', 'gufata', '',
        #              'gu', 'fata', 'fashe', 'she',
        #              '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
        #              '', '', '', '', '', '0', '', '0', '', 'NULL']),
        #     kv.Verb(['991', 'kugabanya', '',
        #              'ku', 'gabanya', 'gabanije', 'nije',
        #              '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
        #              '', '', '', '', '', '0', '', '0', '', 'NULL']),
        #     # 5
        #     kv.Verb(['1135', 'kugenda', '',
        #              'ku', ' gēnda', 'giye', 'giye',
        #              '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
        #              '', '', '', '', '', '0', '', '0', '', 'NULL']),

        #     kv.Verb(['1385', 'gusa', 'gusa',
        #              'gu', 'sa', 'sa', 'sa',
        #              '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
        #              '', '', '', '', '', '0', '', '0', '', 'NULL']),
        #     kv.Verb(['2129', 'kwikorera', 'kwiíkorera',
        #              'kw', 'ikorera', 'ikoreye', 'ye',
        #              '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
        #              '', '', '', '', '', '0', '', '0', '', 'NULL']),
        #     kv.Verb(['2383', 'kuja', '',
        #              'ku', 'ja', 'giye', 'giye',
        #              '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
        #              '', '', '', '', '', '0', '', '0', '', 'NULL']),
        #     # 10
        #     kv.Verb(['2541', 'gukaraba', '',
        #              'gu', 'karaba', 'karavye', 'vye',
        #              '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
        #              '', '', '', '', '', '0', '', '0', '', 'NULL']),
        #     kv.Verb(['2836', 'gukoza', 'gukóza',
        #              'gu', 'koza', 'kojeje', 'jeje',
        #              '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
        #              '', '', '', '', '', '0', '', '0', '', 'NULL']),
        #     kv.Verb(['3696', 'kuraba', 'kurába',
        #              'ku', 'raba', 'ravye', 'vye',
        #              '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
        #              '', '', '', '', '', '0', '', '0', '', 'NULL']),
        #     kv.Verb(['3776', 'kuramutsa', 'kuramutsa',
        #              'ku', 'ramutsa', 'ramukije', 'kije',
        #              '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
        #              '', '', '', '', '', '0', '', '0', '', 'NULL']),
        #     kv.Verb(['3966', '-ri', '-ri',
        #              '-', 'ri', '', '',
        #              '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
        #              '', '', '', '', '3999', '0', '', '0', '', 'NULL']),
        #     # 15
        #     kv.Verb(['5194', '-ti', '-ti',
        #              '-', 'ti', '', '',
        #              '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
        #              '', '', '', '', '', '0', '', '0', '', 'NULL']),
        #     kv.Verb(['8161', 'kwenga', 'kweenga',
        #              'kw', 'enga', 'enze', 'nze',
        #              '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
        #              '', '', '', '', '', '0', '', '0', '', 'NULL']),
        #     kv.Verb(['8235', 'kugema', 'kugema',
        #              'ku', 'gema', 'gemye', 'mye',
        #              '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
        #              '', '', '', '', '', '0', '', '0', '', 'NULL']),
            # kw
            kv.Verb(['8895', 'kwibonera', '',
                     'kw', 'ibonera', 'iboneye', 'ye',
                     '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                     '', '', '', '', '', '0', '', '0', '', 'NULL']),
            kv.Verb(['83', 'kwandika', 'kwaandika',
                     'kw', 'andika', 'anditse', 'tse',
                     '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                     '', '', '', '', '', '0', '', '0', '', 'NULL']),
            # 3
            kv.Verb(['3562', 'kwoza', 'kwoóza',
                     'kw', 'oza', 'ogeje', 'geje',
                     '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                     '', '', '', '', '', '0', '', '0', '', 'NULL']),
            kv.Verb(['2236', 'kwiruka', 'kwiíruka',
                     'kw', 'iruka', 'irutse', 'tse',
                     '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                     '', '', '', '', '', '0', '', '0', '', 'NULL']),
            # m-stem
            kv.Verb(['3120', 'kumira', 'kumira',
                     'ku', 'mira', 'mize', 'ze',
                     '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                     '', '', '', '', '', '0', '', '0', '', 'NULL']),
            # n-stem
            kv.Verb(['3209', 'kunanirana', 'kunanirana',
                     'ku', 'nanirana', 'naniranye', 'nye',
                     '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                     '', '', '', '', '', '0', '', '0', '', 'NULL']),
            kv.Verb(['2795', 'gukora', '',
                     'gu', 'kora', 'koze', 'ze',
                     '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                     '', '', '', '', '', '0', '', '0', '', 'NULL']),
            # 8
            kv.Verb(['2796', 'gukora', 'gukoora',
                     'gu', 'kora', 'koye', 'ye',
                     '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                     '', '', '', '', '', '0', '', '0', '', 'NULL']),
            # with alternatives
            kv.Verb(['1814', 'guhuhuta', '',
                     'gu', 'hūhūta', 'hūhūse', 'se',
                     '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                     'guhuhuta', '', 'huhuta', 'hūhūshe',
                     '', '0', '', '0', '', 'NULL']),
            # passiv and alternativ
            kv.Verb(['4229', 'gusabwa', 'gusabwa',
                     'gu', 'sabwa', 'sabwe', 'bwe',
                     '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                     'gusabga', '', 'sabga', 'bge',
                     '', '0', '', '0', '', 'NULL']),
            # proverbs
            kv.Verb(['6988', 'gukoma amashi', 'gukóma amashí',
                     'gu', 'koma amashi', 'komye', '',
                     '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                     '', '', '', '', '', '0', '', '0', '', 'NULL']),
            kv.Verb(['7161', 'kugira amazinda', 'kugira amaziinda',
                     'ku', 'gira amazinda', 'gize', 'gize',
                     '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                     '', '', '', '', '', '0', '', '0', '', 'NULL']),
            # 13
            kv.Verb(['9999', 'kurararara', '',
                     'ku', 'rararara', 'raye?', '?',
                     '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                     '', '', '', '', '', '0', '', '0', '', 'NULL']),
            kv.Verb(['9999', 'kurururura', '',
                     'ku', 'rururura', '', '',
                     '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                     '', '', '', '', '', '0', '', '0', '', 'NULL']),
            kv.Verb(['5585', 'gupfa', '',
                     'gu', 'pfa', 'pfūye', 'pfūye',
                     '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                     '', '', '', '', '', '0', '', '0', '', 'NULL']),
            kv.Verb(['1223', 'kugira', 'kugira',
                     'ku', 'gira', 'gize', 'gize ',
                     '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                     '', '', '', '', '', '0', '', '0', '', 'NULL']),
            kv.Verb(['4222', 'gusaba', 'gusaba',
                     'gu', 'saba', 'savye', 'vye',
                     '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                     '', '', '', '', '', '0', '', '0', '', 'NULL']),
            # 18
            kv.Verb(['3124', 'kumirwa', 'kumirwa',
                     'ku', 'mirwa', 'mizwe', 'zwe',
                     '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                     '', '', '', '', '', '0', '', '0', '', 'NULL']),
            kv.Verb(['467', 'kuborerwa', 'kuborerwa',
                     'ku', 'borerwa', 'borewe', 'we',
                     '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                     '', '', '', '', '', '0', '', '0', '', 'NULL']),
        ]

    @classmethod
    def tearDownClass(cls):
        """Disconnect from database"""
        global DB_DATA
        DB_DATA = None

    # def tearDown(self):
    #     global NE_DATA
    #     NE_DATA = []

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

    def test_set_end_of_verbs(self):
        """test built verb endings"""
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
        """test get attributes"""
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
        print(row_alt)
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
        self.assertEqual(row_alt[5], 'sabge')

    def test_mark_proverb(self):
        """Test mark proverb"""
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
        self.assertNotIn("kora amashi", stems)
        self.assertIn("gukoma amashi", lemma_after)
        self.assertNotIn("kugira amazinda", lemma_after)

    def test_mark_passiv(self):
        """mark passiv"""
        data = [DB_DATA[i]for i in [8, 10]]
        for verb in data:
            verb.mark_passiv()
        self.assertEqual(data[0].lemma, "gukora")
        self.assertEqual(data[0].passiv, False)
        self.assertEqual(data[1].lemma, "gusabwa")
        self.assertEqual(data[1].passiv, True)

    def test_filter_passiv_out(self):
        """Test filter passiv out:
        skip passiv-lemma if there's a lemma without passiv"""
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
        