#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 30 14:01:20 2023

@author: doreen
"""

import csv  # json
from unittest import TestCase
import kir_db_classes as dbc


DB_DATA = {}
DB_NOUN = []
FREQ_SIM_NOUN = {}
DB_ADJ = []
FREQ_SIM_ADJ = {}

###############################################################
#       T E S T   NOUNS                                       #
###############################################################
class TestNoun(TestCase):
    """Test cases for Noun
    alternatives, plurals, questions
    with and without augment and breakdownrules"""

    @classmethod
    def setUpClass(cls):
        """ Connect and load data needed by tests """
        global DB_NOUN
        global FREQ_SIM_NOUN
        # with open("bsp.csv") as csv_data:
        #     DB_DATA = csv.reader(csv_data, delimiter=";")

        noun0 = dbc.Noun(['8336', 'ubwinshi', 'ubwiínshi',
                          'ubw', 'inshi', '', '', '', '1',
                          '8', 'NULL', '14', 'NULL', '', '', '', '', '',
                          '0', '', '1', '', 'NULL'])
        noun1 = dbc.Noun(['6273', 'umupadiri', 'umupáadíri',
                          'umu', 'padiri', '', '', 'aba', '1',
                          '1', '1', '1', '2',
                          'umupatiri;umupadri; umupatri;patiri;padiri',
                          'umu', '', '', '',
                          '0', '', '0', '', 'la'])
        noun2 = dbc.Noun(['14', 'umwaka', 'umwáaka',
                          'umw', 'aka', '', '', 'imy', '1',
                          '2', '2', '3', '4', '', '', '', '', '',
                          '0', '', '0', '', 'NULL'])
        noun3 = dbc.Noun(['5965', 'inzira', 'inzira',
                          'in', 'zira', '', '', 'in', '1',
                          '3', '3', '9', '10', '', '', '', '', '',
                          '0', '', '0', '', 'NULL'])
        noun4 = dbc.Noun(['5939', 'izina', 'izína',
                          'i', 'zina', '', '', 'ama', '1',
                          '5', '5', '5', '6', '', '', '', '', '',
                          '0', '', '0', '', 'NULL'])
        noun5 = dbc.Noun(['1074', 'amagara', '', 'ama',
                          'gara', '', '', '', '1',
                          'NULL', '5', 'NULL', '6', '', '', '', '', '',
                          '0', '', '0', '', 'NULL'])
        noun6 = dbc.Noun(['3314', 'ikintu', 'ikiintu',
                          'iki', 'ntu', '', '', 'ibi', '1',
                          '4', '4', '7', '8', '', '', '', '', '',
                          '0', '', '0', '', 'NULL'])
        noun7 = dbc.Noun(['6664', 'icaha', 'icáaha',
                          'ic', 'aha', '', '', 'ivy', '1',
                          '4', '4', '7', '8', '', '', '', '', '',
                          '0', '', '0', '', 'NULL'])
        noun8 = dbc.Noun(['2905', 'urukundo', 'urukúundo',
                          'uru', 'kundo', '', '', '', '1',
                          '6', 'NULL', '11', 'NULL', '', '', '', '', '',
                          '0', '', '0', '', 'NULL'])
        noun9 = dbc.Noun(['6805', 'agashusho', 'agashusho',
                          'aga', 'shusho', '', '', 'udu', '1',
                          '7', '7', '12', '13', '', '', '', '', '',
                          '0', '', '0', '', 'NULL'])
        noun10 = dbc.Noun(['7193', 'akaburungu', 'akaburuungu',
                           'aka', 'burungu', '', '', 'utu', '1',
                           '7', '7', '12', '13', '', '', '', '', '',
                           '0', '', '0', '', 'NULL'])
        noun11 = dbc.Noun(['6674', 'uruhago', 'uruhago',
                           'uru', 'hago', '', '', 'im', '1',
                           '6', '6', '11', '10', '', '', '', '', '',
                           '0', '', '0', 'impago', 'NULL'])
        noun12 = dbc.Noun(['6677', 'kanseri', 'kaanséeri',
                           '', 'kanseri', '', '', '', '1',
                           '3', '3', '9', '10', 'kansere', '', '', '', '',
                           '0', '', '1', '', 'fr'])
        noun13 = dbc.Noun(['210', 'ukubaho', 'ukubahó',
                           'uku', 'baho', '', '', '', '1',
                           '9', 'NULL', '15', 'NULL', '', '', '', '', '',
                           '0', '', '1', '', 'NULL'])
        DB_NOUN = [noun0, noun1, noun2, noun3, noun4, noun5, noun6, noun7,
                   noun8, noun9, noun10, noun11, noun12, noun13]
        FREQ_SIM_NOUN = {
            'kaburungu': 70, 'akaburungu': 26, 'utuburungu': 2,
            'bakaburungu': 1, 'tuburungu': 1,
            'urukundo': 2011, 'rukundo': 659, 'ntarukundo': 3, 'atarukundo': 1,
            'nurukundo': 1,
            'icaha': 927, 'ivyaha': 440, 'caha': 192, 'vyaha': 101,
            'nicaha': 6, 'bwicaha': 3, 'kucaha': 2, 'nivyaha': 2,
            'kuvyaha': 2, 'atacaha': 1,
            'nticahama': 1,
            'mubintu': 11, 'kubintu': 10, 'nikintu': 7, 'ntabintu': 6,
            'kukintu': 3, 'yibintu': 2, 'ryikintu': 1, 'sibintu': 1,
            'ikintuma': 2,
            'nkikintu': 1, 'atanikintu': 1, 'ikikintu': 1, 'magara': 154,
            'hamagara': 58, 'ntamagara': 22,
            'namagara': 2, 'kumagara': 1,
            'guhamagara': 100,
            'kwizina': 5, 'ntazina': 4, 'mwizina': 2,
            'cumwaka': 3, 'numwaka': 3, 'nimyaka': 3, 'wimyaka': 3,
            'kumyaka': 3, 'yumwaka': 2, 'vyumwaka': 2, 'ntamwaka': 1,
            'cimyaka': 1, 'ntamyaka': 1,
            'imwaka': 3,
            'abapatiri': 86, 'umupatiri': 46, 'padri': 30, 'mupatiri': 18,
            'bapatiri': 14, 'abapadiri': 8, 'umupadiri': 6, 'bapadiri': 5,
            'mupadiri': 2, 'cabapatiri': 1, 'bapadri': 1, 'umupatri': 12,
            'mupatri': 8, 'bapatri': 10, 'patiri': 429,
            'mpago': 3
            }

    @classmethod
    def tearDownClass(cls):
        """Disconnect from database"""
        global DB_NOUN
        DB_NOUN = None

    # def setUp(self):
    #     """Setup before each test"""

    # def tearDown(self):
    #     """Clean up after test"""

    def test_possibilities(self):
        """Test prepositions glued directly before noun"""
        self.assertEqual(DB_NOUN[2]._possibilities("umwaka"),
                         [r"^([na]ta|[mk]u|s?i)?mwaka$",
                          r"^([bkmrt]?w|[rv]?y|[nsckzbh])?umwaka$"])
        self.assertEqual(DB_NOUN[12]._possibilities("kanseri"),
                         [r"^([na]ta|[mk]u|s?i)?kanseri$",
                          r"^([nckzbh]|[bkmrt]?w|[rv]?y)[ao]kanseri$"])

    def test_init_simple(self):
        """Test direct initializations"""
        self.assertEqual(DB_NOUN[1].lemma, "umupadiri")
        self.assertEqual(DB_NOUN[1].dbid, "6273")
        self.assertEqual(DB_NOUN[1].pos, "NOUN")
        self.assertEqual(DB_NOUN[1].stem, "padiri")

    def test_set_questions_collection(self):
        """Test collect alternatives and plural"""
        self.assertEqual(DB_NOUN[1].alternatives,
                         ['umupatiri', 'umupadri', 'umupatri', 'patiri',
                          'padiri'])
        self.assertEqual(DB_NOUN[1].coll, ['umupadiri', 'abapadiri',
                                           'umupatiri', 'abapatiri',
                                           'umupadri', 'abapadri',
                                           'umupatri', 'abapatri',
                                           'patiri', 'padiri'])
        self.assertEqual(DB_NOUN[11].coll, ['uruhago', 'impago'])

    def test_set_questionsl(self):
        """Test questions for all alternatives"""
        self.assertEqual(DB_NOUN[2].questions,
                         [r"^([na]ta|[mk]u|s?i)?mwaka$",
                          r"^([bkmrt]?w|[rv]?y|[nsckzbh])?umwaka$",
                          r"^([na]ta|[mk]u|s?i)?myaka$",
                          r"^([bkmrt]?w|[rv]?y|[nsckzbh])?imyaka$"])

    def test_partition(self):
        """Test part of nouns collecting before or after verbs"""
        part1, part2 = dbc.noun_partition(DB_NOUN)
        self.assertEqual(len(part1), 12)
        self.assertEqual(len(part2), 2)
        for noun in part2:
            self.assertIn(noun.lemma, ["ubwinshi", "ukubaho"])

    def test_collect_nouns(self):
        """Test collecting all variants of nouns"""
        collection, freq_subs = dbc.collect_nouns(DB_NOUN, FREQ_SIM_NOUN)
        types_num = 0
        for i in collection:
            types_num += i[4]
        self.assertEqual(len(freq_subs), 7)
        self.assertEqual(types_num, 62)
        for i in ['nticahama', 'guhamagara', 'ikintuma', 'nkikintu',
                  'atanikintu', 'ikikintu']:
            self.assertIn(i, freq_subs)


###############################################################
#       T E S T   ADJECTIVES                                  #
###############################################################
class TestAdj(TestCase):
    """ Test for Adjectives
    alternatives, all classes, double-stem """

    @classmethod
    def setUpClass(cls):
        """ Connect and load data needed by tests """
        global DB_ADJ
        global FREQ_SIM_ADJ
        # with open("bsp.csv") as csv_data:
        #     DB_DATA = csv.reader(csv_data, delimiter=";")

        adj0 = dbc.Adjectiv(['3943', '-re-re', '-ree-re',
                             '-', 're-re', '', '', '', '2',
                             '', '', '', '', '', '', '', '', '',
                             '0', '', '0', '', 'NULL'])
        adj1 = dbc.Adjectiv(['2190', '-inshi', '',
                             '-', 'inshi', '', '', '', '2',
                             '', '', '', '', '', '', '', '', '',
                             '0', '', '2', '', 'NULL'])
        adj2 = dbc.Adjectiv(['2937', '-kuru', 'kuru',
                             '-', 'kuru', '', '', '', '2',
                             '', '', '', '', '-kuru-kuru', '', '', '', '',
                             '0', '', '0', '', 'NULL'])
        adj3 = dbc.Adjectiv(['3141', '-ompi', '',
                             '-', 'ompi', 'ompi', '', '', '2',
                             '', '', '', '', 'mwempi; twempi', '', '', '', '',
                             '0', '', '0', '', 'NULL'])
        adj4 = dbc.Adjectiv(['3274', '-nini', '',
                             '-', 'nini', 'nini', '', '', '2',
                             '', '', '', '', '', '', '', '', '',
                             '0', '', '0', '', 'NULL'])
        DB_ADJ = [adj0, adj1, adj2, adj3, adj4]
        FREQ_SIM_ADJ = {
            'abarekure': 1, 'arekure': 3, 'barebare': 7, 'barekure': 4,
            'birebire': 45, 'biregure': 1, 'birekure': 1, 'buregure': 1,
            'burekure': 1, 'burezire': 1, 'harehare': 3, 'ibirebire': 1,
            'irekure': 2, 'karekare': 23, 'kirekire': 147, 'kirerire': 1,
            'kurekure': 3, 'maremare': 28, 'miremire': 37, 'murekure': 7,
            'muremure': 81, 'rirerire': 28, 'rurerure': 35, 'turekure': 2,
            'turerure': 1, 'tureture': 6, 'uburegare': 1, 'umurekure': 1,
            'umuremure': 1, 'urekure': 4, 'yiregure': 8, 'zirezire': 4,
            'ndende': 53,
            'abenshi': 164, 'ahenshi': 12, 'akenshi': 58, 'amenshi': 2,
            'benshi': 2629, 'henshi': 88, 'imyinshi': 2, 'inyinshi': 2,
            'ivyinshi': 11, 'iyinshi': 1, 'menshi': 982, 'myinshi': 433,
            'nyinshi': 822,
            'ahakuru': 4, 'akakuru': 11, 'akuru': 3, 'bikuru': 310,
            'gikuru': 102, 'hakuru': 12, 'ibikuru': 44, 'igikuru': 78,
            'ikikuru': 1, 'ikuru': 2, 'imikuru': 2, 'irikuru': 1, 'kakuru': 2,
            'kikuru': 10, 'mikuru': 217, 'mkuru': 1, 'rikuru': 138,
            'rukuru': 36, 'tukuru': 1, 'ukukuru': 1, 'ukuru': 2, 'utukuru': 2,
            'wukuru': 1,
            'bompi': 87, 'bwompi': 1, 'hompi': 2, 'mwempi': 8, 'twempi': 10,
            'twompi': 6, 'vyompi': 32, 'yompi': 168, 'zompi': 8,
            'abanini': 3, 'ahanini': 273, 'banini': 5, 'hanini': 31,
            'kanini': 132, 'kunini': 5, 'manini': 65, 'minini': 11,
            'munini': 198, 'rinini': 75, 'runini': 126, 'tunini': 8,
            'umunini': 2, 'utunini': 2, 'zinini': 3
            }

    @classmethod
    def tearDownClass(cls):
        """Disconnect from database"""
        global DB_ADJ
        DB_ADJ = None

    # def setUp(self):
    #     """Setup before each test"""

    # def tearDown(self):
    #     """Clean up after test"""

    def test_init_simple(self):
        """Test direct initializations"""
        self.assertEqual(DB_ADJ[0].lemma, "-re-re")
        self.assertEqual(DB_ADJ[0].dbid, "3943")
        self.assertEqual(DB_ADJ[0].pos, "ADJ")
        self.assertEqual(DB_ADJ[0].stem, "re-re")

    def test_set_questionsl(self):
        """Test questions for all alternatives"""
        self.assertEqual(
            DB_ADJ[1].questions,
            ['^((a?[bkmh]e)|(u?[bkmrt]?w[i]+)|(i?[mnrv]?yi|n?zi|[bc]i))(nshi)$'])
        self.assertEqual(len(DB_ADJ[2].questions), 2)
        self.assertEqual(len(DB_ADJ[3].questions), 3)
        self.assertEqual(
            DB_ADJ[4].questions,
            ['^((a?[bgkmhy]?a)|(i?[bgkmryz]?i)|(u?[bgkmrdtwy]?u)|[mn])(nini)$'])
        self.assertEqual(len(DB_ADJ[0].questions), 2)

    def test_collect_adjs(self):
        """Test collecting adjectives for all classes"""
        collection, freq_no_adj = dbc.collect_adjs(DB_ADJ, FREQ_SIM_ADJ)
        types_num = 0
        for i in collection:
            types_num += i[4]
        self.assertEqual(len(freq_no_adj), 17)
        self.assertEqual(types_num, 76)
        for i in ['barekure', 'arekure', 'barekure', 'biregure', 'birekure',
                  'buregure', 'burekure', 'burezire', 'irekure', 'kirerire',
                  'murekure', 'turekure', 'turerure', 'uburegare', 'umurekure',
                  'urekure', 'yiregure']:
            self.assertIn(i, freq_no_adj)
