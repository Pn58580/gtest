import base64

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()


class CryptoPayload(BaseModel):
    plaintext: str


class DecryptPayload(BaseModel):
    ciphertext: str


@router.post("/encrypt")
def encrypt(payload: CryptoPayload) -> dict[str, str]:
    token = base64.b64encode(payload.plaintext.encode("utf-8")).decode("utf-8")
    return {"ciphertext": token}


@router.post('/decrypt')
def decrypt(payload: DecryptPayload) -> dict[str, str]:
    try:
        raw = base64.b64decode(payload.ciphertext.encode('utf-8')).decode('utf-8')
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=400, detail='invalid ciphertext') from exc
    return {'plaintext': raw}
