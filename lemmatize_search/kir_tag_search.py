#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 20 15:32:20 2023

@author: doreen nixdorf
"""


import re
import datetime
from time import ctime
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
    kh.OBSERVER.notify_status(kh._("sorting Named Entities "))
    # names
    # unk_before = len(collection.unk)
    collection.collect_names(names)
    # unk_still = len(collection.unk)
    # kh.OBSERVER.notify(
    #     kh._("\nNamed Entities      : ")
    #     + f"{unk_before-unk_still:16}\t\t({unk_still})")
    # kh.OBSERVER.notify_report((kh._("Named Entities"), unk_before-unk_still))
    # adverbs
    # unk_before = len(collection.unk)
    collection.collect_adverbs(dict_adv)
    # unk_still = len(collection.unk)
    # kh.OBSERVER.notify(
    #     kh._("adverbs etc         : ")
    #     + f"{unk_before-unk_still:7} >> "
    #     + f"{len(collection.advs):5}\t\t({unk_still})")
    # kh.OBSERVER.notify_report((kh._("Adverbs etc"), len(collection.advs)))
    # pronouns
    # unk_before = len(collection.unk)
    collection.collect_pronouns(dict_prns)
    # unk_still = len(collection.unk)
    # kh.OBSERVER.notify_report((kh._("Pronouns"), len(collection.pronouns)))
    # nouns part1
    # Translators: fill points up to 50 letters
    kh.OBSERVER.notify_status(kh._("sorting nouns "))
    # unk_before = len(collection.unk)
    collection.collect_nouns(dict_nouns1)
    # unk_still = len(collection.unk)
    # kh.OBSERVER.notify_report((kh._("Nouns"), len(collection.nouns)))
    # adjectives
    # unk_before = len(collection.unk)
    collection.collect_adjectives(dict_adj)
    # unk_still = len(collection.unk)
    # kh.OBSERVER.notify_report((kh._("Adjektives"), len(collection.adjs)))
    # verbs
    kh.OBSERVER.notify_status(kh._("sorting verbs "))
    # unk_before = len(collection.unk)
    collection.collect_verbs(dict_verbs)
    # unk_still = len(collection.unk)
    # kh.OBSERVER.notify_report((kh._("Verbs"), len(collection.verbs)))
    # nouns part2: the nouns we skipped before verbs (uku...)
    # unk_before = len(collection.unk)
    collection.collect_nouns(dict_nouns2)
    # exclamations
    collection.collect_exclamations(dict_rests)
    # unk_still = len(collection.unk)
    # kh.OBSERVER.notify_report((kh._("Exclamations"), unk_before - unk_still))
    # kh.OBSERVER.notify_report((kh._("Unknown"), unk_still))
    # the rest is unknown
    unk = [(key, "", "UNK", value, 1, [key, value])
           for key, value in collection.unk.items()]
    unk.sort(key=lambda x: x[3], reverse=True)
    collection.unk = unk
    return collection


def make_lemmafreq_fromtext(mytext, dbrundi):
    """takes utf-text, maps to lemmata in db_kirundi,
    returns lemma_freq"""
    simfreq = tc.FreqSimple(mytext)
    lemma_collection = reduce_simplefreq_to_lemma_collection(simfreq.freq,
                                                             dbrundi)
    lemma_collection.put_known()

    table = []
    table.append((kh._("characters"), len(mytext)))
    table.append((kh._("tokens"), simfreq.ntokens))
    table.append((kh._("types"), simfreq.ntypes))
    table.append((kh._("lemmata"), len(lemma_collection.known)))
    kh.OBSERVER.notify_table(kh._("Vocabulary"), table, 2)

    table = []
    # table = [[attr, len(value)] for attr, value in lemma_collection.__dict__.items()]
    table.append((kh._("Adjectives"), len(lemma_collection.adjs)))
    table.append((kh._("Adverbs etc"), len(lemma_collection.advs)))
    table.append((kh._("Pronouns"), len(lemma_collection.pronouns)))
    table.append((kh._("Nouns"), len(lemma_collection.nouns)))
    table.append((kh._("Verbs"), len(lemma_collection.verbs)))
    table.append((kh._("Names"), len(lemma_collection.names)))
    table.append((kh._("unknown"), len(lemma_collection.unk)))
    kh.OBSERVER.notify_table(kh._("\nParts of Speech (lemma based)"), table, 2)

    unk_percent = round(len(lemma_collection.unk) / simfreq.ntypes * 100, 2)
    kh.OBSERVER.notify_add(
        kh._(f"{unk_percent} % broken words, mistakes, unknown types..."))
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


def check_position_in_text(text, word, position):
    """map word in wordlist to its position in cleaned text"""
    check_loops = 0
    if text[position:position+len(word)] != word:
        corr = -len(word)-1
        while (text[position+corr:position+corr+len(word)] != word
               and check_loops < 2*len(word)):
            check_loops += 1
            corr += 1
        position += corr
    return position


def tag_text_with_db(mytext, dbrundi):
    """uses kirundi_db, makes lemma_freq_list of the text,
    returns a list of lists (lemmata sorted by PoS)
        and the tagged text with meta-data
    """
    # collect types of text and map them to lemmata
    collection = make_lemmafreq_fromtext(mytext, dbrundi)
    lemmatypes = prepare_lemmatypes(collection.known)
    # print more statistics: Percentage of unkown types
    # n_known_types = 0
    # for lemma in collection.known:
    #     n_known_types += lemma[4]
    # percent = round(len(collection.unk) / (len(collection.unk)+n_known_types)
    #                 * 100, 2)
    # kh.OBSERVER.notify(kh._(
    #     "unknown types      : {:12} ({}% incl. broken words, mistakes, ...)")
    #     .format(len(collection.unk), percent)
    #     )
    # kh.OBSERVER.notify(kh._(
    #     "recognized lemmata : {:12}").format(len(collection.known)))

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
    kh.OBSERVER.notify_status(
        kh._("\ntagging text, this may take some moments"))
    for sentence in sentences_list:
        nr_sen += 1
        words = sentence.split()
        nr_word_in_sen = -1
        # collect sentence
        for word in words:
            # print("word", word)
            if word == line_end.strip():
                nr_para += 1
                nr_sen += 1
                nr_word_in_sen = -1
                continue
            nr_word_in_sen += 1
            nr_token += 1

            # check for emails, webaddress, number, roman number
            # returns for email and webaddress alias
            tag = tag_word_nrmailweb(word)
            if tag:
                nr_char = check_position_in_text(mytext, word, nr_char)
                tag.set_nrs(nr_sen, nr_word_in_sen, nr_token,
                            nr_char-nr_para, nr_para)
                tagged.append(tag)
                nr_char += len(tag.token)+1
                # print("next:", nr_char)
                continue

            # now we split types by punctuation
            # (w'umuryango. -> w ' umuryango . )
            wordwithoutsign = word.replace("'", " ' ")
            for p_mark in punctuation:
                storage = wordwithoutsign.replace(p_mark, f" {p_mark} ")
                wordwithoutsign = storage
            word_or_char = wordwithoutsign.split()
            # word or letter/punctuation ?
            for w_or_c in word_or_char:
                # check for punctuation
                tag = tag_punctmarks_etc(w_or_c)
                if not tag:
                    # check for lemma
                    tag = tag_lemma(w_or_c, lemmatypes)
                nr_char = check_position_in_text(mytext, w_or_c, nr_char)
                tag.set_nrs(nr_sen, nr_word_in_sen, nr_token,
                            nr_char-nr_para, nr_para)
                tagged.append(tag)
                nr_char += len(w_or_c)+1

        # progress bar
        points, sent_count = kh.show_progress(points,
                                              sent_count,
                                              len(sentences_list))
    text_tagged = tc.TokensMeta(tagged)
    text_tagged.count_tokens()
    # kh.OBSERVER.notify_report((kh._("unknown types"), text_tagged.n_unk))
    # kh.OBSERVER.notify_add(kh._(f"{text_tagged.percent_unk} % broken words, mistakes, unknown tokens..."))
    # kh.OBSERVER.notify_report((kh._("in tag- recognized lemmata"), len(collection.known)))
    # # TODO
    # print("\nin tag text vergleich n_lemma", text_tagged.n_lemmata, len(collection.known))
    # print("vergleich types", text_tagged.n_types, (len(collection.unk)+n_known_types))
    # print("vergleich unbekannt", text_tagged.n_unk, len(collection.unk))
    # print("vergleich prozente", text_tagged.percent_unk, percent)
    # text_tagged.n_lemmata = len(collection.known)
    # text_tagged.percent_unk = percent
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
        neighbour_word = wordlist_tagged[index_end + neighbours].token
        neighbour_word = sd.replace_worded_symbols_back(neighbour_word)
        text_around += neighbour_word+" "
        char_count += len(neighbour_word)+1
        neighbours += 1
    neighbours = -1
    char_count = 0
    # words before searchterm
    while char_count < 50 and index_start+neighbours > 0:
        neighbour_word = wordlist_tagged[index_start + neighbours].token
        neighbour_word = sd.replace_worded_symbols_back(neighbour_word)
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
def find_thing(wordlist_tagged, wtl, searchword):
    """searches a wordform
    or all wordforms of a lemma
    or a tag
    returns all matches with text around the search result
    """
    found = []
    missings = []
    # we need the index because we want to find also the neighbour words
    for index, tagword in enumerate(wordlist_tagged):
        # tag missing?
        if not tagword.pos:
            print("missing tag", index, tagword)
            missings.append(
                ("missing tag by word number:", index, tagword.token)
                )
        if unidecode(searchword.lower()) \
           == unidecode(tagword.get_wtl(wtl).lower()):
            token = sd.replace_worded_symbols_back(tagword.token)
            with_neighbors = collect_words_around_searchterm(
                index, token, wordlist_tagged
                )
            found.append((tagword.id_char, with_neighbors))
    return found, missings


def setquery_nextpart(query, n):
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
    n_count = 0            # index search term
    for index in range(len(wordlist_tagged)-ngram_length):
        yesno, wtl, searchword = setquery_nextpart(query, n_count)
        # tag missing?
        if not wordlist_tagged[index].pos:
            missings.append(("missing tag by word number:",
                             index, wordlist_tagged[index].token))
            continue
        # ignore symbols if not specially asked for
        if (wordlist_tagged[index].pos == "SYMBOL" and
           searchword != "SYMBOL"):
            continue
        # find start of match
        # 1. it is what it should be
        if ((yesno == "y"
             # (we have to lower both: beginnings of sentences and tags)
             and unidecode(wordlist_tagged[index].get_wtl(wtl).lower())
                == unidecode(searchword.lower())
             )
            # 2. or it's not what it shouldn't be
            or (yesno == "n"
                and unidecode(wordlist_tagged[index].get_wtl(wtl).lower())
                != unidecode(searchword.lower())
                )):
            part_found = wordlist_tagged[index].token
            sd.replace_worded_symbols_back(part_found)
            # check next tokens
            n_count = 1
            yesno, wtl, searchword = setquery_nextpart(query, n_count)
            # collect matches till full-match or mismatch of next token
            for candidate in wordlist_tagged[index+1:]:
                # check fpor symbols
                # and add them to found-string
                # but don't count it if not asked for
                if candidate.pos == "SYMBOL":
                    # check if asked for a single symbol or asked in general
                    # (but not '*')
                    if (searchword == "SYMBOL"
                       or searchword in ',.;:!?(){}[]\'"´`#%&+-/<=>@\\^°_|~'):
                        n_count += 1
                        # check if it is the full match already
                        if n_count == ngram_length:
                            with_neighbors = collect_words_around_searchterm(
                                                index,
                                                part_found,
                                                wordlist_tagged)
                            found.append([wordlist_tagged[index].id_char,
                                          with_neighbors])
                            part_found = ""
                            n_count = 0
                            break
                        yesno, wtl, searchword = setquery_nextpart(query, n_count)
                    part_found += " " + sd.replace_worded_symbols_back(candidate.token)
                    continue
                # check other tokens than symbols (matches)
                if (yesno == "y"
                       # wildcard or positive match
                    and (wtl == "?"
                             or candidate.get_wtl(wtl).lower() ==
                             searchword.lower())) \
                    or (yesno == "n"
                        and unidecode(candidate.get_wtl(wtl).lower()) !=
                        unidecode(searchword.lower())
                        ):
                    # add token and count it
                    part_found += " " + sd.replace_worded_symbols_back(candidate.token)
                    n_count += 1
                    # check if it is the full match already
                    if n_count == ngram_length:
                        with_neighbors = collect_words_around_searchterm(
                                            index, part_found, wordlist_tagged)
                        found.append([wordlist_tagged[index].id_char,
                                      with_neighbors])
                        part_found = ""
                        n_count = 0
                        break
                    yesno, wtl, searchword = setquery_nextpart(query, n_count)
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
        found = find_ngrams(
            tagged_list, whattodo.query)
    # tag missing?
    if found[1]:
        kh.OBSERVER.notify_error(kh._("Error: missing tag"))
        for i in found[1]:
            kh.OBSERVER.notify_error(i)
    return found[0]


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
    # print("in multog", date, date.ctime(), str(date.ctime()))
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
          kh._("\nAll tagged files saved in: \n")
          + "\t/" + "/".join(whattext.fn_tag.split("/")[-5:-1])
          + "/tag__bbcall.json")


def tag_multiple(fn_in, dbrundi):
    """tag all single texts in MasakhaNews
    save them all in a special folder"""
    bbc_toomuch = kh.load_meta_file(fn_in)
    kh.OBSERVER.notify_status(kh._("Wir wühlen uns durch die Dateien..."))
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
          + "\t/" + "/".join(whattext.fn_tag.split("/")[-5:-1])+"/tag__...csv")

def show_meta(meta_data):
    """print meta data of tagged text
    called when tags are loaded from csv-file"""
    table = []
    table.append((kh._("characters"),
                 f"{meta_data.get('n_char'):12}  ({meta_data.get('n_odds')}"
                  + kh._(" unreadable chars from bad OCR)")))
    table.append((kh._("tokens"),
                 f"{meta_data.get('n_tokens'):12}"))
    table.append((kh._("tokens (when split by \')"),
                 f"{meta_data.get('n_tokens_split'):12}"))
    table.append((kh._("types"),
                 f"{meta_data.get('n_types'):12}"))
    table.append((kh._("recognized lemmata"),
                 f"{meta_data.get('n_lemmata'):12}"))
    table.append((kh._("unknown types"),
                 f"{float(meta_data.get('n_unk_types').split()[0]):15} %"))
    table.append((kh._("used dictionary"),
                 f"   {meta_data.get('db_version')}"))
    table.append((kh._("short filename"),
                 f"   {meta_data.get('fn_short')}"))
    kh.OBSERVER.notify_table("\nStatistics", table, 2)


def tag_or_load_tags(fn_in, dbrundi):
    """save energy, don't tag twice
    """
    whattext = tc.TextMeta(fn_in)
    kh.OBSERVER.notify_status(kh._("Preparing file ..."))
    pathsep = sd.ResourceNames.sep

    # 1. is the given file itself a csv file? >> already tagged >> read
    if whattext.fn_in[-4:] == ".csv":
        # check if given file is younger than the kirundi-database
        good_old = kh.check_time(sd.ResourceNames.fn_db, whattext.fn_in)
        if good_old:
            meta_data, token_list = load_tagged_text(whattext.fn_in)
            text_tagged = tc.TokensMeta(token_list)
            text_tagged.put_meta_already_done_before(meta_data)
            show_meta(meta_data)
            # clear statusbar
            kh.OBSERVER.notify_status(kh._(" "))
            return text_tagged
        kh.OBSERVER.notify_ask(
            kh._("""Your file is older than our version of the Rundi \
