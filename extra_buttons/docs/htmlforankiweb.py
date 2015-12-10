#!/usr/bin/python2
# -*- coding: utf-8 -*-

import BeautifulSoup
import re
import os
import sys
import string
import inspect
from _version import __version__

class HTMLForAnkiWeb(object):
    def __init__(self):
        self.template_dict = dict()
        self.put_constants_in_dict()
        self.curdir = os.path.dirname(os.path.abspath(
            inspect.getfile(inspect.currentframe())))
        self.doc_start_path = os.path.join(self.curdir, "doc_start.html")
        if (os.path.exists(self.doc_start_path)):
            with open(self.doc_start_path) as f:
                html = f.read()
                self.soup = BeautifulSoup.BeautifulSoup(html)
                self.body = self.soup.find(name="body")
        else:
            sys.exit("Path {!r} does not exist".format(path))

    def put_constants_in_dict(self):
        self.template_dict["version"] = __version__
        self.template_dict["new_features"] = self.create_new_features()

    def create_new_features(self):
        html = """\
            <li>
                Markdown support!
            </li>"""
        return html

    def get_buttons(self):
        """
        Build a dictionary of elements that consists of headers and text from
        lists.
        """
        buttons = self.soup.findAll(attrs={"class": "formatting-button"})
        for button in buttons:
            button_id = button.get("id").replace("-", "_")
            self.template_dict[button_id] = unicode(button.parent)

    def get_headings(self):
        """

        """
        for tag in self.soup.findAll(name="h2", attrs={"class": "heading"}):
            tag_id = tag.get("id").replace("-", "_")
            if tag_id == "formatting_buttons": continue
            self.template_dict[tag_id] = unicode(tag)
            next_elem = tag.nextSibling
            while True:
                if next_elem is None:
                    break
                if (isinstance(next_elem, BeautifulSoup.NavigableString)
                        or not next_elem.name.startswith("h2")):
                    self.template_dict[tag_id] = \
                            self.template_dict.get(tag_id, "") + \
                            unicode(next_elem)
                    next_elem = next_elem.nextSibling
                else:
                    break

    def replace_tags(self):
        replacement_dict = {
                "h1": self.replace_heading_with_bold_tag,
                "h2": self.replace_heading_with_bold_tag,
                "h3": self.replace_heading_with_bold_tag,
                "h4": self.replace_heading_with_bold_tag,
                "h5": self.replace_heading_with_bold_tag,
                "h6": self.replace_heading_with_bold_tag,
                "pre": self.replace_with_children,
                "em": self.replace_tag_with_other,
                "strong": self.replace_tag_with_other,
                "kbd": self.replace_tag_with_other,
                "blockquote": self.replace_with_children,
                "table": self.delete_tag,
                "thead": self.delete_tag,
                "tbody": self.delete_tag,
                "tr": self.delete_tag,
                "td": self.delete_tag,
                "p": self.replace_with_children
        }
        valid_tags = ("img", "a", "b", "i", "code", "ol", "ul", "li")
        for key, value in self.template_dict.iteritems():
            local_soup = BeautifulSoup.BeautifulSoup(value)
            all_tags = set()
            for tag in local_soup.findAll():
                all_tags.add(tag.name)
            for tag in all_tags:
                callback = replacement_dict.get(tag)
                if callback:
                    callback(local_soup, tag)
            self.template_dict[key] = unicode(local_soup)

    def replace_tag_with_other(self, soup_obj, old_name):
        replacement_dict = {
                "strong": "b",
                "em": "i",
                "kbd": "b"
        }
        elems = soup_obj.findAll(name=old_name)
        for elem in elems:
            elem.name = replacement_dict.get(elem.name)

    def replace_with_children(self, soup_obj, name_of_tag):
        elems = soup_obj.findAll(name=name_of_tag)
        for elem in elems:
            elem.replaceWithChildren()

    def delete_tag(self, soup_obj, name_of_tag):
        elems = soup_obj.findAll(name=name_of_tag)
        for elem in elems:
            elem.extract()

    def replace_heading_with_bold_tag(self, soup_obj, name_of_tag):
        elems = soup_obj.findAll(name=name_of_tag)
        for elem in elems:
            elem.name = "b" if name_of_tag[1] < "3" else "i"
            elem.string = elem.string.upper()

    def create_template(self):
        template = string.Template("""\
<b>IMPORTANT</b>: This add-on gets updated quite frequently, so before posting an error or giving it one star, please <b>update</b> the add-on. If, after updating, you still encounter a bug, <b>kindly post a bug report on <a href="https://github.com/Neftas/supplementary-buttons-anki/issues" rel="nofollow">GitHub</a></b>. I can't reply to your comments here, so if you want the issue fixed, you should really consider posting to GitHub.

<b>UPDATING</b> is easy. First, remove the add-on from Anki (<i>Tools &gt; Add-ons &gt; Supplementary buttons Anki &gt; Delete...</i>), then install it again by using the number at the bottom of this page.

<b>New in version ${version}:</b>
<ul>$new_features</ul>

$markdown

FORMATTING BUTTONS

Besides Markdown, this add-on adds the following supplementary formatting buttons to Anki:

<ul>

$code_button

Depending on your CSS definition, this may look like:

<img src="https://i.imgur.com/68WgA0x.png">

$unordered_list_button

$ordered_list_button

$indent_button

$outdent_button

$strikethrough_button

$pre_button

$horizontal_rule_button

$definition_list_button

$table_button

<img src="https://i.imgur.com/Ms3Yzpr.gif">

$keyboard_button

Depending on your CSS, this may look like:

<img src="http://i.imgur.com/K835QyO.png"></li>

$hyperlink_button

$highlight_button

$blockquote_button

$alignment_button

$heading_button

</ul>
$custom_user_defined_keybindings

$disabling_unused_buttons

<b>SOURCE CODE</b>
The source code is available on <a href="https://github.com/Neftas/supplementary-buttons-anki" rel="nofollow">GitHub</a>. If you have any issues, please report them there!

<b>CHANGELOG</b>
--------------------------------------------------
28-08-2014 <b>v0.1.0</b>: initial release
29-08-2014 <b>v0.1.1</b>: bug fix and outdent button added
30-08-2014 <b>v0.1.2</b>: &lt;code&gt; element bug fixed
03-09-2014 <b>v0.1.3</b>: added definition lists and tables
06-09-2014 <b>v0.1.4</b>: bug fixes
24-09-2014 <b>v0.2.0</b>: definition list greatly improved and tables redesigned with light look
25-09-2014 <b>v0.2.1</b>: added proper icons
28-09-2014 <b>v0.2.2</b>: bug fixed with empty definition list
11-10-2014 <b>v0.2.3</b>: bug fix for code tag and improved pre tags to also include a CSS class
19-10-2014 <b>v0.2.4</b>: changed shortcuts for indent and outdent buttons, because they interfered with core Anki shortcuts in Browser
24-10-2014 <b>v0.3.0</b>: improved tables: selected text can now be converted to a table; added hyperlink and keyboard key buttons; improved options menu
25-10-2014 <b>v0.3.1</b>: bug fix with hyperlinks where it would in some cases incorrectly prepend a second <code>http://</code>
27-10-2014 <b>v0.3.2</b>: bug fix where empty lists would be duplicated to complete field when using &lt;code&gt; format
28-10-2014 <b>v0.3.3</b>: added Unicode support to stop tables and other stuff from breaking when non-English is entered (sorry about that :), added optional alignment to tables
16-11-2014 <b>v0.4.0</b>: added text background color
25-11-2014 <b>v0.4.1</b>: add-on now remembers last used color
25-11-2014 <b>v0.4.2</b>: bug fixes
17-02-2015 <b>v0.5.0</b>: highlight colors on all platforms! (yes, it took it while) added text alignment, headings, and blockquotes
24-02-2015 <b>v0.5.1</b>: fixed preference handling, it will now revert to the default settings upon encountering an error; bug fix for tables where HTML (or anything in brackets) wouldn't be escaped; changed shortcut for text align center to Ctrl+Shift+Alt+B to prevent conflict with cloze deletions
24-02-2015 <b>v0.5.2</b>: fixed bug in path location of preference file (was hard-coded)
22-05-2015 <b>v0.6.0</b>: enhanced types of ordered list, added &lt;abbr&gt; tag, added About dialog, cleaned up preferences, refactored code
26-05-2015 <b>v0.6.1</b>: re-enabled text highlighting on Mac OS X and Windows
29-09-2015 <b>v0.7.0</b>: added user-defined keybindings; added author to blockquote
29-11-2015 <b>v0.8.0</b>: added Markdown
""")
        return template.safe_substitute(self.template_dict)

    def fill_in_template(self):
        # template = self.create_template()
        # for key, value in self.template_dict.iteritems():
        #     template = template.safe_substitute(dict(key=value))
        # print template
        pass

if __name__ == "__main__":
    webanki = HTMLForAnkiWeb()
    webanki.get_buttons()
    webanki.get_headings()
    webanki.replace_tags()
    html = webanki.create_template()
    path = os.path.join(os.path.dirname(os.path.abspath(
        inspect.getfile(inspect.currentframe()))), "ankiweb.html")
    print "Path is: {!r}".format(path)
    with open(path, "w") as f:
        f.write(html)
        print "Written {!r}".format(path)
    print "Succesfully written file. Exiting..."
