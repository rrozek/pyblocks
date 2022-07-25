import typing
from hashlib import sha256
import json


def calculate_hash(data: typing.Any) -> str:
    if isinstance(data, list):
        unified_data = json.dumps(data, sort_keys=True)
    elif isinstance(data, object):
        unified_data = json.dumps(
            {key: value for key, value in data.__dict__.items() if key not in ["data", "hash"]}, sort_keys=True
        )
    else:
        unified_data = data
    return sha256(unified_data.encode("utf-8")).hexdigest()


class Block:
    def __init__(
        self, height: int, data: typing.List[typing.Any], timestamp: float, previous_hash: str, difficulty, nonce: int = 0
    ):
        self.data = data

        self.height = height
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.difficulty = difficulty
        self.data_hash = calculate_hash(self.data)
        self.nonce = nonce

        self.hash = None

    def calculate_hash(self) -> str:
        return calculate_hash(self)

    def as_dict(self) -> dict:
        return {
            "height": self.height,
            "timestamp": self.timestamp,
            "previous_hash": self.previous_hash,
            "difficulty": self.difficulty,
            "nonce": self.nonce,
            "data": self.data,
            "hash": self.hash,
        }
