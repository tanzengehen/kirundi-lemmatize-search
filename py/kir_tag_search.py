#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 20 15:32:20 2023

@author: doreen nixdorf
"""


import re
import json
from operator import itemgetter
from sys import exit as sysexit
from unidecode import unidecode
import kir_prepare_verbs as kv
import kir_helper2 as kh
import kir_tag_classes as tc
import kir_db_classes as dbc
import kir_string_depot as sd


def reduce_simplefreq_to_lemma_collection(simple_freq_list,
                                          data_rundi):
    """ mapps types to foreign words, named-entities and all PoS in kirundi_db
     reads simple_freq as list of [type,frequency]
     returns object of class Collection"""
    names = data_rundi.get("names")
    dict_verbs = data_rundi.get("verbs")
    dict_adj = data_rundi.get("adjectives")
    dict_prns = data_rundi.get("pronouns")
    dict_adv = data_rundi.get("unchanging_words")
    dict_rests = data_rundi.get("rests")
    dict_nouns1 = data_rundi.get("nouns1")
    dict_nouns2 = data_rundi.get("nouns2")

    # Translators: fill points up to 50 letters
    kh.OBSERVER.notify(
        kh._("sorting Named Entities ..........................."))
    collection = tc.Collection(simple_freq_list)
    len_before = len(simple_freq_list)
    (collection.names, still_unk) = dbc.collect_names(names, simple_freq_list)
    kh.OBSERVER.notify(
        kh._("\nNamed Entities      : ")
        + f"\t{len_before-len(still_unk)}\t\t({len(still_unk)})")
    len_before = len(still_unk)
    (collection.advs, still_unk) = dbc.collect_adv_plus(dict_adv, still_unk)
    kh.OBSERVER.notify(
        kh._("adverbs etc         : ")
        + f"{len_before-len(still_unk)} >> "
        + f"{len(collection.advs)-1}\t({len(still_unk)})")
    len_before = len(still_unk)
    (collection.pronouns,
     still_unk) = dbc.collect_pronouns(dict_prns, still_unk)
    kh.OBSERVER.notify(
        kh._("pronouns            : ") + f"{len_before-len(still_unk)} >> "
        f"{len(collection.pronouns)-1}\t({len(still_unk)})")
    # Translators: fill points up to 50 letters
    kh.OBSERVER.notify(
        kh._("sorting nouns ...................................."))
    len_before = len(still_unk)
    (collection.nouns,
     still_unk) = dbc.collect_nouns(dict_nouns1, still_unk)
    kh.OBSERVER.notify(
        kh._("\nnouns               : ")
        + f"{len_before-len(still_unk)} >> "
        + f"{len(collection.nouns)-1}\t({len(still_unk)})")
    len_before = len(still_unk)
    (collection.adjs, still_unk) = dbc.collect_adjs(dict_adj, still_unk)
    kh.OBSERVER.notify(
        kh._("adjektives          : ")
        + f"{len_before-len(still_unk)} >> "
        + f"{len(collection.adjs)-1}\t({len(still_unk)})")
    kh.OBSERVER.notify(
        kh._("sorting verbs ...................................."))
    len_before = len(still_unk)
    (collection.verbs, still_unk) = kv.sammle_verben(dict_verbs, still_unk)
    kh.OBSERVER.notify(
        kh._("\nverbs               : ")
        + f"{len_before-len(still_unk)} >> "
        + f"{len(collection.verbs)-1}\t({len(still_unk)})")
    # now we search for the nouns we skipped before verbs (uku...)
    len_before = len(still_unk)
    (found_here,
     still_unk) = dbc.collect_nouns(dict_nouns2, still_unk)
    collection.nouns += found_here
    (exclams,
     still_unk) = dbc.collect_exclamations(dict_rests, still_unk)
    collection.advs += exclams
    collection.advs = dbc.put_same_ids_together(collection.advs)
    kh.OBSERVER.notify(
        kh._("\nexclamations        : ")
        + f"\t\t{len_before-len(still_unk)}"
        + f"\nunknown             :\t\t\t\t({len(still_unk)})")
    # collection.unk=[]
    for key, value in still_unk.items():
        if value != 0:
            collection.unk.append((key, "", "UNK", value, 1, [key, value]))
    return collection


def make_lemmafreq_fromtext(mytext, data):
    """takes utf-text, maps to lemmata in db_kirundi,
    returns lemma_freq"""
    simfreq = tc.FreqSimple(mytext)
    lemma_collection = reduce_simplefreq_to_lemma_collection(simfreq.freq, data)
    kh.OBSERVER.notify(kh._("""\nVocabulary
