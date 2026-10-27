"""Скриншоты для lesson_02: реальные данные из MongoDB выводятся в стиле консоли mongosh."""
import os

from PIL import Image, ImageDraw, ImageFont
from pymongo import MongoClient

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "screens")
os.makedirs(OUT, exist_ok=True)
FONT = ImageFont.truetype(r"C:\Windows\Fonts\consola.ttf", 16)
BAR = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 14)
client = MongoClient("mongodb://localhost:27017")


def render(name, title, lines):
    w = max(900, max(int(FONT.getlength(l)) for l in lines) + 40)
    img = Image.new("RGB", (w, 50 + len(lines) * 22 + 10), (12, 12, 12))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, w, 30], fill=(45, 45, 48))
    d.text((12, 6), title, font=BAR, fill=(230, 230, 230))
    y = 42
    for line in lines:
        d.text((16, y), line, font=FONT,
               fill=(86, 156, 214) if line.startswith(">") else (204, 204, 204))
        y += 22
    img.save(os.path.join(OUT, name))
    print("saved", name)


def size(db):
    s = client[db].command("dbstats")["dataSize"]
    return f"{s / 1024:.1f} KiB" if s < 1024 * 1024 else f"{s / 1024 / 1024:.2f} MiB"


def db_screen(file, db):
    lines = [f"> use {db}", f"switched to db {db}", "> show collections"]
    names = sorted(client[db].list_collection_names())
    lines += [f"  {n}" for n in names] + [""]
    for n in names:
        lines.append(f"> db.{n}.countDocuments({{}})")
        lines.append(f"  {client[db][n].count_documents({})}")
    render(file, f"mongosh - {db}", lines)


dbs = [d for d in ("shop", "hh", "logs", "org") if d in client.list_database_names()]
lines = ["> show dbs"] + [f"  {d:10} {size(d)}" for d in sorted(client.list_database_names())
                          if d not in ("admin", "config", "local")]
render("01-bazy.png", "mongosh - mongodb://localhost:27017", lines)
db_screen("02-shop.png", "shop")
db_screen("03-hh.png", "hh")
db_screen("04-logs.png", "logs")
db_screen("05-org.png", "org")
