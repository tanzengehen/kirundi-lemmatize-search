#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 06:36:50 2023

@author: doreen
"""

import os
import shutil
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
        for i in test_collection.advs:
            print("in test_tag make:", i)
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
                  "norm__test_text0.txt",
                  "lemma__test_text0.txt"]:
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
                  "norm__test_text0.txt",
                  "lemma__test_text0.txt"]:
            if os.path.exists(sd.ResourceNames.dir_tagged + i):
                os.remove(sd.ResourceNames.dir_tagged + i)
            self.assertFalse(os.path.exists(sd.ResourceNames.dir_tagged + i))

    def test_tag_or_load_tags__txt_utf16(self):
        """Test Tag text-file: txt utf16"""
        # prepare
        for i in ["tag__test_utf16.csv",
                  "norm__test_utf16.txt",
                  "lemma__test_utf16.txt"]:
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
                  "norm__test_utf16.txt",
                  "lemma__test_utf16.txt"]:
            if os.path.exists(sd.ResourceNames.dir_tagged + i):
                os.remove(sd.ResourceNames.dir_tagged + i)
            self.assertFalse(os.path.exists(sd.ResourceNames.dir_tagged + i))


###############################################################
#       TEST      S A V E     T A G G E D   T E X T           #
###############################################################
class TestSaveTaggedTextAsCsv(TestCase):
    """Test Save tagged text as csv
    """

    def test_save_tagged_text_as_csv(self):
        """Test Save tagged text as csv"""
        # prepare
        meta = {"n_char": 2345,
                "n_odds": 3,
                "n_tokens": 4711,
                "n_tokens_split": 4712,
                "n_types": 815,
                "n_unk_types": "10.7%",
                "n_lemmata": 248,
                "db_name": "nonsense",
                "datetime": 'Wed Dec 20 03:56:15 2023'
                }
        filename = sd.ResourceNames.dir_tagged + "tag__test_file.csv"
        text = ["Ndarukunda", "cane", "ururimi", "kirundi"]
        collection = {"ndarukunda": ['VERB', 'gukunda', 3143],
                      "cane": ['ADV', 'cane', 314],
                      "ururimi": ['NOUN', 'ururimi', 31],
                      "kirundi": ['PROPN_LANG', 'ikirundi', 3]}
        taglist = []
        for i, word in enumerate(text):
            token = ts.tag_lemma(word, collection)
            token.id_char = i*5
            token.id_token = i
            token.id_sentence = 0
            token.id_tokin_sen = i
            token.id_para = 0
            taglist.append(token)
        if os.path.exists(filename):
            os.remove(filename)
        self.assertFalse(os.path.exists(filename))
        # test
        ts.save_tagged_text_as_csv(meta, taglist, filename)
        self.assertTrue(os.path.exists(filename))
        # clean up
        os.remove(filename)
        self.assertFalse(os.path.exists(filename))


###############################################################
#       TEST       L O A D   T A G G E D   T o k e n s        #
###############################################################
class TestLoadTags(TestCase):
    """Test Load tags from file
    """

    def test_load_tagged_text(self):
        """Test load tagged text from csv"""
        meta, tagged_text = ts.load_tagged_text(TESTPATH+"tag__test_text0.csv")
        self.assertEqual(len(meta), 10)
        self.assertEqual(
            meta,
            {'n_char': 633, 'n_odds': 41, 'n_tokens': 93, 'n_tokens_split': 99,
             'n_types': 65, 'n_unk_types': '10.77 %', 'n_lemmata': 48,
             'db_version': 'lemmata_test', 'time_tagged': 'Fri Dec 8 15:11:35 2023',
             'fn_short': 'test_text0'})
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
class TestSearch(TestCase):
    """Test Search words in the text
    """

    def test_search_initiation(self):
        """Test initiate class Search"""
        test_search = sd.Search(
            "foo/bar.txt", [('y', 'pos', 'verb'),
                            ('n', 'pos', 'noun'),
                            ('y', '?', '*'),
                            ('y', 'token', 'mu'),
                            ('n', 'token', 'foo'),
                            ('y', 'lemma', 'umuntu')])
        self.assertEqual(
            test_search.query, [('y', 'pos', 'verb'),
                                ('n', 'pos', 'noun'),
                                ('y', '?', '*'),
                                ('y', 'token', 'mu'),
                                ('n', 'token', 'foo'),
                                ('y', 'lemma', 'umuntu')])
        filename = test_search.fn_search.split(sd.ResourceNames.sep)[-1]
        self.assertEqual(
            filename,
            "bar__verb_!noun_*_mu(exact)_!foo(exact)_umuntu(lemma)_.txt")

    def test_replace_worded_symbols_back(self):
        """Test replace worded symbols back to the symbols"""
        self.assertEqual(sd.replace_worded_symbols_back("semikolon"), ';')
        self.assertEqual(sd.replace_worded_symbols_back("quotation"), '"')
        self.assertEqual(sd.replace_worded_symbols_back("deg"), '°')

    def test_setquery_nextpart(self):
        """Test Set next token of search query"""
        query = [('y', 'pos', 'verb'),
                 ('n', 'pos', 'noun'),
                 ('y', '?', '*')
                 ]
        self.assertEqual(ts.setquery_nextpart(query, 2), ('y', '?', '*'))

    def test_collect_words_around_searchterm_middle(self):
        """Test Collect up to 50 characters before and after search term """
        tagged = ts.load_tagged_text(TESTPATH+"tag__test_text0.csv")
        token_list = tagged[1]
        index = 0
        for i, token in enumerate(token_list):
            if token.token == "agakoko":
                index = i
                break
        self.assertEqual(index, 43)
        text_around = ts.collect_words_around_searchterm(
            index, "agakoko", token_list
            )
        self.assertEqual(len(text_around), 129)
        self.assertEqual(
            text_around,
            ('   u mutangaro w - úmuryango . Sé yába yibangikanije     '
             + 'agakoko        '
             + 'karímwo ifu y - ámasáka cânké y - úbúro . Yafáta utubabi ')
            )

    def test_collect_words_around_searchterm_textend(self):
        """Test Collect up to 50 characters around search term,
        at the end of the text (after search term is only a stop-point)"""
        # prepare
        tagged = ts.load_tagged_text(TESTPATH+"tag__test_text0.csv")
        token_list = tagged[1]
        index = 0
        for i, token in enumerate(token_list):
            if token.token == "inká":
                index = i
                break
        self.assertEqual(index, 131)
        # test
        text_around = ts.collect_words_around_searchterm(
            index, "inká", token_list
            )
        self.assertEqual(len(text_around), 70)
        self.assertEqual(
            text_around,
            ('  gutaha , ku batunzi , nya mugóre yagénda agábanye     '
             + 'inká        . ')
            )

    def test_find_thing__lemma(self):
        """Test Find all tokens mapped to a certain lemma"""
        # prepare
        tagged = ts.load_tagged_text(TESTPATH+"tag__test_text0.csv")
        token_list = tagged[1]
        self.assertEqual(len(token_list), 133)
        # test
        found = ts.find_thing(token_list, 'lemma', "umuvyeyi")
        self.assertEqual(len(found[0]), 4)
        self.assertEqual(
            found[0],
            [('35', '                          - 32 - Ubwa 11deg Kuramutsa'
              + '     abavyéyi        '
              + '. Iyó umugóre ajé kuramutsa abavyéyi ubwa mbere , '),
             ('71', '   eg Kuramutsa abavyéyi . Iyó umugóre ajé kuramutsa'
              + '     abavyéyi        '
              + 'ubwa mbere , abáje bikoreye báca mw - irémbo nawá '),
             ('477', '   é akarába iyo fu mu gahánga ka sé ati " Kwíbonera'
              + '     abavyéyi        '
              + '" . Nyina wíwé akagira gúrtyo nyéne ati " Kwíbonera '),
             ('626', '  ukobwa wíwé nawé akamúraba iyo fu ati " Kwíbonera'
              + '     abavyéyi        "'
              + ' . Mu gutaha , ku batunzi , nya mugóre yagénda agábanye ')]
            )

    def test_find_thing__token_no_hit(self):
        """Test Don't find absent tokens even it's a lemma and this lemma
        got some hits"""
        # prepare
        tagged = ts.load_tagged_text(TESTPATH+"tag__test_text0.csv")
        token_list = tagged[1]
        self.assertEqual(len(token_list), 133)
        # test
        found = ts.find_thing(token_list, 'token', "umuvyeyi")
        self.assertEqual(len(found[0]), 0)

    def test_find_thing__pos(self):
        """Test Find all tokens mapped to a certain Part-of-Speech tag"""
        # prepare
        tagged = ts.load_tagged_text(TESTPATH+"tag__test_text0.csv")
        token_list = tagged[1]
        self.assertEqual(len(token_list), 133)
        # test
        found = ts.find_thing(token_list, 'pos', "PRON")
        print(found[0])
        self.assertEqual(len(found[0]), 14)

    def test_find_thing__pos_missing(self):
        """Test Warn if a Part-of-Speech tag is missing"""
        # prepare
        tagged = ts.load_tagged_text(TESTPATH+"tag__test_text0.csv")
        token_list = tagged[1][9:17]
        self.assertEqual(token_list[0].token, "Iyó")
        self.assertEqual(token_list[-1].token, ",")
        self.assertEqual(token_list[5].token, "ubwa")
        token_list[5].pos = ""
        # test
        found = ts.find_thing(token_list, 'lemma', "kuramutsa")
        self.assertEqual(len(found[1]), 1)
        self.assertEqual(found[1],
                         [('missing tag by word number:', 5, 'ubwa')]
                         )

    def test_find_ngrams__notpronoun_noun(self):
        """Test Find a 2-gram, first part is a not-this-token"""
        # prepare
        tagged = ts.load_tagged_text(TESTPATH+"tag__test_text0.csv")
        token_list = tagged[1]
        # test
        found = ts.find_ngrams(token_list,
                               [('n', 'pos', 'PRON'),
                                ('y', 'pos', 'NOUN')])
        print(found[0])
        self.assertEqual(len(found[0]), 18)

    def test_find_ngrams__pronoun_noun(self):
        """Test Find a 2-gram, ignore symbols between them: y'amasaka"""
        # prepare
        tagged = ts.load_tagged_text(TESTPATH+"tag__test_text0.csv")
        token_list = tagged[1]
        # test
        found = ts.find_ngrams(token_list,
                               [('y', 'pos', 'PRON'),
                                ('y', 'pos', 'NOUN')])
        print(found[0])
        self.assertEqual(len(found[0]), 5)

    def test_find_ngrams__nya_noun_verb(self):
        """Test Find a 3-gram"""
        # prepare
        tagged = ts.load_tagged_text(TESTPATH+"tag__test_text0.csv")
        token_list = tagged[1]
        # test
        found = ts.find_ngrams(token_list,
                               [('y', 'token', 'nya'),
                                ('y', 'pos', 'NOUN'),
                                ('y', 'pos', 'VERB')])
        print(found[0])
        self.assertEqual(len(found[0]), 2)

    def test_find_ngrams__mu_all_all_noun(self):
        """Test Find a 4-gram including wildcard, don't count symbols"""
        # prepare
        tagged = ts.load_tagged_text(TESTPATH+"tag__test_text0.csv")
        token_list = tagged[1]
        # test
        found = ts.find_ngrams(token_list,
                               [('y', 'lemma', 'mu'),
                                ('y', '?', '*'),
                                ('y', '?', '*'),
                                ('y', 'pos', 'NOUN')])
        print(found[0])
        self.assertEqual(len(found[0]), 2)

    def test_find_ngrams__noun_smybol(self):
        """Test Find a 2-gram including symbol"""
        # prepare
        tagged = ts.load_tagged_text(TESTPATH+"tag__test_text0.csv")
        token_list = tagged[1]
        # test
        found = ts.find_ngrams(token_list,
                               [('y', 'pos', 'NOUN'),
                                ('y', 'pos', 'SYMBOL')])
        print(found[0])
        self.assertEqual(len(found[0]), 10)

    def test_find_ngrams__noun_quotation_smybol(self):
        """Test Find a 3-gram including symbol"""
        # prepare
        tagged = ts.load_tagged_text(TESTPATH+"tag__test_text0.csv")
        token_list = tagged[1]
        # test
        found = ts.find_ngrams(token_list,
                               [('y', 'pos', 'NOUN'),
                                ('y', 'token', '"'),
                                ('y', 'pos', 'SYMBOL')])
        print(found[0])
        self.assertEqual(len(found[0]), 4)

    def test_go_search_ngram(self):
        """Test go_search with 2-gram"""
        # prepare
        tagged = ts.load_tagged_text(TESTPATH+"tag__test_text0.csv")
        token_list = tagged[1]
        whatsearch = sd.Search("foo/bar.txt",
                               [('y', 'pos', 'NOUN'),
                                ('y', 'pos', 'Verb')])
        # test
        found = ts.go_search(token_list, whatsearch)
        print(found)
        self.assertEqual(len(found), 8)
        self.assertEqual(found[-1],
                         ['672',
                          '  íbonera abavyéyi " . Mu gutaha , ku batunzi , '
                          + 'nya     mugóre yagénda        agábanye inká . '])

    def test_go_search_1gram(self):
        """Test go_search with 1-gram"""
        # prepare
        tagged = ts.load_tagged_text(TESTPATH+"tag__test_text0.csv")
        token_list = tagged[1]
        whatsearch = sd.Search("foo/bar.txt",
                               [('y', 'lemma', 'umwana')])
        # test
        found = ts.go_search(token_list, whatsearch)
        print(found)
        self.assertEqual(len(found), 2)
        self.assertEqual(found[-1],
                         ('551', '  . Nyina wíwé akagira gúrtyo nyéne ati "'
                          + ' Kwíbonera     abâna        " , umukobwa wíwé '
                          + 'nawé akamúraba iyo fu ati " Kwíbonera '))

    def test_go_search_no_result(self):
        """Test go_search for no result"""
        # prepare
        tagged = ts.load_tagged_text(TESTPATH+"tag__test_text0.csv")
        token_list = tagged[1]
        whatsearch = sd.Search("foo/bar.txt",
                               [('y', 'token', 'sinzokwibagira')])
        # test
        found = ts.go_search(token_list, whatsearch)
        print(found)
        self.assertFalse(found)

