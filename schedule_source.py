
import re
import urllib.request
from html import unescape

SCHEDULE_URL = (
    "https://bezsvitla.com.ua/kyivska-oblast/bila-tserkva"
)


def get_schedules():
    request = urllib.request.Request(
        SCHEDULE_URL,
        headers={"User-Agent": "Mozilla/5.0"},
    )

    with urllib.request.urlopen(request, timeout=20) as response:
        html = response.read().decode("utf-8", errors="replace")

    cards = re.findall(
        r'<article class="bz-schedule-card">(.*?)</article>',
        html,
        re.DOTALL,
    )

    schedules = {}

    for card in cards:
        heading = re.search(
            r"<strong>\s*Черга\s+([\d.]+)\s*</strong>",
            card,
        )

        if not heading:
            continue

        queue = heading.group(1)

        slots = re.findall(
            r'<div class="bz-schedule-slot([^"]*)">\s*'
            r'<span class="bz-schedule-slot__time">'
            r'(.*?)</span>.*?'
            r'aria-label="([^"]+)"',
            card,
            re.DOTALL,
        )

        schedules[queue] = [
            {
                "time": re.sub(
                    r"\s+", " ", unescape(time)
                ).strip(),
                "status": unescape(status),
                "current": "--current" in classes,
            }
            for classes, time, status in slots
        ]

    return schedules


if __name__ == "__main__":
    schedules = get_schedules()

    for queue, slots in schedules.items():
        print(f"\nПІДЧЕРГА {queue}")

        for slot in slots:
            current = " ← ЗАРАЗ" if slot["current"] else ""
            print(
                f'{slot["time"]} — {slot["status"]}{current}'
            )

    print(f"\nУсього підчерг: {len(schedules)}")
          
