
from schedule_source import get_schedules

schedules = get_schedules()

for queue, slots in schedules.items():
    print(f"\nПІДЧЕРГА {queue}")
    for slot in slots:
        print(f'{slot["time"]} — {slot["status"]}')

print(f"\nУсього підчерг: {len(schedules)}")