characters         : {nchar}
tokens             : {ntokens}
types              : {ntypes} """).format(nchar=len(mytext),
                                          ntokens=simfreq.ntokens,
                                          ntypes=simfreq.ntypes))
    return lemma_collection


def split_in_sentences(mytext, para=" #|* "):
    """splits texts where [?.!;:] + space_character
    it's only a rough approach
    returns list with strings
    """
    # set a headlines and paragraph flag: "#|*"
    mytextn = mytext.replace("\\n", para)
    all_sents = [mytextn, ]
    # to get a list, not a nested list
    for seperator in [".", "?", "!", ":", ";"]:
        storage = []
        for part in all_sents:
            newportions = part.split(seperator+" ")
            if len(newportions) > 1:
                for new in newportions[:-1]:
                    new = new+seperator
                    storage.append(new)
                storage.append(newportions[-1])
            else:
                storage.append(part)
            all_sents = storage
    if len(all_sents[-1].strip()) < 2:
        all_sents.pop(-1)
    # # delete headline flags
    # all_sents = [i.strip("#|*") for i in all_sents if i != "#|*"]
    return all_sents



def tag_word_nrmailweb(myword):
    """finds numbers, roman numbers, emails, webadresses
    returns Token.token .pos .lemma
    """
    regex_email = r'^[\w.!#$%&’*+/=?^_`{|}~-]+@\w+(?:\.\w+)*$'
    regex_web = r'^(http[s]?:\/\/|www.)'
    regex_rom = r'^M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$'
    # delete accents, lower all letters
    word = unidecode(myword.lower())
    if re.search(r"[0-9]+", word):
        tag = tc.Token(word, "NUM", word)
        return tag
    if re.search(regex_rom, word):
        tag = tc.Token(word, "NUM_ROM", word)
        return tag
    if re.search(regex_web, word):
        tag = tc.Token("address_in_web", "WWW", "address_in_web")
        return tag
    if word.find("@") > -1 and re.search(regex_email, word):
        tag = tc.Token("emailAtsomewhere", "EMAIL", "emailAtsomewhere")
        return tag
    return []


def tag_punctmarks_etc(myword):
    """finds symbols and marks
    returns Token.token .pos .lemma
    """
    # if myword in ",.;:!?(){}[]'\"" :
    #     tag = tc.Token(myword,myword,myword)
    #     return tag
    punctuation = sd.punctuation()
    if myword in punctuation:
        tag = tc.Token(myword, "SYMBOL", myword)
        return tag
    return []


def tag_lemma(myword, dict_known_types):
    """finds words in lemmafreq
    returns Token.token .pos .lemma
    """
    word = unidecode(myword).lower()
    word = re.sub(r"\s+", "", word)
    try:
        gotyou = itemgetter(word)(dict_known_types)
        tag = tc.Token(myword, gotyou[0], gotyou[1])
    except KeyError:
        tag = tc.Token(myword, "UNK", word)
    return tag


def prepare_lemmatypes(lemmafreq_known):
    """converts nested list of    lemmata[lemma, id, PoS, ..., types,]
                  into dictionary {type: [PoS, lemma, id]}
    """
    dict_known = {}
    for lemma in lemmafreq_known:
        for lemmatype in lemma[5:]:
            dict_known.update({lemmatype[0]: [lemma[2],
                                              lemma[0].replace(" ", "_"),
                                              lemma[1]]})
    return dict_known


def tag_text_with_db(mytext, dbrundi):
    """uses kirundi_db, makes lemma_freq_list of the text,
    returns a list of lists (lemmata sorted by PoS)
        and the tagged text with meta-data
    """
    collection = make_lemmafreq_fromtext(mytext, dbrundi)
    collection.put_known()
    lemmatypes = prepare_lemmatypes(collection.known)
    # Percentage of unkown types
    n_lemmatypes = 0
    for lemma in collection.known:
        n_lemmatypes += lemma[4]
    percent = round(len(collection.unk) / (len(collection.unk)+n_lemmatypes)
                    * 100, 2)
    kh.OBSERVER.notify(kh._(
        "unknown types      : {} ({}%)").format(len(collection.unk), percent))
    kh.OBSERVER.notify(kh._(
        "recognized lemmata : {}").format(len(collection.known)))
    # split into sentences -- roughly
    line_end = " #|* "
    sentences_list = split_in_sentences(mytext, line_end)
    punctuation = sd.punctuation()
    # punctuation = ',.;:!?(){}[]\'"´`#%&+-*/<=>@\\^°_|~'

    # collect whole text
    tagged = []
    nr_sen = -1
    nr_token = -1
    nr_char = 0
    nr_para = 0
    if len(sentences_list) > 50:
        points = int(len(sentences_list)/50)
    else:
        points = 1
    sent_count = 0
    kh.OBSERVER.notify(
        kh._("\ntagging text, this may take some moments ........."))
    for sentence in sentences_list:
        nr_sen += 1
        words = sentence.split()
        nr_word_in_sen = -1
        # collect sentence
        for word in words:
            if word == line_end.strip():
                nr_para += 1
                nr_sen += 1
                nr_word_in_sen = -1
                continue
            nr_word_in_sen += 1
            nr_token += 1
            # check for emails, webaddress, number, roman number
            # returns for email and webaddress alias
            tag1 = tag_word_nrmailweb(word)
            if tag1:
                tag1.set_nrs(nr_sen, nr_word_in_sen, nr_token, nr_char,
                             nr_para)
                tagged.append(tag1)
                nr_char += len(tag1.token)+1
                continue
            # now we split types by punctuation (w'umuryango.)
            wordwithoutsign = word.replace("'", " ' ")
            for p_mark in punctuation:
                storage = wordwithoutsign.replace(p_mark, f" {p_mark} ")
                wordwithoutsign = storage
            word_or_char = wordwithoutsign.split()
            # word or single character ?
            for w_or_c in word_or_char:
                # check for punctuation
                tag2 = tag_punctmarks_etc(w_or_c)
                if tag2:
                    tag2.set_nrs(nr_sen, nr_word_in_sen, nr_token, nr_char,
                                 nr_para)
                    tagged.append(tag2)
                    # TO DO nr_char is not correct because
                    # we don't know if with whitespace or not
                    nr_char += len(tag2.token)
                else:
                    # check for lemma
                    tag3 = tag_lemma(w_or_c, lemmatypes)
                    tag3.set_nrs(nr_sen, nr_word_in_sen, nr_token, nr_char,
                                 nr_para)
                    tagged.append(tag3)
                    nr_char += len(tag3.token)+1
        # progress bar ;-)
        if sent_count % points == 0:
            kh.OBSERVER.notify_cont('.')
        sent_count += 1
        text_tagged = tc.TokenMeta(tagged)
        text_tagged.percent_unk = percent
    return (collection,
            text_tagged)


# could be a function of a class wordlist_tagged?
def collect_words_around_searchterm(
        index_start, found_string, wordlist_tagged):
    """puts searchresult in it's context
    """
    # collect words around searchword
    index_end = index_start+len(found_string.split())
    text_around = 4*" "+found_string+8*" "
    neighbours = 0
    char_count = 0
    # words behind searchterm
    while char_count < 50 and index_end + neighbours < len(wordlist_tagged):
        neighbor_text = wordlist_tagged[index_end + neighbours].token+" "
        text_around += neighbor_text
        char_count += len(neighbor_text)
        neighbours += 1
    neighbours = -1
    char_count = 0
    # words before searchterm
    while char_count < 50 and index_start+neighbours > 0:
        neighbor_text = wordlist_tagged[index_start+neighbours].token+" "
        text_around = neighbor_text+text_around
        char_count += len(neighbor_text)
        neighbours -= 1
    # cut or fill space before searchterm
    if char_count >= 50:
        text_around = (5-len(str(index_start)))*" "\
                        + text_around[char_count-50:]
    else:
        text_around = (5-len(str(index_start)))*" "\
                        + (50-char_count)*" "+text_around
    return text_around


# could be a function of a class wordlist_tagged?
def find_thing(wordlist_tagged, wtl, questions):
    """searches a wordform
    or all wordforms of a lemma
    or a tag
    returns all matches with text around the search result
    """
    found = []
    missings = []
    searchword = questions[0]
    # we need the index because we want to find also the neighbour words
    for index, tagword in enumerate(wordlist_tagged):
        # tag missing?
        if not tagword.pos:
            missings.append(
                ("missing tag by word number:", index, tagword.token)
                )
            continue
        if searchword.lower() == tagword.get(wtl).lower():
            with_neighbors = collect_words_around_searchterm(
                index, tagword.token, wordlist_tagged)
            found.append((index, with_neighbors))
    return found, missings


def find_ngrams(wordlist_tagged, wtl, nots, questions):
    """finds combinations of n words
    wordforms(w), tags(t), lexems(l) or jokerword(?)
    returns all matches with text around the search result
    """
    missings = []
    ngram_length = len(questions)
    found = []             # collection of found strings
    part_found = ""        # found string
    n_count = 0            # index suchbegriff
    for index in range(len(wordlist_tagged)-ngram_length):
        # tag missing?
        if not wordlist_tagged[index].pos:
            missings.append(("missing tag by word number:",
                             index, wordlist_tagged[index].token))
            continue
        # found start of match
        # (we have to lower both: beginnings of sentences and tags)
        if wordlist_tagged[index].get(wtl[n_count]).lower() == questions[0].lower():
            part_found = wordlist_tagged[index].token
            n_count = 1
            # collect matches till full-match or mismatch of next token
            for candidate in wordlist_tagged[index+1:]:
                # add punctuation to found string but don't count it
                if candidate.pos == "SYMBOL":
                    part_found += " " + candidate.token
                    continue
                # next token also matches
                if (nots[n_count] != "!"
                        and (wtl[n_count] == "?"
                             or candidate.get(wtl[n_count]).lower() ==
                             questions[n_count].lower())) \
                    or (nots[n_count] == "!"
                        and candidate.get(wtl[n_count]).lower() !=
                        questions[n_count].lower()):

                    # add token and count it
                    part_found += " " + candidate.token
                    n_count += 1
                    # full match
                    if n_count == ngram_length:
                        with_neighbors = collect_words_around_searchterm(
                                            index, part_found, wordlist_tagged)
                        found.append([index, with_neighbors])
                        part_found = ""
                        n_count = 0
                        break
                # next token doesn't match
                else:
                    part_found = ""
                    n_count = 0
                    break
    return found, missings


def go_search(tagged_list, whattodo):
    """search in single text
    """
    if len(whattodo.wtl) == 1:
        found = find_thing(
            tagged_list, whattodo.wtl[0], whattodo.questions)
    else:
        found = find_ngrams(
            tagged_list, whattodo.wtl, whattodo.nots, whattodo.questions)
    if found:
        # tag missing?
        if found[1]:
            kh.OBSERVER.notify(kh._("Error: missing tag"))
            for i in found[1]:
                kh.OBSERVER.notify(i)
        return found[0]
    return found


def tag_multogether(fn_in, dbrundi):
    """tag all MasakhaNews in one json
    """
    bbc_toomuch = kh.load_meta_file(fn_in)
    raw = ""
    for i in bbc_toomuch:
        raw += i[5] + "\n" + i[6] + "\n\n"
    whattext = tc.TextMeta("bbcall.txt")
    whattext.setfnbbc()
    whattext.raw = raw
    whattext.replace_strangeletters(whattext.raw)
    lemma_lists, text_tagged = tag_text_with_db(whattext.text, dbrundi)
    lemmafreq = lemma_lists.all_in()
    # prepare data for csv
    lemmafreq.insert(0, sd.column_names_lemmafreq(), )
    kh.save_list(lemmafreq, whattext.fn_freqlemma)
    kh.OBSERVER.notify_frequencies(whattext.fn_in,
                                   whattext.fn_freqlemma.split("/")[-1],
                                   kh.Dates.database)
    # prepare data for json
    meta_data = {"n_char": whattext.nchars,
                 "n_odds": whattext.nodds,
                 "n_tokens": text_tagged.n_tokensbond,
                 "n_tokens_split": text_tagged.n_tokenscut,
                 "n_types": text_tagged.n_types,
                 "n_unk_types": str(text_tagged.percent_unk)+" %",
                 "n_lemmata": len(lemma_lists.known())
                 }
    jtokens = [dict(x.__dict__) for x in text_tagged.tokens]
    kh.save_json({"meta_data": meta_data,
                  "Token": jtokens
                  }, whattext.fn_tag)
    kh.OBSERVER.notify_tagging(whattext.fn_in,
                               whattext.fn_tag.split("/")[-1],
                               kh.Dates.database)
    kh.OBSERVER.notify(
          kh._("\n\nAll tagged files saved in: \n")
          + "\t/" + "/".join(whattext.fn_tag.split("/")[-5:-1])+"/tag__bbcall.json"
          + kh._("\nWe can use them again later."))


def tag_multiple(fn_in, dbrundi):
    """tag all single texts in MasakhaNews
    save them all in a special folder"""
    bbc_toomuch = kh.load_meta_file(fn_in)
    kh.OBSERVER.notify(kh._("Wir wühlen uns durch die Dateien..."))
    #points = len(bbc_toomuch)/50+1
    points = 1
    file_count = 0
    # allallall = []
    for i in bbc_toomuch:
        whattext = tc.TextMeta(i[1])
        whattext.setfnbbc()
        whattext.raw += i[5] + "\n" + i[6] + "\n"
        whattext.replace_strangeletters(whattext.raw)
        lemma_lists, text_tagged = tag_text_with_db(whattext.text, dbrundi)
        # allallall.append((whattext, lemma_lists, text_tagged))
        file_count += 1
        # kh.OBSERVER.notify_yes("'\r{} %".format(file_count/len(bbc_toomuch)*100))
        if file_count % points == 0:
            kh.OBSERVER.notify_cont('.')
#     # save_multiple(allallall)

# def save_multiple(allallall):
#     print("und nun sichern")
#     points = 1
#     file_count = 0
#     for i in allallall:
#         # prepare data for csv
#         whattext = i[0]
#         lemma_lists = i[1]
#         text_tagged = i[2]
        lemmafreq = lemma_lists.all_in()
        # prepare data for csv
        lemmafreq.insert(0, sd.column_names_lemmafreq(), )
        kh.save_list(lemmafreq, whattext.fn_freqlemma)
        kh.OBSERVER.notify_frequencies(whattext.fn_in,
                                       whattext.fn_freqlemma.split("/")[-1],
                                       kh.Dates.database)
        # prepare data for json
        meta_data = {"n_char": whattext.nchars,
                     "n_odds": whattext.nodds,
                     "n_tokens": text_tagged.n_tokensbond,
                     "n_tokens_split": text_tagged.n_tokenscut,
                     "n_types": text_tagged.n_types,
                     "n_unk_types": str(text_tagged.percent_unk)+" %",
                     "n_lemmata": len(lemma_lists.known())
                     }
        jtokens = [dict(x.__dict__) for x in text_tagged.tokens]
        kh.save_json({"meta_data": meta_data,
                      "Token": jtokens
                      }, whattext.fn_tag)
        kh.OBSERVER.notify_tagging(whattext.fn_in,
                                   whattext.fn_tag.split("/")[-1],
                                   kh.Dates.database)
        # file_count += 1
        # # kh.OBSERVER.notify("'\r{} %".format(file_count/len(bbc_toomuch)*100))
        # if file_count % points == 0:
        #     kh.OBSERVER.notify_yescont('.')
    kh.OBSERVER.notify(
          kh._("\n\nAll tagged files saved in: \n")
          + "\t/" + "/".join(whattext.fn_tag.split("/")[-5:-1])+"/tag__...json"
          + kh._("\nWe can use them again later.")
          )


def show_meta(fromjson):
    """print meta data of tagged text"""
    meta_data = fromjson.get("meta_data")
    kh.OBSERVER.notify(
        kh._("""\nStatistics
