
import os
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

CHANNEL_LINK = "https://t.me/bilazerkvatrimaisa"


def make_table():
    image = Image.new("RGB", (1000, 1000), "#101827")
    draw = ImageDraw.Draw(image)

    try:
        font_path = (
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
        )
        bold_path = (
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        )
        font = ImageFont.truetype(font_path, 25)
        title_font = ImageFont.truetype(bold_path, 36)
    except OSError:
        font = ImageFont.load_default()
        title_font = font

    draw.text(
        (35, 25),
        "ГРАФІК ВІДКЛЮЧЕНЬ",
        font=title_font,
        fill="white",
    )
    draw.text(
        (35, 80),
        "Біла Церква — Тримайся!",
        font=font,
        fill="#9BC7FF",
    )
    draw.text(
        (35, 140),
        "ДЕМО-МАКЕТ — НЕ АКТУАЛЬНИЙ ГРАФІК",
        font=font,
        fill="#FFD166",
    )

    queues = [
        "1.1", "1.2", "2.1", "2.2",
        "3.1", "3.2", "4.1", "4.2",
        "5.1", "5.2", "6.1", "6.2",
    ]

    y = 205

    for queue in queues:
        draw.rounded_rectangle(
            (35, y, 965, y + 48),
            radius=10,
            fill="#263449",
        )
        draw.text(
            (55, y + 8),
            queue,
            font=font,
            fill="white",
        )
        draw.text(
            (250, y + 8),
            "Дані ще не підключені",
            font=font,
            fill="#FFD166",
        )
        y += 55

    draw.text(
        (35, 900),
        "Стежте за оновленнями в нашому каналі:",
        font=font,
        fill="white",
    )
    draw.text(
        (35, 940),
        "t.me/bilazerkvatrimaisa",
        font=font,
        fill="#9BC7FF",
    )

    output = BytesIO()
    image.save(output, format="PNG")
    output.seek(0)
    return output


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    await update.message.reply_text(
        "Вітаю! ⚡️ Це бот графіків світла "
        "для Білої Церкви.\n\n"
        "Команда /preview покаже макет таблиці.\n\n"
        "⚠️ Реальні дані ДТЕК ще не підключені.\n"
        f"Наш канал: {CHANNEL_LINK}"
    )


async def preview(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    image = make_table()

    await update.message.reply_photo(
        photo=image,
        caption=(
            "📊 Демонстраційний макет графіка\n"
            "⚠️ Це не актуальний розклад відключень.\n\n"
            f"📢 Наш канал: {CHANNEL_LINK}"
        ),
    )


def main():
    token = os.getenv("BOT_TOKEN")

    if not token:
        raise RuntimeError(
            "Не задано змінну середовища BOT_TOKEN"
        )

    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("preview", preview))

    print("Бот запущено")
    app.run_polling()


if __name__ == "__main__":
    main()
