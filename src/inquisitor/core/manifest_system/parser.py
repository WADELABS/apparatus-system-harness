"""
ManifestParser: Parses YAML or dict manifests into structured objects.
Handles nested configurations and provides error handling for malformed data.
"""

import yaml
from typing import Dict, Any, Optional, Union


class ParsedManifest:
    """Structured representation of a parsed manifest."""
    
    def __init__(self, data: Dict[str, Any]):
        self.data = data
        self.raw_data = data
        
        # Extract top-level manifest data
        manifest_data = data.get('manifest', data)
        
        # Extract sections
        self.version = manifest_data.get('version')
        self.id = manifest_data.get('id')
        self.name = manifest_data.get('name')
        self.metadata = manifest_data.get('metadata', {})
        self.protocol = manifest_data.get('protocol', {})
        self.substrate = manifest_data.get('substrate', {})
        self.instruments = manifest_data.get('instruments', [])
        self.execution = manifest_data.get('execution', {})
        self.analysis = manifest_data.get('analysis', {})
        self.reporting = manifest_data.get('reporting', {})
    
    def get(self, key: str, default=None):
        """Get a value from the manifest data."""
        return self.data.get(key, default)
    
    def __getitem__(self, key: str):
        """Dictionary-style access to manifest data."""
        return self.data[key]
    
    def __contains__(self, key: str):
        """Check if key exists in manifest data."""
        return key in self.data


class ManifestParser:
    """
    Parses inquiry manifests from YAML strings or Python dictionaries.
    Handles nested configurations and provides structured output.
    """
    
    async def parse(self, raw_manifest: Union[str, Dict[str, Any]], context: Optional[Dict[str, Any]] = None) -> ParsedManifest:
        """
        Parse a raw manifest into a structured ParsedManifest object.
        
        Args:
            raw_manifest: Either a YAML string or Python dictionary
            context: Optional parsing context
            
        Returns:
            ParsedManifest object with structured data
            
        Raises:
            ValueError: If manifest is malformed or invalid YAML
            TypeError: If manifest is neither string nor dict
        """
        try:
            # Handle string input (YAML)
            if isinstance(raw_manifest, str):
                parsed_data = self._parse_yaml(raw_manifest)
            # Handle dict input
            elif isinstance(raw_manifest, dict):
                parsed_data = raw_manifest
            else:
                raise TypeError(f"Manifest must be a string (YAML) or dict, got {type(raw_manifest)}")
            
            # Validate basic structure
            self._validate_basic_structure(parsed_data)
            
            # Return structured manifest
            return ParsedManifest(parsed_data)
            
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML format: {str(e)}")
        except Exception as e:
            raise ValueError(f"Error parsing manifest: {str(e)}")
    
    def _parse_yaml(self, yaml_string: str) -> Dict[str, Any]:
        """Parse YAML string into a dictionary."""
        if not yaml_string or not yaml_string.strip():
            raise ValueError("YAML string cannot be empty")
        
        try:
            parsed = yaml.safe_load(yaml_string)
            if parsed is None:
                raise ValueError("YAML resulted in None/null value")
            if not isinstance(parsed, dict):
                raise ValueError(f"YAML must parse to a dictionary, got {type(parsed)}")
            return parsed
        except yaml.YAMLError as e:
            raise ValueError(f"YAML parsing error: {str(e)}")
    
    def _validate_basic_structure(self, data: Dict[str, Any]) -> None:
        """
        Validate basic manifest structure.
        Checks for required top-level keys but doesn't perform deep validation.
        """
        # Check if data is wrapped in 'manifest' key or is the manifest itself
        if 'manifest' in data:
            manifest_data = data['manifest']
        else:
            manifest_data = data
        
        if not isinstance(manifest_data, dict):
            raise ValueError("Manifest data must be a dictionary")
        
        # Check for absolutely required fields
        required_fields = ['version', 'id', 'name']
        missing_fields = [field for field in required_fields if field not in manifest_data]
        
        if missing_fields:
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")
