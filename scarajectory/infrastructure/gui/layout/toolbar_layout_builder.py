# -*- coding: UTF-8 -*-

'''
Module
    toolbar_layout_builder.py
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
    Builder assembling and mounting the top toolbar layout.
'''

from __future__ import annotations

from tkinter import TOP, Tk, X
from typing import Final

from scarajectory.infrastructure.gui.canvas.trajectory_canvas import TrajectoryCanvas
from scarajectory.infrastructure.gui.model.canvas_settings import CanvasSettings
from scarajectory.infrastructure.gui.scarajectory_gui_init_bundle import ScarajectoryGUIInitBundle
from scarajectory.infrastructure.gui.toolbar.bundle import ToolbarBundle
from scarajectory.infrastructure.gui.toolbar.toolbar import Toolbar
from scarajectory.infrastructure.gui.toolbar.toolbar_factory import ToolbarFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ToolbarLayoutBuilder:
    '''
        Assembles and mounts the top toolbar layout in the root window.

        It defines:

            :attributes:
                | _toolbar_factory - Injected factory type for toolbar creation.
            :methods:
                | __init__ - Initializes ToolbarLayoutBuilder with factory collaborator.
                | build - Constructs and mounts top toolbar in the root window.
                | get_version - Returns builder version string.
    '''

    _toolbar_factory: type[ToolbarFactory]

    def __init__(
        self,
        *,
        toolbar_factory: type[ToolbarFactory] = ToolbarFactory,
    ) -> None:
        '''
            Initializes ToolbarLayoutBuilder with injected factory collaborator.

            :param toolbar_factory: ToolbarFactory class or substitute.
            :exceptions: None.
        '''
        self._toolbar_factory: Final[type[ToolbarFactory]] = toolbar_factory

    def build(
        self,
        root: Tk,
        *,
        canvas: TrajectoryCanvas,
        bundle: ScarajectoryGUIInitBundle,
        settings: CanvasSettings,
    ) -> Toolbar:
        '''
            Constructs and mounts top toolbar in the root window.

            :param root: Root Tkinter window.
            :param canvas: TrajectoryCanvas instance.
            :param bundle: GUI initialization dependencies bundle.
            :param settings: Canvas settings configuration.
            :return: Instantiated Toolbar widget.
            :exceptions: None.
        '''
        bounds = getattr(bundle.validator, 'bounds', None)
        deadzone_r = getattr(bounds, 'deadzone_r_min', None)
        r_min: float = bundle.validator.r_min

        if isinstance(deadzone_r, (int, float)):
            r_min = max(r_min, float(deadzone_r))

        toolbar_bundle = ToolbarBundle(
            canvas=canvas,
            navigator=canvas.navigator,
            status_presenter=canvas.status_presenter,
            history=bundle.plan.history,
            r_min=r_min,
            r_max=bundle.validator.r_max,
            settings=settings,
        )
        toolbar = self._toolbar_factory.create(root, toolbar_bundle)
        toolbar.pack(side=TOP, fill=X)

        return toolbar

    def get_version(self) -> str:
        '''
            Returns the builder version string.

            :return: Builder version string.
            :exceptions: None.
        '''
        return __version__
