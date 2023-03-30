"""Esse módulo é responsável por armazenar os ID's
da Celery do Task atualmente em execução.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from datetime import datetime
from pathlib import Path

_ACTIVE_TASKS: dict[str, TaskInfo] = dict()
_INACTIVE_TASKS: dict[str, TaskInfo] = dict()


@dataclass
class TaskInfo:
    id: str
    started_by: str
    start_time: str  # %d/%m/%y-%H:%M:%S
    end_time: str | None  # %d/%m/%y-%H:%M:%S

    def asdict(self):
        return asdict(self)

    @staticmethod
    def loadFromDict(v) -> TaskInfo:
        fieldSet = {f.name for f in fields(TaskInfo) if f.init}
        filteredArgDict = {k: v for k, v in v.items() if k in fieldSet}
        return TaskInfo(**filteredArgDict)


def add_task(task_id, started_by):
    assert task_id not in _ACTIVE_TASKS
    _ACTIVE_TASKS[task_id] = TaskInfo(
        task_id,
        started_by=started_by,
        start_time=datetime.now().strftime("%d/%m/%y-%H:%M:%S"),
        end_time=None)


def get_tasks(type: str = 'all') -> dict[str, TaskInfo]:
    search_dict = None

    if type == 'all':
        search_dict = dict(**_ACTIVE_TASKS, **_INACTIVE_TASKS)
    elif type == 'active':
        search_dict = _ACTIVE_TASKS
    elif type == 'inactive':
        search_dict = _INACTIVE_TASKS

    return search_dict


def remove_task(task_id):
    assert task_id in _ACTIVE_TASKS
    assert task_id not in _INACTIVE_TASKS

    task_info = _ACTIVE_TASKS.pop(task_id)
    task_info.end_time = datetime.now().strftime("%d/%m/%y-%H:%M:%S")
    _INACTIVE_TASKS[task_id] = task_info
