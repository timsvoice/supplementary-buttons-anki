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

from PyQt4 import QtGui, QtCore
from power_format_pack.prefhelper import PrefHelper
import os
import const


class Button(QtGui.QPushButton):
    """
    Represents a clickable button.
    """

    def __init__(self, name, shortcut, tooltip, callback, text=""):
        super(Button, self).__init__(text)
        self.name = name
        self.setShortcut(shortcut)
        self.setToolTip(tooltip)
        self.clicked.connect(callback)
        self.setFixedHeight(20)
        self.setFixedWidth(20)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setIcon(self.name)

    def setIcon(self, name):
        """
        Set icon by `name`.
        """
        c = PrefHelper.get_config()
        icon_path = os.path.join(PrefHelper.get_addons_folder(),
                                 c.get(const.CONFIG_DEFAULT, "FOLDER_NAME"),
                                 "icons",
                                 "{}.png".format(name))
        super(Button, self).setIcon(QtGui.QIcon(icon_path))
