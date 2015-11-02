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
from anki.hooks import addHook

from utility import Utility
import const


class Markdowner(object):
    """
    Convert HTML to Markdown and the other way around. Store the data in a
    database. Revert to previous Markdown or overwrite the data when conflicts
    arise.
    """
    # signal that we don't want the onEdit focus behavior
    button_pressed = False

    def __init__(self, other, parent_window, preferences, note, html,
                 current_field, selected_html):
        self.other                      = other
        self.parent_window              = parent_window
        self.col                        = mw.col
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
        self.has_data                   = self.get_data_from_field()
        self.check_for_data_existence()

    def _init_db(self, db):
        """
        Initialize the markdown database.
        """
        self.db.executescript("""
                create table if not exists markdown (
                    id              text primary key,
                    isconverted     text not null,
                    md              text not null,
                    html            text not null,
                    mod             integer not null
                );""")
        print "INITIALIAZE DATABASE"

    def on_focus_gained(self):
        if self.isconverted:
            self.warn_about_changes(self.current_field, const.MARKDOWN_BG_COLOR)

    def current_field_exists_in_db(self):
        """
        Check if the current field exists in the database. Return True if
        it does, False otherwise.
        """
        sql = "select 1 from markdown where id=?"
        if self.db.first(sql, self.current_note_id_and_field):
            return True
        return False

    def check_for_data_existence(self):
        """
        Check if the data from the field also exists in the database. If it
        exists, but differs, update the database to reflect the changes.
        """
        if self.has_data and self.current_field_exists_in_db():
        # check timestamps and store if newer version
            timestamp_field = self._lastmodified
            timestamp_db = self.db.first("select mod from markdown where id=?",
                                         self.current_note_id_and_field)[0]
            print "timestamp db:", repr(timestamp_db)
            print "timestamp field:", repr(timestamp_field)
            print "field >= db:", timestamp_field >= timestamp_db
            assert timestamp_field >= timestamp_db, \
                    "field timestamp is older than db timestamp!"
            if timestamp_field > timestamp_db:
                self.store_new_markdown_version_in_db(
                    self.isconverted, self.md, self._html, self._lastmodified)

    def apply_markdown(self):
        clean_md = Utility.convert_html_to_markdown(self.html)
        clean_md_escaped = Utility.escape_html_chars(clean_md)
        if not clean_md:
            return
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
            #     self.store_new_markdown_version_in_db(new_html)
            #     return

            if not Utility.is_same_markdown(clean_md, self.md):
                self.handle_conflict()
            else:
                self.revert_to_stored_markdown()
        else:
            new_html = Utility.convert_markdown_to_html(self.preferences,
                                                        clean_md)
            html_with_data = Utility.make_data_ready_to_insert(
                    self.current_note_id_and_field, "True",
                    clean_md_escaped, new_html)
            self.insert_markup_in_field(html_with_data, self.other.currentField)
            # store the Markdown so we can reuse it when the button gets toggled
            self.store_new_markdown_version_in_db(
                    "True", clean_md_escaped, new_html)
            self.warn_about_changes(self.current_field, const.MARKDOWN_BG_COLOR)

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
             self._lastmodified) = resultset
            return True
        return False

    def get_data_from_field(self):
        """
        Get the HTML from the current field and try to extract Markdown data
        from it. The side effect of calling this function is that several
        instance variables get set. Return True when data was found in the
        field, False otherwise.
        """
        md_dict = Utility.get_md_data_from_string(self.html)
        if md_dict and md_dict == "corrupted":
            # TODO: fallback when JSON is corrupted
            pass
        elif md_dict:
            self._id            = md_dict.get("id")
            self.md             = md_dict.get("md")
            self._html          = md_dict.get("html")
            self.isconverted    = md_dict.get("isconverted")
            self._lastmodified  = md_dict.get("lastmodified")
            print "DATA FROM FIELD:\n{}\n{}\n{}\n{}".format(
                    self.md, self._html, self.isconverted, self._lastmodified)
            return True
        return False

    def insert_markup_in_field(self, markup, field):
        """
        Put markup in the specified field.
        """
        self.other.web.eval("""
            document.getElementById('f%s').innerHTML = %s;
        """ % (field, json.dumps(unicode(markup))))

    def warn_about_changes(self, field, color):
        """
        Disable the specified contenteditable field.
        """
        warning_text = "WARNING: changes you make here will be lost when you " + \
        "toggle the Markdown button again."
        self.other.web.eval("""
            if (document.getElementById('mdwarn%s') === null) {
                var style_tag = document.getElementsByTagName('style')[0];
                style_tag.innerHTML += '#f%s { background-color: %s !important; }\\n'
                console.log('style: ' + style_tag.innerHTML);
                var field = document.getElementById('f%s');
                field.setAttribute('title', '%s');
                var warn_div = document.createElement('div');
                warn_div.id = 'mdwarn%s';
                warn_div.setAttribute('style', 'margin: 10px 0px;');
                var text = document.createTextNode('%s');
                warn_div.appendChild(text);
                field.parentNode.insertBefore(warn_div, field.nextSibling);
            }
        """ % (field, field, color, field, warning_text, field, warning_text))

    def remove_warn_msg(self):
        self.other.web.eval("""
            if (document.getElementById('mdwarn%s') !== null) {
                var style_tag = document.getElementsByTagName('style')[0];
                style_tag.innerHTML = style_tag.innerHTML.replace(/^#f%s.*/m, '');
                console.log('style: ' + style_tag.innerHTML);
                var field = document.getElementById('f%s');
                field.removeAttribute('title');
                var warn_msg = document.getElementById('mdwarn%s');
                warn_msg.parentNode.removeChild(warn_msg);
            }
        """ % (self.current_field, self.current_field, self.current_field,
                self.current_field))

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
        Create new Markdown from the current HTML. Remove the data about the current
        field from the database.
        """
        clean_md = Utility.convert_html_to_markdown(
                self.html, keep_empty_lines=True)
        new_html = Utility.convert_clean_md_to_html(
                clean_md, put_breaks=True)
        print "INSERTING THIS:\n", new_html
        self.insert_markup_in_field(new_html, self.other.currentField)
        sql = """
            delete from markdown
            where id=?
        """
        self.db.execute(sql, self.current_note_id_and_field)
        self.db.commit()
        self.remove_warn_msg()

    def revert_to_stored_markdown(self):
        print "REVERTING TO OLD MARKDOWN"
        new_html = Utility.convert_clean_md_to_html(self.md)
        # new_html = Utility.make_data_ready_to_insert(
        #         self.current_note_id_and_field, "False", self.md, new_html)
        print "Inserting this:", repr(new_html)
        self.insert_markup_in_field(new_html, self.other.currentField)
        self.other.saveNow()
        # store the fact that the Markdown is currently not converted to HTML
        sql = """
            update markdown
            set isconverted=?, mod=?
            where id=?
        """
        self.db.execute(sql, "False", intTime(), self.current_note_id_and_field)
        self.db.commit()
        self.remove_warn_msg()

    def store_new_markdown_version_in_db(self, isconverted, new_md, new_html,
                                         lastmodified=None):
        """
        Update current database with new data, or insert a new row into the
        database when there is no prior data.
        """
        replace_stmt = """
            insert or replace into markdown (id, isconverted, md, html, mod)
            values (?, ?, ?, ?, ?)
        """
        self.db.execute(replace_stmt, self.current_note_id_and_field,
                        isconverted, new_md, new_html,
                        intTime() if lastmodified is None else lastmodified)
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
