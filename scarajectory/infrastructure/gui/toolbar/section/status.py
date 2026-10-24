# -*- coding: UTF-8 -*-

'''
Module
    status.py
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
    Subcomponent displaying live cursor coordinates and viewport zoom.
'''

from __future__ import annotations

from tkinter import LEFT, Widget
from tkinter.ttk import Frame, Label
from typing import Final

from scarajectory.infrastructure.gui.canvas.status.ipresenter import ICanvasStatusPresenter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StatusSection(Frame):
    '''
        Subcomponent displaying live cursor telemetry and zoom level.

        It defines:

            :attributes:
                | _status_presenter - Canvas status presenter collaborator.
                | _lbl_cursor - Dynamic cursor coordinate and zoom label.
            :methods:
                | __init__ - Initializes status section controls.
                | build_layout - Builds and registers cursor readout label.
                | cursor_label - Returns cursor info label widget.
    '''

    _status_presenter: ICanvasStatusPresenter
    _lbl_cursor: Label

    def __init__(
        self,
        parent: Widget,
        status_presenter: ICanvasStatusPresenter,
    ) -> None:
        '''
            Initializes status section controls.

            :param parent: Parent container widget.
            :param status_presenter: Canvas status presenter collaborator.
            :exceptions: None.
        '''
        super().__init__(parent)
        self._status_presenter: Final[ICanvasStatusPresenter] = status_presenter
        self.build_layout()

    def build_layout(self) -> None:
        '''
            Builds and registers cursor readout label.

            :exceptions: None.
        '''
        self._lbl_cursor = Label(
            self,
            text='Cursor: X=  0.0 mm | Y=  0.0 mm | R=  0.0 mm | Zoom: 100%',
            font=('DejaVu Sans Mono', 9),
        )
        self._lbl_cursor.pack(side=LEFT, padx=8)
        self._status_presenter.set_hover_label(self._lbl_cursor)

    @property
    def cursor_label(self) -> Label:
        '''
            Returns cursor info label widget.

            :return: Label widget displaying coordinates and zoom.
        '''
        return self._lbl_cursor
