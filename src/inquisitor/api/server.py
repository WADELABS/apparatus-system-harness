"""
Inquisitor Web UI
=================

Simple FastAPI interface for the Inquisitor Framework.
"""

from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any, List

from .core.security.auth import get_api_key
from .core.protocol_engine.conductor import AssayConductor, ExecutionContext

app = FastAPI(title="Inquisitor Framework", version="0.1.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock config
config = {
    'artifact_registry': {'type': 'filesystem', 'base_path': './findings'},
    'scheduler': {'max_concurrent_executions': 5}
}
conductor = AssayConductor(config)

@app.get("/health")
async def health_check():
    return {"status": "ok", "version": "0.1.0"}

@app.post("/assay/run", dependencies=[Depends(get_api_key)])
async def run_assay(manifest: Dict[str, Any]):
    """
    Run an assay from a submitted manifest.
    """
    # In a real scenario, we'd save the manifest to a temp file or pass dict directly
    # conductor.orchestrate expects a path currently, would need refactoring to accept dict
    # For now, return a mock response
    return {"execution_id": "ex_mock_123", "status": "queued"}

@app.get("/assay/{execution_id}", dependencies=[Depends(get_api_key)])
async def get_assay_status(execution_id: str):
    return {"execution_id": execution_id, "status": "running", "progress": 45}

# In a real implementation, we would serve a React/Vue SPA here
# app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
