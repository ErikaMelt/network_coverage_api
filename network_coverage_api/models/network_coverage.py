from typing import Dict

from pydantic import BaseModel


class NetworkCoverageResponseData(BaseModel):
    coverage: Dict[str, bool]
