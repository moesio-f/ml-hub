"""Esse módulo é responsável por armazenar os ID's
da Celery do Task atualmente em execução.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from datetime import datetime

_TASKS: dict[str, TaskInfo] = dict()


@dataclass
class TaskResult:
    metrics: dict
    pipeline_size: int
    train_samples: int
    test_samples: int


@dataclass
class TaskInfo:
    id: str
    started_by: str
    start_time: str  # %d/%m/%y-%H:%M:%S
    end_time: str | None  # %d/%m/%y-%H:%M:%S
    result: TaskResult | None
    status: str

    def asdict(self):
        return asdict(self)

    @staticmethod
    def loadFromDict(v) -> TaskInfo:
        fieldSet = {f.name for f in fields(TaskInfo) if f.init}
        filteredArgDict = {k: v for k, v in v.items() if k in fieldSet}
        return TaskInfo(**filteredArgDict)


def add_task(task_id, started_by, status):
    assert task_id not in _TASKS
    _TASKS[task_id] = TaskInfo(
        task_id,
        started_by=started_by,
        start_time=datetime.now().strftime("%d/%m/%y-%H:%M:%S"),
        end_time=None,
        result=None,
        status=status)


def get_tasks() -> dict[str, TaskInfo]:
    return _TASKS
