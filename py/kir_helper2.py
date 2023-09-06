#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 28 07:37:34 2023

@author: doreen nixdorf
"""

from ast import literal_eval
import os
import time
import json
import kir_tag_classes as tc
import kir_string_depot as sd
from abc import abstractmethod

class Observer:
    @abstractmethod
    def notify(self, message):
        """Receive a status message
        """
        pass
    @abstractmethod
    def notifyTagging(self, source_file, tag_file, db_version):
        """Record that an tag file has been made
        """
        pass
    @abstractmethod
    def notifyFrequencies(self, source_file, frequencies_file, db_version):
        """Record that a frequency statistic has been made
        """
        pass

class PrintConsole(Observer):
    """is notified by observed subject
    to print new messages into console
    """
    def notify(self, message):
        """prints to console
        """
        print(str(message))
    def notifyTagging(self, source_file, tag_file, db_version):
        """ignored in console mode
        """
        pass
    def notifyFrequencies(self, source_file, frequencies_file, db_version):
        """ignored in console mode
        """
        pass

observer = None

def check_file_exits(fn_file, fn_dir):
    """save energy, don't search twice
    """
    files_list = os.listdir(fn_dir)
    # TODO check hash-values corpus/file, freq_fett, code.py and result file
    return fn_file in files_list

def load_columns_fromfile(fname, upto_column= -1, separator=";"):
    """reads first n columns of a table
    returns a list (col_0, ... col_n)
    """
    liste = []
    with open(fname, encoding="utf-8") as file:
        for row in file :
            row = row.replace("\n"," ")
            if upto_column == -1 :
                liste.append(row)
            else:
                cell = row.split(separator)
                cols = []
                for col in cell[:upto_column] :
                    cols.append(col.strip())
                if upto_column == 1 :
                    # only 1 column > string
                    liste.append(cols[0])
                else:
                    liste.append(cols)
    #liste[0][0] = str(liste[0][0]).strip("(")
    return liste

def load_lines(filename):
    """returns a list of the lines of the file (utf-8)
    """
    with open(filename,encoding="utf-8") as fname:
        text = fname.read()
        fname.close()
        lines_list = text.split("\n")
        # delete empty last line
        if lines_list[-1] == '' :
            lines_list.pop(-1)
        return lines_list
    
class Dates:
    """returns version of db_kirundi, named_entities, freqfett
    """
    dates = load_lines(sd.ResourceNames.fn_dates)
    dates = {i.split(";")[0]:i.split(";")[1] for i in dates}
    database = dates.get("db")
    namedentities = dates.get("ne")
    lemmafd = dates.get("lfd")
    def __str__(self):
        return f"database={self.database}, namedentities={self.namedentities}, "\
            +"lemmafd={self.lemmafd}"
    def __repr__(self):
        return f"database={self.database}, namedentities={self.namedentities}, "\
            +f"lemmafd={self.lemmafd}"

def load_text_fromfile(filename,en_code,line_separator="\n"):
    """returns TextMeta with raw,pathname,text,nodds,nchars
    """
    with open(filename, encoding = en_code) as fname:
        text_raw = fname.read().replace("\n",line_separator)
    meta = tc.TextMeta(text_raw,filename)
    return meta

def load_freqfett():
    """reads lemma_freq from file
    returns list with str, int and tuples (str,int) per lemma
    """
    toomuch = load_lines(sd.ResourceNames.fn_freqfett)
    #toomuch = load_lines("/depot_analyse/freq_fett.csv")
    freq_fett =[]
    # from line[14275] frequence < 6
    # from line[38150] only unknown words
    # skip first line (headline)
    for lemma_entry in toomuch[1:]:
        elements = lemma_entry.split(";")
        freq = []
        for col, data in enumerate(elements):
            if col < 2:
                # lemma, id
                freq.append(data)
            elif col == 2:
                #POS
                if data == "?":
                    data = "UNK"
                freq.append(data.upper())
            elif data == "" :
                # empty cells behind freqsum
                continue
            elif col < 5 :
                # freqsum, sum of variants
                freq.append(int(data))
            else :
                # (variant, frequency)
                freq.append(literal_eval(data))
        freq_fett.append(freq)
    return freq_fett

def load_meta_file(fname):
    '''reads files like: line with meta data (||), lines with data, empty line.
    if there is an explanation in the first lines, the n-line-pattern of data starts 
    after the first empty line
    attention: meta-data may vary in number, but data is always the last element'''
    #text_list = load_text_as_linelist("depot_analyse/tags_for_training.txt")
    text_list = load_lines(fname)

    texts = []
    meta = []
    pattern = [0,0,0]
    # find first three empty lines
    for i in range(15):
    # if the file has explanation lines before the data, the next line is empty
        if text_list[i] == "" :
            if pattern[0] == 0 :
                pattern[0] = i
            elif pattern[0] !=0 and pattern[1] == 0 :
                pattern[1] = i
            elif pattern[0] !=0 and pattern[1] != 0 :
                pattern[2] = i
                break
    # first line is explanation?
    if "id" in text_list[0].split("||")[0]:
        pattern_start = pattern[0]+1
    else:
        pattern_start = 0
    # length of explanation may or may not vary from pattern length
    pattern_length = pattern[2]-pattern[1]
    data = []
    for i in range(pattern_start,len(text_list)):
        line = text_list[i].strip()
        if (i+pattern_start)%pattern_length == pattern_length-pattern_start:
            meta = [x.strip() for x in line.split("||") if x != ""]
        elif text_list[i] != "" :
            data.append(line)
        else: #text_list[i] == "":
            texts.append(meta+data)
            data =[]
    return texts

def save_list(mylist, fname, sep_columns =";", sep_rows = "\n") :
    """ writes each elements of a list in one line
    sometimes it's better for reading a txt file by 
        separating the elements with an additional empty line "\n\n"
    if it's a nested list, columns are seperated by default with ";" 
    """
    #with open(CORPUS_ROOT+fname,'w') as file:
    lines_in_file = ""
    for row in mylist :
        # change nested list to string and integrate column-seperator
        if isinstance(row, (tuple, list)) :
            string_list = [str(x) for x in row]
            longstring = sep_columns.join(string_list)+sep_columns
            lines_in_file += longstring + sep_rows
        # element is string or int
        elif isinstance(row, (str, int)) :
            lines_in_file += str(row) + sep_rows
    if lines_in_file:
        with open(fname,'w',encoding="utf-8") as file:
            file.write(lines_in_file)
    else:
        observer.notify("(kh.save_list) Sorry, I didn't save the list that starts with: "+
              f"{mylist[:4]}\nI was expecting str, int, tuple or list as list elements")

def show_twenty(mylist):
    """prints first 20 elements of a list
    """
    for i in mylist[:20]:
        if isinstance(i, str) :
            observer.notify(i)
        elif isinstance(i, (tuple,list)) :
            observer.notify(f"{i[0]} ; {i[1]}")

# will be exchanged with hash value question
def check_time(older, younger):
    """compares timestamps of last changes of two files"""
    tic_o = os.path.getmtime(older)
    tic_y = os.path.getmtime(younger)
    if tic_y > tic_o:
        t_obj = time.strptime(time.ctime(tic_y))
        t_stamp = time.strftime("%d.%m.%Y %H:%M:%S", t_obj)
        return t_stamp
    # older is not the older one
    return False

def save_json(dict_list,filename):
    """saves list of class objects with class_name"""
    if filename.split(".")[-1] != "json" :
        filename = filename[: -len(filename.split(".")[-1])]+"json"
    # write classname into file to identify if loading later
    argo = [dict(x.__dict__) for x in dict_list]
    class_name = str(type(dict_list[0])).split(".")[-1][:-2]
    with open(filename,'w', encoding = "utf-8") as file:
        # consider: without indent it's only half as big
        json.dump({class_name: argo}, file, indent=4)
