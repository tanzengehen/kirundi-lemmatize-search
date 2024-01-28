#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 14 15:02:27 2024

@author: doreen
"""

import sys
import gettext
from PyQt5 import QtCore, QtGui, QtWidgets, uic
# from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QTextCursor
# from PyQt5.QtCore import Qt

try:
    import kir_helper2 as kh
    import kir_string_depot as sd
    import kir_tag_classes as tc
    import kir_tag_search as ts
    import kir_db_classes as dbc
except ImportError:
    from ..lemmatize_search import kir_helper2 as kh
    from ..lemmatize_search import kir_string_depot as sd
    from ..lemmatize_search import kir_tag_classes as tc
    from ..lemmatize_search import kir_tag_search as ts
    from ..lemmatize_search import kir_db_classes as dbc


# set meine UI
# qt_creator_file = "first_test.ui"
qt_creator_file = "ingenzura_ikirundi.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qt_creator_file)


# class IrgendwasModel(QtCore.QAbstractListModel):
#     def __init__(self, *args, todos=None, **kwargs):
#         super(IrgendwasModel, self).__init__(*args, **kwargs)
#         self.todos = todos or []

#     def data(self, index, role):
#         if role == Qt.DisplayRole:
#             _, text = self.todos[index.row()]
#             return text

#         if role == Qt.DecorationRole:
#             status, _ = self.todos[index.row()]
#             return status

class LanguageDialog(QtWidgets.QDialog):
    """Dialog for changing UI-language with next start of the App and if yes,
    close it for now to apply the change"""

    def __init__(self, parent=None, title="change language",
                 message_l="restart the application",
                 ok="OK", cancel="Cancel"):
        """takes titel, message and button-names"""
        super().__init__(parent)
        self.setWindowTitle(title)

        ok_button = QtWidgets.QPushButton(ok)
        ok_button.setDefault(True)
        cancel_button = QtWidgets.QPushButton(cancel)
        cancel_button.setAutoDefault(False)
        button_box = QtWidgets.QDialogButtonBox()
        button_box.addButton(ok_button, QtWidgets.QDialogButtonBox.AcceptRole)
        button_box.addButton(cancel_button,
                             QtWidgets.QDialogButtonBox.RejectRole)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        self.layout = QtWidgets.QVBoxLayout()
        message = QtWidgets.QLabel(message_l)
        self.layout.addWidget(message)
        self.layout.addWidget(button_box)
        self.setLayout(self.layout)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    """main window"""

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        # tagged text
        self.text_tagged = None
        # search query (valid list)
        self.search_words = []
        # set self.search_words from input
        self.check_query()

        self.statusbar = self.statusBar()
        # Menu Languages
        self.actionikirundi.triggered.connect(
            lambda x: self.set_language_for_change_language_dialog("rn"))
        self.actionfran_ais.triggered.connect(
            lambda x: self.set_language_for_change_language_dialog("fr"))
        self.actiondeutsch.triggered.connect(
            lambda x: self.set_language_for_change_language_dialog("de"))
        self.actionenglish.triggered.connect(
            lambda x: self.set_language_for_change_language_dialog("en"))
        # Menu about
        self.actionabout.triggered.connect(self.show_about)
        # fill Help-TextBrowser
        if kh.check_file_exits(sd.ResourceNames.fn_help+LANG+".html"):
            self.help_textBrowser.setSource(
                QtCore.QUrl.fromLocalFile(
                    sd.ResourceNames.fn_help+LANG+".html"))
        else:
            self.help_textBrowser.setSource(
                QtCore.QUrl.fromLocalFile(sd.ResourceNames.fn_help+"en.html"))
        # self.actionHow_to_lemmatize.triggered.connect(self.jumpto_lemmatize)
        # self.actionHow_to_search.triggered.connect(self.jumpto_search)
        # self.actionHow_to_contribute.triggered.connect(self.jumpto_contribute)
        # Buttons
        self.input_filename.textChanged.connect(self.enable_btn_lemmata)
        self.input_filename.textChanged.connect(self.enable_btn_search)
        self.btn_set_filename.clicked.connect(self.select_file)

        self.btn_lemmata.clicked.connect(self.go_for_tags)
        self.input_query.textEdited.connect(self.check_query)
        self.btn_search.clicked.connect(self.start_search)

    def set_language_for_change_language_dialog(self, wish):
        """set language for change-language dialog"""
        if LANG != wish:
            dates = kh.load_lines(sd.ResourceNames().fn_dates)
            dates = ['LANG;'+wish if i[:5] == 'LANG;'
                     else i.strip('\n') for i in dates]
            language = sd.language_dialog.get(wish)
            dialog = LanguageDialog(self,
                                    title=language.get('title'),
                                    message_l=language.get('message_l'),
                                    ok=language.get('ok'),
                                    cancel=language.get('cancel'))
            if dialog.exec_():
                kh.save_list(dates, sd.ResourceNames().fn_dates)
                self.close()

    def show_about(self):
        """show information about the application"""
        info = QtWidgets.QMessageBox(self,
                                     informativeText="not much to say"
                                     + "\nVersion 0.0")
        info.exec_()

    # def jumpto_lemmatize(self):
    #     """jump in help-TextBrowser to explanation of how to lemmatize"""
    #     self.help_textBrowser.anchorClicked( self.help_textBrowser)

    def select_file(self):
        """accept txt or csv file"""
        fnin, text = QtWidgets.QFileDialog.getOpenFileName(
            self, "select file", "", "(*.csv *.txt)")
        if fnin:
            self.input_filename.clear()
            self.input_filename.insert(fnin)
            # self.btn_lemmata.setEnabled(True)

    def enable_btn_lemmata(self):
        """depends on filename, maybe it was changed manually to
        other ending than txt or csv"""
        filename = self.input_filename.text()
        if filename and filename[-4:] in [".txt", ".csv"] and\
           kh.check_file_exits(filename):
            self.btn_lemmata.setEnabled(True)
        else:
            self.btn_lemmata.setEnabled(False)
        # maybe own function, it's for case: fn_in changed but not query
        # till now enable_btn_lemmata is only called when fn_in changed
        if self.statusbar.currentMessage() == kh._("You searched this already"):
            self.statusbar.clearMessage()

    def enable_btn_search(self):
        """search-button depends on filename and hint_for_inputs-visibility"""
        filename = self.input_filename.text()
        query = self.input_query.text()
        text = tc.TextMeta()
        tagged = False
        if filename[-4:] in [".txt", ".csv"]:
            # did we tag it already?
            text = tc.TextMeta(filename)
            text.set_fn_outs()
            tagged = kh.check_file_exits(text.fn_tag)
        if (filename[-4:] == ".csv" or tagged) \
           and query \
           and self.hint_for_inputs.text() == "":
            self.btn_search.setEnabled(True)
        else:
            self.btn_search.setEnabled(False)

    def go_for_tags(self):
        """tag text and show statistics"""
        self.results.clear()
        self.statusbar.clearMessage()
        self.statusbar.showMessage(_("analysiere..."))
        fn_in = self.input_filename.text()
        db_rundi = dbc.get_resources()
        self.text_tagged = ts.tag_or_load_tags(fn_in, db_rundi)

    def check_query(self):
        """check query validity"""
        query = self.input_query.text()
        questions = query.split()
        wrong = None
        for element in questions:
            # check if '*' is inside of a word
            if len(element) > 1 and "*" in element:
                self.hint_for_inputs.setText(
                    _("ATTENTION: * only for words, not for letters."))
                wrong = True
            if "/!" in element:
                self.hint_for_inputs.setText(
                    _("ATTENTION: in case of combining '!' and '/' write '!' first"))
                wrong = True
        if not wrong:
            self.hint_for_inputs.clear()
        which_words = self.input_query.text().split()
        self.search_words, show_search = kh.figure_out_query(which_words)
        if query:
            self.confirm_search.setText(
                _(f"OK, you are looking for a {len(questions)}-gram:\n  ")
                + show_search)
        else:
            self.confirm_search.clear()
        self.enable_btn_search()

    def start_search(self):
        # TODO use already checked names or enough checked because enabled?
        fn_in = self.input_filename.text()
        single = True
        ts.search_or_load_search(
            fn_in, self.search_words, single, self.text_tagged.tokens)


class QtOutput(kh.Observer):
    """is notified by observed subject
    to bring messages to PyQt"""

    def __init__(self, mainwindow):
        self.mainwindow = mainwindow
        self.error_list = []

    def notify(self, message):
        """bring results to PyQt"""
        # text = self.mainwindow.results.toPlainText()
        self.mainwindow.results.append(str(message))
        app.processEvents()

    def notify_add(self, message):
        """writes directly behind the last character, no new line between"""
        cursor = self.mainwindow.results.textCursor()
        text = self.mainwindow.results.toPlainText()
        cursor.setPosition(len(text))
        cursor.insertText(str(message))
        app.processEvents()

    def notify_report(self, message):
        """reports results in results-TextEdit"""
        # text = self.mainwindow.results.toPlainText()
        self.mainwindow.results.append(f"{message[0]}: {message[1]}")
        app.processEvents()

    def notify_table(self, tablename, table, columns):
        """reports results in results-TextEdit"""
        # print(message)
        self.notify(tablename)
        cursor = QTextCursor()
        cursor = self.mainwindow.results.textCursor()
        # table = QTableWidget()
        # table.setItem(0, 0, QTableWidgetItem("cell0"))
        # table.setItem(0, 1, QTableWidgetItem("cell1"))
        cursor.insertTable(len(table), columns)
        for row in table:
            for col in range(len(row)):
                cursor.insertText(f"{row[col]:20}")
                cursor.movePosition(QTextCursor.NextCell)
        app.processEvents()

    def notify_ask(self, message):
        """open window for decision y/n"""
        # text = self.mainwindow.results.toPlainText()
        self.mainwindow.results.append("\n" + message)
        app.processEvents()

    def notify_warn(self, message):
        """write warning or how to in hints_for_input label"""
        self.mainwindow.hint_for_inputs.setText(
            _("ATTENTION: ") + message)
        app.processEvents()

    def notify_error(self, message):
        """Receive an error message
        """
        self.error_list.append(message)
        self.mainwindow.statusbar.showMessage(
            _(f"there are {len(self.error_list)} issues, watch log_file"))
        # TODO write log_file or show the errors

    def notify_status(self, message):
        """Show in statusbar what's going on meanwhile
        """
        self.mainwindow.statusbar.showMessage(message)

    def notify_progress(self, points, n_now, n_max):
        """Show progress in progressbar
        """
        if n_now+1 == n_max:
            self.mainwindow.progressBar.setValue(0)
            self.mainwindow.statusbar.clearMessage()
        else:
            self.mainwindow.progressBar.setValue(int(n_now * 100 / n_max))
        app.processEvents()

    def notify_frequencies(self, fn_in, fn_freq, db_version):
        """do something with the name of freqency_file"""
        # text = self.mainwindow.results.toPlainText()
        # self.mainwindow.results.setText(
        #     text +
        #     "\n" + fn_in +
        #     "\n" + fn_freq +
        #     "\n" + db_version)

    def notify_tagging(self, fn_in, fn_tag, db_version):
        """do something with the name of tagged file
        """
        # text = self.mainwindow.results.toPlainText()
        # self.mainwindow.results.setText(
        #     text +
        #     "\n" + fn_in +
        #     "\n" + fn_tag +
        #     "\n" + db_version)

if __name__ == "__main__":
    LANG = 'rn'
    # read saved language from file
    saved_context = kh.load_lines(sd.ResourceNames().fn_dates)
    for i in saved_context:
        if i[:5] == 'LANG;':
            LANG = i[5:7]
            break
    # install that language
    try:
        translation = gettext.translation("messages",
                                          sd.ResourceNames.fn_i18n,
                                          languages=[LANG], fallback=True)
        if translation:
            translation.install()
            _ = translation.gettext
            ngettext = translation.ngettext
            kh._ = translation.gettext
    except FileNotFoundError:
        pass
    if not _:
        _ = gettext.gettext

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    kh.OBSERVER = QtOutput(window)
    window.show()
    app.exec_()
