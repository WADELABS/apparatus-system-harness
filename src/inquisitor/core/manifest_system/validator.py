class ManifestValidator:
    async def validate(self, manifest, context):
        return ValidationResult(True, [])

class ValidationResult:
    def __init__(self, is_valid, errors):
        self.is_valid = is_valid
        self.errors = errors
