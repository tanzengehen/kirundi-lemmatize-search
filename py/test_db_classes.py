#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 30 14:01:20 2023

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
#       TEST   N O U N S                                   #
###############################################################
class TestNoun(TestCase):
    """Test cases for Noun
    alternatives, plurals, questions
    with and without augment, also breakdownrules"""

    @classmethod
    def setUpClass(cls):
        """ Connect and load data needed by tests """
        global DB_DATA
        global FREQ_SIM
        # with open("bsp.csv") as csv_data:
        #     DB_DATA = csv.reader(csv_data, delimiter=";")

        DB_DATA = [
            dbc.Noun(['8336', 'ubwinshi', 'ubwiínshi',
                      'ubw', 'inshi', '', '', '', '1',
                      '8', 'NULL', '14', 'NULL', '', '', '', '', '',
                      '0', '', '1', '', 'NULL']),
            dbc.Noun(['6273', 'umupadiri', 'umupáadíri',
                      'umu', 'padiri', '', '', 'aba', '1',
                      '1', '1', '1', '2',
                      'umupatiri;umupadri; umupatri;patiri;padiri',
                      'umu', '', '', '',
                      '0', '', '0', '', 'la']),
            dbc.Noun(['14', 'umwaka', 'umwáaka',
                      'umw', 'aka', '', '', 'imy', '1',
                      '2', '2', '3', '4', '', '', '', '', '',
                      '0', '', '0', '', 'NULL']),
            dbc.Noun(['5965', 'inzira', 'inzira',
                      'in', 'zira', '', '', 'in', '1',
                      '3', '3', '9', '10', '', '', '', '', '',
                      '0', '', '0', '', 'NULL']),
            dbc.Noun(['5939', 'izina', 'izína',
                      'i', 'zina', '', '', 'ama', '1',
                      '5', '5', '5', '6', '', '', '', '', '',
                      '0', '', '0', '', 'NULL']),
            # no5
            dbc.Noun(['1074', 'amagara', '', 'ama',
                      'gara', '', '', '', '1',
                      'NULL', '5', 'NULL', '6', '', '', '', '', '',
                      '0', '', '0', '', 'NULL']),
            dbc.Noun(['3314', 'ikintu', 'ikiintu',
                      'iki', 'ntu', '', '', 'ibi', '1',
                      '4', '4', '7', '8', '', '', '', '', '',
                      '0', '', '0', '', 'NULL']),
            dbc.Noun(['6664', 'icaha', 'icáaha',
                      'ic', 'aha', '', '', 'ivy', '1',
                      '4', '4', '7', '8', '', '', '', '', '',
                      '0', '', '0', '', 'NULL']),
            dbc.Noun(['2905', 'urukundo', 'urukúundo',
                      'uru', 'kundo', '', '', '', '1',
                      '6', 'NULL', '11', 'NULL', '', '', '', '', '',
                      '0', '', '0', '', 'NULL']),
            dbc.Noun(['6805', 'agashusho', 'agashusho',
                      'aga', 'shusho', '', '', 'udu', '1',
                      '7', '7', '12', '13', '', '', '', '', '',
                      '0', '', '0', '', 'NULL']),
            # no10
            dbc.Noun(['7193', 'akaburungu', 'akaburuungu',
                      'aka', 'burungu', '', '', 'utu', '1',
                      '7', '7', '12', '13', '', '', '', '', '',
                      '0', '', '0', '', 'NULL']),
            dbc.Noun(['6674', 'uruhago', 'uruhago',
                      'uru', 'hago', '', '', 'im', '1',
                      '6', '6', '11', '10', '', '', '', '', '',
                      '0', '', '0', 'impago', 'NULL']),
            dbc.Noun(['6677', 'kanseri', 'kaanséeri',
                      '', 'kanseri', '', '', '', '1',
                      '3', '3', '9', '10', 'kansere', '', '', '', '',
                      '0', '', '1', '', 'fr']),
            # no13
            dbc.Noun(['210', 'ukubaho', 'ukubahó',
                      'uku', 'baho', '', '', '', '1',
                      '9', 'NULL', '15', 'NULL', '', '', '', '', '',
                      '0', '', '1', '', 'NULL'])
        ]
        FREQ_SIM = {
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
        global DB_DATA
        DB_DATA = None

    # def setUp(self):
    #     """Setup before each test"""

    # def tearDown(self):
    #     """Clean up after test"""

    def test_possibilities(self):
        """Test prepositions glued directly before noun"""
        self.assertEqual(DB_DATA[2]._possibilities("umwaka"),
                         [r"^([na]ta|[mk]u|s?i)?mwaka$",
                          r"^([bkmrt]?w|[rv]?y|[nsckzbh])?umwaka$"])
        self.assertEqual(DB_DATA[12]._possibilities("kanseri"),
                         [r"^([na]ta|[mk]u|s?i)?kanseri$",
                          r"^([nckzbh]|[bkmrt]?w|[rv]?y)[ao]kanseri$"])

    def test_init_simple(self):
        """Test direct initializations"""
        self.assertEqual(DB_DATA[1].lemma, "umupadiri")
        self.assertEqual(DB_DATA[1].dbid, "6273")
        self.assertEqual(DB_DATA[1].pos, "NOUN")
        self.assertEqual(DB_DATA[1].stem, "padiri")

    def test_set_questions_collection(self):
        """Test collect alternatives and plural"""
        self.assertEqual(DB_DATA[1].alternatives,
                         ['umupatiri', 'umupadri', 'umupatri', 'patiri',
                          'padiri'])
        self.assertEqual(DB_DATA[1].coll, ['umupadiri', 'abapadiri',
                                           'umupatiri', 'abapatiri',
                                           'umupadri', 'abapadri',
                                           'umupatri', 'abapatri',
                                           'patiri', 'padiri'])
        self.assertEqual(DB_DATA[11].coll, ['uruhago', 'impago'])

    def test_set_questionsl(self):
        """Test questions for all alternatives"""
        self.assertEqual(DB_DATA[2].questions,
                         [r"^([na]ta|[mk]u|s?i)?mwaka$",
                          r"^([bkmrt]?w|[rv]?y|[nsckzbh])?umwaka$",
                          r"^([na]ta|[mk]u|s?i)?myaka$",
                          r"^([bkmrt]?w|[rv]?y|[nsckzbh])?imyaka$"])

    def test_partition(self):
        """Test part of nouns collecting before or after verbs"""
        part1, part2 = dbc.noun_partition(DB_DATA)
        self.assertEqual(len(part1), 12)
        self.assertEqual(len(part2), 2)
        for noun in part2:
            self.assertIn(noun.lemma, ["ubwinshi", "ukubaho"])

    def test_collect_nouns(self):
        """Test collecting all variants of nouns"""
        collection, freq_subs = dbc.collect_nouns(DB_DATA, FREQ_SIM)
        # collected
        types_num = 0
        for i in collection:
            types_num += i[4]
        self.assertEqual(len(freq_subs), 7)
        self.assertEqual(types_num, 62)
        # not collected
        for i in ['nticahama', 'guhamagara', 'ikintuma', 'nkikintu',
                  'atanikintu', 'ikikintu']:
            self.assertIn(i, freq_subs)


###############################################################
#       TEST   A D J E C T I V E S                            #
###############################################################
class TestAdjectives(TestCase):
    """Test cases for Adjective
    alternatives, all classes, double-stem """

    @classmethod
    def setUpClass(cls):
        """ Connect and load data needed by tests """
        global DB_DATA
        global FREQ_SIM
        # with open("bsp.csv") as csv_data:
        #     DB_DATA = csv.reader(csv_data, delimiter=";")

        DB_DATA = [
            dbc.Adjectiv(['3943', '-re-re', '-ree-re',
                          '-', 're-re', '', '', '', '2',
                          '', '', '', '', '', '', '', '', '',
                          '0', '', '0', '', 'NULL']),
            dbc.Adjectiv(['2190', '-inshi', '',
                          '-', 'inshi', '', '', '', '2',
                          '', '', '', '', '', '', '', '', '',
                          '0', '', '2', '', 'NULL']),
            dbc.Adjectiv(['2937', '-kuru', 'kuru',
                          '-', 'kuru', '', '', '', '2',
                          '', '', '', '', '-kuru-kuru', '', '', '', '',
                          '0', '', '0', '', 'NULL']),
            dbc.Adjectiv(['3141', '-ompi', '',
                          '-', 'ompi', 'ompi', '', '', '2',
                          '', '', '', '', 'mwempi; twempi', '', '', '', '',
                          '0', '', '0', '', 'NULL']),
            dbc.Adjectiv(['3274', '-nini', '',
                          '-', 'nini', 'nini', '', '', '2',
                          '', '', '', '', '', '', '', '', '',
                          '0', '', '0', '', 'NULL'])
        ]
        FREQ_SIM = {
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
        global DB_DATA
        global FREQ_SIM
        DB_DATA = None
        FREQ_SIM = None

    # def setUp(self):
    #     """Setup before each test"""

    # def tearDown(self):
    #     """Clean up after test"""

    def test_init(self):
        """Test direct initializations"""
        self.assertEqual(DB_DATA[0].lemma, "-re-re")
        self.assertEqual(DB_DATA[0].dbid, "3943")
        self.assertEqual(DB_DATA[0].pos, "ADJ")
        self.assertEqual(DB_DATA[0].stem, "re-re")

    def test_set_questionsl(self):
        """Test questions for all alternatives"""
        self.assertEqual(
            DB_DATA[1].questions,
            ['^((a?[bkmh]e)|(u?[bkmrt]?w[i]+)|(i?[mnrv]?yi|n?zi|[bc]i))(nshi)$'])
        self.assertEqual(len(DB_DATA[2].questions), 2)
        self.assertEqual(len(DB_DATA[3].questions), 3)
        self.assertEqual(
            DB_DATA[4].questions,
            ['^((a?[bgkmhy]?a)|(i?[bgkmryz]?i)|(u?[bgkmrdtwy]?u)|[mn])(nini)$'])
        self.assertEqual(len(DB_DATA[0].questions), 2)

    def test_collect_adjs(self):
        """Test collecting adjectives for all classes"""
        collection, freq_no_adj = dbc.collect_adjs(DB_DATA, FREQ_SIM)
        # collected
        types_num = 0
        for i in collection:
            types_num += i[4]
        self.assertEqual(len(freq_no_adj), 17)
        self.assertEqual(types_num, 76)
        # not collected
        for i in ['barekure', 'arekure', 'barekure', 'biregure', 'birekure',
                  'buregure', 'burekure', 'burezire', 'irekure', 'kirerire',
                  'murekure', 'turekure', 'turerure', 'uburegare', 'umurekure',
                  'urekure', 'yiregure']:
            self.assertIn(i, freq_no_adj)


###############################################################
#       TEST   P R O N O U N S                                #
###############################################################
class TestPronouns(TestCase):
    """Test cases for Pronouns
    from db and built, alternatives, all classes"""

    @classmethod
    def setUpClass(cls):
        """ Connect and load data needed by tests """
        global DB_DATA
        global FREQ_SIM
        # with open("bsp.csv") as csv_data:
        #     DB_DATA = csv.reader(csv_data, delimiter=";")

        DB_DATA = [
            kv.Lemma(['8274', 'iki', 'iki',
                      '', 'iki', '', '', '', '5',
                      '', '', '', '', '', '', '', '', '',
                      '0', '', '1', '', 'NULL']),
            kv.Lemma(['8098', '-abo', '-abo',
                      '-', 'abo', '', '', '', '5',
                      '', '', '', '', '', '', '', '', '',
                      '0', '', '0', '', 'NULL']),
            kv.Lemma(['1458', 'hano', 'háno',
                      'ha', 'no', '', '', '', '5',
                      '', '', '', '', '', '', '', '', '',
                      '0', '', '0', '', 'NULL']),
            kv.Lemma(['5447', 'twebwe', 'tweebwé',
                      '', 'twebwe', '', '', '', '5',
                      '', '', '', '', 'twebge;tweho', '', '', '', '',
                      '0', '', '0', '', 'NULL']),
            kv.Lemma(['7863', 'igihe?', 'ígihe?',
                      'igi', 'he?', '', '', '', '5',
                      '', '', '', '', '', '', '', '', '',
                      '0', '', '0', '', 'NULL'])
        ]
        FREQ_SIM = {
            'iki': 6373, 'igi': 3,
            'twebge': 5, 'twebwe': 2060, 'tweho': 130,
            'abiwabo': 15, 'biwabo': 1, 'iwabo': 600, 'iziwabo': 2,
            'kubwabo': 14, 'rwiwabo': 1, 'twabo': 27, 'uwabo': 17, 'wiwabo': 1,
            'yiwabo': 2, 'ziwabo': 1,
            'ahabo': 11, 'akabo': 2, 'icabo': 8, 'iryabo': 7, 'ivyabo': 171,
            'iyabo': 5, 'izabo': 156, 'mwabo': 1, 'nyabo': 18, 'ubwabo': 59,
            'urwabo': 26, 'utwabo': 91,
            'ahano': 4, 'akano': 5, 'ano': 139, 'bano': 290, 'bino': 111,
            'buno': 481, 'hano': 1048, 'ino': 1193, 'irino': 5, 'kano': 155,
            'kino': 657, 'kuno': 59, 'rino': 77, 'runo': 55, 'tuno': 8,
            'ubuno': 1, 'uno': 1611, 'utuno': 1, 'zino': 66,
            'catwo': 2, 'cavyo': 49, 'cawo': 21, 'cayo': 134, 'cazo': 13,
            'habo': 4, 'haho': 4, 'haryo': 2
            }

    @classmethod
    def tearDownClass(cls):
        """Disconnect from database"""
        global DB_DATA
        global FREQ_SIM
        DB_DATA = None
        FREQ_SIM = None

    def test_init(self):
        """Test direct initializations"""
        # single instance
        self.assertEqual(DB_DATA[0].lemma, "iki")
        self.assertEqual(DB_DATA[0].dbid, "8274")
        self.assertEqual(DB_DATA[0].pos, "PRON")
        self.assertEqual(DB_DATA[0].questions, ["iki",])
        # test-db
        self.assertEqual(len(DB_DATA), 5)

    def test_build_pronouns(self):
        """Test composed pronouns"""
        pronouns = dbc.build_pronouns()
        self.assertEqual(len(pronouns), 31)
        self.assertEqual(pronouns[5].lemma, '-o')
        self.assertEqual(pronouns[5].dbid, 40002)
        self.assertEqual(pronouns[5].questions,
                         ['^([bkrt]?w|[rv]?y|[bchkz])o?$',])
        self.assertEqual(pronouns[9].lemma, 'nyene')
        self.assertEqual(pronouns[9].dbid, 3402)
        self.assertEqual(len(pronouns[9].questions), 4)
        self.assertEqual(
            pronouns[9].questions[0],
            '^(na)?((([jw]|[mt]w)e)|([bkrt]?w|[rv]?y|[bchkz])o)nyene$')
        self.assertEqual(pronouns[13].lemma, '-ryo')
        self.assertEqual(pronouns[13].dbid, 40014)
        self.assertEqual(pronouns[13].questions,
                         ['^((a?[bhk]a|i?[bkrz]i|u?[bkrt]u)|[aiu])ryo$'])
        self.assertEqual(pronouns[23].lemma, 'si-')
        self.assertEqual(pronouns[23].dbid, 40012)
        self.assertEqual(pronouns[23].questions,
                         ['^si([bkrt]?w|[rv]?y|[bchkz])o?$'])
        self.assertEqual(pronouns[30].lemma, '-abo')
        self.assertEqual(pronouns[30].dbid, 8098)
        self.assertEqual(len(pronouns[30].questions), 2)
        self.assertEqual(
            pronouns[30].questions[1],
            '^([bkrt]?w|[rv]?y|[bchkz])abo$')

    def test_collect_pronouns(self):
        """Test collect pronouns from db and composed ones """
        collection, freq_no_prn = dbc.collect_pronouns(DB_DATA, FREQ_SIM)
        types_num = 0
        for i in collection:
            types_num += i[4]
        # collected types
        self.assertEqual(types_num, 42)
        # collected lemmata
        self.assertEqual(len(collection), 5)
        # not collected
        self.assertEqual(len(freq_no_prn), 13)
        for no_pronoun in ['igi', 'ahabo', 'akabo', 'icabo', 'iryabo',
                           'ivyabo', 'iyabo', 'izabo', 'mwabo', 'nyabo',
                           'ubwabo', 'urwabo', 'utwabo']:
            self.assertIn(no_pronoun, freq_no_prn)
        # right lemma for merged types
        self.assertEqual(collection[0][0], '-no')


###############################################################
#       TEST   A D V E R B S   etc.                           #
###############################################################
class TestAdverbsEtc(TestCase):
    """Test cases for unchanging words: Adverbs, Prepositions,
    conjunctions, interjections
    lemmata, alternatives"""

    @classmethod
    def setUpClass(cls):
        """ Connect and load data needed by tests """
        global DB_DATA
        global FREQ_SIM
        DB_DATA = [
            kv.Lemma(['7121', 'ubu nyene', 'ubu nyéne',
                      '', 'ubu nyene', '', '', '', '6',
                      '', '', '', '', 'ubunyene', '', '', '', '',
                      '0', '', '0', '', 'NULL']),
            kv.Lemma(['5519', 'inyuma', 'inyuma	',
                      'i', 'nyuma', '', '', '', '7',
                      '', '', '', '', '', '', '', '', '',
                      '0', '', '0', '', 'NULL']),
            kv.Lemma(['5525', 'umengo', 'umeengo',
                      '', 'umengo', '', '', '', '8',
                      '', '', '', '', '', '', '', '', '',
                      '0', '', '0', '', 'NULL']),
            kv.Lemma(['6121', 'i ruhande', 'i ruhánde',
                      'i ru', 'hande', '', '', '', '3',
                      '', '', '', '', 'iruhande', '', '', '', '',
                      '0', '', '0', '', 'NULL']),
            kv.Lemma(['7505', 'mirongwitatu', 'miroongwitaatu',
                      '', 'mirongwitatu', '', '', '', '6',
                      '', '', '', '', 'mirongo itatu;mirongitatu', '', '', '',
                      '', '0', '', '0', '', 'NULL']),
            ]
        FREQ_SIM = {
            'mirongwitatu': 19, 'mirongoitatu': 1, 'mirongitatu': 3,
            'samunani': 13, 'iruhande': 56, 'ubu': 2927, 'nyene': 1544,
            'mirongo': 202,
            }

    @classmethod
    def tearDownClass(cls):
        """Disconnect from database"""
        global DB_DATA
        global FREQ_SIM
        DB_DATA = None
        FREQ_SIM = None

    def test_init(self):
        """Test direct initializations"""
        # test single instance
        ubunyene = kv.Lemma(['7121', 'ubu nyene', 'ubu nyéne',
                             '', 'ubu nyene', '', '', '', '6',
                             '', '', '', '', 'ubunyene', '', '', '', '',
                             '0', '', '0', '', 'NULL'])
        self.assertEqual(ubunyene.lemma, "ubu nyene")
        self.assertEqual(ubunyene.dbid, "7121")
        self.assertEqual(ubunyene.pos, "ADV")
        # test test-database
        self.assertEqual(len(DB_DATA), 5)
        self.assertEqual(DB_DATA[0].lemma, "ubu nyene")
        self.assertEqual(DB_DATA[0].dbid, "7121")
        self.assertEqual(DB_DATA[0].pos, "ADV")
        self.assertEqual(DB_DATA[0].questions, ["ubu nyene", "ubunyene"])
        self.assertEqual(DB_DATA[1].pos, "CONJ")
        self.assertEqual(DB_DATA[2].pos, "INTJ")
        self.assertEqual(DB_DATA[3].pos, "PREP")

    def test_collect_adverbs_plus(self):
        """Test collection unchanging words"""
        collection, freq_no_advbs = dbc.collect_adv_plus(DB_DATA, FREQ_SIM)
        types_num = 0
        for i in collection:
            types_num += i[4]
            print(i)
        # found types
        self.assertEqual(types_num, 3)
        # found lemmata
        self.assertEqual(len(collection), 2)
        # not collected
        self.assertEqual(len(freq_no_advbs), 5)


###############################################################
#       TEST   E X C L A M A T I O N S                        #
###############################################################
class TestExclamations(TestCase):
    """Test cases for Exclamations
    from db and built"""

    @classmethod
    def setUpClass(cls):
        """ Connect and load data needed by tests """
        global DB_DATA
        global FREQ_SIM
        DB_DATA = [
            kv.Lemma(['818', 'ego', '',
                      '', 'ego', '', '', '', '8',
                      '', '', '', '', '', '', '', '', '',
                      '0', '', '0', '', 'NULL']),
            kv.Lemma(['3556', 'oya', 'oya',
                      '', 'oya', '', '', '', '8',
                      '', '', '', '', '', '', '', '', '6570',
                      '0', '', '0', '', 'NULL']),
            kv.Lemma(['7307', 'karibu', 'ikaribú',
                      '', 'karibu', '', '', '', '8',
                      '', '', '', '', '', '', '', '', '',
                      '0', '', '0', '', 'sw']),
            kv.Lemma(['7196', 'egome', 'eegóme',
                      '', 'egome', '', '', '', '8',
                      '', '', '', '', 'ego me', '', '', '', '',
                      '0', '', '0', '', 'NULL'])
            ]
        FREQ_SIM = {'karibu': 5, 'egome': 1, 'ego': 38, 'eeeego': 11,
                    'eeeeh': 191, 'eeego': 15, 'eeegoo': 2, 'oyaa': 117,
                    'oyaaa': 99, 'oya': 2785, 'oyayeeeee': 1, 'oyaye': 128,
                    'oyaha': 27, 'oyaaaah': 2, 'oyaah': 2
                    }

    @classmethod
    def tearDownClass(cls):
        """Disconnect from database"""
        global DB_DATA
        global FREQ_SIM
        DB_DATA = None
        FREQ_SIM = None

    def test_init(self):
        """Test direct initializations"""
        self.assertEqual(len(DB_DATA), 4)
        self.assertEqual(DB_DATA[0].lemma, "ego")
        self.assertEqual(DB_DATA[0].dbid, "818")
        self.assertEqual(DB_DATA[0].pos, "INTJ")
        self.assertEqual(DB_DATA[0].questions, ["ego",])

    def test_build_exclamations(self):
        """Test build exclamations"""
        exclamations = dbc.build_exclamations()
        self.assertEqual(len(exclamations), 12)
        for i in exclamations:
            self.assertIn(
                i.lemma, ["ego", "oya", "ha", "la", "aah", "ooh", "mh", "hee",
                          "kyee", "alleluia", "alo", "euh"])
        self.assertEqual(exclamations[3].dbid, 30001)
        self.assertEqual(exclamations[3].pos, "INTJ")
        self.assertEqual(exclamations[3].questions, [r"^(la)+$",])

    def test_collect_exclamations(self):
        """Test collect exclamations
        from db and built with regex"""
        collection, freq_no_excl = dbc.collect_exclamations(DB_DATA, FREQ_SIM)
        types_num = 0
        for i in collection:
            types_num += i[4]
        self.assertEqual(types_num + len(freq_no_excl), len(FREQ_SIM))
        # found types
        self.assertEqual(types_num, 10)
        # found lemmata
        self.assertEqual(len(collection), 4)
        # not colllected
        self.assertEqual(len(freq_no_excl), 5)


###############################################################
#       TEST   F O R E I G N words and N A M E S (Persons)    #
###############################################################
class TestForeign(TestCase):
    """Test case for collecting Foreign words"""

    @classmethod
    def setUpClass(cls):
        """ Connect and load data needed by tests """
        global NE_DATA
        global FREQ_SIM
        NE_DATA = [
            dbc.Foreign(['blé ', '', 'f', '', '']),
            dbc.Foreign(['Gärten', '', 'F', '', '']),
            dbc.Foreign([' Noël', '', 'F', '', '']),
            dbc.NamedEntities(['euro', '', 'PROPN_CUR', '', 'EUR; euros']),
            dbc.NamedEntities(['barça', '', 'PROPN_ORG', '', 'barca']),
            dbc.NamedEntities(['dmn-tre', '', 'PROPN_SCI', '', 'dmn;tre']),
            dbc.NamedEntities(['Nsengiyumva', '', 'PROPN_NAM', '', '']),
            ]
        FREQ_SIM = {
            'ble': 2, 'garten': 7, 'noel': 33, 'euro': 12, 'euros': 12,
            'nyumva': 14, 'eur': 6, 'barca': 8, 'dmn': 6, 'tre': 6,
            'nsengiyumva': 15
            }

    @classmethod
    def tearDownClass(cls):
        """Disconnect from database"""
        global NE_DATA
        global FREQ_SIM
        NE_DATA = None
        FREQ_SIM = None

    def test_initialization_foreign(self):
        """Test direct initialization foreign words"""
        # single instance
        ble = dbc.Foreign(['blé ', '', 'f', '', ''])
        self.assertEqual(ble.lemma, "ble")
        self.assertEqual(ble.dbid, "")
        self.assertEqual(ble.pos, "F")
        # test test-database
        self.assertEqual(len(NE_DATA), 7)
        self.assertEqual(NE_DATA[0].questions, ["ble",])
        self.assertEqual(NE_DATA[1].lemma, "garten")
        self.assertEqual(NE_DATA[2].lemma, "noel")

    def test_initialization_names(self):
        """Test direct initialization names"""
        # single instance
        euro = dbc.NamedEntities(['euro', '', 'PROPN_CUR', '', 'EUR; euros'])
        self.assertEqual(euro.lemma, "euro")
        self.assertEqual(len(euro.alternatives), 3)
        # test test-database
        for i in NE_DATA[3].alternatives:
            self.assertIn(i, ['euro', 'eur', 'euros'])
        self.assertEqual(NE_DATA[3].pos, "PROPN_CUR")
        self.assertEqual(NE_DATA[4].lemma, "barca")
        self.assertEqual(NE_DATA[4].pos, "PROPN_ORG")
        self.assertEqual(NE_DATA[4].alternatives, ["barca"])
        self.assertEqual(NE_DATA[5].lemma, "dmn-tre")
        self.assertEqual(NE_DATA[5].pos, "PROPN_SCI")
        for i in NE_DATA[5].alternatives:
            self.assertIn(i, ['dmn-tre', 'dmn', 'tre'])
        self.assertEqual(NE_DATA[6].lemma, "nsengiyumva")

    def test_collect_names(self):
        """Test collect names and foreign words"""
        data = NE_DATA[:3]
        for i in NE_DATA[3:]:
            i.questions = i.alternatives
            data.append(i)
        collection, freq_no_names = dbc.collect_names(data, FREQ_SIM)
        self.assertEqual(len(collection), 7)
        types_num = 0
        for i in collection:
            types_num += i[4]
            print(i[0])
        self.assertEqual(types_num, 10)
        self.assertEqual(collection[1][0], 'euro')
        self.assertEqual(collection[1][3], 30)
        self.assertEqual(collection[1][4], 3)
        for i in collection[1][5:]:
            self.assertIn(i[0], ['euro', 'eur', 'euros'])
        # not collected
        self.assertEqual(len(freq_no_names), 1)


###############################################################
#       TEST   N A M E D  E N T I T I E S                     #
###############################################################
class TestNE(TestCase):
    """Test cases for related loacation-person-language Named Entities"""

    @classmethod
    def setUpClass(cls):
        """ Connect and load data needed by tests """
        global FREQ_SIM
        FREQ_SIM = {}

    @classmethod
    def tearDownClass(cls):
        """Disconnect from database"""
        global FREQ_SIM
        FREQ_SIM = None

    def setUp(self):
        global NE_DATA
        NE_DATA = [
            dbc.NamedEntities(['misiri', '',
                               'PROPN_loc', '',
                               'egypt;egiputa;misri;mirisi']),
            dbc.NamedEntities(['ubudagi', '',
                               'PROPN_loc', '',
                               'dagi;german;germany']),
            dbc.NamedEntities(['igihebreyi', '',
                               'PROPN_LNG', '', 'hebrew;hebreyi']),
            dbc.NamedEntities(['ikinyarwanda', '',
                               'PROPN_LNG', '', 'gwanda']),
            dbc.NamedEntities(['ikidagi	', '',
                               'PROPN_LNG', '', 'dagi;dage']),
            dbc.NamedEntities(['umudagi', '',
                               'PROPN_PER', '', 'german;dagi']),
            dbc.NamedEntities(['umworomo', '',
                               'PROPN_PER', '', 'oromo']),
            ]

    def tearDown(self):
        global NE_DATA
        NE_DATA = []

    def test_init_ne(self):
        """Test direct initialization locations, persons, languages"""

        # test single instance
        ubudagi = dbc.NamedEntities(['ubudagi', '', 'PROPN_LOC', '',
                                     'german;germany;dagi'])
        self.assertEqual(ubudagi.lemma, 'ubudagi')
        self.assertEqual(ubudagi.pos, "PROPN_LOC")
        # because it was a set we don't know the order of the alternatives
        self.assertEqual(len(ubudagi.alternatives), 4)
        for i in ['ubudagi', 'german', 'germany', 'dagi']:
            self.assertIn(i, ubudagi.alternatives)

        # test database
        data = [x for x in NE_DATA]
        self.assertEqual(len(data), 7)
        self.assertEqual(len(data[0].alternatives), 5)
        self.assertEqual(data[1].lemma, 'ubudagi')
        self.assertEqual(len(data[1].alternatives), 4)
        for i in ['ubudagi', 'german', 'germany', 'dagi']:
            self.assertIn(i, data[1].alternatives)
        self.assertEqual(data[1].pos, "PROPN_LOC")
        self.assertEqual(
           data[3].row, ['ikinyarwanda', '', 'PROPN_LNG', '', 'gwanda'])
        self.assertEqual(data[3].lemma, 'ikinyarwanda')
        self.assertEqual(len(data[3].alternatives), 2)
        for i in ['ikinyarwanda', 'gwanda']:
            self.assertIn(i, data[3].alternatives)
        self.assertEqual(data[5].lemma, "umudagi")
        self.assertEqual(data[5].pos, "PROPN_PER")
        self.assertEqual(len(data[5].alternatives), 3)
        for i in data[5].alternatives:
            self.assertIn(i, ["umudagi", "german", "dagi"])

    def test_check_entries_location_person_language(self):
        """Test completing: location, language, person
        for all alternatives"""
        # prepare data
        loc = [NE_DATA[0], NE_DATA[1]]
        lng = [NE_DATA[2], NE_DATA[3], NE_DATA[4]]
        per = [NE_DATA[5], NE_DATA[6]]
        # assumed that lemma without augmention is also in alternative-list
        for local in loc:
            local.alternatives = [i for i in local.alternatives
                                  if i[:3] != "ubu"]
        for person in per:
            person.alternatives = [i for i in person.alternatives
                                   if i[:3] not in ["umu", "umw"]]
        for language in lng:
            language.alternatives = [i for i in language.alternatives
                                     if i[:3] not in ["iki", "igi"]]

        # language and person
        self.assertIn('dage', lng[2].alternatives)
        self.assertNotIn('dage', per[0].alternatives)
        lng, per = dbc.check_entries_location_person_language(lng, per)
        for i in ['german', 'dagi', 'dage']:
            self.assertIn(i, per[0].alternatives)
            self.assertIn(i, lng[2].alternatives)

        # language and location
        self.assertIn('dage', lng[2].alternatives)
        self.assertNotIn('dage', loc[1].alternatives)
        for i in ['germany', 'german', 'dagi']:
            self.assertIn(i, loc[1].alternatives)
        loc, lng = dbc.check_entries_location_person_language(loc, lng, "lang")
        for i in ['germany', 'german', 'dagi', 'dage']:
            self.assertIn(i, loc[1].alternatives)
            self.assertIn(i, lng[2].alternatives)

        # location and person
        self.assertNotIn('germany', per[0].alternatives)
        loc, per = dbc.check_entries_location_person_language(loc, per)
        for i in ['germany', 'german', 'dagi', 'dage']:
            self.assertIn(i, per[0].alternatives)
            self.assertIn(i, loc[1].alternatives)
            self.assertIn(i, lng[2].alternatives)

    def test_set_languages(self):
        """Test set questions for PROPN_LNG"""
        # prepare data
        lng = [NE_DATA[2], NE_DATA[3]]
        for language in lng:
            language.alternatives = [i for i in language.alternatives
                                     if i[:3] not in ["iki", "igi"]]
            language.set_languages()
        # test
        self.assertEqual(len(lng[0].questions), 4)
        for i in ['igihebrew', 'gihebrew', 'igihebreyi', 'gihebreyi']:
            self.assertIn(i, lng[0].questions)
        # attention: we assume that stem-only is in alternative-list
        self.assertEqual(len(lng[1].questions), 2)
        for i in ['ikinyagwanda', 'kinyagwanda']:
            self.assertIn(i, lng[1].questions)

    def test_set_persons(self):
        """Test set questions for PROPN_PER"""
        # prepare data
        per = [NE_DATA[5], NE_DATA[6],
               dbc.NamedEntities(['umuntu', '',
                                  'PROPN_PER', '', ''])]
        for person in per:
            person.alternatives = [i for i in person.alternatives
                                   if i[:3] not in ["umu", "umw"]]
            # test
            person.set_persons()
        self.assertEqual(len(per[0].questions), 8)
        for i in [
                '^([na]ta|[mk]u|s?i)?mudagi(kazi)?$',
                '^([bkmrt]?w|[rv]?y|[nsckzbh])?umugerman(kazi)?$',
                '^([na]ta|[mk]u|s?i)?bagerman(kazi)?$',
                '^([bkmrt]?w|[rv]?y|[nsckzbh])?abadagi(kazi)?$'
                ]:
            self.assertIn(i, per[0].questions)
        self.assertEqual(len(per[2].questions), 4)
        self.assertIn('^([na]ta|[mk]u|s?i)?bantu(kazi)?$',
                      per[2].questions)

    def test_perla_from_ub(self):
        """Test creation of language- and person-lemma constructed
        from location with ubu/ubw"""
        # prepare iki
        local = NE_DATA[1]
        local.alternatives = [i for i in local.alternatives if i[:3] != "ubu"]
        self.assertEqual(len(local.alternatives), 3)
        # test iki
        pername, langname = local.perla_from_ub()
        self.assertEqual(pername, "umudagi")
        self.assertEqual(langname, "ikidagi")
        # prepare igi
        local = dbc.NamedEntities(['ubuhindi', '', 'PROPN_LOC', '',
                                   'hinde;hindu;india;endu;indu;hindi'])
        local.alternatives = [i for i in local.alternatives if i[:3] != "ubu"]
        # test igi
        pername, langname = local.perla_from_ub()
        self.assertEqual(pername, "umuhindi")
        self.assertEqual(langname, "igihindi")

    def test_create_new_lang(self):
        """Test create new language-lemma of location"""
        local = NE_DATA[1]
        local.alternatives = [i for i in local.alternatives if i[:3] != "ubu"]
        lang = local.create_new_lang("ikidagi")
        self.assertEqual(lang.lemma, "ikidagi")
        self.assertEqual(len(lang.questions), 6)
        for i in ['ikigerman', 'ikidagi', 'ikigermany',
                  'kigerman', 'kidagi', 'kigermany']:
            self.assertIn(i, lang.questions)

    def test_create_new_person(self):
        """Test create new person-lemma of location"""
        local = NE_DATA[0]
        pers = local.create_new_person("umunya_misiri")
        self.assertEqual(pers.lemma, "umunya_misiri")
        for i in pers.questions:
            print(i)
        self.assertEqual(len(pers.questions), 20)
        for i in ['^([na]ta|[mk]u|s?i)?muny[ae]misiri(kazi)?$',
                  '^([bkmrt]?w|[rv]?y|[nsckzbh])?umunyegypt(kazi)?$',
                  '^([na]ta|[mk]u|s?i)?banyegiputa(kazi)?$',
                  '^([bkmrt]?w|[rv]?y|[nsckzbh])?abany[ae]misri(kazi)?$']:
            self.assertIn(i, pers.questions)

    def test_set_location_and_create_person_language_out_of_location(self):
        """Test set_location_and_create_person_language_out_of_location"""
        # test consonant
        local = NE_DATA[0]
        lang, pers = local.set_location_and_create_person_language_out_of_it()
        self.assertEqual(len(local.questions), 10)
        self.assertEqual(len(lang.questions), 10)
        self.assertEqual(len(pers.questions), 20)

        # test vowel
        local = dbc.NamedEntities(['ostrariya', '', 'PROPN_LOC', '',
                                   'australia;australian'])
        lang, pers = local.set_location_and_create_person_language_out_of_it()
        for i in lang.questions:
            print(i)
        self.assertEqual(len(local.questions), 3)
        self.assertEqual(len(lang.questions), 6)
        self.assertEqual(lang.lemma, "ikinya_ostrariya")
        for i in ['ikinyaustralia', 'kinyostrariya']:
            self.assertIn(i, lang.questions)
        self.assertEqual(len(pers.questions), 12)
        self.assertEqual(pers.lemma, "umunya_ostrariya")
        self.assertIn('^([na]ta|[mk]u|s?i)?banyaustralian(kazi)?$',
                      pers.questions)

        # test ubu + vowel
        local = dbc.NamedEntities(['ubutariyano', '', 'PROPN_LOC', '',
                                   'itariyano; taliyano; tariyano'])
        local.alternatives = [i for i in local.alternatives if i[:3] != "ubu"]
        lang, pers = local.set_location_and_create_person_language_out_of_it()
        for i in local.questions:
            print(i)
        self.assertEqual(len(local.questions), 9)
        self.assertEqual(len(lang.questions), 6)

    def test_complete_location_language_person(self):
        """Test add constructed languages and persons to named-entity-list"""
        # prepare
        ne_dict = {'loc': NE_DATA[:2],
                   'lng': NE_DATA[2:5],
                   'per': NE_DATA[5:],
                   'names': [],
                   'foreign': []
                   }
        # test
        ne_list = dbc.complete_location_language_person(ne_dict)
        locs = 0
        lngs = 0
        pers = 0
        for i in ne_list:
            # print("\nne:", i)
            if i.pos == "PROPN_LOC":
                locs += 1
            elif i.pos == "PROPN_LNG":
                lngs += 1
            elif i.pos == "PROPN_PER":
                pers += 1
        self.assertEqual(len(ne_list), 9)
        self.assertEqual(locs, 2)
        self.assertEqual(lngs, 4)
        self.assertEqual(pers, 3)


###############################################################
#       TEST   L O A D   D A T A                              #
###############################################################
class TestLoading(TestCase):
    """Test loading Named Entities respective rundi dictionary"""

    def test_load_ne(self):
        """Test load Named Entities from csv"""
        ne_data = dbc.load_ne(sd.ResourceNames.root+"/resources/ne_test.csv")
        self.assertEqual(len(ne_data), 5)
        self.assertEqual(len(ne_data.get('loc')), 10)
        self.assertEqual(len(ne_data.get('lng')), 3)
        self.assertEqual(len(ne_data.get('per')), 4)
        self.assertEqual(len(ne_data.get('names')), 24)
        self.assertEqual(len(ne_data.get('foreign')), 4)
        self.assertEqual(ne_data.get('names')[0].pos, 'PROPN_ORG')
        self.assertEqual(ne_data.get('names')[2].lemma, 'bitangwanimana')
        self.assertEqual(ne_data.get('loc')[0].pos, 'PROPN_LOC')
        self.assertEqual(len(ne_data.get('loc')[0].alternatives), 3)
        self.assertEqual(ne_data.get('per')[0].pos, 'PROPN_PER')
        for i in ['umubantu', 'bantu']:
            self.assertIn(i, ne_data.get('per')[1].alternatives)
        self.assertEqual(ne_data.get('lng')[0].pos, 'PROPN_LNG')
        self.assertEqual(ne_data.get('lng')[2].lemma, 'ikizulu')
        self.assertEqual(ne_data.get('foreign')[0].pos, 'F')
        self.assertEqual(ne_data.get('foreign')[1].lemma, 'concert')

    def test_load_dbkirundi(self):
        """Test load rundi dictionary from csv"""
        db_data = dbc.load_dbkirundi(
            sd.ResourceNames.root + "/tests/test_lemmata.csv")
        self.assertEqual(len(db_data), 8)
        self.assertEqual(len(db_data.get('adjectives')), 0)
        self.assertEqual(len(db_data.get('nouns1')), 17)
        self.assertEqual(len(db_data.get('nouns2')), 0)
        self.assertEqual(len(db_data.get('pronouns')), 2)
        self.assertEqual(len(db_data.get('rests')), 1)
        self.assertEqual(len(db_data.get('stems')), 55)
        self.assertEqual(len(db_data.get('unchanging_words')), 9)
        self.assertEqual(len(db_data.get('verbs')), 27)
        self.assertEqual(db_data.get('verbs')[0].lemma, "-ri")
        self.assertEqual(db_data.get('verbs')[0].dbid, "3966")
        self.assertEqual(db_data.get('verbs')[0].pos, "VERB")
        self.assertEqual(db_data.get('verbs')[0].stem, "ri")
        self.assertEqual(db_data.get('verbs')[0].perfective, "")
        self.assertEqual(
            len(db_data.get('verbs')[0].comb), 2)




# def create_test_db():
    # nrs = ids from lemmafreq of test_text
    # db_origin = mysql data

    # test_lemmata = []
    # for i in nrs:
    #     for n in db_origin:
    #         if i == n.split(";")[0].strip('"'):
    #             test_lemmata.append(n)
    # kh.save_list(test_lemmata,
    #              sd.ResourceNames.root + "/tests/test_lemmata.csv")
