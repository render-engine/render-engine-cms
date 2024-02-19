import time
from sys import argv

from textual import on
from textual.app import App, ComposeResult, RenderResult
from textual.widgets import (
    Header,
    Footer,
    Label,
    TextArea,
    ListView,
    ListItem,
    Markdown,
)

from textual.widget import Widget
from render_engine.cli.cli import split_module_site, get_app
from render_engine.site import Site
from render_engine.collection import Collection
from render_engine.page import Page

module, app = split_module_site(argv[1])
site = get_app(module, app)


def get_collections(site: Site) -> list[ListItem]:
    """Get a list of the collections from the site route_list"""
    return [
        ListItem(
            Label(
                collection.__class__.__name__,
            ),
            name=collection.__class__.__name__,
            id=collection.__class__.__name__,
        )
        for _, collection in site.route_list.items()
        if isinstance(collection, Collection)
    ]


class FileLabel(Label):
    def __init__(self, file: Page):
        super().__init__(file.title)
        self.content = file.content


def files_in_collection(collection: Collection) -> list[ListItem]:
    """Get a list of the files in a collection"""
    return [
        ListItem(
            FileLabel(file),
            name=file.__class__.__name__,
        )
        for file in collection
    ]


class CollectionFiles(ListView):
    """A widget for displaying the files in a collection"""

    pass


class CollectionList(ListView):
    """A list of collections"""

    pass


class CollectionSideBar(Widget):
    """A sidebar for the collections"""

    def compose(self) -> ComposeResult:
        yield CollectionList(*get_collections(site))
        yield CollectionFiles(
            *files_in_collection(site.route_list["pages"]), id="file_selection"
        )


class CollectionView(Widget):
    """A view of a collection"""

    content = "No Text Selected"

    DEFAULT_CSS = """
    CollectionView {
        layout: horizontal;
        }
    CollectionSideBar {
    width: 30%;
    }
    CollectionList {
        height: 45%;
        border: solid magenta;
    }
    CollectionFiles {
        height: 45%;
        border: solid magenta;
    }

    MarkdownViewer {
        width: 65%;
        border: solid cyan;
    }
    """

    @on(ListView.Highlighted, "#file_selection")
    def change_message(self, message: ListView.Highlighted) -> None:
        self.content = message.item.children[0].content
        md_viewer = self.query_one("#markdown_viewer", Markdown)
        md_viewer.update(self.content)

    def compose(self) -> ComposeResult:
        yield CollectionSideBar()
        yield Markdown(self.content, id="markdown_viewer")


class CMS(App):
    """A Textual App that provides an CMS interface for Render Engine"""

    BINDINGS = [("q", "quit")]

    def compose(self) -> ComposeResult:
        """Compose the app UI"""
        yield Header()
        yield CollectionView()
        yield Footer()


if __name__ == "__main__":
    cms = CMS()
    cms.run()
