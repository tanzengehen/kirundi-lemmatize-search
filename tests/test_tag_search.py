#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 06:36:50 2023

@author: doreen
"""

import os
# import datetime
from unittest import TestCase
from ..lemmatize_search import kir_string_depot as sd
from ..lemmatize_search import kir_tag_search as ts
from ..lemmatize_search import kir_db_classes as dbc
from ..lemmatize_search import kir_helper2 as kh

# nosetests --with-spec --spec-color --with-coverage --cover-erase

SEP = sd.ResourceNames.sep
TESTPATH = sd.ResourceNames.root+SEP+"tests"+SEP+"test_data"+SEP


###############################################################
#       TEST   lemma frequency distribution                   #
###############################################################
class TestLemmafreqFromText(TestCase):
    """Test case for making lemma-frequency of a textfile
    """

    def test_make_lemmafreq_fromtext(self):
        """Test Make lemma frequency distribution of text"""
        # prepare
        text = kh.load_text_fromfile(TESTPATH+"test_text0.txt",
                                     en_code="utf-8")
        self.assertEqual(
            text[:60],
            "imigenzo - 32 -\nUbwa 11°\tKuramutsa abavyéyi.\n\nIyó umugóre aj")
        db_test = dbc.get_resources(TESTPATH + "lemmata_test.csv",
                                    TESTPATH + "names_test.csv")
        self.assertEqual(len(db_test), 9)
        self.assertEqual(len(db_test.get('verbs')), 27)
        self.assertEqual(len(db_test.get('nouns1')), 17)
        self.assertEqual(len(db_test.get('nouns2')), 0)
        self.assertEqual(len(db_test.get('adjectives')), 0)
        self.assertEqual(len(db_test.get('pronouns')), 2)
        self.assertEqual(len(db_test.get('unchanging_words')), 9)
        self.assertEqual(len(db_test.get('rests')), 1)
        self.assertEqual(len(db_test.get('stems')), 55)
        self.assertEqual(len(db_test.get('names')), 5)
        # test
        test_collection = ts.make_lemmafreq_fromtext(text, db_test)
        # for i in test_collection.advs:
        #     print("in test_tag make:", i)
        self.assertEqual(len(test_collection.adjs), 0)
        self.assertEqual(len(test_collection.advs), 7)
        self.assertEqual(len(test_collection.names), 1)
        self.assertEqual(len(test_collection.nouns), 16)
        self.assertEqual(len(test_collection.pronouns), 5)
        self.assertEqual(len(test_collection.unk), 8)
        self.assertEqual(len(test_collection.verbs), 19)
        # kh.save_list(test_collection.adjs, TESTPATH+"test_adjs.csv")
        # kh.save_list(test_collection.advs, TESTPATH+"test_advs.csv")
        # kh.save_list(test_collection.nouns, TESTPATH+"test_nouns.csv")
        # kh.save_list(test_collection.pronouns, TESTPATH+"test_pronouns.csv")
        # kh.save_list(test_collection.unk, TESTPATH+"test_unk.csv")
        # kh.save_list(test_collection.verbs, TESTPATH+"test_verbs.csv")


###############################################################
#       TEST         split text                               #
###############################################################
class TestSplitInSentences(TestCase):
    """Test case split text insentences
    """

    def test_split_in_sentences(self):
        """Test split text in sentences"""
        # prepare
        text = kh.load_text_fromfile(TESTPATH+"test_text1.txt",
                                     en_code="utf-8")
        self.assertEqual(
            text[:60],
            "imigenzo - 32 -\\nUbwa 11° Kuramutsa abavyéyi.\\n\\nIyó umugóre")
        # test
        sentences = ts.split_in_sentences(text)
        # for i, sentence in enumerate(sentences):
        #     print(i, sentence)
        self.assertEqual(len(sentences), 7)
        self.assertEqual(
            sentences[0],
            "imigenzo - 32 - <prgrph> Ubwa 11° Kuramutsa abavyéyi.")
        self.assertEqual(
            sentences[1][:60],
            "<prgrph>  <prgrph> Iyó umugóre ajé kuramutsa abavyéyi ubwa m")


###############################################################
#       TEST          T A G   T o k e n s                     #
###############################################################
class TestTagToken(TestCase):
    """Test Tag single tokens
    """

    def test_tag_word_nrmailweb__number(self):
        """Test Tag numbers"""
        tag = ts.tag_word_nrmailweb("456")
        self.assertEqual(tag.token, "456")
        self.assertEqual(tag.pos, "NUM")
        self.assertEqual(tag.lemma, "456")

    def test_tag_word_nrmailweb__roman_number(self):
        """Test Tag roman numbers"""
        tag = ts.tag_word_nrmailweb("XII")
        self.assertEqual(tag.token, "xii")
        self.assertEqual(tag.pos, "NUM_ROM")
        self.assertEqual(tag.lemma, "XII")

    def test_tag_word_nrmailweb__mail(self):
        """Test Tag and anonymise email address"""
        tag = ts.tag_word_nrmailweb("someone@any.com")
        self.assertEqual(tag.token, "emailAtsomewhere")
        self.assertEqual(tag.pos, "EMAIL")
        self.assertEqual(tag.lemma, "emailAtsomewhere")

    def test_tag_word_nrmailweb__website(self):
        """Test Tag and anonymise website"""
        tag = ts.tag_word_nrmailweb("www.mywebsite.bi")
        self.assertEqual(tag.token, "address_in_web")
        self.assertEqual(tag.pos, "WWW")
        self.assertEqual(tag.lemma, "address_in_web")

    def test_tag_word_nrmailweb__false(self):
        """Test Don't tag what doesn't fit numbers"""
        tag = ts.tag_word_nrmailweb("ibindi")
        self.assertEqual(tag, [])

    def test_tag_punctmarks_etc__true(self):
        """Test Tag punctuationmarks etc"""
        tag = ts.tag_punctmarks_etc("!")
        self.assertEqual(tag.token, "!")
        self.assertEqual(tag.pos, "SYMBOL")
        self.assertEqual(tag.lemma, "!")

    def test_tag_punctmarks_etc__semikolon(self):
        """Test Tag semikolon"""
        tag = ts.tag_punctmarks_etc(";")
        self.assertEqual(tag.token, "semikolon")
        self.assertEqual(tag.pos, "SYMBOL")
        self.assertEqual(tag.lemma, "semikolon")

    def test_tag_punctmarks_etc__quotation_mark(self):
        """Test Tag quotation mark"""
        tag = ts.tag_punctmarks_etc('"')
        self.assertEqual(tag.token, "quotation")
        self.assertEqual(tag.pos, "SYMBOL")
        self.assertEqual(tag.lemma, "quotation")

    def test_tag_punctmarks_etc__false(self):
        """Test Don't tag what doesn't fit punctuation"""
        tag = ts.tag_punctmarks_etc("ibindi")
        self.assertEqual(tag, [])

    def test_prepare_lemmatypes(self):
        """Test Convert lemmafrequency distribution list to dictionary"""
        # prepare
        lemma_freqency_list = [
            ["-a", 7778, "PRON", 6, 5, ['k', 1], ['ka', 1], ['tw', 1], ['w', 1], ['y', 2]],
            ["mu", 3143, "PREP", 6, 2, ['mu', 5], ['mw', 1]],
            ["-iwe", 2326, "PRON", 5, 1, ['wiwe', 5]]
            ]
        # test
        type_dict = ts.prepare_lemmatypes(lemma_freqency_list)
        self.assertEqual(len(type_dict), 8)
        self.assertEqual(type_dict.get("mu"), ['PREP', 'mu', 3143])
        self.assertEqual(type_dict.get("mw"), ['PREP', 'mu', 3143])

    def test_tag_lemma__true(self):
        """Test Tag word known to rundi database"""
        # prepare
        type_dict = {'mu': ['PREP', 'mu', 3143],
                     'mw': ['PREP', 'mu', 3143],
                     'wiwe': ['PRON', '-iwe', 2326]}
        # test
        tag = ts.tag_lemma("mw", type_dict)
        self.assertEqual(tag.token, "mw")
        self.assertEqual(tag.pos, "PREP")
        self.assertEqual(tag.lemma, "mu")

    def test_tag_lemma__false(self):
        """Test Don't tag word unknown to rundi database"""
        # prepare
        type_dict = {'mu': ['PREP', 'mu', 3143],
                     'mw': ['PREP', 'mu', 3143],
                     'wiwe': ['PRON', '-iwe', 2326]}
        # test
        tag = ts.tag_lemma("Uburundi", type_dict)
        self.assertEqual(tag.token, "Uburundi")
        self.assertEqual(tag.pos, "UNK")
        self.assertEqual(tag.lemma, "uburundi")


