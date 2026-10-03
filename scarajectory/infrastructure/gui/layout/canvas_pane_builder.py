# -*- coding: UTF-8 -*-

'''
Module
    canvas_pane_builder.py
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
    Builder assembling and mounting trajectory canvas layout pane.
'''

from __future__ import annotations

from tkinter import BOTH
from tkinter.ttk import Frame, PanedWindow
from typing import Final

from scarajectory.infrastructure.gui.canvas.bundle import CanvasBundle
from scarajectory.infrastructure.gui.canvas.trajectory_canvas import TrajectoryCanvas
from scarajectory.infrastructure.gui.canvas.trajectory_canvas_factory import TrajectoryCanvasFactory
from scarajectory.infrastructure.gui.model.canvas_settings import CanvasSettings
from scarajectory.infrastructure.gui.scarajectory_gui_init_bundle import ScarajectoryGUIInitBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CanvasPaneBuilder:
    '''
        Assembles and mounts the left pane containing the trajectory canvas.

        It defines:

            :attributes:
                | _canvas_factory - Injected factory type for canvas creation.
            :methods:
                | __init__ - Initializes CanvasPaneBuilder with factory collaborator.
                | build - Constructs and mounts canvas inside parent paned window.
                | get_version - Returns builder version string.
    '''

    _canvas_factory: type[TrajectoryCanvasFactory]

    def __init__(
        self,
        *,
        canvas_factory: type[TrajectoryCanvasFactory] = TrajectoryCanvasFactory,
    ) -> None:
        '''
            Initializes CanvasPaneBuilder with injected factory collaborator.

            :param canvas_factory: TrajectoryCanvasFactory class or substitute.
            :exceptions: None.
        '''
        self._canvas_factory: Final[type[TrajectoryCanvasFactory]] = (
            canvas_factory
        )

    def build(
        self,
        parent: PanedWindow,
        *,
        bundle: ScarajectoryGUIInitBundle,
        settings: CanvasSettings,
    ) -> TrajectoryCanvas:
        '''
            Constructs and mounts canvas inside parent paned window.

            :param parent: Parent PanedWindow container.
            :param bundle: GUI initialization dependencies bundle.
            :param settings: Canvas settings configuration.
            :return: Instantiated TrajectoryCanvas widget.
            :exceptions: None.
        '''
        left_frame = Frame(parent)
        parent.add(left_frame, weight=3)
        canvas_bundle = CanvasBundle(
            store=bundle.plan.store,
            selection=bundle.plan.selection,
            mutation=bundle.plan.mutation,
            dispatcher=bundle.plan.dispatcher,
            validator=bundle.validator,
            settings=settings,
        )
        canvas = self._canvas_factory.create(left_frame, bundle=canvas_bundle)
        canvas.pack(fill=BOTH, expand=True)

        return canvas

    def get_version(self) -> str:
        '''
            Returns the builder version string.

            :return: Builder version string.
            :exceptions: None.
        '''
        return __version__
