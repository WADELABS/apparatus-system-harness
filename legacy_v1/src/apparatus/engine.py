import yaml
import os
from .assay import Assay

class ApparatusEngine:
    def __init__(self):
        self.manifest = None
        self.assay = None

    def load_manifest(self, manifest_path):
        """Loads and validates the assay manifest."""
        if not os.path.exists(manifest_path):
            raise FileNotFoundError(f"Manifest not found: {manifest_path}")
            
        with open(manifest_path, 'r') as f:
            self.manifest = yaml.safe_load(f)
            
        # Here we would validate the manifest schema
        print(f"Manifest loaded: {self.manifest.get('name', 'Untitled Assay')}")
        self.assay = Assay(self.manifest)

    def run_assay(self):
        """Executes the loaded assay."""
        if not self.assay:
            raise ValueError("No assay loaded. Call load_manifest() first.")
            
        return self.assay.execute()

    def report_findings(self, results, output_dir):
        """Generates reports from assay results."""
        # Placeholder for reporting logic
        print(f"Reporting findings to {output_dir}...")
        # Implementation to save results/plots
