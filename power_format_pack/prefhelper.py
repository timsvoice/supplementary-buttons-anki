# -*- coding: utf-8 -*-
#
# Copyright 2014-2017 Stefan van den Akker <neftas@protonmail.com>
#
# This file is part of Power Format Pack.
#
# Power Format Pack is free software: you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Power Format Pack is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with Power Format Pack. If not, see http://www.gnu.org/licenses/.


import base64
import codecs
import const
import copy
import os
import utility
from PyQt4 import QtGui

from anki.utils import json, isMac
from aqt import mw as main_window


class PrefHelper(object):
    """
    Static methods related to preference handling.
    """

    @staticmethod
    def get_preference_path():
        return os.path.join(PrefHelper.get_addons_folder(),
                            const.FOLDER_NAME,
                            ".extra_buttons_prefs")

    @staticmethod
    def get_keybindings_path():
        if isMac:
            filename = "keybindings_macosx"
        else:
            filename = "keybindings_linux_windows"

        return os.path.join(PrefHelper.get_addons_folder(),
                            const.FOLDER_NAME,
                            filename)

    @staticmethod
    def normalize_user_prefs(default_prefs, user_prefs):
        """
        Check if the user preferences are compatible with the currently used
        preferences within the addon. Add keys if they don't exist, and remove
        those that are not recognized. Return a dictionary with the checked
        preferences.
        >>> default_prefs   = dict(b="two")
        >>> user_prefs      = dict(a="one")
        >>> normalize_user_prefs(default_prefs, user_prefs)
        {u'b': u'two'}
        """

        result_dict = user_prefs
        # add items that are not in prefs, but should be (e.g. after update)
        for key, value in default_prefs.iteritems():
            user_val = user_prefs.get(key)
            if user_val is None:
                result_dict[key] = value
        # delete items in prefs that should not be there (e.g. after update)
        for key in user_prefs.keys()[:]:
            if default_prefs.get(key) is None:
                del result_dict[key]

        return result_dict

    @staticmethod
    def get_default_preferences():
        # the default preferences that are used when no custom preferences
        # are found, or when the user preferences are corrupted
        _default_conf = {
                const.CODE_CLASS:                   const.CODE_AND_PRE_CLASS,
                const.LAST_BG_COLOR:                "#00f",
                const.FIXED_OL_TYPE:                "",
                const.MARKDOWN_SYNTAX_STYLE:        "tango",
                const.MARKDOWN_CODE_DIRECTION:      "left",
                const.MARKDOWN_LINE_NUMS:           False,
                const.MARKDOWN_ALWAYS_REVERT:       False,
                const.MARKDOWN_OVERRIDE_EDITING:    False,
                const.MARKDOWN_CLASSFUL_PYGMENTS:   False,
                const.BUTTON_PLACEMENT:             "adjacent",
                const.CODE:                         True,
                const.UNORDERED_LIST:               True,
                const.ORDERED_LIST:                 True,
                const.STRIKETHROUGH:                True,
                const.PRE:                          True,
                const.HORIZONTAL_RULE:              True,
                const.INDENT:                       True,
                const.OUTDENT:                      True,
                const.DEFINITION_LIST:              True,
                const.TABLE:                        True,
                const.STYLE_TABLE:                  True,
                const.KEYBOARD:                     True,
                const.HYPERLINK:                    True,
                const.BACKGROUND_COLOR:             True,
                const.BLOCKQUOTE:                   True,
                const.TEXT_ALLIGN:                  True,
                const.HEADING:                      True,
                const.ABBREVIATION:                 True,
                const.MARKDOWN:                     False
        }

        return _default_conf

    @staticmethod
    def get_default_keybindings():
        # the default keybindings that are used when no custom keybindings
        # are found, or when the user keybindings are corrupted
        _default_keybindings_linux_windows = {
                const.CODE:                         u"ctrl+,",
                const.UNORDERED_LIST:               u"ctrl+[",
                const.ORDERED_LIST:                 u"ctrl+]",
                const.STRIKETHROUGH:                u"alt+shift+5",
                const.PRE:                          u"ctrl+.",
                const.HORIZONTAL_RULE:              u"ctrl+shift+alt+_",
                const.INDENT:                       u"ctrl+shift+]",
                const.OUTDENT:                      u"ctrl+shift+[",
                const.DEFINITION_LIST:              u"ctrl+shift+d",
                const.TABLE:                        u"ctrl+shift+3",
                const.KEYBOARD:                     u"ctrl+shift+k",
                const.HYPERLINK:                    u"ctrl+shift+h",
                const.REMOVE_HYPERLINK:             u"ctrl+shift+alt+h",
                const.BACKGROUND_COLOR:             u"ctrl+shift+b",
                const.BACKGROUND_COLOR_CHANGE:      u"ctrl+shift+n",
                const.BLOCKQUOTE:                   u"ctrl+shift+y",
                const.TEXT_ALLIGN_FLUSH_LEFT:       u"ctrl+shift+alt+l",
                const.TEXT_ALLIGN_FLUSH_RIGHT:      u"ctrl+shift+alt+r",
                const.TEXT_ALLIGN_JUSTIFIED:        u"ctrl+shift+alt+s",
                const.TEXT_ALLIGN_CENTERED:         u"ctrl+shift+alt+b",
                const.HEADING:                      u"ctrl+alt+1",
                const.ABBREVIATION:                 u"shift+alt+a",
                const.MARKDOWN:                     u"ctrl+shift+0"
        }
        # Mac OS keybindings are the same as Linux/Windows bindings,
        # except for the following
        _default_keybindings_macosx = \
            copy.deepcopy(_default_keybindings_linux_windows)
        _default_keybindings_macosx[const.CODE] = u"ctrl+shift+,"
        _default_keybindings_macosx[const.PRE] = u"ctrl+shift+."

        if isMac:
            return _default_keybindings_macosx
        else:
            return _default_keybindings_linux_windows

    @staticmethod
    def get_addons_folder():
        """
        Return the addon folder used by Anki.
        """
        return main_window.pm.addonFolder()

    @staticmethod
    def save_prefs(prefs):
        """
        Save the preferences to disk, base64 encoded.
        """
        encoded_prefs = base64.b64encode(json.dumps(prefs))
        with codecs.open(PrefHelper.get_preference_path(), "w", encoding="utf8") as f:
            f.write(encoded_prefs)

    # @staticmethod
    # def get_current_preferences():
    #     prefs = None
    #     try:
    #         with codecs.open(PrefHelper.get_preference_path(), encoding="utf8") as f:
    #             encoded_prefs = f.read(const.MAX_BYTES_PREFS)
    #             decoded_prefs = base64.b64decode(encoded_prefs)
    #             prefs = json.loads(decoded_prefs)
    #     except:
    #         # file does not exist or is corrupted: fall back to default
    #         with codecs.open(PrefHelper.get_preference_path(), "w", encoding="utf8") as f:
    #             prefs = PrefHelper.get_default_preferences()
    #             json.dump(prefs, f)
    #     else:
    #         prefs = PrefHelper.normalize_user_prefs(
    #                 PrefHelper.get_default_preferences(), prefs)
    #         PrefHelper.save_prefs(prefs)

    #     return prefs

    @staticmethod
    def load_preferences_from_disk():
        """
        Load the current preferences from disk. If no preferences file is
        found, or if it is corrupted, return the default preferences.
        """
        prefs = None
        try:
            with codecs.open(PrefHelper.get_preference_path(), encoding="utf8") as f:
                encoded_prefs = f.read(const.MAX_BYTES_PREFS)
                decoded_prefs = base64.b64decode(encoded_prefs)
                prefs = json.loads(decoded_prefs)
        except:
            prefs = PrefHelper.get_default_preferences()
        else:
            prefs = PrefHelper.normalize_user_prefs(
                        PrefHelper.get_default_preferences(), prefs)

        return prefs

    @staticmethod
    def are_prefs_changed(current, new):
        """
        Return `True` if `current` and `new` contain different values for the
        same key, `False` if all values for the same keys are equal.
        """
        for k, v in current.iteritems():
            if current.get(k) != new.get(k):
                return True
        return False

    @staticmethod
    def get_current_keybindings():
        keybindings = None
        try:
            with codecs.open(PrefHelper.get_keybindings_path(), encoding="utf8") as f:
                # validate JSON
                result_json = u""
                for line in f:
                    line = line.strip()
                    if line == u"":
                        continue
                    # strip out comments from keybindings file
                    if line.startswith(u"//"):
                        continue
                    else:
                        result_json += line
                keybindings = json.loads(result_json)
        except (ValueError, IOError) as e:
            # file is missing or is not valid JSON: revert to default bindings
            # and create a keybindings file if it doesn't exist
            print e  # TODO: log error
            if not os.path.exists(PrefHelper.get_keybindings_path()):
                PrefHelper.create_keybindings_file()
            return PrefHelper.get_default_keybindings()
        else:
            # keybindings loaded from file should have exactly as many
            # key-value pairs as in the default keybindings
            default_keybindings = PrefHelper.get_default_keybindings()
            keybindings = PrefHelper.normalize_user_prefs(
                    default_keybindings, keybindings)
            keybindings = utility.check_user_keybindings(
                    default_keybindings, keybindings, const.PLATFORM)

        return keybindings

    @staticmethod
    def create_keybindings_file():
        """
        Create a default keybindings file with comments. This function is
        called when Power Format Pack cannot find an existing
        keybindings file. Override any changes made to an existing file.
        """

        config_path = os.path.join(PrefHelper.get_addons_folder(),
                                   const.FOLDER_NAME,
                                   const.CONFIG_FILENAME)
        c = utility.get_config_parser(config_path)

        contents = c.get(const.CONFIG_KEYBINDINGS, "help_text")
        contents += u"\n\n{\n"

        for key, value in sorted(PrefHelper.get_default_keybindings().iteritems()):
            contents += u"    \"{}\": \"{}\",\n".format(key, value)

        contents += u"    \"_version\": \"{}\"\n".format(const.VERSION)
        contents += u"}"

        try:
            with codecs.open(PrefHelper.get_keybindings_path(), "w", encoding="utf8") as f:
                f.write(contents)
        except IOError as e:
            raise e

    @staticmethod
    def set_icon(button, name):
        """
        Define the path for the icon the corresponding button should have.
        """
        icon_path = os.path.join(PrefHelper.get_addons_folder(),
                                 const.FOLDER_NAME,
                                 "icons",
                                 "{}.png".format(name))
        button.setIcon(QtGui.QIcon(icon_path))
