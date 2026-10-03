# -*- coding: UTF-8 -*-

'''
Module
    main_content_builder_factory.py
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
    Factory module for instantiating MainContentBuilder components.
'''

from __future__ import annotations

from scarajectory.infrastructure.gui.layout.canvas_pane_builder_factory import CanvasPaneBuilderFactory
from scarajectory.infrastructure.gui.layout.editor_pane_builder_factory import EditorPaneBuilderFactory
from scarajectory.infrastructure.gui.layout.icanvas_pane_builder import ICanvasPaneBuilder
from scarajectory.infrastructure.gui.layout.ieditor_pane_builder import IEditorPaneBuilder
from scarajectory.infrastructure.gui.layout.itoolbar_layout_builder import IToolbarLayoutBuilder
from scarajectory.infrastructure.gui.layout.main_content_builder import MainContentBuilder
from scarajectory.infrastructure.gui.layout.toolbar_layout_builder_factory import ToolbarLayoutBuilderFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MainContentBuilderFactory:
    '''
        Factory providing instantiation of MainContentBuilder components.

        It defines:

            :methods:
                | create - Creates a new MainContentBuilder instance.
                | create_with_collaborators - Creates instance with explicit sub-builders.
                | get_version - Returns the factory version string.
    '''

    @classmethod
    def create(cls) -> MainContentBuilder:
        '''
            Creates a new MainContentBuilder instance with default sub-builders.

            :return: MainContentBuilder instance.
            :exceptions: None.
        '''
        return cls.create_with_collaborators(
            canvas_pane_builder=CanvasPaneBuilderFactory.create(),
            toolbar_builder=ToolbarLayoutBuilderFactory.create(),
            editor_pane_builder=EditorPaneBuilderFactory.create(),
        )

    @classmethod
    def create_with_collaborators(
        cls,
        *,
        canvas_pane_builder: ICanvasPaneBuilder,
        toolbar_builder: IToolbarLayoutBuilder,
        editor_pane_builder: IEditorPaneBuilder,
    ) -> MainContentBuilder:
        '''
            Creates a new MainContentBuilder instance with explicit sub-builders.

            :param canvas_pane_builder: Canvas pane layout builder component.
            :param toolbar_builder: Toolbar layout builder component.
            :param editor_pane_builder: Editor pane layout builder component.
            :return: MainContentBuilder instance.
            :exceptions: None.
        '''
        return MainContentBuilder(
            canvas_pane_builder=canvas_pane_builder,
            toolbar_builder=toolbar_builder,
            editor_pane_builder=editor_pane_builder,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
