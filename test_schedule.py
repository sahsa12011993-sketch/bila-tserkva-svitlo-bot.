

import re
import urllib.request
from html import unescape

url = "https://bezsvitla.com.ua/kyivska-oblast/bila-tserkva"
request = urllib.request.Request(
    url, headers={"User-Agent": "Mozilla/5.0"}
)

with urllib.request.urlopen(request, timeout=20) as response:
    html = response.read().decode("utf-8", errors="replace")

cards = re.findall(
    r'<article class="bz-schedule-card">(.*?)</article>',
    html,
    re.DOTALL
)

found = 0

for card in cards:
    heading = re.search(
        r"<strong>\s*Черга\s+([\d.]+)\s*</strong>", card
    )
    if not heading:
        continue

    group = heading.group(1)
    print(f"\n🔌 ПІДЧЕРГА {group}")

    slots = re.findall(
        r'<div class="bz-schedule-slot([^"]*)">\s*'
        r'<span class="bz-schedule-slot__time">'
        r'(.*?)</span>.*?'
        r'aria-label="([^"]+)"',
        card,
        re.DOTALL
    )

    for classes, time, status in slots:
        time = re.sub(r"\s+", " ", unescape(time)).strip()
        print(f"{time} — {unescape(status)}")
        found += 1

print(f"\nЗнайдено підчерг: {len(cards)}")
print(f"Знайдено інтервалів: {found}")
