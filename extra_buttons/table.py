# -*- coding: utf-8 -*-
#
# Copyright 2014-2016 Stefan van den Akker <srvandenakker.dev@gmail.com>
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

import json

from PyQt4 import QtGui, QtCore
import utility


class Table(object):
    """
    Create a table.
    """
    def __init__(self, other, parent_window, selected_text):
        self.editor_instance    = other
        self.parent_window      = parent_window
        self.selected_text      = selected_text
        self.setup()

    def setup(self):
        """
        Set the number of columns and rows for a new table.
        """

        # if the user has selected text, try to make a table out of it
        if self.selected_text:
            is_table_created = self.create_table_from_selection()
            # if we could not make a table out of the selected text, present
            # user with dialog, otherwise do nothing
            if is_table_created:
                return None

        dialog = QtGui.QDialog(self.parent_window)
        dialog.setWindowTitle("Enter columns and rows")

        form = QtGui.QFormLayout()
        form.addRow(QtGui.QLabel("Enter the number of columns and rows"))

        columnSpinBox = QtGui.QSpinBox(dialog)
        columnSpinBox.setMinimum(1)
        columnSpinBox.setMaximum(10)
        columnSpinBox.setValue(2)
        columnLabel = QtGui.QLabel("Number of columns:")
        form.addRow(columnLabel, columnSpinBox)

        rowSpinBox = QtGui.QSpinBox(dialog)
        rowSpinBox.setMinimum(1)
        rowSpinBox.setMaximum(20)
        rowSpinBox.setValue(3)
        rowLabel = QtGui.QLabel("Number of rows:")
        form.addRow(rowLabel, rowSpinBox)

        buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok |
                                           QtGui.QDialogButtonBox.Cancel,
                                           QtCore.Qt.Horizontal,
                                           dialog)

        buttonBox.accepted.connect(dialog.accept)
        buttonBox.rejected.connect(dialog.reject)

        form.addRow(buttonBox)

        dialog.setLayout(form)

        if dialog.exec_() == QtGui.QDialog.Accepted:

            num_columns = columnSpinBox.value()
            num_rows = rowSpinBox.value() - 1

            num_header = utility.counter(start=1, step=1)
            num_data = utility.counter(start=1, step=1)

            # set width of each column equal
            width = 100 / num_columns

            header_html = \
                u"<th align=\"left\" style=\"width: {0}%; padding: 5px;" \
                + u"border-bottom: 2px solid #00B3FF\">header{1}</th>"
            header_column = "".join(header_html.format(
                    width, next(num_header)) for _ in xrange(num_columns))
            body_html = \
                u"<td style=\"padding: 5px; border-bottom:" \
                + u"1px solid #B0B0B0\">data{}</td>"
            body_column = "".join(
                body_html.format(next(num_data)) for _ in xrange(num_columns))
            body_row = "<tr>{}</tr>".format(body_column) * num_rows

            html = u"""
            <table style="width: 100%; border-collapse: collapse;">
                <thead><tr>{0}</tr></thead>
                <tbody>{1}</tbody>
            </table>""".format(header_column, body_row)

            self.editor_instance.web.eval(
                    "document.execCommand('insertHTML', false, %s);"
                    % json.dumps(html))

    def create_table_from_selection(self):
        """
        Create a table out of the selected text.
        """

        # there is no text to make a table from
        if not self.selected_text:
            return False

        # there is a single line of text
        if not self.selected_text.count(u"\n"):
            return False

        # there is no content in table
        if all(c in (u"|", u"\n") for c in self.selected_text):
            return False

        # split on newlines
        first = [x for x in self.selected_text.split(u"\n") if x]

        # split on pipes
        second = list()
        for elem in first[:]:
            new_elem = [x.strip() for x in elem.split(u"|")]
            new_elem = [utility.escape_html_chars(word) for word in new_elem]
            second.append(new_elem)

        # keep track of the max number of cols
        # so as to make all rows of equal length
        max_num_cols = len(max(second, key=len))

        # decide how much horizontal space each column may take
        width = 100 / max_num_cols

        # check for "-|-|-" alignment row
        if all(x.strip(u":") in (u"-", u"") for x in second[1]):
            start = 2
            align_line = second[1]
            len_align_line = len(align_line)
            if len_align_line < max_num_cols:
                align_line += [u"-"] * (max_num_cols - len_align_line)
            alignments = list()
            for elem in second[1]:
                alignments.append(utility.check_alignment(elem))
        else:
            alignments = [u"left"] * max_num_cols
            start = 1

        # create a table
        head_row = u""
        head_html = \
            u"<th align=\"{0}\" style=\"width: {1}%; padding: 5px;" \
            + u"border-bottom: 2px solid #00B3FF\">{2}</th>"
        for elem, alignment in zip(second[0], alignments):
            head_row += (head_html.format(alignment, width, elem))
        extra_cols = u""
        if len(second[0]) < max_num_cols:
            diff = len(second[0]) - max_num_cols
            assert diff < 0, "Difference between len(second[0]) and max_num_cols is positive"
            extra_html = \
                u"<th align=\"{0}\" style=\"width: {1}%; padding: 5px;" \
                + u"border-bottom: 2px solid #00B3FF\"></th>"
            for alignment in alignments[diff:]:
                extra_cols += (extra_html.format(alignment, width))
        head_row += extra_cols

        body_rows = u""
        for row in second[start:]:
            body_rows += u"<tr>"
            body_html = \
                u"<td style=\"text-align: {0}; padding: 5px; border-bottom:" \
                + u"1px solid #B0B0B0\">{1}</td>"
            for elem, alignment in zip(row, alignments):
                body_rows += (body_html.format(alignment, elem))
            # if particular row is not up to par with number of cols
            extra_cols = ""
            if len(row) < max_num_cols:
                diff = len(row) - max_num_cols
                assert diff < 0, "Difference between len(row) and max_num_cols is positive"
                extra_html = \
                    u"<td style=\"text-align: {0}; padding: 5px;" \
                    + u"border-bottom: 1px solid #B0B0B0\"></td>"
                for alignment in alignments[diff:]:
                    extra_cols += (extra_html.format(alignment))
            body_rows += extra_cols + "</tr>"

        html = u"""
        <table style="width: 100%; border-collapse: collapse;">
            <thead>
                <tr>
                    {0}
                </tr>
            </thead>
            <tbody>
                {1}
            </tbody>
        </table>""".format(head_row, body_rows)

        self.editor_instance.web.eval(
                "document.execCommand('insertHTML', false, %s);"
                % json.dumps(html))

        return True
