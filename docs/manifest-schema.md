# Manifest Schema Reference

The Inquiry Manifest is the canonical interface for defining distributed inquiries in the Apparatus System Harness. All system behavior is declared through these YAML manifests.

## Schema Version

**Current Version**: `v1.0.0`

The schema is formally defined using Pydantic models in `src/inquisitor/core/manifest_system/validator.py` and exported as JSON Schema to `schemas/inquiry-manifest-v1.schema.json`.

## Top-Level Structure

```yaml
manifest:
  version: string          # Schema version (required)
  id: string              # Unique manifest identifier (required)
  name: string            # Human-readable name (required)
  metadata: object        # Manifest metadata (required)
  protocol: object        # Protocol specification (required)
  substrate: object       # Data source specification (required)
  instruments: array      # Instrument configurations (required)
  execution: object       # Execution settings (optional)
  analysis: object        # Analysis specification (optional)
  reporting: object       # Reporting configuration (optional)
```

## Field Definitions

### Manifest Metadata

Information about the manifest author and creation.

```yaml
metadata:
  author: string                    # Author name (required)
  created: string                   # ISO 8601 timestamp (optional)
  description: string               # Manifest description (optional)
  tags: array<string>              # Tags for categorization (optional)
```

**Example**:
```yaml
metadata:
  author: "Jane Doe"
  created: "2026-02-15T10:30:00Z"
  description: "Cold chain monitoring for pharmaceutical shipment"
  tags: ["pharma", "cold-chain", "compliance"]
```

### Protocol Specification

Defines the execution flow and phases.

```yaml
protocol:
  type: string                      # Protocol type: sequential, parallel, dag, hybrid (required)
  phases: array                     # List of phase names or phase objects (required)
```

**Valid Protocol Types**:
- `sequential`: Execute phases one after another
- `parallel`: Execute phases concurrently
- `dag`: Directed acyclic graph with dependencies
- `hybrid`: Mix of sequential and parallel

**Phase Format** (Simple):
```yaml
protocol:
  type: "sequential"
  phases:
    - "initialization"
    - "execution"
    - "analysis"
    - "reporting"
```

**Phase Format** (Detailed):
```yaml
protocol:
  type: "sequential"
  phases:
    - name: "initialization"
      steps:
        - name: "ping_instrument"
          type: "diagnostic"
          instrument: "thermal_probe_1"
          parameters:
            action: "ping"
    - name: "execution"
      steps:
        - name: "measure_temperature"
          type: "measurement"
          instrument: "thermal_probe_1"
          parameters:
            interval: 10
```

### Substrate Specification

Defines the data source for the inquiry.

```yaml
substrate:
  source:
    type: string                    # Source type (required)
    generator: string               # Generator name for synthetic sources (optional)
    path: string                    # Path for file-based sources (optional)
    url: string                     # URL for API-based sources (optional)
    parameters: object              # Source-specific parameters (optional)
```

**Source Types**:
- `synthetic`: Generated test data
- `file`: Local file system
- `api`: REST API endpoint
- `database`: Database connection
- `stream`: Real-time data stream

**Example (Synthetic)**:
```yaml
substrate:
  source:
    type: "synthetic"
    generator: "temperature_simulator"
    parameters:
      mean: 22.0
      stddev: 0.5
      samples: 1000
```

**Example (File)**:
```yaml
substrate:
  source:
    type: "file"
    path: "/data/shipment_logs.csv"
    parameters:
      format: "csv"
      delimiter: ","
```

### Instrument Specifications

Array of instruments to use in the inquiry.

```yaml
instruments:
  - type: string                    # Instrument type (required)
    id: string                      # Unique identifier (required)
    provider: string                # Provider name (optional, default: "internal")
    parameters: object              # Instrument-specific parameters (optional)
```

**Example**:
```yaml
instruments:
  - type: "thermal_probe"
    id: "thermal_1"
    provider: "internal"
    parameters:
      sampling_rate: 1.0
      precision: 0.1
  - type: "rfid_reader"
    id: "rfid_1"
    provider: "acme_sensors"
    parameters:
      protocol_version: "2.0"
      range: 10
```

**Note**: All instrument IDs must be unique within a manifest.

### Execution Configuration

Optional execution settings.

