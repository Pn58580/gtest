from abc import ABC, abstractmethod

from app.schemas.common import RunRequest, RunResult


class BaseRunner(ABC):
    engine_name: str

    @abstractmethod
    def run(self, request: RunRequest) -> RunResult:
        raise NotImplementedError
