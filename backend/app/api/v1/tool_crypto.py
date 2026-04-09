import base64

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class CryptoPayload(BaseModel):
    plaintext: str


@router.post("/encrypt")
def encrypt(payload: CryptoPayload) -> dict[str, str]:
    token = base64.b64encode(payload.plaintext.encode("utf-8")).decode("utf-8")
    return {"ciphertext": token}
