from datetime import time

from pawpal_system import Pet, Task


def test_mark_complete_changes_status():
    """Calling mark_complete() should flip the task's completed flag to True."""
    task = Task("Morning walk", 30, time(7, 30))
    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_add_task_increases_pet_task_count():
    """Adding a task to a pet should increase that pet's task count by one."""
    pet = Pet("Mochi", "dog", 3)
    assert len(pet.get_tasks()) == 0

    pet.add_task(Task("Feed breakfast", 10, time(8, 0)))

    assert len(pet.get_tasks()) == 1
