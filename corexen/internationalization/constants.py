schema_location_area_bound = {
    "$schema": "https://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "northeast": {
            "type": "object",
            "properties": {
                "lat": {"type": "number"},
                "lng": {"type": "number"},
            },
            "required": [
                "lat",
                "lng"
            ]
        },
        "southwest": {
            "type": "object",
            "properties": {
                "lat": {"type": "number"},
                "lng": {"type": "number"},
            },
            "required": [
                "lat",
                "lng"
            ]
        }
    },
    "required": [
        "northeast",
        "southwest"
    ]
}
