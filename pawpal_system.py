from dataclasses import dataclass, field
from datetime import time, datetime, date, timedelta

PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


@dataclass
class Task:
    """A single pet care activity."""
    description: str
    duration_minutes: int
    due_time: time = time(9, 0)
    priority: str = "medium"       # "low" | "medium" | "high"
    frequency: str = "once"        # "once" | "daily" | "weekly"
    completed: bool = False
    pet_name: str = ""

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def end_time(self) -> time:
        """Return the time this task finishes."""
        start = datetime.combine(date.today(), self.due_time)
        return (start + timedelta(minutes=self.duration_minutes)).time()


@dataclass
class Pet:
    """A pet and the care tasks assigned to it."""
    name: str
    species: str
    age: int
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a task to this pet and tag it with the pet's name."""
        task.pet_name = self.name
        self.tasks.append(task)

    def remove_task(self, description: str) -> None:
        """Remove every task with the given description."""
        self.tasks = [t for t in self.tasks if t.description != description]

    def get_tasks(self) -> list[Task]:
        """Return a copy of this pet's task list."""
        return list(self.tasks)


class Owner:
    """A pet owner who manages several pets and a daily time budget."""

    def __init__(self, name: str, available_minutes: int = 120):
        self.name = name
        self.available_minutes = available_minutes
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        self.pets.append(pet)

    def remove_pet(self, name: str) -> None:
        """Remove the pet with the given name."""
        self.pets = [p for p in self.pets if p.name != name]

    def get_all_tasks(self) -> list[Task]:
        """Collect tasks from every pet into one list."""
        all_tasks: list[Task] = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks


class Scheduler:
    """Builds and organizes a daily plan from an owner's pets' tasks."""

    def __init__(self, owner: Owner):
        self.owner = owner

    def sort_by_time(self, tasks: list[Task]) -> list[Task]:
        """Return tasks ordered by their due time."""
        return sorted(tasks, key=lambda t: t.due_time)

    def build_daily_plan(self) -> list[Task]:
        """Pick incomplete tasks by priority until time runs out, ordered by time."""
        pending = [t for t in self.owner.get_all_tasks() if not t.completed]
        by_priority = sorted(
            pending, key=lambda t: (
                PRIORITY_ORDER.get(t.priority, 1), t.due_time)
        )
        plan: list[Task] = []
        minutes_used = 0
        for task in by_priority:
            if minutes_used + task.duration_minutes <= self.owner.available_minutes:
                plan.append(task)
                minutes_used += task.duration_minutes
        return self.sort_by_time(plan)

    def detect_conflicts(self, tasks: list[Task]) -> list[tuple[Task, Task]]:
        """Return pairs of tasks whose time ranges overlap."""
        ordered = self.sort_by_time(tasks)
        conflicts: list[tuple[Task, Task]] = []
        for i, a in enumerate(ordered):
            for b in ordered[i + 1:]:
                if b.due_time < a.end_time():
                    conflicts.append((a, b))
        return conflicts
