# SCARAjectory — Motion Trajectory Studio & Streamer

## 1. Overview
**SCARAjectory** is a standalone CAD/CAM motion planning and trajectory execution software for the 4-DOF SCARA robot.

It provides an interactive vector editor to visually design paths, a kinematic validator to verify reachability boundaries, an ASCII instruction generator, and a flow-controlled hardware serial streamer for the Raspberry Pi Pico RP2040.

---

## 2. SOLID Architecture & DTO Pattern

The application strictly adheres to SOLID design principles and uses **Data Transfer Objects (DTO)** to eliminate bulky parameter lists:

```
                  ┌──────────────────────────────┐
                  │       ScarajectoryGUI        │ (Presenter / Controller)
                  └──────────────┬───────────────┘
                                 │ Uses DTOs (StreamConfigDTO, CanvasSettingsDTO)
         ┌───────────────────────┼───────────────────────┐
         │                       │                       │
         ▼                       ▼                       ▼
┌──────────────────┐    ┌─────────────────┐    ┌──────────────────┐
│ TrajectoryCanvas │    │ TrajectoryTable │    │  TrajectoryPlan  │ (Domain Model)
└──────────────────┘    └─────────────────┘    └────────┬─────────┘
   (Vector CAD)           (Data Grid)                   │
         ▲                       ▲                      │
         └───────────┬───────────┘                      │
                     │ (itrajectory_observer.py)        │
                     └──────────────────────────────────┤
                                                        ▼
                                             ┌────────────────────────┐
                                             │ itrajectory_validator  │ (Interface Segregation)
                                             └──────────┬─────────────┘
                                                        │ Uses PointDTO
                                                        ▼
                                             ┌────────────────────────┐
                                             │ScaraTrajectoryValidator│
                                             └────────────────────────┘
```

### Module Structure:
* [`scarajectory/trajectory_dto.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/trajectory_dto.py) — Data Transfer Objects (`PointDTO`, `ValidationResultDTO`, `ScaraBoundsDTO`, `StreamConfigDTO`, `CanvasSettingsDTO`).
* [`scarajectory/itrajectory_validator.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/itrajectory_validator.py) — **Interface Segregation & DIP**: Validation contract operating on `PointDTO`.
* [`scarajectory/itrajectory_observer.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/itrajectory_observer.py) — **Observer Pattern**: Decouples canvas and data grid from model updates.
* [`scarajectory/iserial_streamer.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/iserial_streamer.py) — **ISP & DIP**: Streamer interface taking `StreamConfigDTO`.
* [`scarajectory/trajectory_validator.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/trajectory_validator.py) — **Single Responsibility (SRP)**: SCARA workspace envelope validation.
* [`scarajectory/trajectory_point.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/trajectory_point.py) — **SRP**: Waypoint entity with DTO conversion and ASCII packet formatting.
* [`scarajectory/trajectory_plan.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/trajectory_plan.py) — **SRP**: Manages sequence, distance, time, undo/redo, JSON persistence.
* [`scarajectory/serial_streamer.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/serial_streamer.py) — **Hardware Flow Control**: Asynchronous background thread monitoring Pico queue depth.
* [`scarajectory/trajectory_canvas.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/trajectory_canvas.py) — **Vector CAD Canvas**: Interactive 2D editing with tool modes.
* [`scarajectory/trajectory_table.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/trajectory_table.py) — **Data Grid**: Numerical coordinate inspector.
* [`scarajectory/scarajectory_gui.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/scarajectory_gui.py) — **Presenter**: Main window orchestration.
* [`main.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/main.py) — **Entry Point**: Application launcher.

---

## 3. Features & Workflow

### 🖌️ Step 1: Design Trajectory & Navigation
* **Zoom & Pan Navigation:**
  * **Mouse Wheel:** Scroll up/down to zoom in/out smoothly centered under the cursor.
  * **Zoom Buttons:** `[ + ]`, `[ - ]`, `[ Fit ]`, `[ 100% ]` on the toolbar.
  * **Pan:** Click and drag with **Middle Mouse Button** or **Right Mouse Button** to pan anywhere.
  * **Keyboard Shortcuts:**
    * `Delete` / `Backspace` — Instant point deletion (without confirmation prompts).
    * `Ctrl+Z` / `Ctrl+Y` — Undo / Redo history.
    * `+` / `-` — Zoom in / Zoom out.
    * `Ctrl+N` / `Ctrl+O` / `Ctrl+S` — New, Open, and Save motion plans.
* **Deadzone & Reach Protection (`Lock Deadzone (30-270mm)` checkbox):**
  * **Translucent Red Shaded Disc:** Highlights the inner forbidden deadzone ($r < 30\,\text{mm}$) around the base.
  * **Active Boundary Enforcement:** When enabled, automatically blocks clicks inside the deadzone or outside maximum reach ($r > 270\,\text{mm}$), and smoothly clamps drag-and-drop actions to valid physical boundaries.
* **Point / Polyline Tool:** Click anywhere on the workspace to add waypoints.
* **Select / Move Tool:** Click and drag points to adjust positions.
* **Parametric Shapes:**
  * **Circle Tool:** Drag from center to create a circular trajectory.
  * **Rectangle Tool:** Drag corner-to-corner to create a closed rectangle.
  * **Freehand Tool:** Draw arbitrary continuous paths with adaptive distance sampling.

### 🔍 Step 2: Validate Plan (`Validate Motion Plan` button)
* Validates all points against annular reach ($R_{min} = 30\,\text{mm}, R_{max} = 270\,\text{mm}$) and height limits ($Z = 0 - 100\,\text{mm}$).
* Computes total path length in mm and estimated duration in seconds.

### ⚙️ Step 3: Generate ASCII Code (`Generate ASCII Code` button)
* Previews complete `<pt#X#Y#Z#SPEED#end>` sequence.
* Direct clipboard copy and export to `.txt` program files.

### 🚀 Step 4: Stream to Robot (`Stream to Robot` button)
* Selects USB Serial Port (`/dev/ttyACM0`) and connects at 115200 bps.
* Streams points with active flow control to prevent buffer overruns on RP2040 Pico.
* Real-time progress bar ($0\% - 100\%$), Pause, Resume, and Emergency Stop.

---

## 4. How to Run

```bash
# Option 1: Direct Python
python3 main.py

# Option 2: Launcher script
./run.sh
```
