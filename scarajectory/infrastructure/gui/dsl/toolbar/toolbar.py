# -*- coding: UTF-8 -*-

'''
Module
    toolbar.py
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

from tkinter import LEFT, VERTICAL, Widget, X, Y
from tkinter.ttk import Button, Combobox, Frame, Label, Separator
from typing import ClassVar, Final

from scarajectory.infrastructure.gui.dsl.handler.binary.idelegate import IDslBinaryDelegate
from scarajectory.infrastructure.gui.dsl.handler.execution.idelegate import IDslExecutionDelegate
from scarajectory.infrastructure.gui.dsl.handler.file.idelegate import IDslFileDelegate

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
                | BTN_COMPILE_TEXT - Label for compile to plan button.
                | BTN_COMPILE_STYLE - ttk style for compile button.
                | BTN_VALIDATE_TEXT - Label for validate code button.
                | BTN_EXPORT_PLAN_TEXT - Label for export plan button.
                | BTN_PREVIEW_TEXT - Label for emulator preview button.
                | BTN_OPEN_TEXT - Label for open file button.
                | BTN_SAVE_TEXT - Label for save file button.
                | BTN_EXPORT_BIN_TEXT - Label for binary export button.
                | BTN_IMPORT_BIN_TEXT - Label for binary import button.
                | LBL_EXAMPLES_TEXT - Label for examples dropdown.
                | BTN_LOAD_DEMO_TEXT - Label for demo loading button.
                | DEFAULT_EXAMPLE_NAME - Default demo script name.
                | COMBOBOX_EVENT - Event name for combobox selection.
                | COMBOBOX_WIDTH - Character width for combobox.
                | PAD_BTN_X - Horizontal padding for action buttons.
                | PAD_SEP_X - Horizontal padding for separators.
                | _cbo_examples - Combobox dropdown listing available example scripts.
                | _execution_delegate - Action delegate handling DSL execution.
                | _file_delegate - Action delegate handling DSL file operations.
                | _binary_delegate - Action delegate handling binary export and import.
            :methods:
                | __init__ - Initializes the toolbar layout and mounts action buttons.
                | handle_example_change - Handles selection event on example dropdown.
                | get_selected_example - Returns the name of the currently selected example script.
                | set_selected_example - Sets the active example name in the dropdown.
                | set_example_files - Populates example choices in dropdown.
                | get_version - Returns toolbar component version string.
    '''

    BTN_COMPILE_TEXT: ClassVar[str] = '⚡ Compile to Plan'
    BTN_COMPILE_STYLE: ClassVar[str] = 'Accent.TButton'
    BTN_VALIDATE_TEXT: ClassVar[str] = '🔍 Validate'
    BTN_EXPORT_PLAN_TEXT: ClassVar[str] = '📤 Export Plan to DSL'
    BTN_PREVIEW_TEXT: ClassVar[str] = '🚀 Preview in SCARAEmu'
    BTN_OPEN_TEXT: ClassVar[str] = '📂 Open...'
    BTN_SAVE_TEXT: ClassVar[str] = '💾 Save...'
    BTN_EXPORT_BIN_TEXT: ClassVar[str] = '💾 Export .bin...'
    BTN_IMPORT_BIN_TEXT: ClassVar[str] = '📂 Import .bin...'
    LBL_EXAMPLES_TEXT: ClassVar[str] = 'Examples:'
    BTN_LOAD_DEMO_TEXT: ClassVar[str] = '📥 Load Demo'
    DEFAULT_EXAMPLE_NAME: ClassVar[str] = '12_industrial_pick_place.scara'
    COMBOBOX_EVENT: ClassVar[str] = '<<ComboboxSelected>>'
    COMBOBOX_WIDTH: ClassVar[int] = 24
    PAD_BTN_X: ClassVar[int] = 2
    PAD_SEP_X: ClassVar[int] = 4

    _cbo_examples: Combobox
    _execution_delegate: IDslExecutionDelegate
    _file_delegate: IDslFileDelegate
    _binary_delegate: IDslBinaryDelegate

    def __init__(
        self,
        parent: Widget,
        *,
        execution_delegate: IDslExecutionDelegate,
        file_delegate: IDslFileDelegate,
        binary_delegate: IDslBinaryDelegate,
    ) -> None:
        '''
            Initializes the toolbar layout and mounts action buttons.

            :param parent: Parent container widget.
            :param execution_delegate: Action delegate handling DSL execution.
            :param file_delegate: Action delegate handling DSL file operations.
            :param binary_delegate: Action delegate handling binary export and import.
            :exceptions: None.
        '''
        super().__init__(parent)
        self._execution_delegate: Final[IDslExecutionDelegate] = execution_delegate
        self._file_delegate: Final[IDslFileDelegate] = file_delegate
        self._binary_delegate: Final[IDslBinaryDelegate] = binary_delegate

        row_actions: Frame = Frame(self)
        row_actions.pack(fill=X, pady=(0, 2))

        Button(
            row_actions,
            text=self.BTN_COMPILE_TEXT,
            style=self.BTN_COMPILE_STYLE,
            command=self._execution_delegate.compile_to_plan,
        ).pack(side=LEFT, padx=self.PAD_BTN_X)

        Button(
            row_actions,
            text=self.BTN_VALIDATE_TEXT,
            command=self._execution_delegate.validate_code,
        ).pack(side=LEFT, padx=self.PAD_BTN_X)

        Button(
            row_actions,
            text=self.BTN_EXPORT_PLAN_TEXT,
            command=self._execution_delegate.export_plan_to_editor,
        ).pack(side=LEFT, padx=self.PAD_BTN_X)

        Separator(row_actions, orient=VERTICAL).pack(
            side=LEFT, fill=Y, padx=self.PAD_SEP_X
        )

        Button(
            row_actions,
            text=self.BTN_PREVIEW_TEXT,
            command=self._execution_delegate.preview_in_scaraemu,
        ).pack(side=LEFT, padx=self.PAD_BTN_X)

        row_files: Frame = Frame(self)
        row_files.pack(fill=X, pady=(0, 4))

        Button(
            row_files,
            text=self.BTN_OPEN_TEXT,
            command=self._file_delegate.open_file,
        ).pack(side=LEFT, padx=self.PAD_BTN_X)

        Button(
            row_files,
            text=self.BTN_SAVE_TEXT,
            command=self._file_delegate.save_file,
        ).pack(side=LEFT, padx=self.PAD_BTN_X)

        Separator(row_files, orient=VERTICAL).pack(
            side=LEFT, fill=Y, padx=self.PAD_SEP_X
        )

        Button(
            row_files,
            text=self.BTN_EXPORT_BIN_TEXT,
            command=self._binary_delegate.export_binary_file,
        ).pack(side=LEFT, padx=self.PAD_BTN_X)

        Button(
            row_files,
            text=self.BTN_IMPORT_BIN_TEXT,
            command=self._binary_delegate.import_binary_file,
        ).pack(side=LEFT, padx=self.PAD_BTN_X)

        Separator(row_files, orient=VERTICAL).pack(
            side=LEFT, fill=Y, padx=self.PAD_SEP_X
        )
        Label(row_files, text=self.LBL_EXAMPLES_TEXT).pack(
            side=LEFT, padx=(self.PAD_BTN_X, self.PAD_BTN_X)
        )

        self._cbo_examples = Combobox(
            row_files,
            state='readonly',
            width=self.COMBOBOX_WIDTH,
        )
        self._cbo_examples.pack(side=LEFT, padx=self.PAD_BTN_X)
        self._cbo_examples.bind(
            self.COMBOBOX_EVENT, self.handle_example_change
        )

        Button(
            row_files,
            text=self.BTN_LOAD_DEMO_TEXT,
            command=self.handle_example_change,
        ).pack(side=LEFT, padx=self.PAD_BTN_X)

    def handle_example_change(self, _event: object = '') -> None:
        '''
            Handles selection event on example dropdown.

            :param _event: Optional Tkinter event.
            :exceptions: None.
        '''
        self._file_delegate.on_example_selected(self.get_selected_example())

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
                self.DEFAULT_EXAMPLE_NAME
                if self.DEFAULT_EXAMPLE_NAME in files
                else files[0]
            )
            self._cbo_examples.set(default_name)

    def get_version(self) -> str:
        '''
            Returns toolbar component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
