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


def reduce_simplefreq_to_lemma_collections(simple_freq_list):
    """ mappt auf Namen und alle Wortarten im kirundi_db
     liest simple_freq als Liste ein von: (Wort, Anzahl)
     lässt Dateien schreiben"""
    fremd = kh.load_columns_fromfile(sd.RessourceNames().fn_namedentities,2, separator=";")
    #fremd = load_text8_aslist(CORPUS_ROOT+, "\n")
    (dict_verbs, dict_subs, dict_adj, dict_prns,
     dict_adv, dict_rests, dict_stems) =dbc.load_dbkirundi()
    print("sorting named entities"+28*'.')
    collection = []
    (found_here, no_names) = dbc.filter_names_out(fremd, simple_freq_list)
    nfound = len(found_here)
    collection.append(found_here)
    (found_here, no_adv) = dbc.sammle_kleine_woerter(dict_adv, no_names)
    nfound += len(found_here)
    collection.append(found_here)
    print("\nnamed entities      :", len(no_names)-len(no_adv))
    (found_here, no_prns) = dbc.sammle_pronouns(dict_prns, no_adv)
    nfound += len(found_here)
    collection.append(found_here)
    print('adverbs etc         :', len(no_adv)-len(no_prns))
    print('sorting nouns'+37*'.')
    (found_here,no_subs,subs_later) = dbc.collect_nouns(dict_subs, no_prns,True)
    nfound += len(found_here)
    collection.append(found_here)
    print('\npronouns            :', len(no_prns)-len(no_subs))
    (found_here, no_adj) = dbc.collect_adjs(dict_adj, no_subs)
    nfound += len(found_here)
    collection.append(found_here)
    print('nouns               :', len(no_subs)-len(no_adj))
    print('sorting verbs'+38*".")
    #??? problem:not enough values to unpack (expected 2, got 1)
    (found_here, no_verbs) = kv.sammle_verben(dict_verbs, no_adj)
    nfound += len(found_here)
    collection.append(found_here)
    print('\nadjektives          :', len(no_adj)-len(no_verbs))
    # now we search for the substantives we skipped before verbs (uku...)

    (found_here, no_subs2, jetztegal) = dbc.collect_nouns(subs_later, no_verbs, False)
    nfound += len(found_here)
    collection.append(found_here)
    print('verbs               :', len(no_verbs)-len(no_subs2))

    (found_here, no_excl) = dbc.collect_exclamations(dict_rests, no_subs2)
    nfound += len(found_here)
    collection.append(found_here)
    freq_rest = []
    for key,value in no_excl.items() :
        if value != 0 :
            freq_rest.append((key, "", "UNK", value,1,[key,value]))
    freq_rest.insert(0,"lemma;id;unk;count",)
    collection.append(freq_rest)
    # if len(freq_l) > 29290 :
    #     len_freq = 29290
    # else : len_freq =len(freq_l)
    len_simfreq =len(simple_freq_list)
    #print('Substantivierte Verben und Ausrufe :',len(no_subs2)-len(freq_rest)+1)
    # print(50*"-"+'\nvocabulary'+21*" "+':'+4*" ",len_simfreq,
    #       '\nLemmata'+25*" "+":"+4*" ", nfound,
    #       '\n\nauf lemmata sortierte Wörter    :'+4*" ", len_simfreq-len(freq_rest),
    #       '\nder Datenbank unbekannte Wörter :'+4*" ",len(freq_rest)," ("+
    #       str(int(len(freq_rest)/len_simfreq*100)), "%)",
    #       '\n(inkl. Tippfehler und evtl. grottig entzifferter Fotokopien)')
    return collection


def make_lemmafreq_fromtext(mytext) :
    """takes utf-text, maps to lemmata in db_kirundi,
    returns lemma_freq"""
    lemmacollections = reduce_simplefreq_to_lemma_collections(tc.FreqSimple(mytext).freq)
    all_in =[]
    for wordgroup in lemmacollections :
        for lemma in wordgroup[1:] :
            all_in.append(lemma)
    all_in.sort(key=lambda x: x[3], reverse = True)
    return all_in

