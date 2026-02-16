#!/usr/bin/env python3
"""
Generate JSON Schema from Pydantic Models
==========================================

This script generates a JSON Schema file from the Pydantic models defined
in the ManifestValidator. This ensures the schema is always in sync with
the validation code.

Usage:
    python scripts/generate-schema.py
    python scripts/generate-schema.py --output schemas/custom-name.json
"""

import argparse
import json
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from inquisitor.core.manifest_system.validator import InquiryManifest


def generate_schema(output_path: str = None):
    """Generate JSON Schema from InquiryManifest Pydantic model."""
    
    # Generate schema using Pydantic's built-in method
    schema = InquiryManifest.model_json_schema()
    
    # Add additional metadata
    schema['$schema'] = 'http://json-schema.org/draft-07/schema#'
    schema['title'] = 'Apparatus Inquiry Manifest'
    schema['description'] = (
        'JSON Schema for Apparatus System Harness Inquiry Manifests. '
        'This schema defines the canonical interface for declaring distributed inquiries.'
    )
    schema['version'] = '1.0.0'
    
    # Set default output path
    if output_path is None:
        repo_root = Path(__file__).parent.parent
        output_path = repo_root / 'schemas' / 'inquiry-manifest-v1.schema.json'
    else:
        output_path = Path(output_path)
    
    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write schema to file
    with open(output_path, 'w') as f:
        json.dump(schema, f, indent=2, sort_keys=False)
    
    print(f"✓ JSON Schema generated successfully: {output_path}")
    print(f"  Schema version: {schema['version']}")
    print(f"  Title: {schema['title']}")
    print(f"  Definitions: {len(schema.get('$defs', {}))}")
    
    return schema


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Generate JSON Schema from Pydantic models'
    )
    parser.add_argument(
        '--output', '-o',
        help='Output path for JSON Schema file',
        default=None
    )
    parser.add_argument(
        '--stdout',
        action='store_true',
        help='Print schema to stdout instead of writing to file'
    )
    
    args = parser.parse_args()
    
    if args.stdout:
        # Generate and print to stdout
        schema = InquiryManifest.model_json_schema()
        schema['$schema'] = 'http://json-schema.org/draft-07/schema#'
        schema['version'] = '1.0.0'
        print(json.dumps(schema, indent=2))
    else:
        # Generate and write to file
        generate_schema(args.output)


if __name__ == '__main__':
    main()
