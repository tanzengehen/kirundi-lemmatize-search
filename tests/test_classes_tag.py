#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 16:25:02 2023

@author: doreen
"""

from unittest import TestCase
from ..lemmatize_search import kir_tag_classes as tc

# nosetests --with-spec --spec-color --with-coverage --cover-erase


###############################################################
#       TEST   T E X T  M E T A                               #
###############################################################
class TestTextMeta(TestCase):
    """Test cases for TextMeta
    first statistics of loaded textfile"""

    def test_replace_strangeletters(self):
        """Test replace non UTF-8 characters from bad OCR
        take: string
        set: text, nodds, nchars
        """
        text = tc.TextMeta()
        text.raw = "lala   la. oh\xc3\xa2"
        text.replace_strangeletters()
        self.assertEqual(text.text, "lala la. ohÃ¢")
        self.assertEqual(text.nodds, 2)
        self.assertEqual(text.nchars, 13)

    def test_set_fn_outs_without_fn(self):
        """set filenames later
        for result of analysis in single mode
        filename for normalised text, lemma-frequency-distribution, tagged text
        and lemma_soup"""
        # prepare: initiation without filename
        text = tc.TextMeta()
        text.fn_in = "imana/ishimwe/naronse/igisomwa.txt"
        # test
        text.set_fn_outs()
        self.assertEqual(text.fn_short, "igisomwa")
        self.assertEqual(text.fn_freqlemma.split("/")[-1], "fl__igisomwa.csv")
        self.assertEqual(text.fn_tag.split("/")[-1], "tag__igisomwa.csv")
        self.assertEqual(text.fn_norm.split("/")[-1], "norm__igisomwa.txt")
        self.assertEqual(text.fn_lemmasoup.split("/")[-1], "lemma__igisomwa.txt")

    def test_set_fn_outs_with_fntxt(self):
        """set filenames with initialisation with input-filename-txt
        for result of analysis in single mode
        filename for normalised text, lemma-frequency-distribution, tagged text
        and lemma_soup"""
        # test initiation with given filename
        text1 = tc.TextMeta("foo/mytext.txt")
        self.assertEqual(text1.fn_in, "foo/mytext.txt")
        self.assertEqual(text1.fn_short, "mytext")
        self.assertEqual(text1.fn_freqlemma.split("/")[-1], "fl__mytext.csv")
        self.assertEqual(text1.fn_tag.split("/")[-1], "tag__mytext.csv")
        self.assertEqual(text1.fn_norm.split("/")[-1], "norm__mytext.txt")
        self.assertEqual(text1.fn_lemmasoup.split("/")[-1], "lemma__mytext.txt")

    def test_set_fn_outs_with_fncsv(self):
        """set filenames with initialisation with input-filename-csv
        for result of analysis in single mode
        filename for normalised text, lemma-frequency-distribution, tagged text
        and lemma_soup"""
        # test initiation with given filename
        text1 = tc.TextMeta("foo/tag__mytext.csv")
        self.assertEqual(text1.fn_in, "foo/tag__mytext.csv")
        self.assertEqual(text1.fn_short, "mytext")
        self.assertEqual(text1.fn_freqlemma.split("/")[-1], "fl__mytext.csv")
        self.assertEqual(text1.fn_tag.split("/")[-1], "tag__mytext.csv")
        self.assertEqual(text1.fn_norm.split("/")[-1], "norm__mytext.txt")
        self.assertEqual(text1.fn_lemmasoup.split("/")[-1], "lemma__mytext.txt")

    def test_set_fn_corpus(self):
        """set filenames for result of analysis in corpus mode
        filename for lemma-frequency-distribution and name for tagged text"""
        text = tc.TextMeta()
        text.fn_short = "amakuru_mashasha"
        text.set_fn_corpus("bbc")
        self.assertEqual(text.fn_freqlemma[-29:],
                         "/bbc/fl__amakuru_mashasha.csv")
        self.assertEqual(text.fn_tag[-30:],
                         "/bbc/tag__amakuru_mashasha.csv")
        self.assertEqual(text.fn_norm[-31:],
                         "/bbc/norm__amakuru_mashasha.txt")
        self.assertEqual(text.fn_lemmasoup[-32:],
                         "/bbc/lemma__amakuru_mashasha.txt")


###############################################################
#       TEST   F R E Q  S I M P L E                           #
###############################################################
class TestFreqSimple(TestCase):
    """Test cases for simple frequency distribution
    """

    def test___f_dist__(self):
        """Test Make simple frequency distribution of text"""

        text = "Oh la la, iki gisomwa biragenda neza, ariko jewe \
ndiko ngenda ku kazi. \n\tHanyuma araguhamagara kubera turashaka kuguha \
ibisomwa bishasha kandi kugendana gutamba!"
        simple = tc.FreqSimple(text)
        self.assertEqual(
            simple.blanktext,
            "oh la la iki gisomwa biragenda neza ariko jewe ndiko ngenda ku \
kazi hanyuma araguhamagara kubera turashaka kuguha ibisomwa bishasha kandi \
kugendana gutamba ")
        self.assertEqual(simple.ntokens, 23)
        self.assertEqual(simple.ntypes, 22)
        self.assertEqual(len(simple.blanktext), 156)
        self.assertEqual(simple.freq, [('la', 2),
                                       ('oh', 1),
                                       ('iki', 1),
                                       ('gisomwa', 1),
                                       ('biragenda', 1),
                                       ('neza', 1),
                                       ('ariko', 1),
                                       ('jewe', 1),
                                       ('ndiko', 1),
                                       ('ngenda', 1),
                                       ('ku', 1),
                                       ('kazi', 1),
                                       ('hanyuma', 1),
                                       ('araguhamagara', 1),
                                       ('kubera', 1),
                                       ('turashaka', 1),
                                       ('kuguha', 1),
                                       ('ibisomwa', 1),
                                       ('bishasha', 1),
                                       ('kandi', 1),
                                       ('kugendana', 1),
                                       ('gutamba', 1)
                                       ])


###############################################################
#       TEST   C O L L E C T I O N                            #
###############################################################
class TestCollection(TestCase):
    """Test cases for collection
    """

    def test_initiate_collection(self):
        """Test initialization"""
        simplefreq = [('la', 2),
                      ('oh', 1),
                      ('iki', 1),
                      ('gisomwa', 1),
                      ('biragenda', 1),
                      ('neza', 1),
                      ('ariko', 1),
                      ('jewe', 1),
                      ('ndiko', 1),
                      ('ngenda', 1),
                      ('ku', 1),
                      ('kazi', 1),
                      ('hanyuma', 1),
                      ('araguhamagara', 1),
                      ('kubera', 1),
                      ('turashaka', 1),
                      ('kuguha', 1),
                      ('ibisomwa', 1),
                      ('bishasha', 1),
                      ('kandi', 1),
                      ('kugendana', 1),
                      ('gutamba', 1)
                      ]
        test_collection = tc.Collection(simplefreq)
        self.assertEqual(test_collection.unk, dict(simplefreq))

    def test_put_known(self):
        """Test Put together PoS-lists of all types which found a lemma,
        sorted by lemma frequency"""
        # preparation
        simplefreq = [('la', 2),
                      ('oh', 1),
                      ]
        test_collection = tc.Collection(simplefreq)
        test_collection.names = [['la', '', 'F', 2, 1, ['la', 2]]]
        test_collection.pronouns = [
            ['iki', '2118', 'PRON', 14, 1, ['iki', 14]],
            ['jewe', '2414', 'PRON', 5, 1, ['jewe', 5]]]
        test_collection.nouns = [
         ['igisomwa', '6667', 'NOUN', 5, 2, ['gisomwa', 4], ['ibisomwa', 1]],
         ['akazi', '5890', 'NOUN', 1, 1, ['kazi', 1]]]
        test_collection.adjs = [
            ['-shasha', '4474', 'ADJ', 1, 1, ['bishasha', 1]]]
        test_collection.verbs = [
            ['kugenda', '1135', 'VERB', 2, 2, ['biragenda', 1], ['ngenda', 1]],
            ['guhamagara', '6242', 'VERB', 1, 1, ['araguhamagara', 1]],
            ['kugendana', '1139', 'VERB', 20, 1, ['kugendana', 20]],
            ['gushaka', '4478', 'VERB', 16, 1, ['turashaka', 16]],
            ['gutamba', '4972', 'VERB', 19, 1, ['gutamba', 19]],
            ['-ri', '3966', 'VERB', 6, 1, ['ndiko', 6]],
            ['guha', '1406', 'VERB', 7, 1, ['kuguha', 7]]]
        test_collection.advs = [
            ['ariko', '142', 'CONJ', 1, 1, ['ariko', 1]],
            ['kandi', '2505', 'CONJ', 1, 1, ['kandi', 1]],
            ['ku', '2841', 'PREP', 17, 1, ['ku', 17]],
            ['ooh', 30003, 'INTJ', 3, 1, ['oh', 3]],
            ['neza', '3239', 'ADV', 9, 1, ['neza', 9]],
            ['hanyuma', '5520', 'CONJ', 13, 1, ['hanyuma', 13]],
            ['kubera', '6286', 'CONJ', 4, 1, ['kubera', 4]]]
        # test
        test_collection.put_known()
        self.assertEqual(len(test_collection.known), 20)
        self.assertEqual(
            test_collection.known[0],
            ['kugendana', '1139', 'VERB', 20, 1, ['kugendana', 20]])
        for i in test_collection.known:
            print(i)
        self.assertEqual(
            test_collection.known[10],
            ['igisomwa', '6667', 'NOUN', 5, 2,
             ['gisomwa', 4], ['ibisomwa', 1]])


###############################################################
#       TEST   F R E Q  M E T A                               #
###############################################################
class TestFreqMeta(TestCase):
    """Test case for metadata of lemma-frequency-distribution
    """

    def test_initiate_freqmeta(self):
        """Test Collect metadata of lemma frequency distribution"""
        # prepare
        lemmafreq = [
          ['kugendana', '1139', 'VERB', 20, 1, ['kugendana', 20]],
          ['gutamba', '4972', 'VERB', 19, 1, ['gutamba', 19]],
          ['ku', '2841', 'PREP', 17, 1, ['ku', 17]],
          ['gushaka', '4478', 'VERB', 16, 1, ['turashaka', 16]],
          ['iki', '2118', 'PRON', 14, 1, ['iki', 14]],
          ['hanyuma', '5520', 'CONJ', 13, 1, ['hanyuma', 13]],
          ['ubutwari', '', 'UNK', 11, 1, ['ubutwari', 11]],
          ['neza', '3239', 'ADV', 9, 1, ['neza', 9]],
          ['uburundi', '', 'PROPN_LOC', 9, 1, ['burundi', 9]],
          ['guha', '1406', 'VERB', 7, 1, ['kuguha', 7]],
          ['-ri', '3966', 'VERB', 6, 1, ['ndiko', 6]],
          ['igisomwa', '6667', 'NOUN', 5, 2, ['gisomwa', 4], ['ibisomwa', 1]],
          ['jewe', '2414', 'PRON', 5, 1, ['jewe', 5]],
          ['kubera', '6286', 'CONJ', 4, 1, ['kubera', 4]],
          ['ooh', 30003, 'INTJ', 3, 1, ['oh', 3]],
          ['kugenda', '1135', 'VERB', 2, 2, ['biragenda', 1], ['ngenda', 1]],
          ['la', '', 'F', 2, 1, ['la', 2]],
          ['akazi', '5890', 'NOUN', 1, 1, ['kazi', 1]],
          ['-shasha', '4474', 'ADJ', 1, 1, ['bishasha', 1]],
          ['guhamagara', '6242', 'VERB', 1, 1, ['araguhamagara', 1]],
          ['ariko', '142', 'CONJ', 1, 1, ['ariko', 1]],
          ['kandi', '2505', 'CONJ', 1, 1, ['kandi', 1]]]
        # test
        meta = tc.FreqMeta(lemmafreq)
        self.assertEqual(meta.length, 22)
        self.assertEqual(meta.n_lemma, 19)
        self.assertEqual(meta.n_unk, 1)
        self.assertEqual(meta.n_one, 5)
        self.assertEqual(meta.n_ne, 1)
        self.assertEqual(meta.n_extern, 1)


###############################################################
#       TEST       T o k e n                                  #
###############################################################
class TestToken(TestCase):
    """Test case for Token in texts
    """

    def test_initiate_token_unknown(self):
        """Test initiate unknown token"""
        token = tc.Token("ndagukunda")
        self.assertEqual(token.id_char, None)
        self.assertEqual(token.id_para, None)
        self.assertEqual(token.id_sentence, None)
        self.assertEqual(token.id_tokin_sen, None)
        self.assertEqual(token.id_token, None)
        self.assertEqual(token.token, "ndagukunda")
        self.assertEqual(token.pos, "UNK")
        self.assertEqual(token.lemma, "ndagukunda")

    def test_initiate_token_known(self):
        """Test initiate known token"""
        token = tc.Token("ndamukunda", "VERB", "gukunda")
        self.assertEqual(token.id_char, None)
        self.assertEqual(token.id_para, None)
        self.assertEqual(token.id_sentence, None)
        self.assertEqual(token.id_tokin_sen, None)
        self.assertEqual(token.id_token, None)
        self.assertEqual(token.token, "ndamukunda")
        self.assertEqual(token.pos, "VERB")
        self.assertEqual(token.lemma, "gukunda")

    def test_set_nrs(self):
        """Test set position numbers for token"""
        # prepare
        token = tc.Token("ndamukunda", "VERB", "gukunda")
        # test
        token.set_nrs(23, 4, 345, 1287, 15)
        self.assertEqual(token.id_sentence, 23)
        self.assertEqual(token.id_tokin_sen, 4)
        self.assertEqual(token.id_token, 345)
        self.assertEqual(token.id_char, 1287)
        self.assertEqual(token.id_para, 15)
