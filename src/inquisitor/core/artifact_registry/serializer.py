"""
Artifact Serializer
===================

Handles serialization of artifacts for storage.
"""

import json
from datetime import datetime
from typing import Any

def to_json(obj: Any) -> str:
    """Serialize object to JSON."""
    return json.dumps(obj, default=str, indent=2)
