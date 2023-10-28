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
    with and without augment and breakdownrules"""

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
        types_num = 0
        for i in collection:
            types_num += i[4]
        self.assertEqual(len(freq_subs), 7)
        self.assertEqual(types_num, 62)
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
        self.assertEqual(DB_DATA[0].lemma, "iki")
        self.assertEqual(DB_DATA[0].dbid, "8274")
        self.assertEqual(DB_DATA[0].pos, "PRON")
        self.assertEqual(DB_DATA[0].questions, ["iki",])

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
        # found types
        self.assertEqual(types_num, 42)
        # found lemmata
        self.assertEqual(len(collection), 5)
        # unknown types
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
        print("test", DB_DATA)
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
        # unknown types
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
        # unknown types
        self.assertEqual(len(freq_no_excl), 5)


###############################################################
#       TEST   F O R E I G N words and N A M E S              #
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
            'eur': 6, 'barca': 8, 'dmn': 6, 'tre': 6, 'nsengiyumva': 15
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
        self.assertEqual(len(NE_DATA), 7)
        self.assertEqual(NE_DATA[0].lemma, "ble")
        self.assertEqual(NE_DATA[0].dbid, "")
        self.assertEqual(NE_DATA[0].pos, "F")
        self.assertEqual(NE_DATA[0].questions, ["ble",])
        self.assertEqual(NE_DATA[1].lemma, "garten")
        self.assertEqual(NE_DATA[2].lemma, "noel")

    def test_initialization_names(self):
        """Test direct initialization names"""
        self.assertEqual(
            NE_DATA[3].row, ['euro', '', 'PROPN_CUR', '', 'EUR; euros'])
        self.assertEqual(NE_DATA[3].lemma, "euro")
        self.assertEqual(len(NE_DATA[3].alternatives), 3)
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
        self.assertEqual(len(freq_no_names), 0)
        self.assertEqual(collection[1][0], 'euro')
        self.assertEqual(collection[1][3], 30)
        self.assertEqual(collection[1][4], 3)
        for i in collection[1][5:]:
            self.assertIn(i[0], ['euro', 'eur', 'euros'])


###############################################################
#       TEST   HELPER                                         #
###############################################################
class TestHelper(TestCase):
    """Test helper functions in db_classes"""

    def test_put_same_ids_together(self):
        """Test merging found types of lemma from db-entry with
        composed types"""
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
        collection = dbc.put_same_ids_together(collection)
        self.assertEqual(len(collection), 2)
        # self.assertEqual(collection[0][0], '-no')
        self.assertIn(['hano', 1048], collection[0])
        self.assertIn(['rino', 77], collection[0])
        self.assertEqual(collection[0][3], 5966)
        self.assertEqual(collection[0][4], 19)
