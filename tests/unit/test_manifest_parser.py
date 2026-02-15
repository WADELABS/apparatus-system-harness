"""
Unit tests for ManifestParser.
Tests YAML parsing, dict parsing, error handling, and nested configuration parsing.
"""

import pytest
import yaml
from inquisitor.core.manifest_system.parser import ManifestParser, ParsedManifest


class TestManifestParser:
    """Test suite for ManifestParser."""
    
    @pytest.fixture
    def parser(self):
        """Create a ManifestParser instance."""
        return ManifestParser()
    
    @pytest.fixture
    def valid_manifest_dict(self):
        """Sample valid manifest as dictionary."""
        return {
            'manifest': {
                'version': '1.0.0',
                'id': 'test_manifest',
                'name': 'Test Manifest',
                'metadata': {
                    'author': 'Test Author',
                    'created': '2026-01-01T00:00:00Z',
                    'tags': ['test', 'unit']
                },
                'protocol': {
                    'type': 'sequential',
                    'phases': ['initialization', 'execution', 'analysis']
                },
                'substrate': {
                    'source': {
                        'type': 'synthetic',
                        'generator': 'test_generator'
                    }
                },
                'instruments': [
                    {
                        'type': 'test_probe',
                        'id': 'probe_1',
                        'provider': 'internal',
                        'parameters': {'key': 'value'}
                    }
                ],
                'execution': {
                    'concurrency': {'max_workers': 2},
                    'retry_policy': {'max_attempts': 3}
                }
            }
        }
    
    @pytest.fixture
    def valid_manifest_yaml(self, valid_manifest_dict):
        """Sample valid manifest as YAML string."""
        return yaml.dump(valid_manifest_dict)
    
    @pytest.mark.asyncio
    async def test_parse_valid_dict(self, parser, valid_manifest_dict):
        """Test parsing a valid dictionary manifest."""
        result = await parser.parse(valid_manifest_dict)
        
        assert isinstance(result, ParsedManifest)
        assert result.version == '1.0.0'
        assert result.id == 'test_manifest'
        assert result.name == 'Test Manifest'
        assert len(result.instruments) == 1
        assert result.instruments[0]['type'] == 'test_probe'
    
    @pytest.mark.asyncio
    async def test_parse_valid_yaml(self, parser, valid_manifest_yaml):
        """Test parsing a valid YAML string."""
        result = await parser.parse(valid_manifest_yaml)
        
        assert isinstance(result, ParsedManifest)
        assert result.version == '1.0.0'
        assert result.id == 'test_manifest'
        assert result.name == 'Test Manifest'
    
    @pytest.mark.asyncio
    async def test_parse_malformed_yaml(self, parser):
        """Test parsing malformed YAML raises appropriate error."""
        malformed_yaml = """
        manifest:
          version: 1.0.0
          id: test
          name: Test
          invalid_syntax: [unclosed
        """
        
        with pytest.raises(ValueError, match="YAML parsing error"):
            await parser.parse(malformed_yaml)
    
    @pytest.mark.asyncio
    async def test_parse_empty_yaml(self, parser):
        """Test parsing empty YAML raises error."""
        with pytest.raises(ValueError, match="YAML string cannot be empty"):
            await parser.parse("")
    
    @pytest.mark.asyncio
    async def test_parse_missing_required_field(self, parser):
        """Test parsing manifest missing required field."""
        invalid_manifest = {
            'manifest': {
                'version': '1.0.0',
                # Missing 'id' and 'name'
            }
        }
        
        with pytest.raises(ValueError, match="Missing required fields"):
            await parser.parse(invalid_manifest)
    
    @pytest.mark.asyncio
    async def test_parse_nested_configurations(self, parser):
        """Test parsing deeply nested configurations."""
        nested_manifest = {
            'manifest': {
                'version': '1.0.0',
                'id': 'nested_test',
                'name': 'Nested Test',
                'metadata': {
                    'author': 'Test',
                    'tags': ['nested', 'complex']
                },
                'protocol': {
                    'type': 'sequential',
                    'phases': ['init', 'exec']
                },
                'substrate': {
                    'source': {
                        'type': 'file',
                        'parameters': {
                            'path': '/data/test.csv',
                            'format': 'csv',
                            'options': {
                                'delimiter': ',',
                                'encoding': 'utf-8'
                            }
                        }
                    }
                },
                'instruments': []
            }
        }
        
        result = await parser.parse(nested_manifest)
        
        assert result.substrate['source']['parameters']['options']['delimiter'] == ','
        assert result.substrate['source']['parameters']['options']['encoding'] == 'utf-8'
    
    @pytest.mark.asyncio
    async def test_parse_unwrapped_manifest(self, parser):
        """Test parsing manifest without 'manifest' wrapper."""
        unwrapped = {
            'version': '1.0.0',
            'id': 'unwrapped',
            'name': 'Unwrapped Manifest',
            'metadata': {'author': 'Test'},
            'protocol': {'type': 'sequential', 'phases': ['init']},
            'substrate': {'source': {'type': 'synthetic'}},
            'instruments': []
        }
        
        result = await parser.parse(unwrapped)
        
        assert result.version == '1.0.0'
        assert result.id == 'unwrapped'
    
    @pytest.mark.asyncio
    async def test_parse_invalid_type(self, parser):
        """Test parsing invalid type raises TypeError."""
        with pytest.raises((TypeError, ValueError)):
            await parser.parse(12345)
    
    @pytest.mark.asyncio
    async def test_parsed_manifest_dict_access(self, parser, valid_manifest_dict):
        """Test ParsedManifest provides dict-like access."""
        result = await parser.parse(valid_manifest_dict)
        
        # Test __getitem__
        assert result['manifest']['version'] == '1.0.0'
        
        # Test get method
        assert result.get('manifest') is not None
        assert result.get('nonexistent', 'default') == 'default'
        
        # Test __contains__
        assert 'manifest' in result
        assert 'nonexistent' not in result
    
    @pytest.mark.asyncio
    async def test_parse_with_context(self, parser, valid_manifest_dict):
        """Test parsing with context parameter."""
        context = {'execution_id': 'test_exec_123'}
        result = await parser.parse(valid_manifest_dict, context)
        
        assert isinstance(result, ParsedManifest)
        assert result.id == 'test_manifest'
    
    @pytest.mark.asyncio
    async def test_parse_yaml_null_result(self, parser):
        """Test parsing YAML that results in null."""
        null_yaml = "null"
        
        with pytest.raises(ValueError, match="YAML resulted in None"):
            await parser.parse(null_yaml)
    
    @pytest.mark.asyncio
    async def test_parse_yaml_non_dict(self, parser):
        """Test parsing YAML that doesn't result in a dict."""
        list_yaml = "- item1\n- item2"
        
        with pytest.raises(ValueError, match="YAML must parse to a dictionary"):
            await parser.parse(list_yaml)
