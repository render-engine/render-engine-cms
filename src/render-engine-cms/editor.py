from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import TextArea


class Editor(TextArea):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.language = "markdown"

    COMPONENT_CLASSES = {"editor"}


class EditorScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Editor(id="file_editor")
