import json
from rdflib import URIRef

# File for saving the data
DATA_FILE = "data.json"

# Predefined common namespaces
COMMON_NAMESPACES = {
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "owl": "http://www.w3.org/2002/07/owl#",
    "skos": "http://www.w3.org/2004/02/skos/core#",
    "dc": "http://purl.org/dc/elements/1.1/",
    "vcard": "http://www.w3.org/2006/vcard/ns#",
    "foaf": "http://xmlns.com/foaf/0.1/",
    "xsd": "http://www.w3.org/2001/XMLSchema#"
}

def get_full_uri(prefix, local_part, namespaces):
    """Get full URI by combining prefix and local part."""
    if prefix in namespaces:
        return URIRef(namespaces[prefix] + local_part)
    return URIRef(local_part)

def add_triple(triples, subject, predicate, object_):
    """Add a triple to the graph."""
    triples.append((subject, predicate, object_))

def save_data(namespaces, triples):
    """Save namespaces and triples to a JSON file."""
    with open(DATA_FILE, "w") as f:
        # Exclude common namespaces from being saved (since they're always available)
        user_namespaces = {k: v for k, v in namespaces.items() if k not in COMMON_NAMESPACES}
        data = {
            "namespaces": user_namespaces,
            "triples": [(str(s), str(p), str(o)) for s, p, o in triples]  # Store as strings
        }
        json.dump(data, f)

def load_data(file=None):
    """Load namespaces and triples from a JSON file."""
    try:
        if file:
            data = json.load(file)
        else:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)

        # Merge user-defined namespaces with common namespaces
        user_namespaces = data.get("namespaces", {})
        namespaces = {**COMMON_NAMESPACES, **user_namespaces}  # Ensure common namespaces are always present
        triples = [(s, p, o) for s, p, o in data.get("triples", [])]
        return namespaces, triples
    except (FileNotFoundError, json.JSONDecodeError):
        # Return common namespaces and empty triples if no file or invalid data is found
        return COMMON_NAMESPACES, []
