import pathlib

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import TextArea, Footer

from render_engine.cli.cli import get_app


class Editor(TextArea):
    BINDINGS = {
        ("ctrl+s", "save"),
        ("escape", "escape"),
    }

    content_path: pathlib.Path

    def action_save(self) -> None:
        self.content_path.write_text(self.document.text)
        self.app.notify(f"Saved {self.content_path}")

    def action_escape(self) -> None:
        self.app.pop_screen()


class EditorScreen(Screen):
    CSS = """
        Editor {
            height: 80%;
        }
    """

    def compose(self) -> ComposeResult:
        yield Editor(
            id="file_editor",
        )
        yield Footer()
