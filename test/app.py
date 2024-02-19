from render_engine import Site, Collection

app = Site()


@app.collection
class Pages(Collection):
    content_path = "test/pages"


@app.collection
class Blog(Collection):
    content_path = "test/pages/blog"