dictionary.
Do you want to use your file or tag again the underlying text?
(maybe now there are less unknown words in your text)"""))
        # TODO (input: y/n) till now: we chose the old file
        meta_data, token_list = load_tagged_text(whattext.fn_in)
        text_tagged = tc.TokensMeta(token_list)
        text_tagged.put_meta_already_done_before(meta_data)
        show_meta(meta_data)
        # clear statusbar
        kh.OBSERVER.notify_status(kh._(" "))
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
                kh._(f"file tagged: {ctime(good_old)[4:-5]}"))
            kh.OBSERVER.notify(
                pathsep.join(whattext.fn_tag.split(pathsep)[-4:]))
            #     + kh._("\nWe use this instead of tagging again.\n"))
            meta_data, token_list = load_tagged_text(whattext.fn_tag)
            text_tagged = tc.TokensMeta(token_list)
            text_tagged.put_meta_already_done_before(meta_data)
            show_meta(meta_data)
            # clear statusbar
            kh.OBSERVER.notify_status(kh._(" "))
            return text_tagged

    # 3. read raw txt utf8 or utf16 (there is no tagged version)
    else:
        try:
            whattext.raw = kh.load_text_fromfile(whattext.fn_in, 'utf-8')
        except UnicodeDecodeError:
            try:
                whattext.raw = kh.load_text_fromfile(whattext.fn_in, 'utf-16')
            except UnicodeDecodeError:
                kh.OBSERVER.notify_warn(kh._(
                    "Sorry, can't use the file: {}").format(whattext.fn_in))
                whattext.raw = ""
        if not whattext.raw:
            sysexit()
    whattext.replace_strangeletters()

    # start whole NLP task: read, clean, tag...
    lemma_lists, text_tagged = tag_text_with_db(whattext.text, dbrundi)
    lemmafreq = lemma_lists.all_in()
    # save cleaned text in txt file "src__filename.txt"
    with open(whattext.fn_norm, 'w', encoding="utf-8") as file:
        file.write(whattext.text)

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
                 "db_version": sd.ResourceNames.db_version,
                 "time_tagged": str(date),
                 "fn_short": whattext.fn_short
                 }
    save_tagged_text_as_csv(meta_data, text_tagged.tokens, whattext.fn_tag)
    kh.OBSERVER.notify_tagging(whattext.fn_in.split(pathsep)[-1],
                               whattext.fn_tag.split(pathsep)[-1],
                               kh.Dates.database)
    # kh.OBSERVER.notify(
    #       kh._("\nSaved files in folder results/tagged/ :")
    #       + "\n\t" + str(whattext.fn_norm.split(pathsep)[-1])
    #       + "\n\t" + str(whattext.fn_freqlemma.split(pathsep)[-1])
    #       + "\n\t" + str(whattext.fn_tag.split(pathsep)[-1])
    #       )
    # TODO we save lemmasoup here, because how testing without waiting for y/n?
    # kh.OBSERVER.notify(kh._(
    #     """\nDo you want to save a lemma-version of the text?
    # (tokens replaced by lemmata) y/n"""))
    # l_soup = input("  : ")
    # if l_soup in ["y", "Y", "yes", "ego", "ja", "j", "oui"]:
    lemmasoup = text_tagged.lemmasoup()
    with open(whattext.fn_lemmasoup, 'w', encoding="utf-8") as file:
        file.write(lemmasoup)
    # kh.OBSERVER.notify(
    #     kh._("Lemma-version of the text saved in folder results/tagged/ :\n\t")
    #     + pathsep.join(whattext.fn_lemmasoup.split(pathsep)[-1:])
    #     )
    # kh.OBSERVER.notify(
    #     "\t" + whattext.fn_lemmasoup.split(pathsep)[-1])
    table = []
    table.append((kh._("normalized text\t\t"), "\t"+whattext.fn_norm.split(pathsep)[-1]))
    table.append((kh._("text tokens replaced by lemma\t"), "\t"+whattext.fn_lemmasoup.split(pathsep)[-1]))
    table.append((kh._("lemma based frequency distribution\t"), "\t"+whattext.fn_freqlemma.split(pathsep)[-1]))
    table.append((kh._("tagged text\t\t\t"), "\t"+whattext.fn_tag.split(pathsep)[-1]))
    kh.OBSERVER.notify(kh._("\nSaved files in folder results/tagged/"))
    for i in table:
        kh.OBSERVER.notify_report(i)
    # clear statusbar
    kh.OBSERVER.notify_status(kh._(" "))
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


