import urllib.request

url = "https://bezsvitla.com.ua/kyivska-oblast/bila-tserkva"

try:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0"}
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        html = response.read().decode("utf-8", errors="replace")

    print("HTTP: успішно")
    print("Розмір сторінки:", len(html), "символів")
    print("Є назва міста:", "Біла Церква" in html)
    print("Є позначення підчерг:", any(
        group in html for group in ["1.1", "1.2", "2.1"]
    ))

except Exception as error:
    print("Помилка:", repr(error))
