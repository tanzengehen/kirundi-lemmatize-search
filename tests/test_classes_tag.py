#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 16:25:02 2023

@author: doreen
"""

from unittest import TestCase
from unidecode import unidecode
from ..lemmatize_search import kir_tag_classes as tc
from ..lemmatize_search import kir_string_depot as sd
from ..lemmatize_search import kir_tag_search as ts

# nosetests --with-spec --spec-color --with-coverage --cover-erase

SEP = sd.ResourceNames.sep
TESTPATH = sd.ResourceNames.root+SEP+"tests"+SEP+"test_data"+SEP


###############################################################
#       TEST   T E X T  M E T A                               #
###############################################################
class TestTextMeta(TestCase):
    """Test cases for TextMeta
    some statistics of loaded textfile"""

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


###############################################################
#       TEST       T o k e n s    M E T A                     #
###############################################################
class TestTokensMeta(TestCase):
    """Test case for Token in texts
    """

    def test_initiate_tokenlist__firsttime(self):
        """Test TokensMeta before saving"""
        tagged = ts.load_tagged_text(TESTPATH+"tag__test_text0.csv")
        token_list = tagged[1]
        print("first token=", token_list[0])
        self.assertEqual(len(token_list), 133)
        types = {unidecode(i.token.lower()) for i in token_list
                 if i.pos not in ["SYMBOL", "NUM"]}
        print("types:", len(types))
        self.assertEqual(len(types), 65)
        dont_count = {i.token for i in token_list
                      if i.pos in ["SYMBOL", "NUM"]}
        print("symbols+numbers types=", len(dont_count), dont_count)
        self.assertEqual(len(dont_count), 6)
        unknown = {i.lemma for i in token_list if i.pos == "UNK"}
        print("unknown types=", len(unknown), unknown)
        self.assertEqual(len(unknown), 7)
        pos = {i.pos for i in token_list}
        print("different pos", pos)
        percent = round(len(unknown) / (len(types)-len(dont_count)) * 100, 2)
        print(percent, "% unknown")
        lemmata = {i.lemma for i in token_list
                   if i.pos not in ["UNK", "SYMBOL", "NUM"]}
        print("lemmata:", len(lemmata))
        self.assertEqual(len(lemmata), 48)
        # test
        tokensmeta = tc.TokensMeta(token_list)
        tokensmeta.count_tokens()
        self.assertEqual(tokensmeta.tokens, token_list)
        # self.assertEqual(tokensmeta.datetime, datetime.datetime.now()
        self.assertEqual(tokensmeta.n_tokensbond, 93)
        self.assertEqual(tokensmeta.n_tokenscut, 99)
        self.assertEqual(tokensmeta.n_unk, 7)
        # it's different from next test because we read tokenlist from file
        # instead of making a really new one: '11deg' is treated different
        self.assertAlmostEqual(percent, 11.86, 1)
        self.assertEqual(tokensmeta.n_types, 65)
        self.assertEqual(tokensmeta.n_lemmata, 48)

    def test_initiate_tokenlist__read_from_file(self):
        """Test TokensMeta read from saved file"""
        meta, token_list = ts.load_tagged_text(TESTPATH+"tag__test_text0.csv")
        # token_list = tagged[1]
        print(meta, token_list[0])
        self.assertEqual(len(token_list), 133)
        types = {i.token for i in token_list}
        print(len(types))
        lemmata = {i.lemma for i in token_list}
        print(lemmata)
        # test
        tokensmeta = tc.TokensMeta(token_list)
        tokensmeta.put_meta_already_done_before(meta)
        self.assertEqual(tokensmeta.tokens, token_list)
        # self.assertEqual(tokensmeta.datetime, datetime.datetime.now()
        self.assertEqual(tokensmeta.n_tokensbond, 93)
        self.assertEqual(tokensmeta.n_tokenscut, 99)
        self.assertEqual(tokensmeta.n_unk, None)
        self.assertEqual(tokensmeta.percent_unk, '10.77 %')
        self.assertEqual(tokensmeta.n_types, 65)
        self.assertEqual(tokensmeta.n_lemmata, 48)

    def test_lemmasoup(self):
        """Test Make lemma soup from list of tagged tokens"""
        # prepare
        # we re only interested in a token_list
        throw_away, token_list = ts.load_tagged_text(TESTPATH+"tag__test_text0.csv")
        # print("in test lemmasoup: tagged meta=", meta)
        # self.assertEqual(
        #     meta,
        #     {'n_char': 633, 'n_odds': 41, 'n_tokens': 93, 'n_tokens_split': 99,
        #      'n_types': 65, 'n_unk_types': '10.77 %', 'n_lemmata': 48,
        #      'db_version': 'lemmata_test',
        #      'time_tagged': 'Fri Dec 8 15:11:35 2023',
        #      'fn_short': 'test_text0'})
        print("in test lemmasoup: length token_list=", len(token_list))
        self.assertEqual(len(token_list), 133)
        tokens_meta = tc.TokensMeta(token_list)
        tokens_meta.count_tokens()
        print("in test tokens_meta=", tokens_meta)
        happy_result = "umugenzo - 32 -\nkuba 11deg kuramutsa umuvyeyi ."\
            "\n\niyo umugore kuja kuramutsa umuvyeyi kuba kubera , kuja "\
            "kwikorera guca mu - irembo _nawa , guca mu icanzo , _agasanga "\
            "gusa , -iwe , mu _mutangaro -a - umuryango . gusa kuba "\
            "kubangikanya -o-o -ri ifu -a - amasaka canke -a - uburo . "\
            "gufata _utubabi -a - umumanda na - _-o - umurinzi gukoza muri "\
            '_nya ifu gukaraba mu _gahanga -a - _umukobwa -iwe -ti " '\
            'kwibonera umwana " . _nya umwigeme -iwe nawe gukaraba iyo ifu mu'\
            ' _gahanga -a gusa -ti " kwibonera umuvyeyi " . nyina -iwe kugira'\
            ' -rtyo nyene -ti " kwibonera umwana " , _umukobwa -iwe nawe '\
            'kuraba iyo ifu -ti " kwibonera umuvyeyi " . mu gutaha , ku '\
            'umutunzi , _nya umugore kugenda kugabanya inka .'
        # test
        lemmasoup = tokens_meta.lemmasoup()
        print("lemmasoup:", lemmasoup)
        self.assertEqual(lemmasoup, happy_result)

    def test_possoup(self):
        """Test Make PoS-soup from list of tagged tokens"""
        # prepare
        tagged = ts.load_tagged_text(TESTPATH+"tag__test_text0.csv")
        tokens = tc.TokensMeta(tagged[1])
        happy_result = 'NOUN - NUM -\nVERB NUM VERB NOUN .\n\nCONJ NOUN VERB '\
            'VERB NOUN VERB VERB , VERB VERB VERB PREP - NOUN UNK , VERB '\
            'PREP NOUN , UNK VERB , PRON , PREP UNK PRON - NOUN . VERB VERB '\
            'VERB PRON VERB NOUN PRON - NOUN CONJ PRON - NOUN . VERB UNK '\
            'PRON - NOUN CONJ - PRON - PROPN_VEG VERB PREP UNK NOUN VERB '\
            'PREP UNK PRON - UNK PRON VERB " VERB NOUN " . UNK NOUN PRON '\
            'INTJ VERB CONJ NOUN PREP UNK PRON VERB VERB " VERB NOUN " . '\
            'NOUN PRON VERB PRON NOUN VERB " VERB NOUN " , UNK PRON INTJ '\
            'VERB CONJ NOUN VERB " VERB NOUN " . PREP VERB , PREP NOUN , '\
            'UNK NOUN VERB VERB NOUN .'
        # test
        possoup = tokens.possoup()
        self.assertEqual(possoup, happy_result)

    def test_remake_text(self):
        """Test Remake text from list of tagged tokens"""
        # prepare
        tagged = ts.load_tagged_text(TESTPATH+"tag__test_text0.csv")
        tokens = tc.TokensMeta(tagged[1])
        happy_result = 'imigenzo - 32 -\nUbwa 11deg Kuramutsa abavyéyi.\n\n'\
            'Iyó umugóre ajé kuramutsa abavyéyi ubwa mbere, abáje bikoreye '\
            'báca mw-irémbo nawá, agaca mu canzo, agasanga sé, wíwé, mu '\
            'mutangaro w-úmuryango. Sé yába yibangikanije agakoko karímwo '\
            'ifu y-ámasáka cânké y-úbúro. Yafáta utubabi tw-úmumândá '\
            'n-utw-úmurinzi agakoza murí nya fu akarába mu gahanga '\
            'k-úmukobwa wíwé ati "Kwíbonera abâna". Nya mwígeme wíwé nawé '\
            'akarába iyo fu mu gahánga ka sé ati "Kwíbonera abavyéyi". Nyina '\
            'wíwé akagira gúrtyo nyéne ati "Kwíbonera abâna", umukobwa wíwé '\
            'nawé akamúraba iyo fu ati "Kwíbonera abavyéyi". Mu gutaha, ku '\
            'batunzi, nya mugóre yagénda agábanye inká.'
        re_text = tokens.remake_text()
        self.assertEqual(re_text, happy_result)
