# -*- coding: UTF-8 -*-

'''
Module
    dependencies.py
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
    SCARAjectory bundle dependencies TypedDict definition.
'''

from __future__ import annotations

from typing import TypedDict

from ats_utilities.base.setup.bundle import BaseBundle

from scarajectory.core.service.iservice import IService
from scarajectory.core.service.itrajectory_streamer import ITrajectoryStreamer
from scarajectory.infrastructure.gui.igui import IGUI
from scarajectory.infrastructure.cli.icli import ICLI

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SCARAjectoryBundleDependencies(TypedDict):
    '''
        SCARAjectory bundle dependencies specification.

        It defines:

            :attributes:
                | base - Base ATS bundle.
                | service - Core trajectory service.
                | gui - GUI presentation adapter.
                | streamer - Robot communication streamer.
                | cli - Command-line interface adapter.
    '''

    base: BaseBundle
    service: IService
    gui: IGUI
    streamer: ITrajectoryStreamer
    cli: ICLI
