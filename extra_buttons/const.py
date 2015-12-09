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

import sys

class _Const(object):
    """Define constants that can be set once, and cannot
    be changed afterwards."""
    class ConstantError(TypeError): pass
    def __setattr__(self, name, value):
        """Check if the constant is already defined. If so, raise an error.
        If not, add the constant as a constant field."""
        if name in self.__dict__:
            raise self.ConstantError("Can't rebind name {0!r}".format(name))
        else:
            self.__dict__[name] = value

# importing modules can directly add constants and
# don't have to worry about instantiating _Const
sys.modules[__name__] = _Const()
