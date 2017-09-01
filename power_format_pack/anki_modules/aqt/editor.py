# -*- coding: utf-8 -*-
# Copyright: Damien Elmes <anki@ichi2.net>
# Changes: Stefan van den Akker <neftas@protonmail.com>

from BeautifulSoup import BeautifulSoup

import aqt
from aqt.qt import *
from aqt.utils import openHelp
from power_format_pack import const


def onHtmlEdit(self):
    self.saveNow()
    d = QDialog(self.widget)
    form = aqt.forms.edithtml.Ui_Dialog()
    form.setupUi(d)
    d.connect(form.buttonBox, SIGNAL("helpRequested()"), lambda: openHelp("editor"))
    org_html = self.note.fields[self.currentField]
    html_without_data = org_html
    start_md_data = org_html.find(const.START_HTML_MARKER)
    end_md_data = org_html.find(const.END_HTML_MARKER, start_md_data)
    contains_data = start_md_data != -1 and end_md_data != -1
    if contains_data:
        md_data = org_html[start_md_data:(end_md_data + len(const.END_HTML_MARKER))]
        html_without_data = org_html[:start_md_data] + org_html[end_md_data + len(const.END_HTML_MARKER):]
    form.textEdit.setPlainText(html_without_data)
    form.textEdit.moveCursor(QTextCursor.End)
    d.exec_()
    html = form.textEdit.toPlainText()
    if contains_data:
        html += md_data
    # filter html through beautifulsoup so we can strip out things like a
    # leading </div>
    html = unicode(BeautifulSoup(html))
    self.note.fields[self.currentField] = html
    self.loadNote()
    # focus field so it's saved
    self.web.setFocus()
    self.web.eval("focusField(%d);" % self.currentField)