```yaml
execution:
  concurrency:
    max_workers: integer            # Max concurrent workers (1-100, default: 1)
  retry_policy:
    max_attempts: integer           # Max retry attempts (1-10, default: 1)
    backoff_factor: float          # Exponential backoff (0.1-10.0, default: 1.0)
    timeout: integer                # Timeout per attempt in seconds (optional)
  timeout: integer                  # Overall timeout in seconds (optional)
```

**Example**:
```yaml
execution:
  concurrency:
    max_workers: 4
  retry_policy:
    max_attempts: 3
    backoff_factor: 2.0
    timeout: 30
  timeout: 300
```

### Analysis Specification

Optional analysis configuration.

```yaml
analysis:
  statistical:
    - test: string                  # Test type (required)
      groups: array<string>        # Groups to compare (optional)
      parameters: object            # Test-specific parameters (optional)
  visualizations:
    - type: string                  # Visualization type
      parameters: object            # Visualization parameters
```

**Statistical Test Types**:
- `mean_comparison`
- `t_test`
- `anova`
- `correlation`
- `regression`

**Example**:
```yaml
analysis:
  statistical:
    - test: "t_test"
      groups: ["control", "treatment"]
      parameters:
        alpha: 0.05
        alternative: "two-sided"
  visualizations:
    - type: "time_series"
      parameters:
        x_axis: "timestamp"
        y_axis: "temperature"
```

### Reporting Specification

Optional reporting configuration.

```yaml
reporting:
  artifacts:
    - type: string                  # Artifact type (required)
      format: string                # Output format (optional, default: "markdown")
      parameters: object            # Artifact-specific parameters (optional)
  destinations:
    - type: string                  # Destination type
      path: string                  # Output path
      parameters: object            # Destination parameters
```

**Artifact Types**:
- `executive_summary`
- `detailed_report`
- `console_summary`
- `compliance_report`

**Output Formats**:
- `markdown`
- `html`
- `pdf`
- `json`

**Example**:
```yaml
reporting:
  artifacts:
    - type: "executive_summary"
      format: "markdown"
      parameters:
        include_charts: true
    - type: "compliance_report"
      format: "pdf"
  destinations:
    - type: "file"
      path: "/artifacts/reports"
    - type: "s3"
      path: "s3://bucket/reports"
      parameters:
        region: "us-east-1"
```

## Complete Examples

### Minimal Viable Manifest

```yaml
manifest:
  version: "1.0.0"
  id: "minimal_inquiry"
  name: "Minimal Inquiry Example"
  
  metadata:
    author: "System"
    description: "Simplest possible inquiry"
  
  protocol:
    type: "sequential"
    phases:
      - "execution"
  
  substrate:
    source:
      type: "synthetic"
      generator: "echo"
  
  instruments:
    - type: "echo"
      id: "echo_1"
```

### Multi-Instrument Inquiry

```yaml
manifest:
  version: "1.0.0"
  id: "multi_instrument_inquiry"
  name: "Multi-Instrument Cold Chain Monitoring"
  
  metadata:
    author: "Logistics Team"
    created: "2026-02-15T10:00:00Z"
    description: "Monitor pharmaceutical shipment with multiple sensors"
    tags: ["pharma", "multi-sensor", "cold-chain"]
  
  protocol:
    type: "parallel"
    phases:
      - "initialization"
      - "execution"
      - "analysis"
  
  substrate:
    source:
      type: "file"
      path: "/data/shipment_001.csv"
      parameters:
        format: "csv"
  
  instruments:
    - type: "thermal_probe"
      id: "thermal_1"
      parameters:
        sampling_rate: 1.0
    - type: "thermal_probe"
      id: "thermal_2"
      parameters:
        sampling_rate: 1.0
    - type: "humidity_sensor"
      id: "humidity_1"
      parameters:
        sampling_rate: 5.0
    - type: "rfid_reader"
      id: "rfid_1"
      parameters:
        read_interval: 30
  
  execution:
    concurrency:
      max_workers: 4
    retry_policy:
      max_attempts: 3
      backoff_factor: 2.0
    timeout: 600
  
  analysis:
    statistical:
      - test: "mean_comparison"
        parameters:
          baseline: 22.0
  
  reporting:
    artifacts:
      - type: "executive_summary"
        format: "markdown"
      - type: "compliance_report"
        format: "pdf"
```

### Complex Analysis Pipeline

