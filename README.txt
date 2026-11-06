LIBRARY MANAGEMENT SYSTEM - PYQT6

FILES
- main.py: User interface, widgets, layouts, styling and event connections.
- library_data.py: Data operations and JSON persistence.
- library_data.json: Created automatically when the app first runs.

SETUP (Windows PowerShell)
1. Open this folder in VS Code.
2. Create a virtual environment:
   py -m venv .venv
3. Activate it:
   .\.venv\Scripts\Activate
4. Install PyQt6:
   python -m pip install --upgrade pip
   python -m pip install PyQt6
5. Run:
   python main.py

USAGE
- Books: Add books, search/filter inventory, and delete selected books.
- Issue Book: Select an available title, enter student details and due date.
- Returns: Select an active loan and mark it as returned.
- Records are saved automatically in library_data.json beside the program.

The app starts with three sample book records on first run. Keep library_data.json
to preserve your saved data.