###############################################################
#       TEST          T A G   T E X T                         #
###############################################################
class TestTagText(TestCase):
    """Test Tag all words of text
    """

    def test_tag_text_with_db(self):
        """Test Tag given text"""
        # prepare
        text = kh.load_text_fromfile(TESTPATH + "test_text1.txt",
                                     en_code="utf-8")
        self.assertEqual(
            text[:60],
            "imigenzo - 32 -\\nUbwa 11° Kuramutsa abavyéyi.\\n\\nIyó umugóre")
        db_test = dbc.get_resources(TESTPATH + "lemmata_test.csv",
                                    TESTPATH + "names_test.csv")
        self.assertEqual(len(db_test), 9)
        self.assertEqual(len(db_test.get('verbs')), 27)
        self.assertEqual(len(db_test.get('nouns1')), 17)
        self.assertEqual(len(db_test.get('nouns2')), 0)
        self.assertEqual(len(db_test.get('adjectives')), 0)
        self.assertEqual(len(db_test.get('pronouns')), 2)
        self.assertEqual(len(db_test.get('unchanging_words')), 9)
        self.assertEqual(len(db_test.get('rests')), 1)
        self.assertEqual(len(db_test.get('stems')), 55)
        self.assertEqual(len(db_test.get('names')), 5)
        # test
        lemma_lists, text_tagged = ts.tag_text_with_db(text, db_test)
        self.assertEqual(len(text_tagged.tokens), 133)
        self.assertEqual(len(lemma_lists.names), 1)
        self.assertEqual(len(lemma_lists.advs), 7)
        self.assertEqual(len(lemma_lists.pronouns), 5)
        self.assertEqual(len(lemma_lists.nouns), 16)
        self.assertEqual(len(lemma_lists.adjs), 0)
        self.assertEqual(len(lemma_lists.verbs), 19)
        self.assertEqual(len(lemma_lists.unk), 8)
        self.assertEqual(len(lemma_lists.known), 48)

    def test_tag_or_load_tags__txt_utf8(self):
        """Test Tag text-file: txt utf8
        check against """
        # prepare
        for i in ["tag__test_text0.csv",
                  "norm__test_text0.txt"]:
            if os.path.exists(sd.ResourceNames.dir_tagged + i):
                os.remove(sd.ResourceNames.dir_tagged + i)
            self.assertFalse(os.path.exists(sd.ResourceNames.dir_tagged + i))
        db_test = dbc.get_resources(TESTPATH+"lemmata_test.csv",
                                    TESTPATH+"names_test.csv")
        # test
        tagged = ts.tag_or_load_tags(TESTPATH+"test_text0.txt", db_test)
        self.assertEqual(len(tagged.tokens), 133)
        self.assertEqual(tagged.tokens[7].id_token, 7)
        self.assertEqual(tagged.tokens[7].id_char, 36)
        self.assertEqual(tagged.tokens[7].id_sentence, 1)
        self.assertEqual(tagged.tokens[7].id_tokin_sen, 3)
        self.assertEqual(tagged.tokens[7].id_para, 1)
        self.assertEqual(tagged.tokens[7].token, "abavyéyi")
        self.assertEqual(tagged.tokens[7].pos, "NOUN")
        self.assertEqual(tagged.tokens[7].lemma, "umuvyeyi")
        self.assertEqual(tagged.tokens[8].id_token, 7)
        self.assertEqual(tagged.tokens[8].id_char, 44)
        self.assertEqual(tagged.tokens[8].id_sentence, 1)
        self.assertEqual(tagged.tokens[8].id_tokin_sen, 3)
        self.assertEqual(tagged.tokens[8].id_para, 1)
        self.assertEqual(tagged.tokens[8].token, ".")
        self.assertEqual(tagged.tokens[8].pos, "SYMBOL")
        self.assertEqual(tagged.tokens[8].lemma, ".")
        # check positions against the file made by this function: norm__ (utf8)
        text = kh.load_text_fromfile(
            sd.ResourceNames.dir_tagged+"norm__test_text0.txt", "utf8")
        self.assertEqual(text[36:45], "abavyéyi.")
        self.assertEqual(tagged.tokens[130].id_token, 92)
        self.assertEqual(tagged.tokens[130].id_char, 619)
        self.assertEqual(tagged.tokens[130].id_sentence, 9)
        self.assertEqual(tagged.tokens[130].id_tokin_sen, 7)
        self.assertEqual(tagged.tokens[130].id_para, 3)
        self.assertEqual(tagged.tokens[130].token, "agábanye")
        self.assertEqual(tagged.tokens[130].pos, "VERB")
        self.assertEqual(tagged.tokens[130].lemma, "kugabanya")
        self.assertEqual(text[619:628], "agábanye ")
        # clean up
        for i in ["tag__test_text0.csv",
                  "fl__test_text0.csv",
                  "norm__test_text0.txt"]:
            os.remove(sd.ResourceNames.dir_tagged + i)
            self.assertFalse(os.path.exists(sd.ResourceNames.dir_tagged + i))

    def test_tag_or_load_tags__txt_utf16(self):
        """Test Tag text-file: txt utf16"""
        # prepare
        for i in ["tag__test_utf16.csv",
                  "norm__test_utf16.txt"]:
            if os.path.exists(sd.ResourceNames.dir_tagged + i):
                os.remove(sd.ResourceNames.dir_tagged + i)
            self.assertFalse(os.path.exists(sd.ResourceNames.dir_tagged + i))
        db_test = dbc.get_resources(TESTPATH+"lemmata_test.csv",
                                    TESTPATH+"names_test.csv")
        # test
        # tag origin: utf16
        tagged = ts.tag_or_load_tags(TESTPATH+"test_utf16.txt", db_test)
        self.assertEqual(len(tagged.tokens), 313)
        self.assertEqual(tagged.tokens[78].id_token, 61)
        self.assertEqual(tagged.tokens[78].id_char, 463)
        self.assertEqual(tagged.tokens[78].id_sentence, 2)
        self.assertEqual(tagged.tokens[78].id_tokin_sen, 8)
        self.assertEqual(tagged.tokens[78].id_para, 0)
        self.assertEqual(tagged.tokens[78].token, "yabana")
        self.assertEqual(tagged.tokens[78].pos, "NOUN")
        self.assertEqual(tagged.tokens[78].lemma, "umwana")
        # check positions against the file made by this function: norm__ (utf8)
        text = kh.load_text_fromfile(
            sd.ResourceNames.dir_tagged+"norm__test_utf16.txt", "utf8")
        self.assertEqual(text[463:470], "yabana ")
        self.assertEqual(tagged.tokens[309].id_token, 240)
        self.assertEqual(tagged.tokens[309].id_char, 1661)
        self.assertEqual(tagged.tokens[309].id_sentence, 12)
        self.assertEqual(tagged.tokens[309].id_tokin_sen, 30)
        self.assertEqual(tagged.tokens[309].id_para, 0)
        self.assertEqual(tagged.tokens[309].token, "hari")
        self.assertEqual(tagged.tokens[309].pos, "VERB")
        self.assertEqual(tagged.tokens[309].lemma, "-ri")
        self.assertEqual(text[1661:1666], "hari ")
        # clean up
        for i in ["tag__test_utf16.csv",
                  "fl__test_utf16.csv",
                  "norm__test_utf16.txt"]:
            os.remove(sd.ResourceNames.dir_tagged + i)
            self.assertFalse(os.path.exists(sd.ResourceNames.dir_tagged + i))


