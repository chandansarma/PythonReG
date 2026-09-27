from typing_extensions import TypedDict


class StepState(TypedDict, total=False):
    topic: str
    keywords: str
    summary: str
    status: str
