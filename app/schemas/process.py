from pydantic import BaseModel

class ProcessResponse(BaseModel):
    msg: str
    total: int
    classified: int
    unclassified: int
