import base64, dash
from dash import html, dcc, Input, Output, State
import dash_cytoscape as cyto
from rdflib import Graph, URIRef, Namespace
import autosave
from autosave import AutoSaver
from helpers import base_stylesheet, json_to_elements

cyto.load_extra_layouts()
saver = AutoSaver()
ns = Namespace("http://example.org/ontology/")

raw_start = saver.load_last()
initial_elements = json_to_elements(raw_start) if raw_start else []

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H2("JSON → Ontology Editor"),

    dcc.Upload(
        id       = "upload-json",
        children = html.Button("Import JSON"),
        multiple = False
    ),

    dcc.Input(
        id          = "edge-type",
        type        = "text",
        value       = "relatedTo",
        placeholder = "edge predicate"
    ),

    dcc.Store(id = "current-json"),

    cyto.Cytoscape(
        id                  = "cytoscape",
        layout              = {"name"   : "dagre"},
        style               = {"width"  : "100%",
                               "height" : "600px"},
        elements            = initial_elements,
        userPanningEnabled  = True,
        userZoomingEnabled  = True,
        boxSelectionEnabled = True,
        stylesheet          = base_stylesheet()
    ),

    dcc.Store(id = "selected-node"),

    html.Button("Save JSON Permanently", id = "save-json-btn"),
    html.Button("Export as JSON-LD",     id = "export-btn"),

    dcc.Download(id = "download-jsonld")
])


@app.callback(
    [Output("cytoscape", "elements", allow_duplicate=True), Output("current-json", "data")],
    Input("upload-json", "contents"),
    prevent_initial_call=True,
)
def populate(contents: str):
    _, b64 = contents.split(",", 1)
    raw = base64.b64decode(b64).decode()
    saver.save(raw)
    return json_to_elements(raw), raw


@app.callback(
    Output("save-json-btn", "disabled"),
    Input("save-json-btn", "n_clicks"),
    State("current-json", "data"),
    prevent_initial_call=True,
)
def save_perm(_, raw: str):
    if raw:
        (autosave.PERM_DIR / f"{autosave.datetime.datetime.now():%Y%m%d%H%M%S}.json").write_text(raw)
    return dash.no_update


@app.callback(
    [Output("selected-node", "data"), Output("cytoscape", "elements", allow_duplicate=True)],
    Input("cytoscape", "tapNodeData"),
    State("selected-node", "data"),
    State("cytoscape", "elements"),
    State("edge-type", "value"),
    prevent_initial_call=True,
)
def add_edge(tapped, first, elements, relation):
    if first is None:
        return tapped["id"], elements
    new_edge = {
        "data": {
            "id": f"{first}-{tapped['id']}",
            "source": first,
            "target": tapped["id"],
            "relation": relation or "relatedTo",
        }
    }
    return None, elements + [new_edge]


@app.callback(Output("cytoscape", "stylesheet"), Input("selected-node", "data"))
def style_selected(source_id):
    base = base_stylesheet()
    if source_id:
        base.append(
            {
                "selector": f'node[id="{source_id}"]',
                "style": {"border-width": 3, "border-color": "red"},
            }
        )
    return base


@app.callback(
    Output("download-jsonld", "data"),
    Input("export-btn", "n_clicks"),
    State("cytoscape", "elements"),
    prevent_initial_call=True,
)
def export_jsonld(_, elements):
    g = Graph()
    g.bind("ex", ns)
    for el in elements:
        d = el["data"]
        if "source" in d:
            g.add(
                (
                    URIRef(ns[d["source"]]),
                    URIRef(ns[d.get("relation", "relatedTo")]),
                    URIRef(ns[d["target"]]),
                )
            )
    return {"content": g.serialize(format="json-ld", indent=2), "filename": "ontology.jsonld"}


if __name__ == "__main__":
    app.run(debug=True)
