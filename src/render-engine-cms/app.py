from sys import argv

from textual import on
from textual.app import App, ComposeResult
from textual.widgets import (
    Header,
    Footer,
    Label,
    ListView,
    ListItem,
    Markdown,
)

from textual.widget import Widget
from render_engine.cli.cli import split_module_site, get_app
from render_engine.collection import Collection
from render_engine.page import Page

module, app = split_module_site(argv[1])
site = get_app(module, app)


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
        for file in collection.sorted_pages
    ]


class CollectionLabel(Label):
    def __init__(self, collection: Collection):
        super().__init__(collection.__class__.__name__)
        self.collection = collection


def get_collections(site):
    """Get a list of the collections from the site route_list"""
    return [collection for _, collection in site.route_list.items() if isinstance(collection, Collection)]


def get_collection_labels(collections: list[Collection]) -> list[ListItem]:
    """Get a list of the collections from the site route_list"""
    return [
        ListItem(
            CollectionLabel(
                collection,
            ),
            name=collection.__class__.__name__,
            id=collection.__class__.__name__,
        )
        for collection in collections
    ]


class CollectionList(ListView):
    """A list of collections"""


class CollectionFiles(ListView):
    """A widget for displaying the files in a collection"""


class CollectionSideBar(Widget):
    """A sidebar for the collections"""

    def compose(self) -> ComposeResult:
        collections = get_collections(site)
        yield CollectionList(*get_collection_labels(collections), id="collection_list")
        yield CollectionFiles(*files_in_collection(collections[0]), id="file_selection")


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
    CollectionList {
        height: 45%;
        border: solid magenta;
    }
    CollectionFiles {
        height: 45%;
        border: solid magenta;
    }

    Markdown {
        width: 70%;
        border: solid cyan;
    }
    """

    default_markdown = "Select a Page Title to View"

    def update_markdown(self, content: str) -> None:
        md_viewer = self.query_one("#markdown_viewer", Markdown)
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
        yield Markdown(self.default_markdown, id="markdown_viewer")


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