###############################################################
#       TEST       L O A D   T A G G E D   T o k e n s        #
###############################################################
class TestLoadTags(TestCase):
    """Test Load tags from file
    """

    def test_load_tagged_text(self):
        """Test load tagged text from csv"""
        meta, tagged_text = ts.load_tagged_text(TESTPATH+"tag__test_text0.csv")
        self.assertEqual(len(meta), 9)
        self.assertEqual(
            meta,
            {'n_char': 633, 'n_odds': 41, 'n_tokens': 93, 'n_tokens_split': 99,
             'n_types': 79, 'n_unk_types': '12.12 %', 'n_lemmata': 48,
             'db_name': 'lemmata_test', 'datetime': 'Fri Dec 8 15:11:35 2023'})
        self.assertEqual(len(tagged_text), 133)

    def test_load_tagged_text__wrong_csv(self):
        """Test load tagged text from csv (no meta-data dictionary)"""
        self.assertRaises(
            SystemExit,
            ts.load_tagged_text, TESTPATH+"fl__text_test.csv")

    def test_load_tagged_text__wrong1_csv(self):
        """Test load tagged text from csv (wrong keys in meta-data)
        """
        self.assertRaises(
            SystemExit,
            ts.load_tagged_text, TESTPATH+"tag__wrong1.csv")

    def test_load_tagged_text__wrong2_csv(self):
        """Test load tagged text from csv (wrong type in first row)
        """
        self.assertRaises(
            SystemExit,
            ts.load_tagged_text, TESTPATH+"tag__wrong2.csv")

    def test_load_tagged_text__wrong3_csv(self):
        """Test load tagged text from csv (wrong keys for Token-attributes)
        """
        self.assertRaises(
            SystemExit,
            ts.load_tagged_text, TESTPATH+"tag__wrong3.csv")

    def test_tag_or_load_tags__csv(self):
        """Test tag text or load tagged text: from csv"""
        # prepare
        db_test = dbc.get_resources(TESTPATH+"lemmata_test.csv",
                                    TESTPATH+"names_test.csv")
        # test
        tagged = ts.tag_or_load_tags(TESTPATH+"tag__test_text0.csv", db_test)
        self.assertEqual(len(tagged.tokens), 133)

    def test_tag_or_load_tags__wrong_csv(self):
        """Test tag text or load tagged text: wrong csv"""
        db_test = dbc.get_resources(TESTPATH+"lemmata_test.csv",
                                    TESTPATH+"names_test.csv")
        self.assertRaises(
            SystemExit,
            ts.tag_or_load_tags, TESTPATH+"fl__text_test.csv", db_test)


###############################################################
#       TEST          S E A R C H                             #
###############################################################