def search_or_load_search(fn_in, quterms, single, tagged):
    """main
    """
    # whattodo = sd.Search(f_in, wtl, nots, quterms)
    whattodo = sd.Search(fn_in, quterms)
    # check if search was already done before
    sep = sd.ResourceNames.sep
    already_done = kh.check_file_exits(sd.ResourceNames.dir_searched
                                       + whattodo.fn_search.split(sep)[-1])
    if already_done:
        result = kh.load_lines(whattodo.fn_search)
        kh.OBSERVER.notify_status(kh._("You searched this already"))
    else:
        kh.OBSERVER.notify_status(kh._(" "))
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
        if len(result) == 1:
            kh.OBSERVER.notify(
                kh._(f"\nThere is only 1 hit. "
                     + "It is saved in file:\n\t")
                + f'/{sep.join(whattodo.fn_search.split(sep)[-3:])}\n')
        else:
            if len(result) < 20:
                maximal_20 = len(result)
            else:
                maximal_20 = 20
            kh.OBSERVER.notify(
                kh._(f"\nHit 1-{maximal_20} (out of {len(result)}). "
                     + "All results are saved in file:\n\t")
                + f'/{sep.join(whattodo.fn_search.split(sep)[-3:])}\n')
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
    try:
        # first line should be a dictionary
        meta_data = literal_eval(raw[0])
    except (SyntaxError, TypeError, ValueError):
        kh.OBSERVER.notify_warn(kh._("Sorry, missing meta-data in csv-file"))
        sysexit()
    # check if each Metadata-attribute finds a key in the dictionary
    try:
        for i in ['n_char', 'n_odds', 'n_tokens', 'n_tokens_split', 'n_types',
                  'n_unk_types', 'n_lemmata', 'db_version', 'time_tagged',
                  'fn_short']:
            if i not in meta_data.keys():
                raise KeyError()
    except KeyError:
        kh.OBSERVER.notify_warn(kh._("Sorry, wrong meta-data keys in your csv"))
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
        kh.OBSERVER.notify_warn(kh._("Sorry, I can't read your csv-file as a \
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
