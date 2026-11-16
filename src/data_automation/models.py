from typing import TypedDict


class MachineStats(TypedDict):
    count: int
    total_stop_s: int


class AnalysisReporrt(TypedDict):
    machines: dict[str, MachineStats]
    rejected: int
    errors: list[str]


class ReportErrors(TypedDict):
    importing: list
    validation: list


class FinalReport(TypedDict):
    machines: dict[str, MachineStats]
    rejected: int
    errors: ReportErrors
