# -*- coding: UTF-8 -*-

'''
Module
    tabs_bundle.py
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
    Container bundle holding instantiated child control tabs.
'''

from __future__ import annotations

from dataclasses import dataclass

from scarajectory.infrastructure.gui.dsl.dsl_editor_tab import DslEditorTab
from scarajectory.infrastructure.gui.manipulator.jog.jog_tab import JogTab
from scarajectory.infrastructure.gui.preview.preview_tab import PreviewTab
from scarajectory.infrastructure.gui.streaming.streamer_tab import StreamerTab
from scarajectory.infrastructure.gui.validation.validation_tab import ValidationTab

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(slots=True, frozen=True)
class ControlsTabsBundle:
    '''
        Immutable data container holding the five notebook control tabs.

        It defines:

            :attributes:
                | dsl_editor_tab - SCARA DSL script editor and compiler tab.
                | streamer_tab - Hardware streaming and logging tab.
                | validation_tab - Kinematic validation tab.
                | jog_tab - Manual jog movement and actuator control tab.
                | preview_tab - ASCII microcontroller program preview tab.
    '''

    dsl_editor_tab: DslEditorTab
    streamer_tab: StreamerTab
    validation_tab: ValidationTab
    jog_tab: JogTab
    preview_tab: PreviewTab
