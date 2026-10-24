# -*- coding: UTF-8 -*-

'''
Module
    canvas_settings.py
Copyright
    Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>
    scarajectory is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by the
    Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    scarajectory is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    See the GNU General Public License for more details.
    You should have received a copy of the GNU General Public License along
    with this program. If not, see <http://www.gnu.org/licenses/>.
Info
    Defines CanvasSettings data transfer object for editor settings.
'''

from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True, kw_only=True)
class CanvasSettings:
    '''
        DTO encapsulating default canvas creation settings and workspace restrictions.

        It defines:

            :attributes:
                | DEFAULT_Z_MM - Default Z coordinate for new points in mm.
                | DEFAULT_SPEED_MMS - Default feedrate speed in mm/s.
                | DEFAULT_ENFORCE_DEADZONE - Flag whether deadzone validation is active.
                | default_z - Default Z coordinate for new points in mm.
                | default_speed - Default feedrate speed in mm/s.
                | enforce_deadzone - Flag whether deadzone validation is active.
    '''

    DEFAULT_Z_MM: ClassVar[float] = 20.0
    DEFAULT_SPEED_MMS: ClassVar[float] = 40.0
    DEFAULT_ENFORCE_DEADZONE: ClassVar[bool] = True

    default_z: float = DEFAULT_Z_MM
    default_speed: float = DEFAULT_SPEED_MMS
    enforce_deadzone: bool = DEFAULT_ENFORCE_DEADZONE
