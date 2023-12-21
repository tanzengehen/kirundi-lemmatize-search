#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 22:18:33 2023

@author: doreen nixdorf
"""

from unittest import TestCase
import os
from ..lemmatize_search import kir_helper2 as kh
from ..lemmatize_search import kir_string_depot as sd
from ..lemmatize_search import kir_start_input_console as ic

# nosetests --with-spec --spec-color --with-coverage --cover-erase


####################################################
#     T E S T        UI-Language                   #
####################################################
class TestUiLanguage(TestCase):
    """Test case for UI-language
    """

    def test_set_ui_language_de(self):
        """Test find german strings"""
        language = kh.set_ui_language("de")
        self.assertEqual(
            language.gettext('Are you sure, that this is a tagged file?'),
            "Ist das ganz sicher eine Datei mit Etiketten?")

    def test_set_ui_language_rn(self):
        """Test find rundi strings"""
        language = kh.set_ui_language("rn")
        self.assertEqual(
            language.gettext('Are you sure, that this is a tagged file?'),
            "Urazi neza ko ico ni ifishi n'indanzi?")

    # def test_set_ui_language_fr(self):
    #     """Test find french strings"""
    #     language = kh.set_ui_language("fr")
    #     self.assertEqual(
    #         language.gettext('Are you sure, that this is a tagged file?'),
    #         "Urazi neza ko ico ni ifishi n'indanzi?")

    def test_set_ui_language_en(self):
        """Test take english strings"""
        language = kh.set_ui_language("en")
        self.assertEqual(
            language.gettext('Are you sure, that this is a tagged file?'),
            "Are you sure, that this is a tagged file?")

    def test_set_ui_language_invalid(self):
        """Test invalid language input"""
        wrong = kh.set_ui_language("not_valid")
        self.assertEqual(wrong, "not")


####################################################
#     T E S T       S A V I N G  FILES             #
####################################################
class TestSaveResources(TestCase):
    """Test cases for saving nested list or tuple
    """

    def test_save_list(self):
        """Test save list (also nested list or tuple)"""
        # prepare
        lemmafreq = [
          ['kugendana', '1139', 'VERB', 20, 1, ['kugendana', 20]],
          ['igisomwa', '6667', 'NOUN', 5, 2, ['gisomwa', 4], ['ibisomwa', 1]],
          ['ubutwari', '', 'UNK', 11, 1, ['ubutwari', 11]],
          'only string']
        fname = sd.ResourceNames.root+"/tests/test_data/save_list.csv"
        if os.path.exists(fname):
            os.remove(fname)
        self.assertFalse(os.path.exists(fname))
        # test
        kh.save_list(lemmafreq, fname)
        self.assertTrue(os.path.exists(fname))
        with open(fname, encoding="utf-8") as testfile:
            text = testfile.readlines()
        self.assertEqual(len(text), 4)
        self.assertEqual(
            text[0],
            "kugendana;1139;VERB;20;1;['kugendana', 20];\n")
        self.assertEqual(
            text[1],
            "igisomwa;6667;NOUN;5;2;['gisomwa', 4];['ibisomwa', 1];\n")
        self.assertEqual(
            text[2],
            "ubutwari;;UNK;11;1;['ubutwari', 11];\n")
        self.assertEqual(text[3], "only string\n")
        os.remove(fname)

    def test_save_list_wrong(self):
        """Test List with nested dict will not be saved"""
        # prepare
        wrong_list = ["wrong", {"wer": "was"}]
        fname = sd.ResourceNames.root+"/tests/test_data/save_list.csv"
        if os.path.exists(fname):
            os.remove(fname)
        self.assertFalse(os.path.exists(fname))
        # test
        kh.save_list(wrong_list, fname)
        self.assertFalse(os.path.exists(fname))

    def test_save_list_with_changed_separators(self):
        """Test save list with different separators"""
        # prepare
        text_list = [["my text has many", "many", "lots of", "\nwords"],
                     ["my text much", "much", "more", "\nwords words"]]
        fname = sd.ResourceNames.root+"/tests/test_data/save_list.txt"
        if os.path.exists(fname):
            os.remove(fname)
        self.assertFalse(os.path.exists(fname))
        # test
        kh.save_list(text_list, fname, sep_columns="||", sep_rows="\n\n")
        self.assertTrue(os.path.exists(fname))
        with open(fname, encoding="utf-8") as testfile:
            text = testfile.readlines()
        self.assertEqual(len(text), 6)
        self.assertEqual(text[0], "my text has many||many||lots of||\n")
        self.assertEqual(text[1], "words||\n")
        self.assertEqual(text[2], "\n")
        self.assertEqual(text[3], "my text much||much||more||\n")
        os.remove(fname)

#     def test_save_tagged_text_as_csv(self): is indirect tested as part of tag_ot_load

####################################################
#     T E S T       L O A D I N G  FILES           #
####################################################
#     def test_load_tagged_text(self):

#     def test_load_meta_file(self):

#     def test_show_twenty(self):

#     def test_load_lemmafreq(self):

    
####################################################
#     T E S T       C H E C K  INPUT               #
####################################################
class TestGetQuery(TestCase):
    """Test cases for check the search-query
    """

    # def test_input_searchterm(self):
    #     question = ic.input_searchterm()
    #     # input = "verb !noun * /mu !/foo umuntu"
    #     self.assertEqual(len(question), 6)
    #     self.assertEqual(question,
    #                      ['verb', '!noun', '*', '/mu', '!/foo', 'umuntu'])

    # def test_input_searchterm_asterix_inside(self):
    #     question1 = ic.input_searchterm("verb !noun /m*u !/foo")
    #     self.assertEqual(len(question1), 4)
    #     self.assertEqual(question1, [])

    def test_figure_out_query(self):
        question = ic.figure_out_query(
            ['verb', '!noun', '*', '/mu', '!/foo', 'umuntu'])
        self.assertEqual(question,
                         [('y', 'pos', 'verb'),
                          ('n', 'pos', 'noun'),
                          ('y', '?', '*'),
                          ('y', 'token', 'mu'),
                          ('n', 'token', 'foo'),
                          ('y', 'lemma', 'umuntu')
                          ])
