#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 28 07:37:34 2023

@author: doreen nixdorf
"""

from ast import literal_eval
# from time import sleep
import gettext
import os.path as osp
import time
import json
from abc import abstractmethod
try:
    import kir_string_depot as sd
except (ImportError):
    from ..lemmatize_search import kir_string_depot as sd

# def N_(message):
#    """if we use kh._ in loops"""
#     return message


class Observer:
    @abstractmethod
    def notify(self, message):
        """Receive a status message
        """
        # pass

    @abstractmethod
    def notify_tagging(self, source_file, tag_file, db_version):
        """Record that an tag file has been made
        """
        # pass

    @abstractmethod
    def notify_frequencies(self, source_file, frequencies_file, db_version):
        """Record that a frequency statistic has been made
        """
        # pass


class PrintConsole(Observer):
    """is notified by observed subject
    to print messages to terminal
    """

    def notify(self, message):
        """prints to console only in single mode
        """
        print(message)

    def notify_cont(self, message):
        """continue next print without linebreak
        """
        print(message, end="")

    # def notify_yes(self, message):
    #     """prints alwaysy to console (single and multiple mode)
    #     """
    #     print(message)

    # def notify_yescont(self, message):
    #     """prints alwaysy to console (single and multiple mode)
    #     """
    #     print(message, end="")

    def notify_tagging(self, source_file, tag_file, db_version):
        """ignored in console mode
        """
        # pass

    def notify_frequencies(self, source_file, frequencies_file, db_version):
        """ignored in console mode
        """
        # pass


def set_ui_language(language_name):
    """ translated to german, french, english, rundi
    accepts de, fr, en, rn
    """
    if language_name.lower() in ["d", "de", "deutsch"]:
        mylang = gettext.translation("messages", sd.ResourceNames.fn_i18n,
                                     languages=["de"], fallback=True)
    elif language_name.lower() in ["r", "k", "", "rn", "kirundi", "rundi"]:
        mylang = gettext.translation("messages", sd.ResourceNames.fn_i18n,
                                     languages=["rn"], fallback=True)
    elif language_name.lower() in ["f", "fr", "fra", "francais", "français"]:
        mylang = gettext.translation("messages", sd.ResourceNames.fn_i18n,
                                     languages=["fr"], fallback=True)
    elif language_name.lower() in ["e", "en", "uk", "english"]:
        mylang = gettext.translation("messages", sd.ResourceNames.fn_i18n,
                                     languages=["en_UK"], fallback=True)
    else:
        return "not"
    return mylang


# LANG_DE = gettext.translation("messages", sd.ResourceNames.fn_i18n,
#                               languages=["de"], fallback=True)
# # _ = LANG_DE.gettext
# LANG_RN = gettext.translation("messages", sd.ResourceNames.fn_i18n,
#                               languages=["rn", "fr"], fallback=True)
OBSERVER = None
# _ = GNUTranslation()
# _ = None


def check_file_exits(fn_file):
    """save energy, don't search twice
    """
    # TODO check hash-values
    return osp.exists(fn_file)


def load_columns_fromfile(fname, upto_column=-1, separator=";"):
    """reads first n columns of a table
    returns a list (col_0, ... col_n)
    """
    liste = []
    with open(fname, encoding="utf-8") as file:
        for row in file:
            row = row.replace("\n", " ")
            if upto_column == -1:
                liste.append(row)
            else:
                cell = row.split(separator)
                cols = []
                for col in cell[:upto_column]:
                    cols.append(col.strip())
                if upto_column == 1:
                    # only 1 column > string
                    liste.append(cols[0])
                else:
                    liste.append(cols)
    # liste[0][0] = str(liste[0][0]).strip("(")
    return liste


def load_lines(filename):
    """returns a list of the lines of the file (utf-8)
    """
    with open(filename, encoding="utf-8") as fname:
        text = fname.read()
        fname.close()
        lines_list = text.split("\n")
        # delete empty last line
        if lines_list[-1] == '':
            lines_list.pop(-1)
        return lines_list


class Dates:
    """returns version of db_kirundi, named_entities, freqfett
    """
    dates = load_lines(sd.ResourceNames().fn_dates)
    dates = {i.split(";")[0]: i.split(";")[1] for i in dates}
    database = dates.get("db")
    namedentities = dates.get("ne")
    lemmafd = dates.get("lfd")

    def __str__(self):
        return f"database={self.database}, "\
               f"namedentities={self.namedentities}, lemmafd={self.lemmafd}"

    def __repr__(self):
        return f"database={self.database}, "\
               f"namedentities={self.namedentities}, lemmafd={self.lemmafd}"