# https://stackovercoder.com.de/programming/4219717/how-to-assert-output-with-nosetest-unittest-in-python
    # def test_go_search_missing_tag(self):
    #     # prepare
    #     tagged = ts.load_tagged_text(TESTPATH+"tag__test_text0.csv")
    #     token_list = tagged[1]
    #     token_list[4].pos = ""
    #     whatsearch = sd.Search("foo/bar.txt",
    #                            [('y', 'lemma', 'umwana')])
    #     # test
    #     found = ts.go_search(token_list, whatsearch)
    #     print("\nfound:", found)
    #     self.assertEqual(len(found), 2)
    #     # self.assertEqual(
    #     #    fakeOutput,
    #     #    "('missing tag by word number:', 4, 'Ubwa')")

    def test_search_or_load_search__search(self):
        """Test search or load search"""
        # prepare
        if os.path.exists(sd.ResourceNames.dir_searched
                          + "bar__umwana(lemma)_.txt"):
            os.remove(sd.ResourceNames.dir_searched
                      + "bar__umwana(lemma)_.txt")
        self.assertFalse(os.path.exists(sd.ResourceNames.dir_searched
                                        + "bar__umwana(lemma)_.txt"))
        tagged = ts.load_tagged_text(TESTPATH+"tag__test_text0.csv")
        token_list = tagged[1]
        fn_in = "foo/bar.txt"
        quterms = [('y', 'lemma', 'umwana')]
        single = True
        # test
        ts.search_or_load_search(fn_in, quterms, single, token_list)
        self.assertTrue(os.path.exists(sd.ResourceNames.dir_searched
                                       + "bar__umwana(lemma)_.txt"))
        searchresult = kh.load_lines(sd.ResourceNames.dir_searched
                                     + "bar__umwana(lemma)_.txt")
        self.assertEqual(len(searchresult), 2)
        self.assertEqual(
            searchresult[1],
            '551;  . Nyina wíwé akagira gúrtyo nyéne ati " Kwíbonera'
            + '     abâna        '
            + '" , umukobwa wíwé nawé akamúraba iyo fu ati " Kwíbonera ;\n')
        # clean up
        os.remove(sd.ResourceNames.dir_searched
                  + "bar__umwana(lemma)_.txt")
        self.assertFalse(os.path.exists(sd.ResourceNames.dir_searched
                                        + "bar__umwana(lemma)_.txt"))

    def test_search_or_load_search__load(self):
        """Test search or load search"""
        # prepare
        self.assertTrue(os.path.exists(
            TESTPATH+"test_text0__NOUN_wíwé(exact)_.txt"))
        shutil.copy(TESTPATH+"test_text0__NOUN_wíwé(exact)_.txt",
                    sd.ResourceNames.dir_searched
                    + "test_text0__NOUN_wíwé(exact)_.txt")
        token_list = [1, 2, 3]
        fn_in = "tag__test_text0.csv"
        quterms = [('y', 'pos', 'NOUN'), ('y', 'token', 'wíwé')]
        single = True
        # test
        ts.search_or_load_search(fn_in, quterms, single, token_list)
        self.assertTrue(os.path.exists(sd.ResourceNames.dir_searched
                                       + "test_text0__NOUN_wíwé(exact)_.txt"))
        searchresult = kh.load_lines(sd.ResourceNames.dir_searched
                                     + "test_text0__NOUN_wíwé(exact)_.txt")
        self.assertEqual(len(searchresult), 2)
        print(searchresult)
        self.assertEqual(
            searchresult[1],
            '496;    fu mu gahánga ka sé ati " Kwíbonera abavyéyi " .'
            + '     Nyina wíwé        '
            + 'akagira gúrtyo nyéne ati " Kwíbonera abâna " , umukobwa ;\n')
        # clean up
        os.remove(sd.ResourceNames.dir_searched
                  + "test_text0__NOUN_wíwé(exact)_.txt")
        self.assertFalse(os.path.exists(sd.ResourceNames.dir_searched
                                        + "test_text0__NOUN_wíwé(exact)_.txt"))
