import json

def elements_from_json(obj: dict) -> list[dict]:
    out: list[dict] = []

    def walk(d: dict, prefix: str = "") -> None:
        for k, v in d.items():
            nid = f"{prefix}{k}"
            out.append({"data": {"id": nid, "label": nid}})
            if isinstance(v, dict):
                walk(v, f"{nid}.")
    walk(obj)
    return out


def base_stylesheet() -> list[dict]:
    return [
        {
            "selector": "node",
            "style": {"label": "data(label)"},
        },
        {
            "selector": "edge",
            "style": {
                "curve-style": "bezier",
                "target-arrow-shape": "triangle",
                "label": "data(relation)",
                "text-rotation": "autorotate",
                "text-margin-y": -10,
            },
        },
    ]


def json_to_elements(raw: str) -> list[dict]:
    return elements_from_json(json.loads(raw))
