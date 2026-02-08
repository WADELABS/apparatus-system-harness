class Assay:
    def __init__(self, manifest):
        self.config = manifest
        self.steps = manifest.get('steps', [])
        
    def execute(self):
        """Runs the assay steps sequentially."""
        print("Starting assay execution...")
        results = {}
        
        for step in self.steps:
            step_name = step.get('name', 'Unknown Step')
            print(f"Running step: {step_name}")
            # Logic to dispatch step execution to appropriate instruments/substrates
            # ...
            results[step_name] = "Executed" # Placeholder result
            
        return results
