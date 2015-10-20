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
        self.db                         = mw.col.db
        self.preferences                = preferences
        self.note                       = note
        self.html                       = html
        self.current_field              = current_field
        self.selected_html              = selected_html
        self.current_note_id_and_field  = str(self.note.id) + \
                                          "-{:03}".format(self.current_field)
        self._init_db(self.db)
        self.has_data                   = self.get_data_from_db()
        self.apply_markdown()

    def _init_db(self, db):
        db.executescript("""
            create table if not exists markdown (
                id text primary key,
                isconverted text not null,
                md text not null,
                html text not null,
                lastmodified integer not null
            );
        """)
        print "SUCCESFULLY INITIALIZED DATABASE"

    def apply_markdown(self):
        # data is a list of tuples: [(id, isconverted, md, html, lastmodified)]
        clean_md = Utility.convert_html_to_markdown(self.html)
        print "clean_md from apply_markdown:\n", clean_md
        # check for changed Markdown between the database and the current text
        if (self.has_data and self.isconverted == "True"):
            if self.selected_html:
                # only convert the selected text
                clean_md = Utility.convert_html_to_markdown(self.selected_html)
                new_html = Utility.convert_markdown_to_html(self.preferences,
                                                            clean_md)
                self.other.web.eval(
                        "document.execCommand('insertHTML', false, %s);"
                        % json.dumps(new_html))
                self.store_new_markdown_version(new_html)
                return

            if not Utility.is_same_markdown(clean_md, self.md):
                self.handle_conflict()
            else:
                self.revert_to_stored_markdown()
        else:
            new_html = Utility.convert_markdown_to_html(self.preferences, clean_md)
            self.insert_new_markup(new_html)
            # store the Markdown so we can reuse it when the button gets toggled
            if clean_md:
                self.store_new_markdown_version(clean_md, new_html)

    def get_data_from_db(self):
        """
        Set the first row of markup information from the database to variables.
        Return True when data is retrieved, False if the result set is empty.
        """
        sql = "select * from markdown where id=?"
        # data = Utility.execute_query(sql, self.current_note_id_and_field)
        data = self.db.first(sql, self.current_note_id_and_field)
        print "DATA WE GOT BACK FROM DB:", data
        if data:
            (self.id,
             self.isconverted,
             self.md,
             self._html,
             self.lastmodified) = data
            return True
        return False

    def insert_new_markup(self, markup):
        """
        Put markup in the current field.
        """
        self.other.web.eval("""
            document.getElementById('f%s').innerHTML = %s;
        """ % (self.other.currentField, json.dumps(unicode(markup))))

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
        # new_html = Utility.convert_markdown_to_html(self.preferences, new_md)
        print "INSERTING THIS:\n", new_html
        self.insert_new_markup(new_html)
        # sql = """\
        #         update markdown
        #         set isconverted=?, md=?, html=?
        #         where id=?
        # """
        # Utility.execute_query(sql, "True", new_md, new_html,
        #         self.current_note_id_and_field)
        sql = """\
                update markdown
                set isconverted=?, md=?, lastmodified=?
                where id=?
        """
        # Utility.execute_query(sql, "False", clean_md,
        #         intTime(1000), self.current_note_id_and_field)
        self.db.execute(sql, "False", clean_md,
                intTime(1000), self.current_note_id_and_field)
        self.db.commit()

    def revert_to_stored_markdown(self):
        print "REVERTING TO OLD MARKDOWN"
        # stored_md = self.data[0][2]
        new_html = Utility.convert_clean_md_to_html(self.md)
        print repr(self.md)
        self.insert_new_markup(new_html)
        # store the fact that the Markdown is currently not converted to HTML
        sql = "update markdown set isconverted=?, lastmodified=? where id=?"
        # Utility.execute_query(sql, "False", self.current_note_id_and_field)
        self.db.execute(sql, "False",
                intTime(1000), self.current_note_id_and_field)
        self.db.commit()

    def store_new_markdown_version(self, clean_md, new_html):
        """
        Update current database with new data, or insert a new row into the
        database when there is no prior data.
        """
        update_sql = """\
                update markdown
                set isconverted=?, md=?, html=?, lastmodified=?
                where id=?
        """
        insert_sql = """\
                insert into markdown (id, isconverted, md, html, lastmodified)
                values (?, ?, ?, ?, ?)
        """
        if self.has_data:
            # Utility.execute_query(update_sql, "True", clean_md, new_html,
            #         self.current_note_id_and_field)
            self.db.execute(update_sql, "True", clean_md, new_html,
                    intTime(1000), self.current_note_id_and_field)
        else:
            # Utility.execute_query(insert_sql, self.current_note_id_and_field,
            #         "True", clean_md, new_html)
            self.db.execute(insert_sql, self.current_note_id_and_field,
                    "True", clean_md, new_html, intTime(1000))
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