```yaml
manifest:
  version: "1.0.0"
  id: "complex_analysis_pipeline"
  name: "Advanced Analytics Pipeline"
  
  metadata:
    author: "Data Science Team"
    created: "2026-02-15T14:30:00Z"
    description: "Complex multi-stage analysis with statistical tests"
    tags: ["analytics", "statistical", "advanced"]
  
  protocol:
    type: "dag"
    phases:
      - name: "initialization"
        steps:
          - name: "calibrate_instruments"
            type: "calibration"
      - name: "data_collection"
        steps:
          - name: "collect_readings"
            type: "measurement"
            depends_on: ["calibrate_instruments"]
      - name: "analysis"
        steps:
          - name: "statistical_analysis"
            type: "analysis"
            depends_on: ["collect_readings"]
          - name: "visualization"
            type: "visualization"
            depends_on: ["statistical_analysis"]
  
  substrate:
    source:
      type: "api"
      url: "https://api.example.com/data"
      parameters:
        auth_token: "${API_TOKEN}"
        dataset: "production"
  
  instruments:
    - type: "data_collector"
      id: "collector_1"
      parameters:
        buffer_size: 1000
    - type: "statistical_analyzer"
      id: "analyzer_1"
      parameters:
        methods: ["t_test", "anova", "regression"]
  
  execution:
    concurrency:
      max_workers: 8
    retry_policy:
      max_attempts: 5
      backoff_factor: 1.5
      timeout: 60
    timeout: 1800
  
  analysis:
    statistical:
      - test: "t_test"
        groups: ["group_a", "group_b"]
        parameters:
          alpha: 0.05
      - test: "anova"
        groups: ["group_a", "group_b", "group_c"]
        parameters:
          alpha: 0.01
      - test: "regression"
        parameters:
          independent: ["x1", "x2", "x3"]
          dependent: "y"
    visualizations:
      - type: "scatter_plot"
        parameters:
          x: "x1"
          y: "y"
      - type: "histogram"
        parameters:
          variable: "y"
          bins: 50
  
  reporting:
    artifacts:
      - type: "executive_summary"
        format: "markdown"
      - type: "detailed_report"
        format: "html"
        parameters:
          include_raw_data: false
          include_charts: true
      - type: "compliance_report"
        format: "pdf"
    destinations:
      - type: "file"
        path: "/artifacts/reports"
      - type: "s3"
        path: "s3://analytics-bucket/reports"
        parameters:
          region: "us-east-1"
```

## Schema Validation

### Programmatic Validation

```python
from inquisitor.core.manifest_system import ManifestParser, ManifestValidator

# Parse and validate
parser = ManifestParser()
manifest = await parser.parse("manifest.yaml")

validator = ManifestValidator()
result = await validator.validate(manifest)

if result.is_valid:
    print("✓ Manifest is valid")
else:
    print("✗ Validation errors:")
    for error in result.errors:
        print(f"  - {error}")
```

### CLI Validation

```bash
# Validate a manifest file
inquisitor validate manifests/my-inquiry.yaml

# Export the JSON Schema
inquisitor-schema > inquiry-manifest-v1.schema.json
```

## Schema Evolution

### Version Compatibility Table

| Schema Version | Compatible Versions | Breaking Changes |
|----------------|-------------------|------------------|
| 1.0.0 | 1.0.x | Initial release |

### Adding Custom Fields

The schema allows custom fields in the `parameters` objects throughout the manifest. This enables extension without schema changes:

```yaml
instruments:
  - type: "custom_probe"
    id: "custom_1"
    parameters:
      # Custom parameters specific to this instrument
      custom_field_1: "value"
      custom_field_2: 42
      nested_config:
        option_a: true
        option_b: "test"
```

## Best Practices

1. **Use Descriptive IDs**: Make instrument and manifest IDs descriptive and unique
2. **Version Your Manifests**: Always specify the schema version
3. **Document in Metadata**: Use description and tags for searchability
4. **Validate Early**: Validate manifests before deployment
5. **Use Templates**: Create templates for common inquiry patterns
6. **Parameterize**: Use environment variables for secrets and environment-specific values
7. **Keep It Simple**: Start with minimal manifests and add complexity as needed

## Related Documentation

- [Architecture Overview](architecture.md)
- [Seven Layers Deep Dive](layers.md)
- [Local Development Guide](local-quickstart.md)
- [Kubernetes Deployment](deployment.md)

## Schema Source

The canonical schema definition is maintained as Pydantic models in:
- `src/inquisitor/core/manifest_system/validator.py`

The exported JSON Schema is available at:
- `schemas/inquiry-manifest-v1.schema.json`
