#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 30 14:01:20 2023

@author: doreen
"""

from unittest import TestCase
import kir_db_classes as dbc
import kir_prepare_verbs as kv
import kir_string_depot as sd

# nosetests --with-spec --spec-color --with-coverage --cover-erase
# coverage report -m


###############################################################
#       TEST   S I N G L E   N O U N                          #
###############################################################
class TestPrepareNoun(TestCase):
    """Test cases for Noun
    alternatives, plurals, questions
    with and without augment, also breakdownrules"""

    def test_possibilities_with_augment(self):
        """Test prepositions glued directly before noun with augment"""
        data = dbc.Noun(
            {'dbid': '14', 'lemma': 'umwaka', 'prefix': 'umw',
             'stem': 'aka', 'perfective': '',
             'prefix_plural': 'imy', 'pos': 'NOUN',
             'alternatives': '', 'alternative_singular': '',
             'alternative_stem': '', 'alternative_perfective': '',
             'plural_irregular': ''})
        self.assertEqual(data._possibilities("umwaka"),
                         [r"^([na]ta|[mk]u|s?i)?mwaka$",
                          r"^([bkmrt]?w|[rv]?y|[nsckzbh])?umwaka$"])

    def test_possibilities_without_augment(self):
        """Test prepositions glued directly before noun without augment"""
        data = dbc.Noun(
            {'dbid': '6677', 'lemma': 'kanseri', 'prefix': '',
             'stem': 'kanseri', 'perfective': '',
             'prefix_plural': '', 'pos': 'NOUN',
             'alternatives': 'kansere', 'alternative_singular': '',
             'alternative_stem': '', 'alternative_perfective': '',
             'plural_irregular': ''})
        self.assertEqual(data._possibilities("kanseri"),
                         [r"^([na]ta|[mk]u|s?i)?kanseri$",
                          r"^([nckzbh]|[bkmrt]?w|[rv]?y)[ao]kanseri$"])

    def test_init_simple(self):
        """Test direct initializations"""
        data = dbc.Noun(
            {'dbid': '6273', 'lemma': 'umupadiri', 'prefix': 'umu',
             'stem': 'padiri', 'perfective': '',
             'prefix_plural': 'aba', 'pos': 'NOUN',
             'alternatives': 'umupatiri;umupadri; umupatri;patiri;padiri',
             'alternative_singular': 'umu',
             'alternative_stem': '', 'alternative_perfective': '',
             'plural_irregular': ''})
        self.assertEqual(data.lemma, "umupadiri")
        self.assertEqual(data.dbid, "6273")
        self.assertEqual(data.pos, "NOUN")
        self.assertEqual(data.stem, "padiri")
        self.assertEqual(data.alternatives,
                         ['umupatiri', 'umupadri', 'umupatri', 'patiri',
                          'padiri'])
        self.assertEqual(data.coll, ['umupadiri', 'abapadiri',
                                     'umupatiri', 'abapatiri',
                                     'umupadri', 'abapadri',
                                     'umupatri', 'abapatri',
                                     'patiri', 'padiri'])

    def test_exception_plural(self):
        """Test irregular plural"""
        data = dbc.Noun(
            {'dbid': '6674', 'lemma': 'uruhago', 'prefix': 'uru',
             'stem': 'hago', 'perfective': '',
             'prefix_plural': 'im', 'pos': 'NOUN',
             'alternatives': '', 'alternative_singular': '',
             'alternative_stem': '', 'alternative_perfective': '',
             'plural_irregular': 'impago'})
        self.assertEqual(data.coll, ['uruhago', 'impago'])

    def test_set_questionsl(self):
        """Test questions for all alternatives"""
        data = dbc.Noun(
            {'dbid': '14', 'lemma': 'umwaka', 'prefix': 'umw',
             'stem': 'aka', 'perfective': '',
             'prefix_plural': 'imy', 'pos': 'NOUN',
             'alternatives': '', 'alternative_singular': '',
             'alternative_stem': '', 'alternative_perfective': '',
             'plural_irregular': ''})
        self.assertEqual(data.questions,
                         [r"^([na]ta|[mk]u|s?i)?mwaka$",
                          r"^([bkmrt]?w|[rv]?y|[nsckzbh])?umwaka$",
                          r"^([na]ta|[mk]u|s?i)?myaka$",
                          r"^([bkmrt]?w|[rv]?y|[nsckzbh])?imyaka$"])


###############################################################
#       TEST   N O U N   L I S T S                            #
###############################################################

class TestNounLists(TestCase):
    """Test cases for noun-lists"""

    data = [
        dbc.Noun(
            {'dbid': '8336', 'lemma': 'ubwinshi', 'prefix': 'ubw',
             'stem': 'inshi', 'perfective': '',
             'prefix_plural': '', 'pos': 'NOUN',
             'alternatives': '', 'alternative_singular': '',
             'alternative_stem': '', 'alternative_perfective': '',
             'plural_irregular': ''}),
        dbc.Noun(
            {'dbid': '6273', 'lemma': 'umupadiri', 'prefix': 'umu',
             'stem': 'padiri', 'perfective': '',
             'prefix_plural': 'aba', 'pos': 'NOUN',
             'alternatives': 'umupatiri;umupadri; umupatri;patiri;padiri',
             'alternative_singular': 'umu',
             'alternative_stem': '', 'alternative_perfective': '',
             'plural_irregular': ''}),
        dbc.Noun(
            {'dbid': '14', 'lemma': 'umwaka', 'prefix': 'umw',
             'stem': 'aka', 'perfective': '',
             'prefix_plural': 'imy', 'pos': 'NOUN',
             'alternatives': '', 'alternative_singular': '',
             'alternative_stem': '', 'alternative_perfective': '',
             'plural_irregular': ''}),
        dbc.Noun(
            {'dbid': '5939', 'lemma': 'izina', 'prefix': 'i',
             'stem': 'zina', 'perfective': '',
             'prefix_plural': 'ama', 'pos': 'NOUN',
             'alternatives': '', 'alternative_singular': '',
             'alternative_stem': '', 'alternative_perfective': '',
             'plural_irregular': ''}),
        dbc.Noun(
            {'dbid': '1074', 'lemma': 'amagara', 'prefix': 'ama',
             'stem': 'gara', 'perfective': '',
             'prefix_plural': '', 'pos': 'NOUN',
             'alternatives': '', 'alternative_singular': '',
             'alternative_stem': '', 'alternative_perfective': '',
             'plural_irregular': ''}),
        dbc.Noun(
            {'dbid': '3314', 'lemma': 'ikintu', 'prefix': 'iki',
             'stem': 'ntu', 'perfective': '',
             'prefix_plural': 'ibi', 'pos': 'NOUN',
             'alternatives': '', 'alternative_singular': '',
             'alternative_stem': '', 'alternative_perfective': '',
             'plural_irregular': ''}),
        dbc.Noun(
            {'dbid': '6664', 'lemma': 'icaha', 'prefix': 'ic',
             'stem': 'aha', 'perfective': '',
             'prefix_plural': 'ivy', 'pos': 'NOUN',
             'alternatives': '', 'alternative_singular': '',
             'alternative_stem': '', 'alternative_perfective': '',
             'plural_irregular': ''}),
        dbc.Noun(
            {'dbid': '2905', 'lemma': 'urukundo', 'prefix': 'uru',
             'stem': 'kundo', 'perfective': '',
             'prefix_plural': '', 'pos': 'NOUN',
             'alternatives': '', 'alternative_singular': '',
             'alternative_stem': '', 'alternative_perfective': '',
             'plural_irregular': ''}),
        dbc.Noun(
            {'dbid': '7193', 'lemma': 'akaburungu', 'prefix': 'aka',
             'stem': 'burungu', 'perfective': '',
             'prefix_plural': 'utu', 'pos': 'NOUN',
             'alternatives': '', 'alternative_singular': '',
             'alternative_stem': '', 'alternative_perfective': '',
             'plural_irregular': ''}),
        dbc.Noun(
            {'dbid': '6674', 'lemma': 'uruhago', 'prefix': 'uru',
             'stem': 'hago', 'perfective': '',
             'prefix_plural': 'im', 'pos': 'NOUN',
             'alternatives': '', 'alternative_singular': '',
             'alternative_stem': '', 'alternative_perfective': '',
             'plural_irregular': 'impago'}),
        dbc.Noun(
            {'dbid': '210', 'lemma': 'ukubaho', 'prefix': 'uku',
             'stem': 'baho', 'perfective': '',
             'prefix_plural': '', 'pos': 'NOUN',
             'alternatives': '', 'alternative_singular': '',
             'alternative_stem': '', 'alternative_perfective': '',
             'plural_irregular': ''}),
    ]

    def test_partition(self):
        """Test part of nouns collecting before or after verbs"""
        part1, part2 = dbc.noun_partition(TestNounLists.data)
        self.assertEqual(len(part1), 9)
        self.assertEqual(len(part2), 2)
        for noun in part2:
            self.assertIn(noun.lemma, ["ubwinshi", "ukubaho"])

    def test_collect_nouns(self):
        """Test collecting all variants of nouns"""
        freq_simple = {
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
        collection, not_collected = dbc.collect_nouns(
            TestNounLists.data, freq_simple)
        # collected
        types_num = 0
        for i in collection:
            types_num += i[4]
        self.assertEqual(len(not_collected), 7)
        self.assertEqual(types_num, 62)
        # not collected
        for i in ['nticahama', 'guhamagara', 'ikintuma', 'nkikintu',
                  'atanikintu', 'ikikintu']:
            self.assertIn(i, not_collected)


###############################################################
#       TEST   A D J E C T I V E S                            #
###############################################################
class TestAdjectives(TestCase):
    """Test cases for Adjective
    alternatives, all classes, double-stem """

    def test_init(self):
        """Test direct initializations"""
        data = dbc.Adjectiv(
            {'dbid': '3943', 'lemma': '-re-re', 'prefix': '-',
             'stem': 're-re', 'perfective': '',
             'prefix_plural': '', 'pos': 'ADJ',
             'alternatives': '', 'alternative_singular': '',
             'alternative_stem': '', 'alternative_perfective': '',
             'plural_irregular': ''})
        self.assertEqual(data.lemma, "-re-re")
        self.assertEqual(data.dbid, "3943")
        self.assertEqual(data.pos, "ADJ")
        self.assertEqual(data.stem, "re-re")

    def test_set_questions_i(self):
        """Test questions i-adjective"""
        data = dbc.Adjectiv(
            {'dbid': '2190', 'lemma': '-inshi', 'prefix': '-',
             'stem': 'inshi', 'perfective': '',
             'prefix_plural': '', 'pos': 'ADJ',
             'alternatives': '', 'alternative_singular': '',
             'alternative_stem': '', 'alternative_perfective': '',
             'plural_irregular': ''})
        self.assertEqual(
            data.questions,
            ['^((a?[bkmh]e)|(u?[bkmrt]?w[i]+)|(i?[mnrv]?yi|n?zi|[bc]i))(nshi)$'])

    def test_set_questions_in_two_alternatives(self):
        """Test questions for adjective with alternative"""
        data = dbc.Adjectiv(
            {'dbid': '2937', 'lemma': '-kuru', 'prefix': '-',
             'stem': 'kuru', 'perfective': '',
             'prefix_plural': '', 'pos': 'ADJ',
             'alternatives': '-kuru-kuru', 'alternative_singular': '',
             'alternative_stem': '', 'alternative_perfective': '',
             'plural_irregular': ''})
        self.assertEqual(len(data.questions), 2)

    def test_set_questions_in_three_alternatives(self):
        """Test questions for o-adjective in 3 alternatives"""
        data = dbc.Adjectiv(
            {'dbid': '3141', 'lemma': '-ompi', 'prefix': '-',
             'stem': 'ompi', 'perfective': 'ompi',
             'prefix_plural': '', 'pos': 'ADJ',
             'alternatives': 'mwempi; twempi', 'alternative_singular': '',
             'alternative_stem': '', 'alternative_perfective': '',
             'plural_irregular': ''})
        self.assertEqual(len(data.questions), 3)

    def test_collect_adjs(self):
        """Test collecting adjectives for all classes"""
        data = [dbc.Adjectiv(
            {'dbid': '3943', 'lemma': '-re-re', 'prefix': '-',
             'stem': 're-re', 'perfective': '',
             'prefix_plural': '', 'pos': 'ADJ',
             'alternatives': '', 'alternative_singular': '',
             'alternative_stem': '', 'alternative_perfective': '',
             'plural_irregular': ''}),
                dbc.Adjectiv(
            {'dbid': '2190', 'lemma': '-inshi', 'prefix': '-',
             'stem': 'inshi', 'perfective': '',
             'prefix_plural': '', 'pos': 'ADJ',
             'alternatives': '', 'alternative_singular': '',
             'alternative_stem': '', 'alternative_perfective': '',
             'plural_irregular': ''}),
                dbc.Adjectiv(
            {'dbid': '2937', 'lemma': '-kuru', 'prefix': '-',
             'stem': 'kuru', 'perfective': '',
             'prefix_plural': '', 'pos': 'ADJ',
             'alternatives': '-kuru-kuru', 'alternative_singular': '',
             'alternative_stem': '', 'alternative_perfective': '',
             'plural_irregular': ''}),
                dbc.Adjectiv(
            {'dbid': '3141', 'lemma': '-ompi', 'prefix': '-',
             'stem': 'ompi', 'perfective': 'ompi',
             'prefix_plural': '', 'pos': 'ADJ',
             'alternatives': 'mwempi; twempi', 'alternative_singular': '',
             'alternative_stem': '', 'alternative_perfective': '',
             'plural_irregular': ''}),
                dbc.Adjectiv(
            {'dbid': '3274', 'lemma': '-nini', 'prefix': '-',
             'stem': 'nini', 'perfective': 'nini',
             'prefix_plural': '', 'pos': 'ADJ',
             'alternatives': '', 'alternative_singular': '',
             'alternative_stem': '', 'alternative_perfective': '',
             'plural_irregular': ''})
        ]
        freq_simple = {
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
        collection, not_collected = dbc.collect_adjs(data, freq_simple)
        # collected
        types_num = 0
        for i in collection:
            types_num += i[4]
        self.assertEqual(len(not_collected), 17)
        self.assertEqual(types_num, 76)
        # not collected
        for i in ['barekure', 'arekure', 'barekure', 'biregure', 'birekure',
                  'buregure', 'burekure', 'burezire', 'irekure', 'kirerire',
                  'murekure', 'turekure', 'turerure', 'uburegare', 'umurekure',
                  'urekure', 'yiregure']:
            self.assertIn(i, not_collected)


###############################################################
#       TEST   P R O N O U N S                                #
###############################################################
class TestPronouns(TestCase):
    """Test cases for Pronouns
    from db and built, alternatives, all classes"""

    def test_init(self):
        """Test direct initializations"""
        # single instance
        data = kv.Lemma(
            {'dbid': '8274', 'lemma': 'iki', 'prefix': '',
             'stem': 'iki', 'perfective': '',
             'prefix_plural': '', 'pos': 'PRON',
             'alternatives': '', 'alternative_singular': '',
             'alternative_stem': '', 'alternative_perfective': '',
             'plural_irregular': ''})
        self.assertEqual(data.lemma, "iki")
        self.assertEqual(data.dbid, "8274")
        self.assertEqual(data.pos, "PRON")
        self.assertEqual(data.questions, ["iki",])

    def test_build_pronouns(self):
        """Test pronouns composed by the program"""
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
        data = [kv.Lemma(
            {'dbid': '8274', 'lemma': 'iki', 'prefix': '',
             'stem': 'iki', 'perfective': '',
             'prefix_plural': '', 'pos': 'PRON',
             'alternatives': '', 'alternative_singular': '',
             'alternative_stem': '', 'alternative_perfective': '',
             'plural_irregular': ''}),
                kv.Lemma(
            {'dbid': '8098', 'lemma': '-abo', 'prefix': '-',
             'stem': 'abo', 'perfective': '',
             'prefix_plural': '', 'pos': 'PRON',
             'alternatives': '', 'alternative_singular': '',
             'alternative_stem': '', 'alternative_perfective': '',
             'plural_irregular': ''}),
                kv.Lemma(
            {'dbid': '1458', 'lemma': 'hano', 'prefix': 'ha',
             'stem': 'no', 'perfective': '',
             'prefix_plural': '', 'pos': 'PRON',
             'alternatives': '', 'alternative_singular': '',
             'alternative_stem': '', 'alternative_perfective': '',
             'plural_irregular': ''}),
                kv.Lemma(
            {'dbid': '5447', 'lemma': 'twebwe', 'prefix': '',
             'stem': 'twebwe', 'perfective': '',
             'prefix_plural': '', 'pos': 'PRON',
             'alternatives': 'twebge;tweho', 'alternative_singular': '',
             'alternative_stem': '', 'alternative_perfective': '',
             'plural_irregular': ''}),
                kv.Lemma(
            {'dbid': '7863', 'lemma': 'igihe?', 'prefix': 'igi',
             'stem': 'he?', 'perfective': '',
             'prefix_plural': '', 'pos': 'PRON',
             'alternatives': '', 'alternative_singular': '',
             'alternative_stem': '', 'alternative_perfective': '',
             'plural_irregular': ''}),
        ]
        freq_simple = {
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
        # test-db
        self.assertEqual(len(data), 5)
        collection, not_collected = dbc.collect_pronouns(data, freq_simple)
        types_num = 0
        for i in collection:
            types_num += i[4]
        # collected types
        self.assertEqual(types_num, 42)
        # collected lemmata
        self.assertEqual(len(collection), 5)
        # not collected
        self.assertEqual(len(not_collected), 13)
        for no_pronoun in ['igi', 'ahabo', 'akabo', 'icabo', 'iryabo',
                           'ivyabo', 'iyabo', 'izabo', 'mwabo', 'nyabo',
                           'ubwabo', 'urwabo', 'utwabo']:
            self.assertIn(no_pronoun, not_collected)
        # right lemma for merged types
        self.assertEqual(collection[0][0], '-no')


###############################################################
#       TEST   A D V E R B S   etc.                           #
###############################################################
class TestAdverbsEtc(TestCase):
    """Test cases for unchanging words: Adverbs, Prepositions,
    conjunctions, interjections
    lemmata, alternatives"""

    def test_init(self):
        """Test direct initializations"""
        # test single instance
        data = kv.Lemma(
            {'dbid': '7121', 'lemma': 'ubu nyene', 'prefix': '',
             'stem': 'ubu nyene', 'perfective': '',
             'prefix_plural': '', 'pos': 'ADV',
             'alternatives': 'ubunyene', 'alternative_singular': '',
             'alternative_stem': '', 'alternative_perfective': '',
             'plural_irregular': ''})
        self.assertEqual(data.lemma, "ubu nyene")
        self.assertEqual(data.dbid, "7121")
        self.assertEqual(data.pos, "ADV")
        self.assertEqual(data.questions, ["ubu nyene", "ubunyene"])

    def test_collect_adverbs_plus(self):
        """Test collection unchanging words"""
        data = [kv.Lemma(
            {'dbid': '7121', 'lemma': 'ubu nyene', 'prefix': '',
             'stem': 'ubu nyene', 'perfective': '',
             'prefix_plural': '', 'pos': 'ADV',
             'alternatives': 'ubunyene', 'alternative_singular': '',
             'alternative_stem': '', 'alternative_perfective': '',
             'plural_irregular': ''}),
                kv.Lemma(
            {'dbid': '5519', 'lemma': 'inyuma', 'prefix': 'i',
             'stem': 'nyuma', 'perfective': '',
             'prefix_plural': '', 'pos': 'CONJ',
             'alternatives': '', 'alternative_singular': '',
             'alternative_stem': '', 'alternative_perfective': '',
             'plural_irregular': ''}),
                kv.Lemma(
            {'dbid': '5525', 'lemma': 'umengo', 'prefix': '',
             'stem': 'umengo', 'perfective': '',
             'prefix_plural': '', 'pos': 'INTJ',
             'alternatives': '', 'alternative_singular': '',
             'alternative_stem': '', 'alternative_perfective': '',
             'plural_irregular': ''}),
                kv.Lemma(
            {'dbid': '6121', 'lemma': 'i ruhande', 'prefix': 'i ru',
             'stem': 'hande', 'perfective': '',
             'prefix_plural': '', 'pos': 'PREP',
             'alternatives': 'iruhande', 'alternative_singular': '',
             'alternative_stem': '', 'alternative_perfective': '',
             'plural_irregular': ''}),
                kv.Lemma(
            {'dbid': '7505', 'lemma': 'mirongwitatu', 'prefix': '',
             'stem': 'mirongwitatu', 'perfective': '',
             'prefix_plural': '', 'pos': 'ADV',
             'alternatives': 'mirongo itatu;mirongitatu',
             'alternative_singular': '',
             'alternative_stem': '', 'alternative_perfective': '',
             'plural_irregular': ''}),
            ]
        freq_simple = {
            'mirongwitatu': 19, 'mirongoitatu': 1, 'mirongitatu': 3,
            'samunani': 13, 'iruhande': 56, 'ubu': 2927, 'nyene': 1544,
            'mirongo': 202,
            }
        self.assertEqual(len(data), 5)
        self.assertEqual(data[0].questions, ["ubu nyene", "ubunyene"])
        self.assertEqual(data[1].pos, "CONJ")
        self.assertEqual(data[2].pos, "INTJ")
        self.assertEqual(data[3].pos, "PREP")
        collection, not_collected = dbc.collect_adv_plus(data, freq_simple)
        types_num = 0
        for i in collection:
            types_num += i[4]
        # found types
        self.assertEqual(types_num, 3)
        # found lemmata
        self.assertEqual(len(collection), 2)
        # not collected
        self.assertEqual(len(not_collected), 5)
        for i in ['samunani', 'mirongoitatu', 'ubu', 'nyene', 'mirongo']:
            self.assertIn(i, not_collected)


###############################################################
#       TEST   E X C L A M A T I O N S                        #
###############################################################
class TestExclamations(TestCase):
    """Test cases for Exclamations
    from db and built"""

    def test_init(self):
        """Test direct initializations"""
        data = kv.Lemma(
            {'dbid': '818', 'lemma': 'ego', 'prefix': '',
             'stem': 'ego', 'perfective': '',
             'prefix_plural': '', 'pos': 'INTJ',
             'alternatives': '', 'alternative_singular': '',
             'alternative_stem': '', 'alternative_perfective': '',
             'plural_irregular': ''})
        self.assertEqual(data.lemma, "ego")
        self.assertEqual(data.dbid, "818")
        self.assertEqual(data.pos, "INTJ")
        self.assertEqual(data.questions, ["ego",])

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
        data = [kv.Lemma(
            {'dbid': '818', 'lemma': 'ego', 'prefix': '',
             'stem': 'ego', 'perfective': '',
             'prefix_plural': '', 'pos': 'INTJ',
             'alternatives': '', 'alternative_singular': '',
             'alternative_stem': '', 'alternative_perfective': '',
             'plural_irregular': ''}),
                kv.Lemma(
            {'dbid': '3556', 'lemma': 'oya', 'prefix': '',
             'stem': 'oya', 'perfective': '',
             'prefix_plural': '', 'pos': 'INTJ',
             'alternatives': '', 'alternative_singular': '',
             'alternative_stem': '', 'alternative_perfective': '',
             'plural_irregular': ''}),
                kv.Lemma(
            {'dbid': '7307', 'lemma': 'karibu', 'prefix': '',
             'stem': 'karibu', 'perfective': '',
             'prefix_plural': '', 'pos': 'INTJ',
             'alternatives': '', 'alternative_singular': '',
             'alternative_stem': '', 'alternative_perfective': '',
             'plural_irregular': ''}),
                kv.Lemma(
            {'dbid': '7196', 'lemma': 'egome', 'prefix': '',
             'stem': 'egome', 'perfective': '',
             'prefix_plural': '', 'pos': 'INTJ',
             'alternatives': 'ego me', 'alternative_singular': '',
             'alternative_stem': '', 'alternative_perfective': '',
             'plural_irregular': ''}),
            ]
        freq_simple = {'karibu': 5, 'egome': 1, 'ego': 38, 'eeeego': 11,
                       'eeeeh': 191, 'eeego': 15, 'eeegoo': 2, 'oyaa': 117,
                       'oyaaa': 99, 'oya': 2785, 'oyayeeeee': 1, 'oyaye': 128,
                       'oyaha': 27, 'oyaaaah': 2, 'oyaah': 2
                       }
        self.assertEqual(len(data), 4)
        collection, not_collected = dbc.collect_exclamations(data, freq_simple)
        types_num = 0
        for i in collection:
            types_num += i[4]
        self.assertEqual(types_num + len(not_collected), len(freq_simple))
        # found types
        self.assertEqual(types_num, 10)
        # found lemmata
        self.assertEqual(len(collection), 4)
        # not colllected
        self.assertEqual(len(not_collected), 5)


############################################################################
#  TEST   F O R E I G N words and N A M E S (Persons, Organisations, ...)  #
############################################################################
class TestForeign(TestCase):
    """Test case for collecting Foreign words and personal Names """

    @classmethod
    def setUpClass(cls):
        """ Connect and load data needed by tests """
        global NE_DATA
        global FREQ_SIM
        NE_DATA = [
            dbc.Foreign({'lemma': 'blé', 'pos': 'f', 'alternatives': ''}),
            dbc.Foreign({'lemma': 'Gärten', 'pos': 'F', 'alternatives': ''}),
            dbc.Foreign({'lemma': ' Noël', 'pos': 'F', 'alternatives': ''}),
            dbc.NamedEntities({'lemma': 'euro', 'pos': 'PROPN_CUR',
                               'alternatives': 'EUR; euros'}),
            dbc.NamedEntities({'lemma': 'barça', 'pos': 'PROPN_ORG',
                               'alternatives': 'barca'}),
            dbc.NamedEntities({'lemma': 'dmn-tre', 'pos': 'PROPN_SCI',
                               'alternatives': 'dmn;tre'}),
            dbc.NamedEntities({'lemma': 'Nsengiyumva', 'pos': 'PROPN_NAM',
                               'alternatives': ''}),
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
        data = dbc.Foreign({'lemma': 'ble', 'pos': 'f', 'alternatives': ''})
        self.assertEqual(data.lemma, "ble")
        self.assertEqual(data.dbid, "")
        self.assertEqual(data.pos, "F")
        self.assertEqual(data.questions, ["ble",])
        # test test-database
        self.assertEqual(len(NE_DATA), 7)
        self.assertEqual(NE_DATA[1].lemma, "garten")
        self.assertEqual(NE_DATA[2].lemma, "noel")

    def test_initialization_names(self):
        """Test direct initialization names"""
        # single instance
        euro = dbc.NamedEntities({'lemma': 'euro', 'pos': 'PROPN_CUR',
                                  'alternatives': 'EUR; euros'})
        self.assertEqual(euro.lemma, "euro")
        self.assertEqual(len(euro.alternatives), 3)
        for i in euro.alternatives:
            self.assertIn(i, ['euro', 'eur', 'euros'])
        self.assertEqual(euro.pos, "PROPN_CUR")

        # test test-database
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
        data =[
            dbc.Foreign({'lemma': 'blé', 'pos': 'f', 'alternatives': ''}),
            dbc.Foreign({'lemma': 'Gärten', 'pos': 'F', 'alternatives': ''}),
            dbc.Foreign({'lemma': ' Noël', 'pos': 'F', 'alternatives': ''})]
        for i in [dbc.NamedEntities({'lemma': 'euro', 'pos': 'PROPN_CUR',
                                     'alternatives': 'EUR; euros'}),
                  dbc.NamedEntities({'lemma': 'barça', 'pos': 'PROPN_ORG',
                                     'alternatives': 'barca'}),
                  dbc.NamedEntities({'lemma': 'dmn-tre', 'pos': 'PROPN_SCI',
                                     'alternatives': 'dmn;tre'}),
                  dbc.NamedEntities({'lemma': 'Nsengiyumva', 'pos': 'PROPN_NAM',
                                     'alternatives': ''}),
                  ]:
            i.questions = i.alternatives
            data.append(i)
        freq_simple = {
            'ble': 2, 'garten': 7, 'noel': 33, 'euro': 12, 'euros': 12,
            'nyumva': 14, 'eur': 6, 'barca': 8, 'dmn': 6, 'tre': 6,
            'nsengiyumva': 15
            }
        collection, not_collected = dbc.collect_names(data, freq_simple)
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
        self.assertEqual(len(not_collected), 1)


############################################################################
#   TEST   N A M E D  E N T I T I E S  (Locations, Languages, Inhabitants) #
############################################################################
class TestNE(TestCase):
    """Test cases for related location-inhabitants-language Named Entities"""

    def test_init_ne(self):
        """Test direct initialization locations, persons, languages"""

        # test single instance
        data = dbc.NamedEntities({'lemma': 'ubudagi',
                                  'pos': 'PROPN_loc',
                                  'alternatives': 'dagi;german;germany'})
        self.assertEqual(data.lemma, 'ubudagi')
        self.assertEqual(data.pos, "PROPN_LOC")
        # because it was a set we don't know the order of the alternatives
        self.assertEqual(len(data.alternatives), 4)
        for i in ['ubudagi', 'german', 'germany', 'dagi']:
            self.assertIn(i, data.alternatives)

        # test database
        data = [
            dbc.NamedEntities({'lemma': 'misiri',
                               'pos': 'PROPN_loc',
                               'alternatives': 'egypt;egiputa;misri;mirisi'}),
            dbc.NamedEntities({'lemma': 'ubudagi',
                               'pos': 'PROPN_loc',
                               'alternatives': 'dagi;german;germany'}),
            dbc.NamedEntities({'lemma': 'igihebreyi',
                               'pos': 'PROPN_LNG',
                               'alternatives': 'hebrew;hebreyi'}),
            dbc.NamedEntities({'lemma': 'ikinyarwanda',
                               'pos': 'PROPN_LNG',
                               'alternatives': 'gwanda'}),
            dbc.NamedEntities({'lemma': 'ikidagi	',
                               'pos': 'PROPN_LNG',
                               'alternatives': 'dagi;dage'}),
            dbc.NamedEntities({'lemma': 'umudagi',
                               'pos': 'PROPN_PER',
                               'alternatives': 'german;dagi'}),
            dbc.NamedEntities({'lemma': 'umworomo',
                               'pos': 'PROPN_PER',
                               'alternatives': 'oromo'}),
                ]
        self.assertEqual(len(data), 7)
        self.assertEqual(len(data[0].alternatives), 5)
        self.assertEqual(data[1].lemma, 'ubudagi')
        self.assertEqual(len(data[1].alternatives), 4)
        for i in ['ubudagi', 'german', 'germany', 'dagi']:
            self.assertIn(i, data[1].alternatives)
        self.assertEqual(data[1].pos, "PROPN_LOC")
        self.assertEqual(
           data[3].row, {'lemma': 'ikinyarwanda',
                         'pos': 'PROPN_LNG', 'alternatives': 'gwanda'})
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
        loc = [dbc.NamedEntities({'lemma': 'misiri',
                                  'pos': 'PROPN_loc',
                               'alternatives': 'egypt;egiputa;misri;mirisi'}),
               dbc.NamedEntities({'lemma': 'ubudagi',
                                  'pos': 'PROPN_loc',
                                  'alternatives': 'dagi;german;germany'})]
        lng = [dbc.NamedEntities({'lemma': 'igihebreyi',
                                  'pos': 'PROPN_LNG',
                                  'alternatives': 'hebrew;hebreyi'}),
               dbc.NamedEntities({'lemma': 'ikinyarwanda',
                                  'pos': 'PROPN_LNG',
                                  'alternatives': 'gwanda'}),
               dbc.NamedEntities({'lemma': 'ikidagi	',
                                  'pos': 'PROPN_LNG',
                                  'alternatives': 'dagi;dage'})]
        per = [dbc.NamedEntities({'lemma': 'umudagi',
                                  'pos': 'PROPN_PER',
                                  'alternatives': 'german;dagi'}),
               dbc.NamedEntities({'lemma': 'umworomo',
                                  'pos': 'PROPN_PER',
                                  'alternatives': 'oromo'})]
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
        lng = [dbc.NamedEntities({'lemma': 'igihebreyi',
                                  'pos': 'PROPN_LNG',
                                  'alternatives': 'hebrew;hebreyi'}),
               dbc.NamedEntities({'lemma': 'ikinyarwanda',
                                  'pos': 'PROPN_LNG',
                                  'alternatives': 'gwanda'})]
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
        per = [dbc.NamedEntities({'lemma': 'umudagi',
                                  'pos': 'PROPN_PER',
                                  'alternatives': 'german;dagi'}),
               dbc.NamedEntities({'lemma': 'umworomo',
                                  'pos': 'PROPN_PER',
                                  'alternatives': 'oromo'}),
               dbc.NamedEntities({'lemma': 'umuntu',
                                  'pos': 'PROPN_PER', 'alternatives': ''})]
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

    def test_perla_from_ub_iki_language(self):
        """Test creation of Name (.lemma) of new iki-language and person
        constructed from locations with ubu"""
        # prepare iki
        local = dbc.NamedEntities({'lemma': 'ubudagi',
                                   'pos': 'PROPN_loc',
                                   'alternatives': 'dagi;german;germany'})
        local.alternatives = [i for i in local.alternatives if i[:3] != "ubu"]
        self.assertEqual(len(local.alternatives), 3)
        # test iki
        pername, langname = local.perla_from_ub()
        self.assertEqual(pername, "umudagi")
        self.assertEqual(langname, "ikidagi")

    def test_perla_from_ub_igi_language(self):
        """Test creation of Name (.lemma) of new igi-language and person
        constructed from locations with ubu"""
        # prepare igi
        local = dbc.NamedEntities(
            {'lemma': 'ubuhindi', 'pos': 'PROPN_LOC',
             'alternatives': 'hinde;hindu;india;endu;indu;hindi'})
        local.alternatives = [i for i in local.alternatives if i[:3] != "ubu"]
        # test igi
        pername, langname = local.perla_from_ub()
        self.assertEqual(pername, "umuhindi")
        self.assertEqual(langname, "igihindi")

    def test_create_new_lang(self):
        """Test create new language-instance of location"""
        local = dbc.NamedEntities({'lemma': 'ubudagi',
                                   'pos': 'PROPN_loc',
                                   'alternatives': 'dagi;german;germany'})
        local.alternatives = [i for i in local.alternatives if i[:3] != "ubu"]
        lang = local.create_new_lang("ikidagi")
        self.assertEqual(lang.lemma, "ikidagi")
        self.assertEqual(len(lang.questions), 6)
        for i in ['ikigerman', 'ikidagi', 'ikigermany',
                  'kigerman', 'kidagi', 'kigermany']:
            self.assertIn(i, lang.questions)

    def test_create_new_person(self):
        """Test create new person-instance of location"""
        local = dbc.NamedEntities(
            {'lemma': 'misiri', 'pos': 'PROPN_loc',
             'alternatives': 'egypt;egiputa;misri;mirisi'})
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
        """Test set_location_and_create_person_language_out_of_location.
        consonant-stem
        questions for location; instances for related person and language"""
        # test consonant
        local = dbc.NamedEntities(
            {'lemma': 'misiri', 'pos': 'PROPN_loc',
             'alternatives': 'egypt;egiputa;misri;mirisi'})
        lang, pers = local.set_location_and_create_person_language_out_of_it()
        self.assertEqual(len(local.questions), 10)
        self.assertEqual(len(lang.questions), 10)
        self.assertEqual(len(pers.questions), 20)

    def test_set_location_create_person_language_out_of_location_vowel1(self):
        """Test set_location_and_create_person_language_out_of_location.
        vowel-stem, without augmention
        questions for location; instances for related person and language"""
        # test vowel
        local = dbc.NamedEntities({'lemma': 'ostrariya', 'pos': 'PROPN_LOC',
                                   'alternatives': 'australia;australian'})
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

    def test_set_location_create_person_language_out_of_location_vowel2(self):
        """Test set_location_and_create_person_language_out_of_location.
        vowel-stem, with augmention
        questions for location; instances for related person and language"""
        # test ubu + vowel
        local = dbc.NamedEntities(
            {'lemma': 'ubutariyano', 'pos': 'PROPN_LOC',
             'alternatives': 'itariyano; taliyano; tariyano'})
        local.alternatives = [i for i in local.alternatives if i[:3] != "ubu"]
        lang, pers = local.set_location_and_create_person_language_out_of_it()
        for i in local.questions:
            print(i)
        self.assertEqual(len(local.questions), 9)
        self.assertEqual(len(lang.questions), 6)

    def test_complete_location_language_person(self):
        """Test add constructed languages and persons to named-entity-list"""
        # prepare
        ne_dict = {
            'loc': [dbc.NamedEntities(
                {'lemma': 'misiri', 'pos': 'PROPN_loc',
                 'alternatives': 'egypt;egiputa;misri;mirisi'}),
                    dbc.NamedEntities(
                {'lemma': 'ubudagi', 'pos': 'PROPN_loc',
                 'alternatives': 'dagi;german;germany'})],
            'lng': [dbc.NamedEntities(
                {'lemma': 'igihebreyi', 'pos': 'PROPN_LNG',
                 'alternatives': 'hebrew;hebreyi'}),
                   dbc.NamedEntities(
                {'lemma': 'ikinyarwanda',  'pos': 'PROPN_LNG',
                 'alternatives': 'gwanda'}),
                   dbc.NamedEntities(
                {'lemma': 'ikidagi	', 'pos': 'PROPN_LNG',
                 'alternatives': 'dagi;dage'})],
            'per': [dbc.NamedEntities(
                {'lemma': 'umudagi', 'pos': 'PROPN_PER',
                 'alternatives': 'german;dagi'}),
                   dbc.NamedEntities(
                {'lemma': 'umworomo', 'pos': 'PROPN_PER',
                 'alternatives': 'oromo'})],
            'names': [],
            'foreign': []
                   }

        loc_before = len(ne_dict.get('loc'))
        per_before = len(ne_dict.get('per'))
        lng_before = len(ne_dict.get('lng'))
        # test
        ne_list = dbc.complete_location_language_person(ne_dict)
        locs = 0
        lngs = 0
        pers = 0
        for i in ne_list:
            # print("\nne:", i)
            if i.pos == "PROPN_LOC":
                locs += 1
            elif i.pos == "PROPN_PER":
                pers += 1
            elif i.pos == "PROPN_LNG":
                lngs += 1
        self.assertEqual(len(ne_list), 9)
        self.assertEqual(locs, loc_before)
        self.assertEqual(pers, per_before+1)
        self.assertEqual(lngs, lng_before+1)


###############################################################
#       TEST   L O A D   D A T A                              #
###############################################################
class TestLoading(TestCase):
    """Test loading Named Entities respective rundi dictionary"""

    def test_read_named_entities(self):
        """Test mapping db"""
        database = dbc.read_named_entities(
            sd.ResourceNames.root+"/resources/ne_test.csv")
        self.assertEqual(len(database), 45)

    def test_map_ne(self):
        """Test load Named Entities from csv"""
        database = dbc.read_named_entities(
            sd.ResourceNames.root+"/resources/ne_test.csv")
        ne_data = dbc.map_ne(database)
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

    def test_read_db_kirundi(self):
        """Test mapping db"""
        database = dbc.read_db_kirundi(
            sd.ResourceNames.root + "/tests/lemmata_test.csv")
        self.assertEqual(len(database), 56)

    def test_map_db_kirundi(self):
        """Test load rundi dictionary from csv"""

        database = dbc.read_db_kirundi(
            sd.ResourceNames.root + "/tests/lemmata_test.csv")
        db_data = dbc.map_db_kirundi(database)
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
    #              sd.ResourceNames.root + "/tests/lemmata_test.csv")
