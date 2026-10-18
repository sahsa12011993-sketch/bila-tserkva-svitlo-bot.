import re
import urllib.request
from html import unescape

url = "https://bezsvitla.com.ua/kyivska-oblast/bila-tserkva"

request = urllib.request.Request(
    url, headers={"User-Agent": "Mozilla/5.0"}
)

with urllib.request.urlopen(request, timeout=20) as response:
    html = response.read().decode("utf-8", errors="replace")

text = unescape(re.sub(r"<[^>]+>", " ", html))
text = re.sub(r"\s+", " ", text)

for group in ["1.1", "1.2", "2.1"]:
    print(f"\n--- Підчерга {group} ---")
    match = re.search(re.escape(group), text)
    if match:
        start = max(0, match.start() - 150)
        end = min(len(text), match.end() + 400)
        print(text[start:end])
    else:
        print("Не знайдено")

print("\n--- Часові інтервали ---")
times = re.findall(
    r"\b\d{1,2}[:.]\d{2}\s*[-–—]\s*\d{1,2}[:.]\d{2}\b",
    text
)
print(times[:30] if times else "Інтервали не знайдено")
