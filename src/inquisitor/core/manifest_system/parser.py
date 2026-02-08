class ManifestParser:
    async def parse(self, raw_manifest, context):
        return raw_manifest

class ManifestValidator:
    async def validate(self, manifest, context):
        return ValidationResult(True, [])

class ExecutionPlanCompiler:
    async def compile(self, manifest, context):
        return {"phases": []}

class ValidationResult:
    def __init__(self, is_valid, errors):
        self.is_valid = is_valid
        self.errors = errors
