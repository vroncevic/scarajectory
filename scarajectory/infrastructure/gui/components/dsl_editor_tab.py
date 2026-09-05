# -*- coding: UTF-8 -*-

'''
Module
    dsl_editor_tab.py
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
    Dedicated SCARA DSL code editor and compiler tab integrated into the controls notebook.
'''

from __future__ import annotations

from os import environ
from pathlib import Path
from subprocess import Popen
from sys import executable
from tempfile import NamedTemporaryFile
from tkinter import (
    BOTH, DISABLED, END, Event, LEFT, Misc,
    NORMAL, RIGHT, VERTICAL, Widget, X, Y, Text,
)
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import showerror
from tkinter.ttk import (
    Button, Combobox, Frame, Label, LabelFrame, Scrollbar, Separator,
)
from typing import Final

from scarajectory.core.model.trajectory_plan import TrajectoryPlan
from scarajectory.core.service.dsl.iscara_dsl_service import IScaraDslService
from scarajectory.core.service.dsl.scara_dsl_service import ScaraDslService
from scarajectory.core.service.itrajectory_validator import ITrajectoryValidator
from scarajectory.infrastructure.gui.components.dsl_syntax_highlighter import DslSyntaxHighlighter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DslEditorTab(Frame):
    '''
        SCARA DSL script editor with syntax highlighting, compilation, validation and export.

        It defines:

            :attributes:
                | _plan - Active trajectory plan instance.
                | _dsl_service - High-level DSL compilation and serialization service.
                | _examples_dir - Filesystem path to bundled examples directory.
                | _cbo_examples - Combobox dropdown for selecting bundled example scripts.
                | _txt_editor - Multi-line source code editor widget.
                | _txt_console - Status and compiler error log console.
                | _highlighter - Syntax highlighter instance.
            :methods:
                | __init__ - Initializes the editor tab layout and binds events.
                | _on_example_selected - Loads selected example script into the editor.
                | compile_to_plan - Compiles editor code and updates the active plan.
                | validate_code - Validates editor code syntax and kinematics without mutating plan.
                | export_plan_to_editor - Serializes current plan into the editor text.
                | preview_in_scaraemu - Launches SCARAEmu visualizer with active script.
                | open_file - Opens a .scara file into the editor.
                | save_file - Saves editor contents to a .scara file.
                | load_example - Inserts standard demonstration SCARA script.
    '''

    _EXAMPLE_SCRIPT: str = (
        '# ==========================================================\n'
        '# SCARA DSL Industrial Pick & Place Demonstration\n'
        '# ==========================================================\n'
        'CONFIG ELBOW RIGHT\n'
        'SPEED RAPID 120.0\n'
        'SPEED WORK 40.0\n'
        'ACCEL 500.0\n'
        'ZONE BLEND R=5.0\n'
        'TOOL_ORIENT TANGENTIAL\n'
        '\n'
        '# Define sorting pallet grid (3 rows x 4 cols, 20mm pitch)\n'
        'PALLET_DEF TRAY ROWS=3 COLS=4 DX=20.0 DY=20.0\n'
        '\n'
        '# 1. Homing and rapid positioning\n'
        'HOME\n'
        'MOVE_J X=120.0 Y=50.0 Z=20.0 PHI=0.0\n'
        '\n'
        '# 2. Pick & Place arc jump to pallet index 0\n'
        'JUMP X=160.0 Y=80.0 Z=10.0 ARCH=25.0 SPEED=45.0\n'
        'APPROACH DIST=10.0 SPEED=20.0\n'
        'PUMP ON\n'
        'WAIT_MS 100\n'
        'RETRACT DIST=15.0 SPEED=80.0\n'
        '\n'
        '# 3. Transfer to pallet cell 5\n'
        'MOVE_PALLET TRAY INDEX=5 Z=15.0\n'
        'PUMP OFF\n'
        'VALVE ON\n'
        'WAIT_MS 50\n'
        'VALVE OFF\n'
        '\n'
        '# 4. Circular inspection arc\n'
        'ARC_CW X=150.0 Y=40.0 I=0.0 J=-20.0 SPEED=30.0\n'
        'HOME\n'
    )

    _plan: TrajectoryPlan
    _dsl_service: IScaraDslService
    _examples_dir: Path
    _cbo_examples: Combobox
    _txt_editor: Text
    _txt_console: Text
    _highlighter: DslSyntaxHighlighter

    def __init__(
        self,
        parent: Widget,
        *,
        plan: TrajectoryPlan,
        validator: ITrajectoryValidator | None = None,
        dsl_service: IScaraDslService | None = None,
        **kwargs: object,
    ) -> None:
        '''
            Initializes the SCARA DSL editor tab.

            :param parent: Parent container widget.
            :param plan: Active TrajectoryPlan instance.
            :param validator: Optional ITrajectoryValidator instance.
            :param dsl_service: Optional IScaraDslService instance.
            :exceptions: None.
        '''
        super().__init__(parent, padding=4, **kwargs)
        self._plan: Final[TrajectoryPlan] = plan
        self._dsl_service: Final[IScaraDslService] = (
            dsl_service
            if dsl_service is not None
            else ScaraDslService(validator=validator)
        )
        self._examples_dir: Final[Path] = (
            Path(__file__).resolve().parents[4] / 'examples'
        )

        self._build_layout()
        self._load_initial_content()

    def _build_layout(self) -> None:
        '''
            Constructs action toolbar, code editor, and status console.

            :exceptions: None.
        '''
        row_actions: Frame = Frame(self)
        row_actions.pack(fill=X, pady=(0, 2))

        Button(
            row_actions,
            text='⚡ Compile to Plan',
            style='Accent.TButton',
            command=self.compile_to_plan,
        ).pack(side=LEFT, padx=2)

        Button(
            row_actions,
            text='🔍 Validate',
            command=self.validate_code,
        ).pack(side=LEFT, padx=2)

        Button(
            row_actions,
            text='📤 Export Plan to DSL',
            command=self.export_plan_to_editor,
        ).pack(side=LEFT, padx=2)

        Separator(row_actions, orient=VERTICAL).pack(
            side=LEFT, fill=Y, padx=4
        )

        Button(
            row_actions,
            text='🚀 Preview in SCARAEmu',
            command=self.preview_in_scaraemu,
        ).pack(side=LEFT, padx=2)

        row_files: Frame = Frame(self)
        row_files.pack(fill=X, pady=(0, 4))

        Button(
            row_files,
            text='📂 Open...',
            command=self.open_file,
        ).pack(side=LEFT, padx=2)

        Button(
            row_files,
            text='💾 Save...',
            command=self.save_file,
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
        if self._examples_dir.is_dir():
            files = sorted(p.name for p in self._examples_dir.glob('*.scara'))
            if files:
                self._cbo_examples['values'] = files
                default_name = (
                    '12_industrial_pick_place.scara'
                    if '12_industrial_pick_place.scara' in files
                    else files[0]
                )
                self._cbo_examples.set(default_name)
        self._cbo_examples.bind('<<ComboboxSelected>>', self._on_example_selected)

        Button(
            row_files,
            text='📥 Load Demo',
            command=self._on_example_selected,
        ).pack(side=LEFT, padx=2)

        editor_frame: Frame = Frame(self)
        editor_frame.pack(fill=BOTH, expand=True)

        scroll_y = Scrollbar(editor_frame, orient=VERTICAL)
        scroll_y.pack(side=RIGHT, fill=Y)

        self._txt_editor = Text(
            editor_frame,
            width=1,
            bg='#14161a',
            fg='#abb2bf',
            insertbackground='#61afef',
            font=('DejaVu Sans Mono', 9),
            wrap='none',
            yscrollcommand=scroll_y.set,
            undo=True,
        )
        self._txt_editor.pack(fill=BOTH, expand=True)
        scroll_y.config(command=self._txt_editor.yview)

        self._highlighter = DslSyntaxHighlighter(self._txt_editor)
        self._txt_editor.bind('<KeyRelease>', self._on_key_release)

        console_frame = LabelFrame(self, text=' Compilation & Diagnostics ', padding=2)
        console_frame.pack(fill=X, pady=(4, 0))

        self._txt_console = Text(
            console_frame,
            width=1,
            height=4,
            bg='#1a1d23',
            fg='#98c379',
            font=('DejaVu Sans Mono', 8),
            wrap='word',
            state=DISABLED,
        )
        self._txt_console.pack(fill=BOTH, expand=True)

    def _load_initial_content(self) -> None:
        '''
            Loads either the exported active plan or the demonstration script into the editor.

            :exceptions: None.
        '''
        if self._plan.count > 0:
            self.export_plan_to_editor()
        elif self._cbo_examples.get():
            self._on_example_selected()
        else:
            self.load_example()

    def _on_key_release(self, _event: Event[Misc]) -> None:
        '''
            Refreshes syntax highlighting on keystrokes.

            :param _event: Tkinter event.
            :exceptions: None.
        '''
        self._highlighter.highlight(self._txt_editor)

    def _log_console(self, text: str, is_error: bool = False) -> None:
        '''
            Appends message to the status console.

            :param text: Message string.
            :param is_error: True if message indicates error.
            :exceptions: None.
        '''
        self._txt_console.config(state=NORMAL)
        self._txt_console.delete('1.0', END)
        self._txt_console.config(fg='#e06c75' if is_error else '#98c379')
        self._txt_console.insert(END, text)
        self._txt_console.config(state=DISABLED)

    def compile_to_plan(self) -> None:
        '''
            Compiles editor code and replaces waypoints in the active TrajectoryPlan.

            :exceptions: None.
        '''
        source: str = self._txt_editor.get('1.0', END).strip()
        if not source:
            self._log_console('❌ Editor is empty. Nothing to compile.', is_error=True)
            return

        try:
            compiled_plan: TrajectoryPlan = self._dsl_service.compile_script(
                source=source
            )
            self._plan.set_waypoints(compiled_plan.waypoints)
            msg = (
                f'✅ Successfully compiled and synchronized!\n'
                f'Waypoints in Plan: {compiled_plan.count} | '
                f'Kinematic Feasibility: PASSED'
            )
            self._log_console(msg, is_error=False)
        except Exception as exc:
            self._log_console(f'❌ Compilation error: {exc}', is_error=True)

    def validate_code(self) -> None:
        '''
            Validates editor code syntax and kinematics without modifying the plan.

            :exceptions: None.
        '''
        source: str = self._txt_editor.get('1.0', END).strip()
        if not source:
            self._log_console('❌ Editor is empty. Nothing to validate.', is_error=True)
            return

        is_valid, messages = self._dsl_service.validate_script(source=source)
        self._log_console(
            '\n'.join(messages),
            is_error=not is_valid,
        )

    def export_plan_to_editor(self) -> None:
        '''
            Serializes the active plan waypoints into the editor.

            :exceptions: None.
        '''
        script = self._dsl_service.export_plan(plan=self._plan)
        self._txt_editor.delete('1.0', END)
        self._txt_editor.insert(END, script)
        self._highlighter.highlight(self._txt_editor)
        self._log_console(
            f'ℹ️ Exported {self._plan.count} waypoints to SCARA DSL format.',
            is_error=False,
        )

    def preview_in_scaraemu(self) -> None:
        '''
            Exports active DSL script to temporary file and launches SCARAEmu for visual twin preview.

            :exceptions: None.
        '''
        code: str = self._txt_editor.get('1.0', END).strip()
        if not code:
            self._log_console('[WARN]: DSL editor is empty. Nothing to preview.', is_error=True)
            return

        candidate_dirs: list[Path] = [
            Path(__file__).resolve().parents[6] / 'scaraemu' / 'github' / 'scaraemu',
            Path('/data/dev/python/3_tools/scaraemu/github/scaraemu')
        ]
        emu_dir: Path | None = next((d for d in candidate_dirs if (d / 'main.py').is_file()), None)
        if not emu_dir:
            self._log_console('[ERR]: SCARAEmu directory with main.py not found.', is_error=True)
            return

        with NamedTemporaryFile(mode='w', suffix='.scara', delete=False, encoding='utf-8') as tmp:
            tmp.write(code)
            tmp_path: str = tmp.name

        try:
            cmd: list[str] = [
                executable,
                str(emu_dir / 'main.py'),
                'emulator',
                '--file',
                tmp_path,
            ]
            env: dict[str, str] = dict(environ)
            env['PYTHONPATH'] = f"{emu_dir}:{env.get('PYTHONPATH', '')}"
            Popen(cmd, cwd=str(emu_dir), env=env)
            self._log_console(f'🚀 Launched SCARAEmu preview with {tmp_path}', is_error=False)
        except OSError as exc:
            self._log_console(f'[ERR]: Failed to launch SCARAEmu: {exc}', is_error=True)

    def open_file(self) -> None:
        '''
            Opens a .scara file and loads it into the editor.

            :exceptions: None.
        '''
        self.update_idletasks()
        init_dir: str | None = (
            str(self._examples_dir) if self._examples_dir.is_dir() else None
        )
        filepath = askopenfilename(
            parent=self.winfo_toplevel(),
            initialdir=init_dir,
            filetypes=[('SCARA DSL Scripts', '*.scara'), ('All Files', '*.*')]
        )
        if not filepath:
            return

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            self._txt_editor.delete('1.0', END)
            self._txt_editor.insert(END, content)
            self._highlighter.highlight(self._txt_editor)
            self._log_console(f'ℹ️ Loaded file: {filepath}', is_error=False)
            self.update_idletasks()
        except OSError as exc:
            showerror('File Error', f'Failed to open file:\n{exc}')

    def save_file(self) -> None:
        '''
            Saves editor content to a .scara file.

            :exceptions: None.
        '''
        self.update_idletasks()
        filepath = asksaveasfilename(
            parent=self.winfo_toplevel(),
            defaultextension='.scara',
            filetypes=[('SCARA DSL Scripts', '*.scara'), ('All Files', '*.*')],
        )
        if not filepath:
            return

        try:
            content = self._txt_editor.get('1.0', END)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            self._log_console(f'ℹ️ Saved file: {filepath}', is_error=False)
            self.update_idletasks()
        except OSError as exc:
            showerror('File Error', f'Failed to save file:\n{exc}')

    def _on_example_selected(self, _event: object = None) -> None:
        '''
            Loads the selected example script from disk into the editor.

            :param _event: Optional Tkinter event.
            :exceptions: None.
        '''
        selected = self._cbo_examples.get()
        if selected and self._examples_dir.is_dir():
            target_file = self._examples_dir / selected
            if target_file.is_file():
                try:
                    with open(target_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    self._txt_editor.delete('1.0', END)
                    self._txt_editor.insert(END, content)
                    self._highlighter.highlight(self._txt_editor)
                    self._log_console(f'ℹ️ Loaded example: {selected}', is_error=False)
                    return
                except OSError as exc:
                    self._log_console(f'❌ Failed to read example: {exc}', is_error=True)
                    return
        self.load_example()

    def load_example(self) -> None:
        '''
            Inserts standard demonstration SCARA script.

            :exceptions: None.
        '''
        self._txt_editor.delete('1.0', END)
        self._txt_editor.insert(END, self._EXAMPLE_SCRIPT)
        self._highlighter.highlight(self._txt_editor)
        self._log_console('ℹ️ Demonstration SCARA DSL script loaded.', is_error=False)
