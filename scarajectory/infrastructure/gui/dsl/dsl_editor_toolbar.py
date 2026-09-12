# -*- coding: UTF-8 -*-

'''
Module
    dsl_editor_toolbar.py
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
    Dedicated action toolbar subcomponent for the SCARA DSL script editor.
'''

from __future__ import annotations

from collections.abc import Callable
from tkinter import LEFT, VERTICAL, Widget, X, Y
from tkinter.ttk import Button, Combobox, Frame, Label, Separator
from typing import Final

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DslEditorToolbar(Frame):
    '''
        Toolbar subcomponent containing compilation, validation, export and file action buttons.

        It defines:

            :attributes:
                | _cbo_examples - Combobox dropdown listing available example scripts.
                | _on_example_selected - Callback invoked when an example is selected.
            :methods:
                | __init__ - Initializes the toolbar layout and mounts action buttons.
                | get_selected_example - Returns the name of the currently selected example script.
                | set_selected_example - Sets the active example name in the dropdown.
                | set_example_files - Populates example choices in dropdown.
    '''

    _cbo_examples: Combobox
    _on_example_selected: Callable[[str], None] | None

    def __init__(
        self,
        parent: Widget,
        *,
        on_compile: Callable[[], None],
        on_validate: Callable[[], None],
        on_export: Callable[[], None],
        on_preview: Callable[[], None],
        on_open: Callable[[], None],
        on_save: Callable[[], None],
        on_example_selected: Callable[[str], None] | None = None,
        **kwargs: object,
    ) -> None:
        '''
            Initializes the toolbar layout and mounts action buttons.

            :param parent: Parent container widget.
            :param on_compile: Callback for compiling DSL to active plan.
            :param on_validate: Callback for syntax and kinematic validation.
            :param on_export: Callback for serializing plan to DSL.
            :param on_preview: Callback for launching SCARAEmu preview.
            :param on_open: Callback for opening .scara file.
            :param on_save: Callback for saving .scara file.
            :param on_example_selected: Optional callback for loading example script.
            :exceptions: None.
        '''
        super().__init__(parent, **kwargs)
        self._on_example_selected: Final[Callable[[str], None] | None] = on_example_selected

        row_actions: Frame = Frame(self)
        row_actions.pack(fill=X, pady=(0, 2))

        Button(
            row_actions,
            text='⚡ Compile to Plan',
            style='Accent.TButton',
            command=on_compile,
        ).pack(side=LEFT, padx=2)

        Button(
            row_actions,
            text='🔍 Validate',
            command=on_validate,
        ).pack(side=LEFT, padx=2)

        Button(
            row_actions,
            text='📤 Export Plan to DSL',
            command=on_export,
        ).pack(side=LEFT, padx=2)

        Separator(row_actions, orient=VERTICAL).pack(
            side=LEFT, fill=Y, padx=4
        )

        Button(
            row_actions,
            text='🚀 Preview in SCARAEmu',
            command=on_preview,
        ).pack(side=LEFT, padx=2)

        row_files: Frame = Frame(self)
        row_files.pack(fill=X, pady=(0, 4))

        Button(
            row_files,
            text='📂 Open...',
            command=on_open,
        ).pack(side=LEFT, padx=2)

        Button(
            row_files,
            text='💾 Save...',
            command=on_save,
        ).pack(side=LEFT, padx=2)

        Separator(row_files, orient=VERTICAL).pack(
            side=LEFT, fill=Y, padx=4
        )
        Label(row_files, text='Examples:').pack(side=LEFT, padx=(2, 2))

        self._cbo_examples = Combobox(
            row_files,
            state='readonly',
            width=24,
        )
        self._cbo_examples.pack(side=LEFT, padx=2)
        self._cbo_examples.bind('<<ComboboxSelected>>', self._handle_example_change)

        Button(
            row_files,
            text='📥 Load Demo',
            command=lambda: self._handle_example_change(None),
        ).pack(side=LEFT, padx=2)

    def _handle_example_change(self, _event: object = None) -> None:
        '''
            Handles selection event on example dropdown.

            :param _event: Optional Tkinter event.
            :exceptions: None.
        '''
        if self._on_example_selected is not None:
            self._on_example_selected(self.get_selected_example())

    def get_selected_example(self) -> str:
        '''
            Returns the name of the currently selected example script.

            :return: String filename of example script.
            :exceptions: None.
        '''
        return self._cbo_examples.get()

    def set_selected_example(self, name: str) -> None:
        '''
            Sets the active example name in the dropdown.

            :param name: Filename to select.
            :exceptions: None.
        '''
        self._cbo_examples.set(name)

    def set_example_files(self, files: list[str]) -> None:
        '''
            Populates example choices in dropdown.

            :param files: List of available example filenames.
            :exceptions: None.
        '''
        self._cbo_examples['values'] = files
        if files:
            default_name: str = (
                '12_industrial_pick_place.scara'
                if '12_industrial_pick_place.scara' in files
                else files[0]
            )
            self._cbo_examples.set(default_name)
