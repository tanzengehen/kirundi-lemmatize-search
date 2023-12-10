#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 20 15:32:20 2023

@author: doreen nixdorf
"""


import re
import datetime
from ast import literal_eval
from operator import itemgetter
from sys import exit as sysexit
from unidecode import unidecode


try:
    import kir_helper2 as kh
    import kir_tag_classes as tc
    import kir_string_depot as sd
except ImportError:
    from ..lemmatize_search import kir_helper2 as kh
    from ..lemmatize_search import kir_tag_classes as tc
    from ..lemmatize_search import kir_string_depot as sd


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

    collection = tc.Collection(simple_freq_list)
    # Translators: fill points up to 50 letters
    kh.OBSERVER.notify(
        kh._("sorting Named Entities ..........................."))
    # names
    unk_before = len(collection.unk)
    collection.collect_names(names)
    unk_still = len(collection.unk)
    kh.OBSERVER.notify(
        kh._("\nNamed Entities      : ")
        + f"{unk_before-unk_still:16}\t\t({unk_still})")
    # adverbs
    unk_before = len(collection.unk)
    collection.collect_adverbs(dict_adv)
    unk_still = len(collection.unk)
    kh.OBSERVER.notify(
        kh._("adverbs etc         : ")
        + f"{unk_before-unk_still:7} >> "
        + f"{len(collection.advs):5}\t\t({unk_still})")
    # pronouns
    unk_before = len(collection.unk)
    collection.collect_pronouns(dict_prns)
    unk_still = len(collection.unk)
    kh.OBSERVER.notify(
        kh._("pronouns            : ")
        + f"{unk_before - unk_still:7} >> "
        f"{len(collection.pronouns):5}\t\t({unk_still})")
    # nouns part1
    # Translators: fill points up to 50 letters
    kh.OBSERVER.notify(
        kh._("sorting nouns ...................................."))
    unk_before = len(collection.unk)
    collection.collect_nouns(dict_nouns1)
    unk_still = len(collection.unk)
    kh.OBSERVER.notify(
        kh._("\nnouns               : ")
        + f"{unk_before - unk_still:7} >> "
        + f"{len(collection.nouns):5}\t\t({unk_still})")
    # adjectives
    unk_before = len(collection.unk)
    collection.collect_adjectives(dict_adj)
    unk_still = len(collection.unk)
    kh.OBSERVER.notify(
        kh._("adjektives          : ")
        + f"{unk_before - unk_still:7} >> "
        + f"{len(collection.adjs):5}\t\t({unk_still})")
    # verbs
    kh.OBSERVER.notify(
        kh._("sorting verbs ...................................."))
    unk_before = len(collection.unk)
    collection.collect_verbs(dict_verbs)
    unk_still = len(collection.unk)
    kh.OBSERVER.notify(
        kh._("\nverbs               : ")
        + f"{unk_before - unk_still:7} >> "
        + f"{len(collection.verbs):5}\t\t({unk_still})")
    # nouns part2: the nouns we skipped before verbs (uku...)
    unk_before = len(collection.unk)
    collection.collect_nouns(dict_nouns2)
    # exclamations
    collection.collect_exclamations(dict_rests)
    unk_still = len(collection.unk)
    kh.OBSERVER.notify(
        kh._("\nexclamations        : ")
        + " "*9 + f"{unk_before - unk_still:7}"
        + "\nunknown             :" + " "*23 + f"{unk_still}")
    # for key, value in collection.unk.items():
    #     if value != 0:
    #         collection.unk.append((key, "", "UNK", value, 1, [key, value]))
    unk = [(key, "", "UNK", value, 1, [key, value]) for key, value in collection.unk.items()]
    unk.sort(key=lambda x: x[3], reverse=True)
    collection.unk = unk
    return collection


def make_lemmafreq_fromtext(mytext, data):
    """takes utf-text, maps to lemmata in db_kirundi,
    returns lemma_freq"""
    simfreq = tc.FreqSimple(mytext)
    lemma_collection = reduce_simplefreq_to_lemma_collection(simfreq.freq,
                                                             data)
    kh.OBSERVER.notify(kh._("""\nVocabulary
