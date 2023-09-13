#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 20 15:32:20 2023

@author: doreen nixdorf
"""


import re
import json
from sys import exit as sysexit
from unidecode import unidecode
import kir_prepare_verbs as kv
import kir_helper2 as kh
import kir_tag_classes as tc
import kir_db_classes as dbc
import kir_string_depot as sd


def reduce_simplefreq_to_lemma_collection(simple_freq_list):
    """ mapps types to foreign words, named-entities and all PoS in kirundi_db
     reads simple_freq as list of [type,frequency]
     returns object of class Collection"""
    names = dbc.load_ne()
    kh.OBSERVER.notify(
        kh._("\nPreparing dictionary, just a moment ..."))
    (dict_verbs, dict_subs, dict_adj, dict_prns,
     dict_adv, dict_rests, dict_stems) = dbc.load_dbkirundi()
    # Translators: fill points up to 50 letters
    kh.OBSERVER.notify(
        kh._("sorting Named Entities ..........................."))
    collection = tc.Collection(simple_freq_list)
    (collection.names, still_unk) = dbc.filter_names_out(names,
                                                         simple_freq_list)
    len_before = len(still_unk)
    (collection.advs, still_unk) = dbc.collect_adv_plus(dict_adv, still_unk)
    kh.OBSERVER.notify(kh._("\nNamed Entities      : ")
                      + f"\t\t{len_before-len(still_unk)}\t({len(still_unk)})")
    len_before = len(still_unk)
    (collection.pronouns,
     still_unk) = dbc.collect_pronouns(dict_prns, still_unk)
    kh.OBSERVER.notify(kh._("adverbs etc         : ")
                       + f"{len_before-len(still_unk)} >> "
                       + f"{len(collection.advs)-1}\t({len(still_unk)})")
    # Translators: fill points up to 50 letters
    kh.OBSERVER.notify(
        kh._("sorting nouns ...................................."))
    len_before = len(still_unk)
    (collection.nouns,
     still_unk, subs_later) = dbc.collect_nouns(dict_subs, still_unk, True)
    kh.OBSERVER.notify(
        kh._("\npronouns            : ") + f"{len_before-len(still_unk)} >> "
        f"{len(collection.pronouns)-1}\t({len(still_unk)})")
    len_before = len(still_unk)
    (collection.adjs, still_unk) = dbc.collect_adjs(dict_adj, still_unk)
    kh.OBSERVER.notify(kh._("nouns               : ")
                       + f"{len_before-len(still_unk)} >> "
                       + f"{len(collection.nouns)-1}\t({len(still_unk)})")
    kh.OBSERVER.notify(
        kh._("sorting verbs ...................................."))
    len_before = len(still_unk)
    (collection.verbs, still_unk) = kv.sammle_verben(dict_verbs, still_unk)
    kh.OBSERVER.notify(kh._("\nadjektives          : ")
                       + f"{len_before-len(still_unk)} >> "
                       + f"{len(collection.adjs)-1}\t({len(still_unk)})")
    # now we search for the substantives we skipped before verbs (uku...)
    len_before = len(still_unk)
    (found_here,
     still_unk,
     doesntmatteranymore) = dbc.collect_nouns(subs_later, still_unk, False)
    collection.nouns += found_here
    kh.OBSERVER.notify(kh._("verbs               : ")
                       + f"{len_before-len(still_unk)} >> "
                       + f"{len(collection.verbs)-1}\t({len(still_unk)})")

    (collection.exclams,
     still_unk) = dbc.collect_exclamations(dict_rests, still_unk)
    # collection.unk=[]
    for key, value in still_unk.items():
        if value != 0:
            collection.unk.append((key, "", "UNK", value, 1, [key, value]))
    return collection


def make_lemmafreq_fromtext(mytext):
    """takes utf-text, maps to lemmata in db_kirundi,
    returns lemma_freq"""
    simfreq = tc.FreqSimple(mytext)
    lemma_collection = reduce_simplefreq_to_lemma_collection(simfreq.freq)
    # known = tc.Collection.known(lemma_collection)
    # return known, lemma_collection.unk
    return lemma_collection


def split_in_sentences(mytext):
    """splits texts where [?.!;:] + space_character
    that's only a rough approach
    returns list with strings
    """
    # set a headlines and paragraph flag: "#|*"
    mytextn = mytext.replace("\\n", " #|* ")
    all_sents = [mytextn, ]
    # to get a list, not a nested list
    for seperator in [".", "?", "!", ":", ";", "#|*"]:
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
    # delete headline flags
    all_sents = [i.strip("#|*") for i in all_sents if i != "#|*"]
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
    if myword in ',.;:!?(){}[]\'"´`#$%&*+-/<=>@\\^_|~':
        tag = tc.Token(myword, "SYMBOL", myword)
        return tag
    return []


def tag_lemma(myword, knownlemmafreq):
    """finds words in lemmafreq
    returns Token.token .pos .lemma
    """
    word = unidecode(myword).lower()
    word = re.sub(r"\s+", "", word)
    for entry in knownlemmafreq:
        # entry: [lemma, db-id, PoS, freq, nr of variants, [variants]]
        # lemmata with more than one word get an underline instead of spaces
        qu_entry = entry[0].replace(" ", "_")
        try:
            for variant in entry[5:]:
                if word == variant[0]:
                    tag = tc.Token(myword, entry[2], qu_entry)
                    return tag
        except:
            kh.OBSERVER.notify(f"{entry} {word} {variant}")
    tag = tc.Token(myword, "UNK", word)
    return tag


def tag_text_with_db(mytext):  # , lemmafreq_all) :
    """uses kirundi_db, makes lemma_freq_list of the text,
    (but tags with big_lemma_freq)
    returns lemma_freq, list of tagged tokens
    """
    collection = make_lemmafreq_fromtext(mytext)
    known = collection.known()
    # TODO where to put the metadata
    kh.OBSERVER.notify(kh._("\nlemmata of text: {}").format(len(known)))
    kh.OBSERVER.notify(kh._("unknown types  : {}").format(len(collection.unk)))
    # split into sentences -- roughly
    sentences_list = split_in_sentences(mytext)
    punctuation = sd.punctuation()
    # punctuation = r'´`\'.!"#$%&()*+,-/:<=>?[\\]^_{|}~;@'

    # collects whole text
    tagged = []
    nr_sen = -1
    nr_token = -1
    nr_char = 0
    if len(sentences_list) > 50:
        points = int(len(sentences_list)/50)
    else:
        points = 1
    sent_count = 0
    kh.OBSERVER.notify(
        kh._("\ntagging text, this may take some moments ........."))
    for sentence in sentences_list:
        nr_sen += 1
        # len_sen = len(sentence)
        words = sentence.split()
        # collects sentence
        nr_word_in_sen = -1
        for word in words:
            nr_word_in_sen += 1
            nr_token += 1
            # check for emails, webaddress, number, roman number
            # returns for email and webaddress alias
            tag1 = tag_word_nrmailweb(word)
            if tag1:
                tag1.set_nrs(nr_sen, nr_word_in_sen, nr_token, nr_char)
                tagged.append(tag1)
                nr_char += len(tag1.token)+1
                continue
            # now we seperate letters from other characters (w'umuryango)
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
                    tag2.set_nrs(nr_sen, nr_word_in_sen, nr_token, nr_char)
                    tagged.append(tag2)
                    # TO DO nr_char is not correct because
                    # we don't know if with whitespace or not
                    nr_char += len(tag2.token)
                else:
                    # check for lemma
                    # tag3 = tag_lemma(w_or_c,lemmafreq_all)
                    tag3 = tag_lemma(w_or_c, known)
                    tag3.set_nrs(nr_sen, nr_word_in_sen, nr_token, nr_char)
                    tagged.append(tag3)
                    nr_char += len(tag3.token)+1
        # progress bar ;-)
        if sent_count % points == 0:
            print('.', end="")
        sent_count += 1
    lemmafreq = collection.all_in()
    return (lemmafreq,
            tagged)


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


def tag_or_load_tags(whattodo):
    """save energy, don't tag twice
    """
    # 1. is there already a tagged json variant?
    # TODO check hash values
    if kh.check_file_exits(whattodo.fn_tag.split("/")[-1],
                           sd.ResourceNames.dir_tagged):
        # check if tagged version is younger than big lemma collection
        good_old = kh.check_time(
            sd.ResourceNames.root+"/resources/freq_fett.csv",
            whattodo.fn_tag)
        if good_old:
            kh.OBSERVER.notify(
                kh._("There is already a tagged file: (made {})").format(good_old)
                + "\n\t" + '/'.join(whattodo.fn_tag.split('/')[-4:])
                + kh._("\nWe use this instead of tagging again.\n"))
            text_tagged = load_json(whattodo.fn_tag)
            return text_tagged
    # 2. maybe the given file itself is a json file? >> already tagged >> read
    if whattodo.fn_in[-5:] == ".json":
        try:
            text_tagged = load_json(whattodo.fn_in)
            return text_tagged
        except:
            kh.OBSERVER.notify(
                kh._("Are you sure, that this is a tagged file?"))
            # TODO get new data
    # 3. read raw txt utf8 or utf16
    try:
        meta = kh.load_text_fromfile(whattodo.fn_in, 'utf-8')
        # raw = meta.raw
    except:
        try:
            meta = kh.load_text_fromfile(whattodo.fn_in, 'utf-16')
            # raw = meta.raw
        except:
            kh.OBSERVER.notify(
                kh._("Sorry, can't use the file: {}").format(whattodo.fn_in))
            meta = ""
    if not meta:
        sysexit
    # start whole NLP task: read, clean, tag...
    # freq_lemma_all = kh.load_freqfett()
    kh.OBSERVER.notify(kh._("Preparing file ..."))
    lemmafreq, text_tagged = tag_text_with_db(meta.text)  # ,freq_lemma_all)
    # insert first line as head for csv file
    lemmafreq.insert(0, sd.first_line_in_pos_collection(), )
    kh.save_list(lemmafreq, whattodo.fn_freqlemma)
    # remove first line again
    lemmafreq.pop(0)
    kh.OBSERVER.notify_frequencies(whattodo.fn_in.split("/")[-1],
                                   whattodo.fn_freqlemma.split("/")[-1],
                                   kh.Dates.database)
    # save tagged file for reuse
    kh.save_json(text_tagged, whattodo.fn_tag)
    kh.OBSERVER.notify_tagging(whattodo.fn_in.split("/")[-1],
                               whattodo.fn_tag.split("/")[-1],
                               kh.Dates.database)
    kh.OBSERVER.notify(
          kh._("\n\nTagged file saved as: \n")
          + "\t/" + "/".join(whattodo.fn_tag.split("/")[-4:])
          + kh._("\nWe can use it again later.")
          )
    return text_tagged


def search_or_load_search(f_in, wtl, nots, quterms, multiple):
    """main
    """
    whattodo = sd.Search(f_in, wtl, nots, quterms, multiple)
    # check if search was already done before
    already_done = kh.check_file_exits(whattodo.fn_search.split("/")[-1],
                                       sd.ResourceNames.dir_searched)
    if already_done:
        result = kh.load_lines(whattodo.fn_search)
        count_results = len(result)
    else:
        count_results = 0
        if multiple is True:
            # already tagged files of the corpus
            tagged_meta = kh.load_meta_file(
                sd.ResourceNames.root+"/depot_analyse/meta_tags_for_training.txt")
            result = []
            for tagged in tagged_meta:
                result1 = go_search(tagged, whattodo)
                if result1:
                    count_results += len(result1)
                    result.append(f"***** {tagged[0]} || {tagged[1]} ||" +
                                  "{tagged[3]} || {len(result1))} || *****")
                    for res in result1:
                        result.append(res)
            # headline
            if result:
                result.insert(0, "file_id || characters || path || results counted || results")
        else:
            # tags the file or takes an already tagged version of the file
            text_with_tags = tag_or_load_tags(whattodo)
            # searches in the tagged file
            result = go_search(text_with_tags, whattodo)
            count_results = len(result)
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


def load_json(filename):  # , klasse="Token"):
    """reads and maps json-file
    class name be written in file
    """
    with open(filename, encoding='utf-8') as file:
        raw = json.load(file)
    class_name = list(raw.keys())[0]
    objects = []
    if class_name == "Token":
        for i in raw.get(class_name):
            tag = tc.Token(i.get('token'), i.get('pos'), i.get('lemma'))
            tag.set_nrs(i.get('id_sentence'), i.get('id_tokin_sen'),
                        i.get('id_token'), i.get('id_char'))
            objects.append(tag)
    # TODO other classes: PreparedFile
    # elif klasse == "Corpus/Single" and class_name == klasse :
    #     for i in raw.get(class_name):
    #         text = Corpus(i.get('dbid'),i.get('lemma'),i.get('stem'),
    #                     i.get('perfective'),i.get('alternative'),
    #                     i.get('comb'),i.get('proverb'))
    #         objects.append(verb)
    else:
        kh.OBSERVER.notify(kh._("Sorry, unknown format."))
        return objects
    return objects
