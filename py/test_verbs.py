#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 13:12:22 2023

@author: doreen
"""

from unittest import TestCase
import kir_prepare_verbs as kv

# nosetests --with-spec --spec-color --with-coverage --cover-erase
# coverage report -m


###############################################################
#       TEST   V E R B S                                      #
###############################################################
class TestPrepareVerbs(TestCase):
    """Test cases for Verb preparation:
        build alternative spellings, perfective, set questions
    """

    def test_simple_initiation(self):
        """Test direct initializations"""
        data = kv.Verb(['180', 'kuba', 'kubá',
                        'ku', 'ba', 'baye', 'baye',
                        '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                        '', '', '', '', '', '0', '', '0', '', 'NULL'])
        self.assertEqual(data.lemma, "kuba")
        self.assertEqual(data.dbid, "180")
        self.assertEqual(data.pos, "VERB")
        self.assertEqual(data.stem, "ba")
        self.assertEqual(data.perfective, "baye")

    def test_check_perfective(self):
        """Test check unclear perfective"""
        data = kv.Verb(['9999', 'kurararara', '',
                        'ku', 'rararara', 'raye?', '?',
                        '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                        '', '', '', '', '', '0', '', '0', '', 'NULL'])
        self.assertEqual(data.perfective, None)
        self.assertEqual(
            data.unclear,
            [['kurararara', 'perfective unclear:', 'raye?']])

    def test_simple_initiation_with_alternative(self):
        data = kv.Verb(['1814', 'guhuhuta', '',
                        'gu', 'hūhūta', 'hūhūse', 'se',
                        '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                        'guhuhuta', '', 'huhuta', 'hūhūshe',
                        '', '0', '', '0', '', 'NULL'])
        self.assertEqual(data.lemma, "guhuhuta")
        self.assertEqual(data.dbid, "1814")
        self.assertEqual(data.alternatives, ['guhuhuta'])
        self.assertEqual(data.comb, None)

    def test_set_end_of_verbs_m(self):
        """Test built verb endings"""
        data = kv.Verb(['3120', 'kumira', 'kumira',
                        'ku', 'mira', 'mize', 'ze',
                        '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                        '', '', '', '', '', '0', '', '0', '', 'NULL'])
        data._set_end_of_ends()
        self.assertEqual(data.lemma, "kumira")
        self.assertEqual(data._end_a, 'mir(w?a)((([hyk]|mw)o)?$)')
        self.assertEqual(data._end_e, 'mire((([hyk]|mw)o)?$)')
        self.assertEqual(data._end_y, 'miz((w)?e)((([hyk]|mw)o)?$)')

    def test_set_end_of_verbs_perfective_with_u(self):
        data = kv.Verb(['5585', 'gupfa', '',
                        'gu', 'pfa', 'pfūye', 'pfūye',
                        '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                        '', '', '', '', '', '0', '', '0', '', 'NULL'])
        data._set_end_of_ends()
        self.assertEqual(data.lemma, "gupfa")
        self.assertEqual(data.perfective[-3], "u")
        self.assertEqual(
            data._end_y, 'pfu(ye|((ri)?we))((([hyk]|mw)o)?$)')

    def test_set_end_of_verbs_perfective_with_f(self):
        data = kv.Verb(['7962', 'gucapa', 'gucápa',
                        'gu', 'capa', 'cafye', 'fye',
                        '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                        '', '', '', '', '', '0', '', '0', '', 'sw'])
        data._set_end_of_ends()
        self.assertEqual(
            data._end_y, 'capuwe((([hyk]|mw)o)?$)')

    def test_set_end_of_verbs_perfective_with_l(self):
        data = kv.Verb(['9999', 'kulalalala', '',
                        'ku', 'rararara', 'calye', '',
                        '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                        '', '', '', '', '', '0', '', '0', '', 'NULL'])
        data._set_end_of_ends()
        self.assertIn(['perfective: unexpected letter before [y] ',
                       'kulalalala', 'calye'],
                      data.unclear)

    def test_set_end_of_verbs_exception_zi(self):
        data = kv.Verb(['24', '-zi', '',
                        '-', 'zi', '', '',
                        '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                        '', '', '', '', '', '0', '', '0', '', 'NULL'])
        data.stem = "zi"
        data._set_end_of_ends()
        self.assertEqual(data._end_y, '')
        self.assertEqual(data._end_a, 'zw?i((([hyk]|mw)o)?$)')

    def test_set_end_of_verbs_exception_fise(self):
        data = kv.Verb(['908', '-fise', '',
                        '-', 'fise', '', '',
                        '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                        '', '', '', '', '', '0', '', '0', '', 'NULL'])
        data.stem = "fise"
        data._set_end_of_ends()
        self.assertEqual(data._end_y, 'fise((([hyk]|mw)o)?$)')

    def test_prepare_verb_alternativ_with_long_perfective(self):
        """Test prepare_verb_alternativ"""
        row_alt = kv.prepare_verb_alternativ(
            ['1814', 'guhuhuta', '',
             'gu', 'hūhūta', 'hūhūse', 'se',
             '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
             'guhuhuta', '', 'huhuta', 'hūhūshe',
             '', '', '0', '', '0', '', 'NULL'])
        self.assertEqual(row_alt[0], '1814')
        self.assertEqual(row_alt[1], 'guhuhuta')
        self.assertEqual(row_alt[4], 'huhuta')
        self.assertEqual(row_alt[5], 'hūhūshe')
        self.assertEqual(row_alt[13], 'x')

    def test_prepare_verb_alternativ_with_short_perfective(self):
        row_alt = kv.prepare_verb_alternativ(
            ['4229', 'gusabwa', 'gusabwa',
             'gu', 'sabwa', 'sabwe', 'bwe',
             '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
             'gusabga', '', 'sabga', 'bge',
             '', '0', '', '0', '', 'NULL'])
        self.assertEqual(row_alt[0], '4229')
        self.assertEqual(row_alt[4], 'sabga')
        self.assertEqual(row_alt[5], 'sabge')
        self.assertEqual(row_alt[13], 'x')

    def test_set_questions_short_verb(self):
        """Test set regEx"""
        data = kv.Verb(['180', 'kuba', 'kubá',
                        'ku', 'ba', 'baye', 'baye',
                        '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                        '', '', '', '', '', '0', '', '0', '', 'NULL'])
        data.set_questions()
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

    def test_set_questions_kw_a(self):
        data = kv.Verb(['83', 'kwandika', 'kwaandika',
                        'kw', 'andika', 'anditse', 'tse',
                        '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                        '', '', '', '', '', '0', '', '0', '', 'NULL'])
        self.assertEqual(data.lemma, "kwandika")
        data.set_questions()
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

    def test_set_questions_kw_i(self):
        data = kv.Verb(['2236', 'kwiruka', 'kwiíruka',
                        'kw', 'iruka', 'irutse', 'tse',
                        '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                        '', '', '', '', '', '0', '', '0', '', 'NULL'])
        data.set_questions()
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

    def test_set_questions_stem_m(self):
        data = kv.Verb(['3120', 'kumira', 'kumira',
                        'ku', 'mira', 'mize', 'ze',
                        '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                        '', '', '', '', '', '0', '', '0', '', 'NULL'])
        data.set_questions()
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

    def test_set_questions_gu(self):
        data = kv.Verb(['2795', 'gukora', '',
                        'gu', 'kora', 'koze', 'ze',
                        '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                        '', '', '', '', '', '0', '', '0', '', 'NULL'])
        data.set_questions()
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

    def test_set_questions_stem_r(self):
        data = kv.Verb(['3984', 'kurima', 'kurima',
                        'ku', 'rima', 'rimye', 'mye',
                        '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                        '', '', '', '', '', '0', '', '0', '', 'NULL'])
        data.set_questions()
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

    def test_set_questions_stem_h(self):
        data = kv.Verb(['6364', 'guhagarara', 'guhágarara',
                        'gu', 'hagarara', 'hagaraze', 'ze',
                        '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                        '', '', '', '', '', '0', '', '0', '', 'NULL'])
        data.set_questions()
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

    def test_get(self):
        """Test get attributes"""
        data = kv.Verb(['1135', 'kugenda', '',
                        'ku', 'gēnda', 'giye', 'giye',
                        '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                        '', '', '', '', '', '0', '', '0', '', 'NULL'])
        self.assertEqual(data.get('lemma'), 'kugenda')
        self.assertEqual(data.get('dbid'), '1135')
        self.assertEqual(data.get('stem'), 'genda')
        self.assertEqual(data.get('perfective'), 'giye')
        self.assertEqual(data.get(
            'alternative'), 'Hm, does class Verb has this feature?')
        self.assertEqual(data.get('alternatives'), '')
        self.assertEqual(data.get('comb'), None)
        self.assertEqual(data.get('proverb'), False)
        self.assertEqual(data.get('unclear'), [])


class TestVerbLists(TestCase):
    """Test cases for Verb
    sort out passiv forms and proverbs,
    collect types for ku/gu/kw-verbs
        in time, mode, negation, ...
    """
# TODO   test subjects, objects

    def test_mark_proverb(self):
        """Test mark proverb
        is preparation for 'filter proverbs out'"""
        data = [kv.Verb(['7161', 'kugira amazinda', 'kugira amaziinda',
                         'ku', 'gira amazinda', 'gize', 'gize',
                         '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                         '', '', '', '', '', '0', '', '0', '', 'NULL']),
                kv.Verb(['1223', 'kugira', 'kugira',
                         'ku', 'gira', 'gize', 'gize ',
                         '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                         '', '', '', '', '', '0', '', '0', '', 'NULL'])
                ]
        for verb in data:
            verb.mark_proverb()
        self.assertEqual(data[0].lemma, "kugira amazinda")
        self.assertEqual(data[0].proverb, True)
        self.assertEqual(data[1].lemma, "kugira")
        self.assertEqual(data[1].proverb, False)

    def test_filter_proverbs_out(self):
        """Test filter proverbs out:
        take only verb from stem and only if there's no same solo form"""
        # prepare
        data = [kv.Verb(['6988', 'gukoma amashi', 'gukóma amashí',
                         'gu', 'koma amashi', 'komye', '',
                         '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                         '', '', '', '', '', '0', '', '0', '', 'NULL']),
                kv.Verb(['7161', 'kugira amazinda', 'kugira amaziinda',
                         'ku', 'gira amazinda', 'gize', 'gize',
                         '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                         '', '', '', '', '', '0', '', '0', '', 'NULL']),
                kv.Verb(['2795', 'gukora', '',
                         'gu', 'kora', 'koze', 'ze',
                         '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                         '', '', '', '', '', '0', '', '0', '', 'NULL']),
                kv.Verb(['1223', 'kugira', 'kugira',
                         'ku', 'gira', 'gize', 'gize ',
                         '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                         '', '', '', '', '', '0', '', '0', '', 'NULL']),
                kv.Verb(['1135', 'kugenda', '',
                         'ku', 'gēnda', 'giye', 'giye',
                         '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                         '', '', '', '', '', '0', '', '0', '', 'NULL'])
                ]
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
        data = [kv.Verb(['2796', 'gukora', 'gukoora',
                         'gu', 'kora', 'koye', 'ye',
                         '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                         '', '', '', '', '', '0', '', '0', '', 'NULL']),
                kv.Verb(['4229', 'gusabwa', 'gusabwa',
                         'gu', 'sabwa', 'sabwe', 'bwe',
                         '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                         'gusabga', '', 'sabga', 'bge',
                         '', '0', '', '0', '', 'NULL'])
                ]
        for verb in data:
            verb.mark_passiv()
        self.assertEqual(data[0].lemma, "gukora")
        self.assertEqual(data[0].passiv, False)
        self.assertEqual(data[1].lemma, "gusabwa")
        self.assertEqual(data[1].passiv, True)

    def test_filter_passiv_out(self):
        """Test filter passiv out:
        skip passiv-lemma if there's already same lemma without passiv"""
        data = [kv.Verb(['2236', 'kwiruka', 'kwiíruka',
                         'kw', 'iruka', 'irutse', 'tse',
                         '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                         '', '', '', '', '', '0', '', '0', '', 'NULL']),
                kv.Verb(['3120', 'kumira', 'kumira',
                         'ku', 'mira', 'mize', 'ze',
                         '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                         '', '', '', '', '', '0', '', '0', '', 'NULL']),
                kv.Verb(['4229', 'gusabwa', 'gusabwa',
                         'gu', 'sabwa', 'sabwe', 'bwe',
                         '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                         'gusabga', '', 'sabga', 'bge',
                         '', '0', '', '0', '', 'NULL']),
                kv.Verb(['4222', 'gusaba', 'gusaba',
                         'gu', 'saba', 'savye', 'vye',
                         '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                         '', '', '', '', '', '0', '', '0', '', 'NULL']),
                kv.Verb(['3124', 'kumirwa', 'kumirwa',
                         'ku', 'mirwa', 'mizwe', 'zwe',
                         '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                         '', '', '', '', '', '0', '', '0', '', 'NULL']),
                kv.Verb(['467', 'kuborerwa', 'kuborerwa',
                         'ku', 'borerwa', 'borewe', 'we',
                         '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                         '', '', '', '', '', '0', '', '0', '', 'NULL'])
                ]
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

    def test_collect_verbs(self):
        """Test collect verbs"""
        data = [kv.Verb(['180', 'kuba', 'kubá',
                         'ku', 'ba', 'baye', 'baye',
                         '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                         '', '', '', '', '', '0', '', '0', '', 'NULL']),
                kv.Verb(['83', 'kwandika', 'kwaandika',
                         'kw', 'andika', 'anditse', 'tse',
                         '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                         '', '', '', '', '', '0', '', '0', '', 'NULL']),
                kv.Verb(['3562', 'kwoza', 'kwoóza',
                         'kw', 'oza', 'ogeje', 'geje',
                         '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                         '', '', '', '', '', '0', '', '0', '', 'NULL']),
                kv.Verb(['2236', 'kwiruka', 'kwiíruka',
                         'kw', 'iruka', 'irutse', 'tse',
                         '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                         '', '', '', '', '', '0', '', '0', '', 'NULL']),
                kv.Verb(['3120', 'kumira', 'kumira',
                         'ku', 'mira', 'mize', 'ze',
                         '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                         '', '', '', '', '', '0', '', '0', '', 'NULL']),
                kv.Verb(['3209', 'kunanirana', 'kunanirana',
                         'ku', 'nanirana', 'naniranye', 'nye',
                         '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                         '', '', '', '', '', '0', '', '0', '', 'NULL']),
                kv.Verb(['2795', 'gukora', '',
                         'gu', 'kora', 'koze', 'ze',
                         '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                         '', '', '', '', '', '0', '', '0', '', 'NULL']),
                kv.Verb(['2796', 'gukora', 'gukoora',
                         'gu', 'kora', 'koye', 'ye',
                         '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                         '', '', '', '', '', '0', '', '0', '', 'NULL']),
                kv.Verb(['1814', 'guhuhuta', '',
                         'gu', 'hūhūta', 'hūhūse', 'se',
                         '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                         'x', '', 'huhuta', 'hūhūshe',
                         '', '0', '', '0', '', 'NULL']),
                kv.Verb(['1814', 'guhuhuta', '',
                         'gu', 'hūhūta', 'hūhūshe', '',
                         '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                         'x', '', '', '',
                         '', '0', '', '0', '', 'NULL']),
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
                kv.Verb(['3984', 'kurima', 'kurima',
                         'ku', 'rima', 'rimye', 'mye',
                         '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                         '', '', '', '', '', '0', '', '0', '', 'NULL']),
                kv.Verb(['6364', 'guhagarara', 'guhágarara',
                         'gu', 'hagarara', 'hagaraze', 'ze',
                         '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                         '', '', '', '', '', '0', '', '0', '', 'NULL']),
                kv.Verb(['1135', 'kugenda', '',
                         'ku', 'gēnda', 'giye', 'giye',
                         '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                         '', '', '', '', '', '0', '', '0', '', 'NULL']),
                kv.Verb(['1406', 'guha', '',
                         'gu', 'ha', 'haye', 'haye',
                         '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                         '', '', '', '', '', '0', '', '0', '', 'NULL'])
                ]
        freq_simple = {
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
        for i in data:
            i.set_questions()
            print(i.lemma, i.alternatives)
        collection, freq_verbs = kv.collect_verbs(data, freq_simple)
        for i in freq_verbs:
            print(i)
        # TODO check if they should be collected:
        # ukwoza, namize, nomize, nuwandika
        self.assertEqual(len(freq_verbs), 4)
        self.assertEqual(len(collection), 9)
        types = 0
        for i in collection:
            types += i[4]
            print(i)
        self.assertEqual(len(freq_verbs), len(freq_simple)-types)
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

    def test_collect_verbs_only_alternative_verb_hits(self):
        """Test only one of two spelling-alternatives
        from a verbs finds types"""
        data = [kv.Verb(['1114', 'guhuhuta', '',
                         'gu', 'hūhūta', 'hūhūshe', '',
                         '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                         'x', '', '', '',
                         '', '0', '', '0', '', 'NULL']),
                kv.Verb(['1135', 'kugenda', '',
                         'ku', 'gēnda', 'giye', 'giye',
                         '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                         '', '', '', '', '', '0', '', '0', '', 'NULL']),
                kv.Verb(['1406', 'guha', '',
                         'gu', 'ha', 'haye', 'haye',
                         '', '0', 'NULL', 'NULL', 'NULL', 'NULL',
                         '', '', '', '', '', '0', '', '0', '', 'NULL'])
                ]
        for i in data:
            i.set_questions()
        freq_simple = {'abandika': 3, 'iciruka': 3,
                       'mpa': 3, 'wahuhushe': 3}
        collection, freq_verbs = kv.collect_verbs(data, freq_simple)
        for i in collection:
            print(i)
        self.assertEqual(len(freq_verbs), 2)
        self.assertEqual(len(collection), 2)


###############################################################
#       TEST   HELPER                                         #
###############################################################
class TestHelper(TestCase):
    """Test helper functions for PoS classes"""

    def test_put_alternatives_of_same_id_together(self):
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
        collection = kv.put_alternatives_of_same_id_together(collection)
        self.assertEqual(len(collection), 2)
        self.assertEqual(collection[0][0], '-no')
        self.assertIn(['hano', 1048], collection[0])
        self.assertIn(['rino', 77], collection[0])
        self.assertEqual(collection[0][3], 1048+4918)
        self.assertEqual(collection[0][4], 1+18)