characters         : {nchar:12}
tokens             : {ntokens:12}
types              : {ntypes:12} """).format(nchar=len(mytext),
                                             ntokens=simfreq.ntokens,
                                             ntypes=simfreq.ntypes))
    return lemma_collection


def split_in_sentences(mytext, paragraph=" <prgrph> "):
    """splits texts where [?.!;:] + space_character
    it's only a rough approach
    returns list with strings
    """
    # set a headlines and paragraph flag: "<paragraph>"
    mytextn = mytext.replace("\\n", paragraph)
    all_sents = [mytextn, ]
    # to get a list, not a nested list
    for seperator in ["...", ".", "?", "!", ":", ";"]:
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
    # all_sents = [i.strip("<prgrph>") for i in all_sents if i != <prgrph>"]
    return all_sents


def tag_word_nrmailweb(myword):
    """finds numbers, roman numbers, emails, webadresses
    returns Token.token .pos .lemma
    """
    regex_email = r'^[\w.!#$%&’*+/=?^_`{|}~-]+@\w+(?:\.\w+)*$'
    regex_web = r'^(http[s]?:\/\/|www.)'
    # regex_rom = r'^M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$'
    regex_rom = r'^m{0,3}(cm|cd|d?c{0,3})(xc|xl|l?x{0,3})(ix|iv|v?i{0,3})$'
    # delete accents, lower all letters
    word = unidecode(myword.lower())
    if re.search(r"[0-9]+", word):
        tag = tc.Token(word, "NUM", word)
        return tag
    if re.search(regex_rom, word):
        tag = tc.Token(word, "NUM_ROM", myword)
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
    # ,.;:!?(){}[]\'"´`#%&+-*/<=>@\\^°_|~
    punctuation = sd.punctuation()
    if myword == '"':
        # we give quotation-mark a name, because it's textmarker in csv-file
        tag = tc.Token("quotation", "SYMBOL", "quotation")
        return tag
    if myword == ";":
        # we give semikolon a name, because it's the separator in csv-file
        tag = tc.Token("semikolon", "SYMBOL", "semikolon")
        return tag
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
    # collect types of text and map them to lemmata
    collection = make_lemmafreq_fromtext(mytext, dbrundi)
    collection.put_known()
    lemmatypes = prepare_lemmatypes(collection.known)

    # print more statistics: Percentage of unkown types
    n_lemmatypes = 0
    for lemma in collection.known:
        n_lemmatypes += lemma[4]
    percent = round(len(collection.unk) / (len(collection.unk)+n_lemmatypes)
                    * 100, 2)
    kh.OBSERVER.notify(kh._(
        "unknown types      : {:12} ({}% incl. broken words, mistakes, ...)")
        .format(len(collection.unk), percent)
        )
    kh.OBSERVER.notify(kh._(
        "recognized lemmata : {:12}").format(len(collection.known)))

    # split text into sentences -- roughly
    line_end = " <paragraph> "
    sentences_list = split_in_sentences(mytext, line_end)
    punctuation = sd.punctuation()
    # punctuation = ',.;:!?(){}[]\'"´`#%&+-*/<=>@\\^°_|~'

    # tag tokens in text with lemma, PoS and position
    tagged = []
    nr_sen = -1
    nr_token = -1
    nr_char = 0
    nr_para = 0
    points = 0
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
        points, sent_count = kh.show_progress(points,
                                              sent_count,
                                              len(sentences_list))
        text_tagged = tc.TokenMeta(tagged)
        text_tagged.percent_unk = percent
    return (collection,
            text_tagged)


def replace_worded_symbols_back(neighbour_word):
    """replace worded symbols back to symbols"""
    if neighbour_word in sd.replaced_symbols.keys():
        return sd.replaced_symbols.get(neighbour_word)
    return neighbour_word


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
        neighbour_word = wordlist_tagged[index_end + neighbours].token
        neighbour_word = replace_worded_symbols_back(neighbour_word)
        text_around += neighbour_word+" "
        char_count += len(neighbour_word)+1
        neighbours += 1
    neighbours = -1
    char_count = 0
    # words before searchterm
    while char_count < 50 and index_start+neighbours > 0:
        neighbour_word = wordlist_tagged[index_start + neighbours].token
        neighbour_word = replace_worded_symbols_back(neighbour_word)
        text_around = neighbour_word + " " + text_around
        char_count += len(neighbour_word)+1
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
def find_thing(wordlist_tagged, wtl, question):
    """searches a wordform
    or all wordforms of a lemma
    or a tag
    returns all matches with text around the search result
    """
    found = []
    missings = []
    searchword = question
    # we need the index because we want to find also the neighbour words
    for index, tagword in enumerate(wordlist_tagged):
        # tag missing?
        if not tagword.pos:
            for i in range(index-3, index+3):
                print("missing tag", i, wordlist_tagged[i])
            missings.append(
                ("missing tag by word number:", index, tagword.token)
                )
            continue
        if searchword.lower() == tagword.get(wtl).lower():
            with_neighbors = collect_words_around_searchterm(
                index, tagword.token, wordlist_tagged)
            found.append((index, with_neighbors))
    return found, missings


def set_query_part(query, n):
    """update question for next token in text"""
    yesno = query[n][0]
    wtl = query[n][1]
    searchword = query[n][2]
    return yesno, wtl, searchword


def find_ngrams(wordlist_tagged, query):
    """finds combinations of n words
    wordforms(w), tags(t), lexems(l) or jokerword(?)
    returns all matches and text around the search result
    """
    missings = []
    ngram_length = len(query)
    found = []             # collection of found strings
    part_found = ""        # found string
    n_count = 0            # index suchbegriff
    for index in range(len(wordlist_tagged)-ngram_length):
        yesno, wtl, searchword = set_query_part(query, n_count)
        # tag missing?
        if not wordlist_tagged[index].pos:
            missings.append(("missing tag by word number:",
                             index, wordlist_tagged[index].token))
            continue
        # found start of match
        # (we have to lower both: beginnings of sentences and tags)
        if wordlist_tagged[index].get(wtl).lower() == searchword.lower():
            part_found = wordlist_tagged[index].token
            n_count = 1
            yesno, wtl, searchword = set_query_part(query, n_count)
            # collect matches till full-match or mismatch of next token
            for candidate in wordlist_tagged[index+1:]:
                # add punctuation to found string but don't count it
                if candidate.pos == "SYMBOL":
                    if candidate.token == "semikolon":
                        part_found += " " + ";"
                    elif candidate.token == "quotation":
                        part_found += ' ' + '"'
                    elif candidate.token == "deg":
                        part_found += ' ' + '°'
                    else:
                        part_found += " " + candidate.token
                    continue
                # next token also matches
                if (yesno != "!"
                        and (wtl == "?"
                             or candidate.get(wtl).lower() ==
                             searchword.lower())) \
                    or (yesno == "!"
                        and candidate.get(wtl).lower() !=
                        searchword.lower()):

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
                    yesno, wtl, searchword = set_query_part(query, n_count)
                # next token doesn't match
                else:
                    part_found = ""
                    n_count = 0
                    break
    return found, missings


def go_search(tagged_list, whattodo):
    """search in single text
    """
    if len(whattodo.query) == 1:
        found = find_thing(
            tagged_list, whattodo.query[0][1], whattodo.query[0][2])
    else:
        # found = find_ngrams(
        #     tagged_list, whattodo.wtl, whattodo.nots, whattodo.questions)
        found = find_ngrams(
            tagged_list, whattodo.query)
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
    whattext.replace_strangeletters()
    lemma_lists, text_tagged = tag_text_with_db(whattext.text, dbrundi)
    lemmafreq = lemma_lists.all_in()
    # prepare data for csv
    lemmafreq.insert(0, sd.column_names_lemmafreq(), )
    kh.save_list(lemmafreq, whattext.fn_freqlemma)
    kh.OBSERVER.notify_frequencies(whattext.fn_in,
                                   whattext.fn_freqlemma.split("/")[-1],
                                   kh.Dates.database)
    # prepare data for csv
    date = datetime.datetime.now()
    print("in multog", date, date.ctime(), str(date.ctime()))
    meta_data = {"n_char": whattext.nchars,
                 "n_odds": whattext.nodds,
                 "n_tokens": text_tagged.n_tokensbond,
                 "n_tokens_split": text_tagged.n_tokenscut,
                 "n_types": text_tagged.n_types,
                 "n_unk_types": str(text_tagged.percent_unk)+" %",
                 "n_lemmata": len(lemma_lists.known()),
                 "db_name": sd.ResourceNames.db_name,
                 "datetime": date.ctime()
                 }
    save_tagged_text_as_csv(meta_data, text_tagged.tokens, whattext.fn_tag)
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
        whattext.replace_strangeletters()
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
        # prepare data for csv
        meta_data = {"n_char": whattext.nchars,
                     "n_odds": whattext.nodds,
                     "n_tokens": text_tagged.n_tokensbond,
                     "n_tokens_split": text_tagged.n_tokenscut,
                     "n_types": text_tagged.n_types,
                     "n_unk_types": str(text_tagged.percent_unk)+" %",
                     "n_lemmata": len(lemma_lists.known())
                     }
        save_tagged_text_as_csv(meta_data, text_tagged.tokens, whattext.fn_tag)
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


def show_meta(meta_data):
    """print meta data of tagged text if tags are loaded from csv-file"""

    kh.OBSERVER.notify(
        kh._("""\nStatistics
