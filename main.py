

import os
import asyncio
from io import BytesIO
from datetime import datetime
from zoneinfo import ZoneInfo

from PIL import Image, ImageDraw, ImageFont
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

from schedule_source import get_schedules

CHANNEL_LINK = "https://t.me/bilazerkvatrimaisa"


def make_table(schedules):
    queues = sorted(
        schedules.items(),
        key=lambda item: tuple(
            int(part) for part in item[0].split(".")
        ),
    )

    card_width = 560
    margin = 30
    gap = 20
    header_height = 150
    card_gap = 15
    line_height = 30
    card_header = 42

    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    bold_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

    try:
        font = ImageFont.truetype(font_path, 18)
        small_font = ImageFont.truetype(font_path, 15)
        title_font = ImageFont.truetype(bold_path, 32)
        queue_font = ImageFont.truetype(bold_path, 23)
    except OSError:
        font = ImageFont.load_default()
        small_font = font
        title_font = font
        queue_font = font

    card_heights = [
        card_header + max(1, len(slots)) * line_height + 16
        for _, slots in queues
    ]

    rows = (len(queues) + 1) // 2
    content_height = 0

    for row in range(rows):
        heights = card_heights[row * 2:row * 2 + 2]
        content_height += max(heights, default=100) + card_gap

    missing_height = 50 if "3.1" not in schedules else 0
    image_height = header_height + content_height + missing_height + 100

    image = Image.new(
        "RGB",
        (margin * 2 + card_width * 2 + gap, image_height),
        "#101827",
    )
    draw = ImageDraw.Draw(image)

    draw.text(
        (margin, 20),
        "ГРАФІК ВІДКЛЮЧЕНЬ",
        font=title_font,
        fill="white",
    )
    draw.text(
        (margin, 65),
        "Біла Церква — Тримайся!",
        font=font,
        fill="#9BC7FF",
    )

    now = datetime.now(ZoneInfo("Europe/Kyiv"))
    draw.text(
        (margin, 100),
        f"Дані з bezsvitla.com.ua • {now:%d.%m.%Y %H:%M}",
        font=small_font,
        fill="#FFD166",
    )

    y = header_height

    for row in range(rows):
        pair = queues[row * 2:row * 2 + 2]
        heights = card_heights[row * 2:row * 2 + 2]
        row_height = max(heights, default=100)

        for col, (queue, slots) in enumerate(pair):
            x = margin + col * (card_width + gap)

            draw.rounded_rectangle(
                (x, y, x + card_width, y + row_height),
                radius=12,
                fill="#263449",
            )

            draw.text(
                (x + 16, y + 9),
                f"Підчерга {queue}",
                font=queue_font,
                fill="white",
            )

            line_y = y + card_header

            for slot in slots:
                status = slot["status"]
                color = "#52D273" if status == "Є світло" else "#FF7373"
                time_text = slot["time"]

                draw.text(
                    (x + 16, line_y),
                    time_text,
                    font=font,
                    fill="white",
                )

                draw.text(
                    (x + 220, line_y),
                    status,
                    font=font,
                    fill=color,
                )

                if slot.get("current"):
                    draw.text(
                        (x + 390, line_y + 2),
                        "ЗАРАЗ",
                        font=small_font,
                        fill="#FFD166",
                    )

                line_y += line_height

        y += row_height + card_gap

    if "3.1" not in schedules:
        draw.text(
            (margin, y + 3),
            "Підчергу 3.1 джерело не надало.",
            font=small_font,
            fill="#FFD166",
        )
        y += missing_height

    draw.text(
        (margin, y + 10),
        "Графік може відрізнятися від офіційних даних.",
        font=small_font,
        fill="#D5DCE8",
    )
    draw.text(
        (margin, y + 35),
        "Канал: t.me/bilazerkvatrimaisa",
        font=small_font,
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
        "Вітаю! ⚡️ Це бот графіків світла для Білої Церкви.\n\n"
        "Команда /preview покаже опубліковані графіки.\n"
        "Джерело даних — bezsvitla.com.ua.\n\n"
        f"Наш канал: {CHANNEL_LINK}"
    )


async def preview(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    await update.message.reply_text("⏳ Завантажую графіки...")

    try:
        schedules = await asyncio.to_thread(get_schedules)

        if not schedules:
            await update.message.reply_text(
                "Не вдалося отримати графіки. Спробуй пізніше."
            )
            return

        image = make_table(schedules)

        await update.message.reply_photo(
            photo=image,
            caption=(
                "📊 Графіки відключень для Білої Церкви\n\n"
                "ℹ️ Дані отримано зі стороннього сайту. "
                "Перевіряй офіційні повідомлення ДТЕК.\n\n"
                f"📢 {CHANNEL_LINK}"
            ),
        )

    except Exception as error:
        print(f"Помилка завантаження графіків: {error}")
        await update.message.reply_text(
            "Не вдалося завантажити графік із сайту. "
            "Спробуй трохи пізніше."
        )


def main():
    token = os.getenv("BOT_TOKEN")

    if not token:
        raise RuntimeError("Не задано змінну середовища BOT_TOKEN")

    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("preview", preview))

    print("Бот запущено")
    app.run_polling()


if __name__ == "__main__":
    main()
    
