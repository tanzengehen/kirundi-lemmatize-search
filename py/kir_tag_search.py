#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 20 15:32:20 2023

@author: doreen nixdorf
"""


import re
import json
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
    #names = kh.load_columns_fromfile(sd.ResourceNames().fn_namedentities,2, separator=";")
    names = dbc.load_ne()
    #fremd = load_text8_aslist(CORPUS_ROOT+, "\n")
    (dict_verbs, dict_subs, dict_adj, dict_prns,
     dict_adv, dict_rests, dict_stems) =dbc.load_dbkirundi()
    print("sorting Named Entities"+28*'.')
    collection = tc.Collection
    (collection.names, still_unk) = dbc.filter_names_out(names, simple_freq_list)
    len_before = len(still_unk)
    (collection.advs, still_unk) = dbc.collect_adv_plus(dict_adv, still_unk)
    print("\nNamed Entities      :", len_before-len(still_unk),"/",len(still_unk))
    len_before = len(still_unk)
    (collection.pronouns, still_unk) = dbc.collect_pronouns(dict_prns, still_unk)
    print('adverbs etc         :', len_before-len(still_unk), ">>",
          len(collection.advs)-1,"/",len(still_unk))
    print('sorting nouns '+36*'.')
    len_before = len(still_unk)
    (collection.nouns,still_unk,subs_later) = dbc.collect_nouns(dict_subs, still_unk, True)
    print('\npronouns            :', len_before-len(still_unk),">>",
          len(collection.pronouns)-1,"/",len(still_unk))
    len_before = len(still_unk)
    (collection.adjs, still_unk) = dbc.collect_adjs(dict_adj, still_unk)
    print('nouns               :', len_before-len(still_unk),">>",
          len(collection.nouns)-1,"/",len(still_unk))
    print('sorting verbs '+36*".")
    len_before = len(still_unk)
    (collection.verbs, still_unk) = kv.sammle_verben(dict_verbs, still_unk)
    print('\nadjektives          :', len_before-len(still_unk),">>",
          len(collection.adjs)-1,"/",len(still_unk))
    # now we search for the substantives we skipped before verbs (uku...)
    len_before = len(still_unk)
    (found_here, still_unk, doesntmatteranymore) = dbc.collect_nouns(subs_later, still_unk, False)
    collection.nouns += found_here
    print('verbs               :', len_before-len(still_unk),">>",
          len(collection.verbs)-1,"/",len(still_unk))

    (collection.exclams, still_unk) = dbc.collect_exclamations(dict_rests, still_unk)
    collection.unk=[]
    for key,value in still_unk.items() :
        if value != 0 :
            collection.unk.append((key, "", "UNK", value,1,[key,value]))
    return collection


def make_lemmafreq_fromtext(mytext) :
    """takes utf-text, maps to lemmata in db_kirundi,
    returns lemma_freq"""
    simfreq = tc.FreqSimple(mytext)
    lemma_collection = reduce_simplefreq_to_lemma_collection(simfreq.freq)
    known = tc.Collection.known(lemma_collection)
    return known, lemma_collection.unk

def split_in_sentences(mytext):
    """splits texts where [?.!;:] + space_character
    that's only a rough approach
    returns list with strings
    """
    # mach lesbar, aber Zeichensetzung ist noch drin
    # print("Zeichenanzahl"+16*" "+":"+4*" ",len(readabletext),
    #       "\nersetzte Buchstaben"+10*" "+":"+4*" ", mistakes)
    #all_sents =[readabletext,]
    all_sents =[mytext,]
    # teile die Portionen alle gleichwertig, nicht geschachtelt
    for seperator in ".?!:;" :
        storage = []
        for part in all_sents:
            newportion = part.split(seperator+" ")
            if len(newportion)>1 :
                for new in newportion[:-1] :
                    new = new+seperator
                    storage.append(new)
                storage.append(newportion[-1])
            else: storage.append(part)
            all_sents = storage
    if len(all_sents[-1].strip()) < 2 :
        all_sents.pop(-1)
    return all_sents


def tag_word_nrmailweb(myword):
    """finds numbers, roman numbers, emails, webadresses
    returns Token.token .pos .lemma
    """
    regex_email = r'^[\w.!#$%&’*+/=?^_`{|}~-]+@\w+(?:\.\w+)*$'
    regex_web = r'^(http[s]?:\/\/|www.)'
    regex_rom = r'^M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$'
    # delete accents, lower all letters
    word= unidecode(myword.lower())
    if re.search(r"[0-9]+",word) :
        tag = tc.Token(word,"NUM",word)
        return tag
    if re.search(regex_rom,word) :
        tag = tc.Token(word,"NUM_ROM",word)
        return tag
    if re.search(regex_web,word) :
        tag = tc.Token("address_in_web","WWW","address_in_web")
        return tag
    if word.find("@") > -1 and re.search(regex_email,word) :
        tag = tc.Token("emailAtsomewhere","EMAIL","emailAtsomewhere")
        return tag
    return []


def tag_punctmarks_etc(myword):
    """finds symbols and marks
    returns Token.token .pos .lemma
    """
    if myword in ",.;:!?(){}[]'\"" :
        tag = tc.Token(myword,myword,myword)
        return tag
    if myword in '´`#$%&*+-/<=>@\\^_|~':
        tag = tc.Token(myword,"SYMBOL",myword)
        return tag
    return []


def tag_lemma(myword,knownlemmafreq):
    """finds words in lemmafreq
    returns Token.token .pos .lemma
    """
    word = unidecode(myword).lower()
    word = re.sub(r"\s+","",word)
    for entry in knownlemmafreq:
        # entry: [lemma, db-id, PoS, freq, nr of variants, [variants]]
        #lemmata with more than one word get an underline instead of spaces
        qu_entry = entry[0].replace(" ","_")
        try:
            for variant in entry[5:] :
                if word == variant[0]:
                    tag = tc.Token(myword,entry[2],qu_entry)
                    return tag
        except :
            print(entry, word, variant)
    tag = tc.Token(myword,"UNK",word)
    return tag



def tag_text_with_db(mytext):#, lemmafreq_all) :
    """uses kirundi_db, makes lemma_freq_list of the text, (but tags with big_lemma_freq)
    returns lemma_freq, list of tagged tokens
    """
    known, unknown = make_lemmafreq_fromtext(mytext)
    # TODO where to put the metadata
    print ("lemmata of text:", len(known), "\nunknown types  :", len(unknown))
    # split into sentences -- roughly
    sentences_list = split_in_sentences(mytext)
    punctuation = r'´`\'.!"#$%&()*+,-/:<=>?[\\]^_{|}~;@'

    # collects whole text
    tagged =[]
    nr_sen = -1
    nr_token = -1
    nr_char = 0
    if len(sentences_list) > 50 :
        points = int(len(sentences_list)/50)
    else:
        points = 1
    sent_count = 0
    print("\ntagging text, this may take some moments ..........")
    for sentence in sentences_list:
        nr_sen +=1
        #len_sen = len(sentence)
        words = sentence.split()
        # collects sentence
        nr_word_in_sen = -1
        for word in words:
            nr_word_in_sen +=1
            nr_token +=1
            #check for emails, webaddress, number, roman number
            # returns for email and webaddress alias
            tag1 = tag_word_nrmailweb(word)
            if tag1 :
                tag1.set_nrs(nr_sen, nr_word_in_sen, nr_token, nr_char)
                tagged.append(tag1)
                nr_char += len(tag1.token)+1
                continue
            # now we seperate letters from other characters (w'umuryango)
            wordwithoutsign = word.replace("'" , " ' ")
            for p_mark in punctuation:
                storage = wordwithoutsign.replace(p_mark , " "+p_mark+" ")
                wordwithoutsign = storage
            word_or_char = wordwithoutsign.split()
            # word or single character ?
            for w_or_c in word_or_char :
                # check for punctuation
                tag2 = tag_punctmarks_etc(w_or_c)
                if tag2:
                    tag2.set_nrs(nr_sen, nr_word_in_sen, nr_token, nr_char)
                    tagged.append(tag2)
                    # TO DO nr_char is not correct because we don't know if with whitespace or not
                    nr_char += len(tag2.token)
                else :
                    # check for lemma
                    #tag3 = tag_lemma(w_or_c,lemmafreq_all)
                    tag3 = tag_lemma(w_or_c,known)
                    tag3.set_nrs(nr_sen, nr_word_in_sen, nr_token, nr_char)
                    tagged.append(tag3)
                    nr_char += len(tag3.token)+1
        # progress bar ;-)
        if sent_count%points == 0 :
            print('.',end = "")
        sent_count +=1
    lemmafreq = known+unknown
    lemmafreq.sort(key=lambda x: x[3], reverse = True)
    return (lemmafreq,
            tagged)



def collect_words_around_searchterm(index, found_string, wordlist_tagged):
    """puts searchresult in it's context
    """
    # collect words around searchword
    index_behind = index+len(found_string.split())
    text_around = 4*" "+found_string+8*" "
    neighbours= 0
    char_count = 0
    # words behind searchterm
    while char_count < 50 and index_behind + neighbours < len(wordlist_tagged) :
        neighbor_text = wordlist_tagged[index_behind + neighbours].token+" "
        text_around += neighbor_text
        char_count += len(neighbor_text)
        neighbours += 1
    neighbours= -1
    char_count = 0
    # words before searchterm
    while char_count < 50  and index+neighbours > 0 :
        neighbor_text = wordlist_tagged[index+neighbours].token+" "
        text_around = neighbor_text+text_around
        char_count += len(neighbor_text)
        neighbours -= 1
    # cut or fill space before searchterm
    if char_count >= 50:
        text_around = (5-len(str(index)))*" "+text_around[char_count-50:]
    else:
        text_around = (5-len(str(index)))*" "+(50-char_count)*" "+text_around
    return text_around


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
        if not tagword.pos :
            missings.append(("missing tag by word number:", index, tagword.token))
            continue
        if searchword == tagword.get(wtl):#.lower() :
            with_neighbors= collect_words_around_searchterm(index, tagword.token, wordlist_tagged)
            found.append((index, with_neighbors))
    return found, missings


def find_ngrams(wordlist_tagged, wtl, questions):
    """finds combinations of n words 
    wordforms(w), tags(t), lexems(l) or jokerword(?)
    returns all matches with text around the search result
    """
    missings = []
    ngram_length = len(questions)
    found = []
    for index_list in range(len(wordlist_tagged)-ngram_length):
        # tag missing?
        if not wordlist_tagged[index_list].pos :
            missings.append(("missing tag by word number:",index_list,
                             wordlist_tagged[index_list].token))
            continue
        n_count = 0
        part_found = ""
        such_index = index_list
        # collect matches till mismatch of next token or full-match
        # (we have to lower both: beginnings of sentences and tags)
        while n_count < ngram_length and \
            (wtl[n_count] == "?" \
             or wordlist_tagged[such_index].get(wtl[n_count]).lower()
                == questions[n_count].lower()) :
            part_found += " "+ wordlist_tagged[such_index].token
            if n_count == ngram_length-1 :
                with_neighbors= collect_words_around_searchterm(\
                                    index_list, part_found, wordlist_tagged)
                found.append([index_list , with_neighbors])
            n_count +=1
            such_index += 1
    return found, missings


def go_search(tagged_list, whattodo):
    """search in single text
    """
    if  len(whattodo.wtl) == 1 :
        found = find_thing(tagged_list,whattodo.wtl[0],whattodo.questions)
    else:
        found = find_ngrams(tagged_list,whattodo.wtl,whattodo.questions)
    if found :
        # tag missing?
        if found[1] :
            print("hari ikosa: indanzi irabuze")
            for i in found[1]:
                print (i)
        return found[0]
    return found


def tag_or_load_tags(whattodo):
    """save energy, don't tag twice
    """
    # 1. is there already a tagged json variant?
    # TODO check hash values
    if kh.check_file_exits(whattodo.fn_tag.split("/")[-1],
                           sd.ResourceNames().dir_tagged):
        # check if tagged version is younger than big lemma collection
        good_old = kh.check_time(sd.ResourceNames().root+"/resources/freq_fett.csv",
                                 whattodo.fn_tag)
        if good_old:
            print("Hari ifishi n'indanzi: (rikorwa", good_old,
                  ")\n"+"\t"*6+"/".join(whattodo.fn_tag.split("/")[-4:]),         
                  "\nniryo ndakoresha ku kibanza ca gusubira gukora indanzi")
            text_tagged = load_json(whattodo.fn_tag)
            return text_tagged
    # 2. maybe the given file itself is a json file? >> already tagged >> read
    if whattodo.fn_in[-5:] == ".json" :
        try:
            text_tagged = load_json(whattodo.fn_in)
            return text_tagged
        except:
            print("Are you sure, that this is a tagged file?")
            # TODO get new data
    # 3. read raw txt utf8 or utf16
    try:
        meta =kh.load_text_fromfile(whattodo.fn_in,'utf-8')
        #raw =meta.raw
    except:
        try:
            meta =kh.load_text_fromfile(whattodo.fn_in,'utf-16')
            #raw =meta.raw
        except:
            print("Sorry, can't use the file ", whattodo.fn_in)
    # start whole NLP task: read,clean,tag...
    print("\nRindira akanya, ndiko ndategura amajambo ya kazinduzi ...")
    #freq_lemma_all = kh.load_freqfett()
    print("ndiko ndategura ifishi ...\n")
    lemmafreq, text_tagged = tag_text_with_db(meta.text)#,freq_lemma_all)
    # insert first line as head for csv file
    lemmafreq.insert(0,sd.first_line_in_pos_collection(),)
    kh.save_list(lemmafreq, whattodo.fn_freqlemmac)
    # remove first line again
    lemmafreq.pop(0)
   # #kh.freq_to_dict(lemmafreq, whattodo.fn_freqlemmaj)
    # save tagged file for reuse
    kh.save_json(text_tagged, whattodo.fn_tag)
    print("\n\nNashinguye iki gisomwa n'indanzi mu fishi: \n"
          +"\t"*6+"/"+"/".join(whattodo.fn_tag.split("/")[-4:]),
          "\nTurashobora gusubira kurikoresha ikindi gihe.")
    return text_tagged


def search_or_load_search(f_in, how, what, multiple):
    """main
    """
    whattodo = sd.Search(f_in, multiple)
    whattodo.set_search(how, what)
    # check if search was already done before
    already_done = kh.check_file_exits(whattodo.fn_search.split("/")[-1],
                                       sd.ResourceNames().dir_searched)
    if already_done:
        result = kh.load_lines(whattodo.fn_search)
        count_results = len(result)
    else:
        count_results = 0
        if multiple is True :
            # already tagged files of the corpus
            tagged_meta = kh.load_meta_file(\
                sd.ResourceNames().root+"/depot_analyse/meta_tags_for_training.txt")
            result = []
            for tagged in tagged_meta :
                result1 = go_search(tagged,whattodo)
                if result1 :
                    count_results += len(result1)
                    result.append("***** "+tagged[0]+"||"+tagged[1]+"||"+
                                  tagged[3]+"||"+str(len(result1))+"|| *****")
                    for res in result1 :
                        result.append(res)
            #headline
            if result :
                result.insert(0,"file_id||characters||path||results counted||results")
        else :
            # tags the file or takes an already tagged version of the file
            text_with_tags = tag_or_load_tags(whattodo)
            # searches in the tagged file
            result = go_search(text_with_tags, whattodo)
            count_results = len(result)
    if result :
        print(f"\nInyishu 1-20 (hari {len(result)}). Uraronka zose mu fishi: "+
              "\n"+"\t"*6+f'/{"/".join(whattodo.fn_search.split("/")[-3:])}\n')
        kh.show_twenty(result)
        # save results as txt
        if not already_done:
            kh.save_list(result,whattodo.fn_search)
    else :
        print("Nta nyishu.")


def load_json(filename):#, klasse="Token"):
    """reads and maps json-file
    class name be written in file
    """
    with open(filename ,encoding='utf-8') as file:
        raw = json.load(file)
    class_name = list(raw.keys())[0]
    objects = []
    if class_name == "Token" :
        for i in raw.get(class_name):
            tag = tc.Token(i.get('token'),i.get('pos'),i.get('lemma'))
            tag.set_nrs(i.get('id_sentence'),i.get('id_tokin_sen'),
                        i.get('id_token'),i.get('id_char'))
            objects.append(tag)
    # TODO other classes: PreparedFile
    # elif klasse == "Corpus/Single" and class_name == klasse :
    #     for i in raw.get(class_name):
    #         text = Corpus(i.get('dbid'),i.get('lemma'),i.get('stem'),
    #                     i.get('perfective'),i.get('alternative'),
    #                     i.get('comb'),i.get('proverb'))
    #         objects.append(verb)
    else:
        print("sorry, unknown format")
        return objects
    return objects
