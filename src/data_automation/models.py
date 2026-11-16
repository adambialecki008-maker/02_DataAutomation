from typing import TypedDict


class MachineStats(TypedDict):
    count: int
    total_stop_s: int


class AnalysisReport(TypedDict):
    machines: dict[str, MachineStats]
    rejected: int
    errors: list[str]


class ReportErrors(TypedDict):
    importing: list[str]
    validation: list[str]


class FinalReport(TypedDict):
    machines: dict[str, MachineStats]
    rejected: int
    errors: ReportErrors


class ParsedEvent(TypedDict):
    id: str | None
    machine: str | None
    duration_s: int
