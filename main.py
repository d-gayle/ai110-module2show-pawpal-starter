from datetime import time

from pawpal_system import Owner, Pet, Task, Scheduler


def print_schedule(owner: Owner, plan: list[Task]) -> None:
    """Print a readable daily schedule to the terminal."""
    print("=" * 50)
    print(f"  Today's Schedule for {owner.name}")
    print("=" * 50)
    for task in plan:
        start = task.due_time.strftime("%I:%M %p")
        end = task.end_time().strftime("%I:%M %p")
        status = "x" if task.completed else " "
        print(f"[{status}] {start} - {end}  {task.pet_name:<8} {task.description} "
              f"({task.duration_minutes} min, {task.priority})")
    total = sum(t.duration_minutes for t in plan)
    print("-" * 50)
    print(f"  {len(plan)} tasks, {total} of {owner.available_minutes} min used")


def main() -> None:
    owner = Owner("Jordan", available_minutes=120)

    mochi = Pet("Mochi", "dog", 3)
    luna = Pet("Luna", "cat", 5)
    owner.add_pet(mochi)
    owner.add_pet(luna)

    mochi.add_task(Task("Morning walk", 30, time(7, 30), "high", "daily"))
    mochi.add_task(Task("Vet appointment", 45, time(14, 0), "high", "once"))
    luna.add_task(Task("Feed breakfast", 10, time(8, 0), "high", "daily"))
    luna.add_task(Task("Give medication", 5, time(8, 5), "medium", "daily"))
    luna.add_task(Task("Play session", 20, time(18, 0), "low", "daily"))

    scheduler = Scheduler(owner)
    plan = scheduler.build_daily_plan()
    print_schedule(owner, plan)

    conflicts = scheduler.detect_conflicts(plan)
    if conflicts:
        print("\nWarning: time conflicts detected")
        for a, b in conflicts:
            print(
                f"  {a.pet_name}: {a.description} overlaps {b.pet_name}: {b.description}")


if __name__ == "__main__":
    main()
