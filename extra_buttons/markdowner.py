# -*- coding: utf-8 -*-
#
# Copyright 2014-2015 Stefan van den Akker <srvandenakker.dev@gmail.com>
#
# This file is part of Supplementary Buttons for Anki.
#
# Supplementary Buttons for Anki is free software: you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Supplementary Buttons for Anki is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with Supplementary Buttons for Anki. If not, see http://www.gnu.org/licenses/.

import re
import sqlite3

from anki.utils import json, intTime
from aqt import mw
from PyQt4 import QtGui

from utility import Utility


class Markdowner(object):
    """
    Convert HTML to Markdown and the other way around. Store the data in a
    database. Revert to previous Markdown or overwrite the data when conflicts
    arise.
    """
    def __init__(self, other, parent_window, preferences,
                    note, html, current_field, selected_html):
        self.other                      = other
        self.parent_window              = parent_window
        self.col                        = mw.col
        print "self.server:", self.col.server
        self.db                         = mw.col.db
        self.preferences                = preferences
        self.note                       = note
        self.html                       = html
        self.current_field              = current_field
        self.selected_html              = selected_html
        self.current_note_id_and_field  = str(self.note.id) + \
                                          "-{:03}".format(self.current_field)
        self._init_db(self.db)
        self._id                        = None
        self.isconverted                = None
        self.md                         = None
        self._html                      = None
        self._lastmodified              = None
        self._usn                       = None
        self.has_data                   = self.get_data_from_db()
        self.apply_markdown()

    def _init_db(self, db):
        self.db.executescript("""
                create table if not exists markdown (
                    id              text primary key,
                    isconverted     text not null,
                    md              text not null,
                    html            text not null,
                    mod             integer not null,
                    usn             integer not null
                );""")
        print "INITIALIAZE DATABASE"

    def apply_markdown(self):
        clean_md = Utility.convert_html_to_markdown(self.html)
        # check for changed Markdown between the database and the current text
        if (self.has_data and self.isconverted == "True"):
            # if self.selected_html:
            #     # only convert the selected text
            #     clean_md = Utility.convert_html_to_markdown(self.selected_html)
            #     new_html = Utility.convert_markdown_to_html(self.preferences,
            #                                                 clean_md)
            #     self.other.web.eval(
            #             "document.execCommand('insertHTML', false, %s);"
            #             % json.dumps(new_html))
            #     self.store_new_markdown_version(new_html)
            #     return

            if not Utility.is_same_markdown(clean_md, self.md):
                self.handle_conflict()
            else:
                self.revert_to_stored_markdown()
        else:
            new_html = Utility.convert_markdown_to_html(self.preferences, clean_md)
            self.insert_markup_in_field(new_html, self.other.currentField)
            # store the Markdown so we can reuse it when the button gets toggled
            if clean_md:
                clean_md = Utility.escape_html_chars(clean_md)
                self.store_new_markdown_version(clean_md, new_html)

    # def get_data_from_db_old(self):
    #     """
    #     Set the first row of markup information from the database to variables.
    #     Return True when data is retrieved, False if the result set is empty.
    #     """
    #     sql = "select * from markdown where id=?"
    #     # data = Utility.execute_query(sql, self.current_note_id_and_field)
    #     data = self.db.first(sql, self.current_note_id_and_field)
    #     print "DATA WE GOT BACK FROM DB:", data
    #     if data:
    #         (self.id,
    #          self.isconverted,
    #          self.md,
    #          self._html,
    #          self.lastmodified) = data
    #         return True
    #     return False

    # def get_md_data_from_dict(self, data):
    #     """
    #     Set the markdown data associated with the note and field.
    #     Return True if data was found, False otherwise.
    #     """
    #     result = None
    #     for entry in data.keys():
    #         if entry == self.current_note_id_and_field:
    #             result = data[entry]
    #             break
    #     if result:
    #         self.md              = result.get("md")
    #         self._html           = result.get("html")
    #         self.isconverted     = result.get("isconverted")
    #         self.lastmodified    = result.get("lastmodified")
    #         print "DATA FROM DATABASE: {} : {} : {} : {}".format(
    #                 self.md, self._html, self.isconverted, self.lastmodified)
    #         return True
    #     return False

    def get_data_from_db(self):
        """
        Fill a variable with information from the database, if any.
        Return True when data is retrieved, False if the result set is empty.
        """
        sql = "select * from markdown where id=?"
        resultset = self.db.first(sql, self.current_note_id_and_field)
        print "DATA WE GOT BACK FROM DB:", resultset
        if resultset:
            (self._id,
             self.isconverted,
             self.md,
             self._html,
             self._lastmodified,
             self._usn) = resultset
            return True
        return False

    def insert_markup_in_field(self, markup, field):
        """
        Put markup in the specified field.
        """
        self.other.web.eval("""
            document.getElementById('f%s').innerHTML = %s;
        """ % (field, json.dumps(unicode(markup))))

    def disable_field(self, field):
        """
        Disable the specified contenteditable field.
        """
        pass

    def handle_conflict(self):
        """
        Show a warning dialog. Based on the user decision, either revert the
        changes to the text, replace the stored data, or cancel.
        """
        ret = self.show_overwrite_warning()
        if ret == 0:
            self.revert_to_stored_markdown()
        elif ret == 1:
            # overwrite database
            self.overwrite_stored_data()
        else:
            print "User canceled on warning dialog."

    def overwrite_stored_data(self):
        """
        Use the current HTML to update the stored Markdown and HTML in the
        database. Set the isconverted column to True.
        """
        clean_md = Utility.convert_html_to_markdown(self.html, keep_empty_lines=True)
        new_html = Utility.convert_clean_md_to_html(clean_md, put_breaks=True)
        print "INSERTING THIS:\n", new_html
        self.insert_markup_in_field(new_html, self.other.currentField)
        sql = """\
                update markdown
                set md=?, html=?, usn=?, mod=?
                where id=?
        """
        self.db.execute(sql, clean_md, new_html, self.col.usn(), intTime(),
                self.current_note_id_and_field)
        self.db.commit()

    def revert_to_stored_markdown(self):
        print "REVERTING TO OLD MARKDOWN"
        new_html = Utility.convert_clean_md_to_html(self.md)
        # print repr(new_html)
        self.insert_markup_in_field(new_html, self.other.currentField)
        # store the fact that the Markdown is currently not converted to HTML
        sql = """
            update markdown
            set isconverted=?, mod=?, usn=?
            where id=?
        """
        self.db.execute(sql, "False", intTime(), self.col.usn(),
                self.current_note_id_and_field)
        self.db.commit()

    def store_new_markdown_version(self, new_md, new_html):
        """
        Update current database with new data, or insert a new row into the
        database when there is no prior data.
        """
        update_stmt = """
            update markdown
            set isconverted=?, md=?, html=?, mod=?, usn=?
            where id=?
        """
        insert_stmt = """
            insert into markdown (id, isconverted, md, html, mod, usn)
            values (?, ?, ?, ?, ?, ?)
        """
        if self.has_data:
            self.db.execute(update_stmt, "True", new_md, new_html,
                    intTime(), self.col.usn(), self.current_note_id_and_field)
        else:
            self.db.execute(insert_stmt, self.current_note_id_and_field,
                    "True", new_md, new_html, intTime(), self.col.usn())
        self.db.commit()

    def show_overwrite_warning(self):
        """
        Show a warning modal dialog box, informing the user that the changes
        have taken place in the formatted text that are not in the Markdown.
        Returns a 0 for replacing the new changes with the database version of
        the Markdown, 1 for overwriting the database, and QMessageBox.Cancel for
        no action.
        """
        mess = QtGui.QMessageBox(self.parent_window)
        mess.setIcon(QtGui.QMessageBox.Warning)
        # TODO: think about putting the text of the dialog in property files
        mess.setWindowTitle("Content of card changed!")
        mess.setText("<b>The text of this field seems to have changed while "
                "Markdown mode was disabled, or the original syntax cannot be "
                "automatically restored.</b>")
        mess.setInformativeText("Please choose to either store "
                "your current version of this field (overwriting the old "
                "version), replace your current version with the stored "
                "version, or cancel.\n\nWARNING: Overwriting may result "
                "in the loss of of some of your stored Markdown syntax.")
        replaceButton = QtGui.QPushButton("&Replace", mess)
        mess.addButton(replaceButton, QtGui.QMessageBox.ApplyRole)
        mess.addButton("&Overwrite", QtGui.QMessageBox.ApplyRole)
        mess.setStandardButtons(QtGui.QMessageBox.Cancel)
        mess.setDefaultButton(replaceButton)
        return mess.exec_()
