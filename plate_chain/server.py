#!/usr/bin/env python
"""PlateChain server exposes a chain to parse microplate data."""
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from langchain.pydantic_v1 import BaseModel

from langserve import add_routes
from .chain import chain


app = FastAPI(
    title="PlateChain Server",
    version="0.1",
    description="Spin up a simple api server to parse plate data",
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


# The input type is automatically inferred from the runnable
# interface; however, if you want to override it, you can do so
# by passing in the input_type argument to add_routes.
class ChainInput(BaseModel):
    """The input to the chain."""

    input: UploadFile = File(...)
    num_plates: int | None = None
    num_rows: int | None = None
    num_cols: int | None = None


@app.get("/")
async def root(f: UploadFile = File(...)):
    pass


add_routes(app, chain, input_type=ChainInput, config_keys=["configurable"])

# Alternatively, you can rely on langchain's type inference
# to infer the input type from the runnable interface.
# add_routes(app, chain)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8002, log_level="info")
