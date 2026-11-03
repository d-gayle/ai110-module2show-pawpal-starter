from dataclasses import dataclass, field


@dataclass
class Task:
    description: str
    duration_minutes: int
    priority: str = "medium"
    due_time: str = "09:00"
    frequency: str = "once"
    completed: bool = False

    def mark_complete(self) -> None:
        pass


@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass

    def remove_task(self, description: str) -> None:
        pass

    def get_tasks(self) -> list[Task]:
        pass


class Owner:
    def __init__(self, name: str, available_minutes: int = 120):
        self.name = name
        self.available_minutes = available_minutes
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        pass

    def remove_pet(self, name: str) -> None:
        pass

    def get_all_tasks(self) -> list[Task]:
        pass


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner

    def build_daily_plan(self) -> list[Task]:
        pass

    def sort_by_time(self, tasks: list[Task]) -> list[Task]:
        pass

    def detect_conflicts(self, tasks: list[Task]) -> list:
        pass
