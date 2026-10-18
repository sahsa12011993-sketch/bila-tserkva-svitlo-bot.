
import re
import urllib.request

url = "https://bezsvitla.com.ua/kyivska-oblast/bila-tserkva"

request = urllib.request.Request(
    url,
    headers={"User-Agent": "Mozilla/5.0"}
)

with urllib.request.urlopen(request, timeout=20) as response:
    html = response.read().decode("utf-8", errors="replace")

for phrase in ["Черга 1.1", "Черга 1.2", "Черга 2.1"]:
    position = html.find(phrase)

    print(f"\n{'=' * 20} {phrase} {'=' * 20}")

    if position == -1:
        print("Не знайдено")
    else:
        start = max(0, position - 1000)
        end = min(len(html), position + 2500)
        print(html[start:end])

print("\nПеревірка завершена.")