characters               {char}\t(broken char from bad OCR: {odds})
tokens                   {tokensbond}
tokens (split by \')      {tokens_split}
types                    {types}
recognized lemmata       {lemmata}
unknown types            {unk}""").
        format(char=meta_data.get("n_char"),
               odds=meta_data.get("n_odds"),
               tokensbond=meta_data.get("n_tokens"),
               tokens_split=meta_data.get("n_tokens_split"),
               types=meta_data.get("n_types"),
               lemmata=meta_data.get("n_lemmata"),
               unk=meta_data.get("n_unk_types")
               ))


def tag_or_load_tags(fn_in, dbrundi):
    """save energy, don't tag twice
    """
    whattext = tc.TextMeta(fn_in)
    kh.OBSERVER.notify(kh._("Preparing file ..."))
    # 1. maybe the given file itself is a json file? >> already tagged >> read
    if whattext.fn_in[-5:] == ".json":
        try:
            fromjson = load_json(whattext.fn_in)
        except:
            kh.OBSERVER.notify(
                kh._("Are you sure, that this is a tagged file?"))
        text_tagged = tc.TokenMeta(fromjson.get("TokenList"))
        show_meta(fromjson)
        return text_tagged
            # TODO get new data
    # 2. has the given txt a tagged json variant already?
    # TODO check hash values
    if kh.check_file_exits(sd.ResourceNames.dir_tagged
                           + whattext.fn_tag.split("/")[-1]):
        # check if tagged version is younger than big lemma collection
        good_old = kh.check_time(
            sd.ResourceNames.root+"/resources/freq_fett.csv",
            whattext.fn_tag)
        if good_old:
            kh.OBSERVER.notify(
                kh._("There is already a tagged file: (made {})").format(good_old)
                + "\n\t" + '/'.join(whattext.fn_tag.split('/')[-4:])
                + kh._("\nWe use this instead of tagging again.\n"))
            fromjson = load_json(whattext.fn_in)
            text_tagged = tc.TokenMeta(fromjson.get("TokenList"))
            show_meta(fromjson)
            return text_tagged

    # 3. read raw txt utf8 or utf16
    else:
        try:
            whattext.raw = kh.load_text_fromfile(whattext.fn_in, 'utf-8')
        except:
            try:
                whattext.raw = kh.load_text_fromfile(whattext.fn_in, 'utf-16')
            except:
                kh.OBSERVER.notify(
                    kh._("Sorry, can't use the file: {}").format(whattext.fn_in))
                whattext.raw = ""
        if not whattext.raw:
            sysexit()
    whattext.replace_strangeletters(whattext.raw)
    # start whole NLP task: read, clean, tag...
    # freq_lemma_all = kh.load_freqfett()
    lemma_lists, text_tagged = tag_text_with_db(whattext.text, dbrundi)
    lemmafreq = lemma_lists.all_in()

    # prepare data for csv file
    lemmafreq.insert(0, sd.column_names_lemmafreq(), )
    kh.save_list(lemmafreq, whattext.fn_freqlemma)
    kh.OBSERVER.notify_frequencies(whattext.fn_in.split("/")[-1],
                                   whattext.fn_freqlemma.split("/")[-1],
                                   kh.Dates.database)
    # prepare data for json
    meta_data = {"n_char": whattext.nchars,
                 "n_odds": whattext.nodds,
                 "n_tokens": text_tagged.n_tokensbond,
                 "n_tokens_split": text_tagged.n_tokenscut,
                 "n_types": text_tagged.n_types,
                 "n_unk_types": str(text_tagged.percent_unk)+" %",
                 "n_lemmata": len(lemma_lists.known)
                 }
    jtokens = [dict(x.__dict__) for x in text_tagged.tokens]
    kh.save_json({"meta_data": meta_data,
                  "Token": jtokens
                  }, whattext.fn_tag)
    kh.OBSERVER.notify_tagging(whattext.fn_in.split("/")[-1],
                               whattext.fn_tag.split("/")[-1],
                               kh.Dates.database)
    kh.OBSERVER.notify(
          kh._("\n\nTagged file saved as: \n")
          + "\t/" + "/".join(whattext.fn_tag.split("/")[-4:])
          + kh._("\nWe can use it again later.")
          )
    return text_tagged


def search_or_load_search(f_in, wtl, nots, quterms, single, tagged):
    """main
    """
    whattodo = sd.Search(f_in, wtl, nots, quterms)
    # check if search was already done before
    already_done = kh.check_file_exits(sd.ResourceNames.dir_searched
                                       + whattodo.fn_search.split("/")[-1])
    if already_done:
        result = kh.load_lines(whattodo.fn_search)
        kh.OBSERVER.notify(kh._("You searched this already"))
    else:
        # TODO
        if single is False:
            pass
            # # already tagged files of the corpus
            # tagged_meta = kh.load_meta_file(
            #     sd.ResourceNames.root+"/depot_analyse/meta_tags_for_training.txt")
            # result = []
            # count_results = 0  #? hierhin?
            # print(tagged_meta[0][:10])
            # for tags in tagged_meta:
            #     result1 = go_search(tags, whattodo)
            #     if result1:
            #         count_results += len(result1)
            #         result.append(f"***** {tags[0]} || {tags[1]} ||" +
            #                       "{tags[3]} || {len(result1))} || *****")
            #         for res in result1:
            #             result.append(res)
            # # headline
            # if result:
            #     result.insert(0, "file_id || characters || path || results counted || results")
        else:
            # searches in the tagged file
            result = go_search(tagged, whattodo)
    if result:
        kh.OBSERVER.notify(
            kh._("\nHit 1-20 (out of {}). All results are saved in file:")
            .format(len(result))
            + "\n\t"
            + f'/{"/".join(whattodo.fn_search.split("/")[-3:])}\n')
        kh.show_twenty(result)
        # save results as txt
        if not already_done:
            kh.save_list(result, whattodo.fn_search)
    else:
        kh.OBSERVER.notify(kh._("\nNo results for this query."))


# this function has to be in this module
# because module kh can't import module tc
def load_json(filename):
    """read json-file with meta data and tagged text
    return nested dict
    """
    with open(filename, encoding='utf-8') as file:
        raw = json.load(file)
    data = {}
    for num in range(len(list(raw.keys()))):
        class_name = list(raw.keys())[num]
        objects = []
        # tagged text as list of objects Token
        if class_name == "Token":
            for i in raw.get(class_name):
                tag = tc.Token(i.get('token'), i.get('pos'), i.get('lemma'))
                tag.set_nrs(i.get('id_sentence'), i.get('id_tokin_sen'),
                            i.get('id_token'), i.get('id_char'),
                            i.get('id_para'))
                objects.append(tag)
            data.update({"TokenList": objects})
        # meta data as dict
        if class_name == "meta_data":
            meta_data = raw.get(class_name)
            data.update({"meta_data": meta_data})
    return data
