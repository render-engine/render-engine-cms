from sys import argv

from textual.app import App, ComposeResult, RenderResult
from textual.widgets import (
    Header,
    Footer,
    TextArea,
)

from textual.widget import Widget
from render_engine.cli.cli import split_module_site, get_app
from render_engine.site import Site
from render_engine.collection import Collection
from render_engine.page import Page


def get_collections(site: Site) -> list[Collection]:
    """Get a list of the collections from the site route_list"""
    return [
        collection
        for _, collection in site.route_list.items()
        if isinstance(collection, Collection)
    ]


def files_in_collection(collection: Collection) -> list[Page]:
    """Get a list of the files in a collection"""
    return [file for file in collection]


class CollectionFiles(Widget):
    """A widget for displaying the files in a collection"""

    def render(self) -> RenderResult:
        module, app = split_module_site(argv[1])
        site = get_app(module, app)
        collection = get_collections(site)[0]
        return "Test Collection Files"  # "\n".join(collection.files_in_collection(collection))


class CollectionList(Widget):
    """A list of collections"""

    def render(self) -> RenderResult:
        module, app = split_module_site(argv[1])
        return "Test Collection List"  # str(get_collections(get_app(module, app)))


class CollectionSideBar(Widget):
    """A sidebar for the collections"""

    def compose(self) -> ComposeResult:
        yield CollectionList()
        yield CollectionFiles()


class CollectionView(Widget):
    """A view of a collection"""

    DEFAULT_CSS = """
    CollectionView {
        layout: horizontal;
        }
    CollectionSideBar {
    width: 30%;
    }
    CollectionList {
        height: 45%;
    }
    CollectionFiles {
        height: 45%;
    }

    TextArea {
    width: 65%;
    }
    """

    def compose(self) -> ComposeResult:
        yield CollectionSideBar()
        yield TextArea("Hello, World!", language="markdown")


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