characters               :{char:12}  ({odds} unreadable chars from bad OCR)
tokens                   :{tokensbond:12}
tokens (when split by \') :{tokens_split:12}
types                    :{types:12}
recognized lemmata       :{lemmata:12}
unknown types            :{unk:15} %
used dictionary          :   {db_name}""").
        format(char=meta_data.get("n_char"),
               odds=meta_data.get("n_odds"),
               tokensbond=meta_data.get("n_tokens"),
               tokens_split=meta_data.get("n_tokens_split"),
               types=meta_data.get("n_types"),
               lemmata=meta_data.get("n_lemmata"),
               unk=float(meta_data.get("n_unk_types").split()[0]),
               db_name=meta_data.get("db_name")
               ))


def tag_or_load_tags(fn_in, dbrundi):
    """save energy, don't tag twice
    """
    whattext = tc.TextMeta(fn_in)
    kh.OBSERVER.notify(kh._("Preparing file ..."))
    pathsep = sd.ResourceNames.sep

    # 1. given file itself is a csv file? >> already tagged >> read
    if whattext.fn_in[-4:] == ".csv":
        # check if given file is younger than the kirundi-database
        good_old = kh.check_time(sd.ResourceNames.fn_db, whattext.fn_in)
        if good_old:
            meta_data, token_list = load_tagged_text(whattext.fn_in)
            text_tagged = tc.TokenMeta(token_list)
            show_meta(meta_data)
            return text_tagged
        kh.OBSERVER.notify(
            kh._("""Your file is older than our version of the Rundi \
dictionary.
Do you want to use your file or tag again the underlying text?
(maybe now there are less unknown words in your text)"""))
        # TODO (input: y/n) till now: we chose the old file
        meta_data, token_list = load_tagged_text(whattext.fn_in)
        text_tagged = tc.TokenMeta(token_list)
        show_meta(meta_data)
        return text_tagged

    # 2. has the given txt-file a tagged csv variant already?
    # TODO check hash values
    if kh.check_file_exits(sd.ResourceNames.dir_tagged
                           + whattext.fn_tag.split(pathsep)[-1]):
        # check if tagged version of given file is younger
        #     than the kirundi-database
        good_old = kh.check_time(sd.ResourceNames.fn_db, whattext.fn_tag)
        if good_old:
            kh.OBSERVER.notify(
                kh._("There is already a tagged file: (made {})").format(good_old)
                + "\n\t" + pathsep.join(whattext.fn_tag.split(pathsep)[-4:])
                + kh._("\nWe use this instead of tagging again.\n"))
            meta_data, token_list = load_tagged_text(whattext.fn_tag)
            text_tagged = tc.TokenMeta(token_list)
            show_meta(meta_data)
            return text_tagged

    # 3. read raw txt utf8 or utf16 (there is no tagged version)
    else:
        try:
            whattext.raw = kh.load_text_fromfile(whattext.fn_in, 'utf-8')
        except UnicodeDecodeError:
            try:
                whattext.raw = kh.load_text_fromfile(whattext.fn_in, 'utf-16')
            except UnicodeDecodeError:
                kh.OBSERVER.notify(
                    kh._("Sorry, can't use the file: {}").format(whattext.fn_in))
                whattext.raw = ""
        if not whattext.raw:
            sysexit()
    whattext.replace_strangeletters()
    # print("in tag_or_load:", whattext.text)
    # start whole NLP task: read, clean, tag...
    lemma_lists, text_tagged = tag_text_with_db(whattext.text, dbrundi)
    lemmafreq = lemma_lists.all_in()

    # save lemma-frequency-distribution in csv file
    lemmafreq.insert(0, sd.column_names_lemmafreq(), )
    kh.save_list(lemmafreq, whattext.fn_freqlemma)
    kh.OBSERVER.notify_frequencies(whattext.fn_in.split(pathsep)[-1],
                                   whattext.fn_freqlemma.split(pathsep)[-1],
                                   kh.Dates.database)
    # save tagged text in csv
    date = datetime.datetime.now()
    meta_data = {"n_char": whattext.nchars,
                 "n_odds": whattext.nodds,
                 "n_tokens": text_tagged.n_tokensbond,
                 "n_tokens_split": text_tagged.n_tokenscut,
                 "n_types": text_tagged.n_types,
                 "n_unk_types": str(text_tagged.percent_unk)+" %",
                 "n_lemmata": len(lemma_lists.known),
                 "db_name": sd.ResourceNames.db_name,
                 "datetime": date.ctime()
                 }
    save_tagged_text_as_csv(meta_data, text_tagged.tokens, whattext.fn_tag)
    kh.OBSERVER.notify_tagging(whattext.fn_in.split(pathsep)[-1],
                               whattext.fn_tag.split(pathsep)[-1],
                               kh.Dates.database)
    kh.OBSERVER.notify(
          kh._("\n\nTagged file saved as: \n")
          + "\t"+pathsep + pathsep.join(whattext.fn_tag.split(pathsep)[-4:])
          + kh._("\nWe can use it again later.")
          )
    return text_tagged


def save_tagged_text_as_csv(meta, tagged_text, filename):
    """save tagged text in csv-file
    first line: meta-data
    second line: attribut-names for class Token
    from third line on: tokens of the tagged text
    """
    if filename.split(".")[-1] != "csv":
        filename = filename[: -len(filename.split(".")[-1])]+"csv"
    keys = list(tagged_text[0].__dict__.keys())
    keys = str(keys).replace(",", ";").replace("'", "")[1:-1]
    tags = ""
    for tagged_token in tagged_text:
        for value in tagged_token.__dict__.values():
            tags += str(value)+";"
        tags += "\n"
    with open(filename, 'w', encoding="utf-8") as file:
        file.write(str(meta)+"\n")
        file.write(keys+"\n")
        file.write(tags)


def search_or_load_search(f_in, quterms, single, tagged):
    """main
    """
    # whattodo = sd.Search(f_in, wtl, nots, quterms)
    whattodo = sd.Search(f_in, quterms)
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
def load_tagged_text(filename):
    """read csv-file with meta data and tagged text
    return nested dict
    """
    raw = kh.load_lines(filename)
    # check format of tagged-text-file
    # meta_data = literal_eval(raw[0])
    try:
        # first line should be a dictionary
        meta_data = literal_eval(raw[0])
    except (SyntaxError, TypeError, ValueError):
        kh.OBSERVER.notify(kh._("Sorry, missing meta-data in csv-file"))
        sysexit()
    # check if each Metadata-attribute finds a key in the dictionary
    try:
        for i in ['n_char', 'n_odds', 'n_tokens', 'n_tokens_split', 'n_types',
                  'n_unk_types', 'n_lemmata', 'db_name', 'datetime']:
            if i not in meta_data.keys():
                raise KeyError()
    except KeyError:
        kh.OBSERVER.notify(kh._("Sorry, wrong meta-data keys in your csv"))
        sysexit()
    # second line should be the column names for Token-attributes
    try:
        # map column-numbers to column-names
        column_keys = {key.strip(): i
                       for i, key in enumerate(raw[1].split(";"))
                       }
        # check if each Token-attribute finds a column-name
        for i in ['token', 'pos', 'lemma', 'id_sentence', 'id_tokin_sen',
                  'id_token', 'id_char', 'id_para']:
            if i not in column_keys.keys():
                raise KeyError()
    except KeyError:
        kh.OBSERVER.notify(kh._("Sorry, I can't read your csv-file as a \
tagged text."))
        sysexit()
    # make list of mapped Tokens
    tagged = []
    for token_line in raw[2:]:
        token_data = token_line.split(";")
        tag = tc.Token(token_data[column_keys.get('token')],
                       token_data[column_keys.get('pos')],
                       token_data[column_keys.get('lemma')])
        tag.set_nrs(token_data[column_keys.get('id_sentence')],
                    token_data[column_keys.get('id_tokin_sen')],
                    token_data[column_keys.get('id_token')],
                    token_data[column_keys.get('id_char')],
                    token_data[column_keys.get('id_para')])
        tagged.append(tag)
    return meta_data, tagged