def load_text_fromfile(filename, en_code, line_separator="\n"):
    """returns TextMeta with raw,pathname,text,nodds,nchars
    """
    with open(filename, encoding=en_code) as fname:
        text_raw = fname.read().replace("\n", line_separator)
    #meta = tc.TextMeta(text_raw, filename)
    return text_raw


def load_freqfett():
    """reads lemma_freq from file
    returns list with str, int and tuples (str,int) per lemma
    """
    toomuch = load_lines(sd.ResourceNames.fn_freqfett)
    # toomuch = load_lines("/depot_analyse/freq_fett.csv")
    freq_fett = []
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
                # PoS
                if data == "?":
                    data = "UNK"
                freq.append(data.upper())
            elif data == "":
                # empty cells behind freqsum
                continue
            elif col < 5:
                # freqsum, sum of variants
                freq.append(int(data))
            else:
                # (variant, frequency)
                freq.append(literal_eval(data))
        freq_fett.append(freq)
    return freq_fett


def load_meta_file(fname):
    '''reads files like: line with meta data (||), lines with data, empty line.
    If there is an explanation in the first lines, the n-line-pattern of
    data starts after the first empty line
    attention: meta-data may vary in number,
    but data is always the last element'''
    # text_list = load_text_as_linelist("depot_analyse/tags_for_training.txt")
    text_list = load_lines(fname)

    texts = []
    meta = []
    pattern = [0, 0, 0]
    # find first three empty lines
    for i in range(15):
        # if the file has explanation lines before the data,
        # the next line is empty
        if text_list[i] == "":
            if pattern[0] == 0:
                pattern[0] = i
            elif pattern[0] != 0 and pattern[1] == 0:
                pattern[1] = i
            elif pattern[0] != 0 and pattern[1] != 0:
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
    for i in range(pattern_start, len(text_list)):
        line = text_list[i].strip()
        if (i+pattern_start) % pattern_length == pattern_length-pattern_start:
            meta = [x.strip() for x in line.split("||") if x != ""]
        elif text_list[i] != "":
            data.append(line)
        else:  # text_list[i] == "":
            texts.append(meta+data)
            data = []
    return texts


def save_list(mylist, fname, sep_columns=";", sep_rows="\n"):
    """ writes each elements of a list in one line
    sometimes it's better for reading a txt file by
        separating the elements with an additional empty line "\n\n"
    if it's a nested list, columns are seperated by default with ";"
    """
    # with open(CORPUS_ROOT+fname,'w') as file:
    lines_in_file = ""
    for row in mylist:
        # change nested list to string and integrate column-seperator
        if isinstance(row, (tuple, list)):
            string_list = [str(x) for x in row]
            longstring = sep_columns.join(string_list)+sep_columns
            lines_in_file += longstring + sep_rows
        # element is string or int
        elif isinstance(row, (str, int)):
            lines_in_file += str(row) + sep_rows
    if lines_in_file:
        with open(fname, 'w', encoding="utf-8") as file:
            file.write(lines_in_file)
    else:
        # TODO try except
        # Translators: debugging mode
        OBSERVER.notify(_("""Sorry, I didn't save the list that starts with:
{}\nI was expecting str, int, tuple or list
as list elements.""").format(mylist[:4]))


def show_twenty(mylist):
    """prints first 20 elements of a list
    """
    for i in mylist[:20]:
        if isinstance(i, str):
            OBSERVER.notify(i)
        elif isinstance(i, (tuple, list)):
            OBSERVER.notify(f"{i[0]} ; {i[1]}")


# will be exchanged with hash value question
def check_time(older, younger):
    """compares timestamps of last changes of two files"""
    tic_o = osp.getmtime(older)
    tic_y = osp.getmtime(younger)
    if tic_y > tic_o:
        t_obj = time.strptime(time.ctime(tic_y))
        t_stamp = time.strftime("%d.%m.%Y %H:%M:%S", t_obj)
        return t_stamp
    # older is not the older one
    return False


def save_json(dict_list, filename):
    """saves nested dicts"""
    if filename.split(".")[-1] != "json":
        filename = filename[: -len(filename.split(".")[-1])]+"json"
    with open(filename, 'w', encoding="utf-8") as file:
        # consider: without indent it's only as half as big
        json.dump(dict_list, file, indent=4)


def show_progress(points, n_now, n_max):
    more = int(n_now * 50 / n_max) - points
    OBSERVER.notify_cont(more * '.')
    points += more
    n_now += 1
    return points, n_now


lang = set_ui_language("de")
lang.install()
_ = lang.gettext
OBSERVER = PrintConsole()
SINGLE = True
