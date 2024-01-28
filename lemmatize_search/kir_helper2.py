#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 28 07:37:34 2023

@author: doreen nixdorf
"""

from ast import literal_eval
# from time import sleep
import csv
import gettext
import os.path as osp
import time
from abc import abstractmethod
try:
    import kir_string_depot as sd
except ImportError:
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

    # @abstractmethod
    # def notify_tagging(self, source_file, tag_file, db_version):
    #     """Record that an tag file has been made
    #     """
    #     # pass

    # @abstractmethod
    # def notify_frequencies(self, source_file, frequencies_file, db_version):
    #     """Record that a frequency statistic has been made
    #     """
    #     # pass

    @abstractmethod
    def notify_status(self, message):
        """Receive a status message
        """
        # pass

    @abstractmethod
    def notify_ask(self, message):
        """Show window to decide something with yes/no
        """
        # pass

    @abstractmethod
    def notify_warn(self, message):
        """Show window with warning
        """
        # pass

    @abstractmethod
    def notify_error(self, message):
        """Receive an error message
        """
        # pass

    @abstractmethod
    def notify_progress(self, message):
        """Receive a progress
        """
        # pass


class PrintConsole(Observer):
    """is notified by observed subject
    to print messages to terminal
    """

    def notify(self, message):
        """prints to console
        """
        print(message)

    def notify_add(self, message):
        """prints to console
        """
        print(message)

    def notify_report(self, message):
        """prints to console
        """
        print(message[0]+(25-len(message[0]))*' '+f": {message[1]:9}")

    def notify_table(self, tablename, table, columns):
        """takes a table"""
        self.notify(tablename)
        for row in table:
            if len(row) == 2:
                self.notify_report(row)
            else:
                self.notify(row)

    def notify_ask(self, message):
        """prints to console only in single mode
        """
        yesno = input(message+"\ny/n : ")
        if yesno in ["yesYes"]:
            return True
        return False

    def notify_error(self, message):
        """prints error-messages to console
        """
        print(message)

    # def notify_cont(self, message):
    #     """continue next print without linebreak
    #     """
    #     print(message, end="")

    def notify_status(self, message):
        """prints translated message and points up to 50 to mark how long
        the process will last (line before progressbar)"""
        print("\n"+(message)+(50-len(message))*'.')

    def notify_progress(self, points, n_now, n_max):
        """continue next print without linebreak
        """
        more = int(n_now * 50 / n_max) - points
        print(more * '.', end="")
        if n_now >= n_max-1:
            print(".", end="\n")

    def notify_tagging(self, source_file, tag_file, db_version):
        """ignored in console mode
        """
        # pass

    def notify_frequencies(self, source_file, frequencies_file, db_version):
        """ignored in console mode
        """
        # pass


def show_progress(points, n_now, n_max):
    """takes already printed points, actual index, maximum
    50 because of 50 points"""
    # 
    more = int(n_now * 50 / n_max) - points
    OBSERVER.notify_progress(points, n_now, n_max)
    points += more
    n_now += 1
    return points, n_now


def figure_out_query(which_words):
    """figure the searchterm out
    return list of tuples:
    (to exclude or not, word/tag/lemma/wildcard, searchword)"""
    # which_words = self.input_query.text().split()
    quest = []
    show = ""
    for interest in which_words:
        whichtag = ""
        # discard this word/tag/lemma
        if interest[0] == "!" and len(interest) > 1:
            yesno = "n"
            interest = interest[1:]
            show += _("all except ")
        else:
            yesno = "y"
        # exact word
        if interest[0] == "/" and len(interest) > 1:
            interest = interest[1:]
            whichtag = "token"
            show += _("(exact) " + interest + "\n  ")
        # wildcard
        if interest == "*":
            whichtag = "?"
            show += _("anything\n  ")
        # pos-tag
        elif interest.upper() in sd.possible_tags:
            whichtag = "pos"
            show += interest.upper() + "\n  "
        # lemma
        elif whichtag == "":
            whichtag = "lemma"
            show += "(lemma) " + interest + "\n  "
        quest.append((yesno, whichtag, interest))
    return quest, show[:-3]


def set_ui_language(language_name="rn"):
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


def check_file_exits(fn_file):
    """save energy, don't tag or search again what already is done
    """
    # TODO check hash-values
    return osp.exists(fn_file)


def load_lines(filename):
    """returns a list of the lines of the file (utf-8)
    """
    with open(filename, encoding="utf-8") as fname:
        lines_list = fname.readlines()
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
    """returns the text as string
    """
    with open(filename, encoding=en_code) as fname:
        text_raw = fname.read().replace("\n", line_separator)
    return text_raw


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
        else:
            # TODO try except
            # Translators: debugging mode
            OBSERVER.notify(_(
                """Sorry, I didn't save the list that starts with:
    {}\nI was expecting only str, int, tuple or list as list elements.""")
                .format(mylist[:4]))
            return
    if lines_in_file:
        with open(fname, 'w', encoding="utf-8") as file:
            file.write(lines_in_file)


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
        return tic_y
        # t_obj = time.strptime(time.ctime(tic_y))
        # t_stamp = str(t_obj)  # time.strftime("%d.%m.%Y %H:%M:%S", t_obj)
        # return t_stamp
    # older is not the older one
    return False


def check_csv_column_names(filename, columns):
    """check if column names correspond to required attributes"""
    with open(filename, encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=";")
        missed_columns = [i for i in columns if i not in csv_reader.fieldnames]
    return missed_columns


def show_missing_column_names(filename, missed_columns):
    """print list of missing column names"""
    for missed in missed_columns:
        OBSERVER.notify(_(f"missing column in {filename}: '{missed}'"))


# if __name__ == "__main__":
OBSERVER = None
# _ = GNUTranslation()
# _ = None
lang = set_ui_language()
lang.install()
_ = lang.gettext
# OBSERVER = PrintConsole()
SINGLE = True
