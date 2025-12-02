# backend/app/routers/autocomplete.py
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class AutoReq(BaseModel):
    code: str
    cursorPosition: int
    language: str = "python"

@router.post("/autocomplete")
async def autocomplete(req: AutoReq):
    # simple, deterministic mocked suggestions
    tail = req.code[max(0, req.cursorPosition - 40): req.cursorPosition]
    if tail.rstrip().endswith("def") or tail.endswith("def "):
        suggestion = " my_function(params):\n    \"\"\"docstring\"\"\"\n    pass"
    elif tail.endswith("import "):
        suggestion = "sys"
    elif tail.strip().endswith(":"):
        suggestion = "\n    # TODO: implement"
    else:
        suggestion = "# suggestion: consider adding a helper function here"
    return {"suggestion": suggestion}
