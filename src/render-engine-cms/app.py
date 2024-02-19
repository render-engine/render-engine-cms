from logging import debug
from sys import argv

from editor import EditorScreen
from render_engine.cli.cli import get_app, split_module_site
from textual import on
from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widget import Widget
from textual.widgets import (
    Footer,
    Header,
    ListView,
)
from title_screen import (
    CollectionSideBar,
    MarkdownPreview,
    files_in_collection,
)

module, app = split_module_site(argv[1])
site = get_app(module, app)


class CollectionView(Widget):
    """A view of a collection"""

    BINDINGS = [
        (
            "return",
            "focus_files",
        )
    ]

    def action_focus_files(self) -> None:
        self.query_one("#file_selection", ListView).focus()

    DEFAULT_CSS = """
    CollectionView {
        layout: horizontal;
    }

    CollectionSideBar {
        width: 30%;
    }

    ListView .listview-sidebar {
        height: 45%;
        border: solid magenta;
    }
    .editor {
        width: 70%;
        border: solid cyan;
    }
    """

    default_markdown = "Select a Page Title to View"

    def update_markdown(self, content: str) -> None:
        md_viewer = self.query_one("#markdown_viewer", MarkdownPreview)
        md_viewer.update(content)

    @on(ListView.Highlighted, "#file_selection")
    def change_message(self, message: ListView.Highlighted) -> None:
        try:
            content = message.item.children[0].content
        except AttributeError:
            content = ""

        self.update_markdown(content)

    @on(ListView.Highlighted, "#collection_list")
    def change_collection(self, message: ListView.Highlighted):
        collection = self.query_one("#file_selection", ListView)
        collection.clear()
        collection.extend(files_in_collection(message.item.children[0].collection))

    def compose(self) -> ComposeResult:
        yield CollectionSideBar()
        yield MarkdownPreview(
            self.default_markdown,
            id="markdown_viewer",
        )


class CMS(App):
    """A Textual App that provides an CMS interface for Render Engine"""

    BINDINGS = [("q", "quit")]
    SCREENS = {"editor": EditorScreen()}

    def compose(self) -> ComposeResult:
        """Compose the app UI"""
        yield Header()
        yield CollectionView()
        yield Footer()


if __name__ == "__main__":
    cms = CMS()
    cms.run()