def makeandsave_lemmafreq_fromfile(fname_in,fname_out):
    """liest eine .txt ein, schreibt lemmata_freq in csv
    Achtung:  path oder filename ?
    legt zwischendurch einzelne/keine Wortartdateien an -- zurzeit nicht!!!
    """
    print("lade Datei ...")
    meta=""
    try :
        meta = kh.load_text_fromfile(fname_in,'utf-8',line_separator=" ")
    except UnicodeDecodeError:
        meta = kh.load_text_fromfile(fname_in,'utf-16',line_separator=" ")
    finally:
        if meta:
            print("erstelle Wortliste ...")
            lemma_freq = make_lemmafreq_fromtext(meta.text)
            lemma_freq.insert(0,"lemma;id;POS;count;counted forms;forms")
            output = fname_out[:-4]+"_marmelade.csv"
            # ??? TODO list or json?:
            kh.save_list(lemma_freq, output)
            return lemma_freq, meta
        print("makeandsave_lemmafreq_fromfile: couldn't read file",fname_in)
        return



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
            if len(newportion)>1:
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
    # semikolon is extra, else it would be read as separator later
    if myword == ";":
        tag = tc.Token("semicolon","SEM","semicolon")
        return tag
    if myword in ",.:!?(){}[]'\"" :
        tag = tc.Token(myword,myword,myword)
        return tag
    if myword in '´`#$%&*+-/<=>@\\^_|~':
        tag = tc.Token(myword,"SYMBOL",myword)
        return tag
    return []


def tag_lemma(myword,lemmafreq):
    """finds words in lemmafreq
    returns Token.token .pos .lemma
    """
    word = unidecode(myword).lower()
    word = re.sub(r"\s+","",word)
    for entry in lemmafreq:
        # entry: [lemma, db-id, PoS, freq, nr of variants, [variants]]
        #lemmata with more than one word get an underline instead of spaces
        qu_entry = entry[0].replace(" ","_")
        for variant in entry[5:] :
            if word == variant[0]:
                tag = tc.Token(myword,entry[2],qu_entry)
                return tag
    tag = tc.Token(myword,"UNK",word)
    return tag


def tag_text_with_db(mytext):#, lemmafreq_all) :
    """uses kirundi_db, makes lemma_freq_list of the text,but tags with big_lemma_freq
    returns list of tagged tokens
    """
    # ??? TODO: oder make_and_save?
    lemmafreq_file = make_lemmafreq_fromtext(mytext)
    print ("lemmata of text:", len(lemmafreq_file))
    # split into sentences -- roughly
    sentences_list = split_in_sentences(mytext)
    punctuation = r'´`\'.!"#$%&()*+,-/:<=>?[\\]^_{|}~;@'

    # collects whole text
    tagged =[]
    nr_sen = -1
    nr_token = -1
    nr_char = 0
    #TODO division /0
    points = int(len(sentences_list)/50)+1
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
            if tag1:
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
                    # ??? nr_char is not correct because we don't know if with whitespace or not
                    nr_char += len(tag2.token)
                else :
                    # check for lemma
                    #tag3 = tag_lemma(w_or_c,lemmafreq_all)
                    tag3 = tag_lemma(w_or_c,lemmafreq_file)
                    tag3.set_nrs(nr_sen, nr_word_in_sen, nr_token, nr_char)
                    tagged.append(tag3)
                    nr_char += len(tag3.token)+1
        # progress bar ;-)
        if sent_count%points == 0 :
            print('.',end = "")
        sent_count +=1
    return (lemmafreq_file,
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
        if searchword == tagword.get(wtl).lower() :
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
    if  len(whattodo.wtl) == 1:
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
                           sd.RessourceNames().dir_tagged):
        # check if tagged version is younger than big lemma collection
        good_old = kh.check_time(sd.RessourceNames().root+"/ressources/freq_fett.csv",
                                 whattodo.fn_tag)
        if good_old:
            print("Hari ifishi n'indanzi: (rikorwa", good_old,
                  ")\n            /"+"/".join(whattodo.fn_tag.split("/")[-4:]),         
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
        raw =meta.raw
    except:
        try:
            meta =kh.load_text_fromfile(whattodo.fn_in,'utf-16')
            raw =meta.raw
        except:
            print("Sorry, can't use the file ", whattodo.fn_in)
    # start whole NLP task: read,clean,tag...
    print("\nRindira akanya, ndiko ndategura amajambo ya kazinduzi ...")
    #freq_lemma_all = kh.load_freqfett()
    print("ndiko ndategura ifishi ...\n")
    # TODO : change to class and get also lemmafreq to save it
    lemmafreq, text_tagged = tag_text_with_db(raw)#,freq_lemma_all)
    kh.freq_to_dict(lemmafreq, whattodo.fn_freqlemmaj)
    kh.save_list(lemmafreq, whattodo.fn_freqlemmac)
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
                                       sd.RessourceNames().dir_searched)
    if already_done:
        result = kh.load_lines(whattodo.fn_search)
        count_results = len(result)
    else:
        count_results = 0
        if multiple is True :
            # already tagged files of the corpus
            tagged_meta = kh.load_meta_file(\
                sd.RessourceNames().root+"/depot_analyse/meta_tags_for_training.txt")
            result = []
            for tagged in tagged_meta :
                result1 = go_search(tagged,whattodo)
                if result1 :
                    count_results += len(result1)
                    result.append("***** "+tagged[0]+"||"+tagged[1]+"||"+
                                  tagged[3]+"||"+str(len(result1))+"|| *****")
                    for res in result1:
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
