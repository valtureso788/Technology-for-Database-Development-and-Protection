"""Генерирует скриншоты консоли для отчёта: реальный вывод catalog.py рисуется в PNG."""
import contextlib
import io
import json
import os

import catalog as c

c.products.drop()  # чистый запуск на реальной MongoDB
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "screens")
os.makedirs(OUT, exist_ok=True)
FONT = ImageFont.truetype(r"C:\Windows\Fonts\consola.ttf", 16)
BAR = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 14)


def render(name, title, text):
    lines = text.rstrip("\n").split("\n")
    w = max(900, max(int(FONT.getlength(l)) for l in lines) + 40)
    h = 40 + len(lines) * 22 + 20
    img = Image.new("RGB", (w, h), (12, 12, 12))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, w, 30], fill=(45, 45, 48))
    d.text((12, 6), title, font=BAR, fill=(230, 230, 230))
    y = 42
    for line in lines:
        color = (86, 156, 214) if line.startswith(("$", ">")) else (
            (78, 201, 176) if line.startswith("==") else (204, 204, 204))
        d.text((16, y), line, font=FONT, fill=color)
        y += 22
    img.save(os.path.join(OUT, name))
    print("saved", name)


def capture(fn, *a, **k):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        fn(*a, **k)
    return buf.getvalue()


TITLE = "PowerShell - lesson_03"

# 01 запуск
c.init()
render("01-program-start.png", TITLE,
       "$ python catalog.py\n"
       "Подключение: mongodb://localhost:27017  (база catalog_db, коллекция products)\n"
       "Индексы созданы: sku (unique), category\n\n"
       "1. Показать все\n2. Поиск по названию\n3. Добавить товар\n4. Изменить цену\n"
       "5. Удалить товар\n6. Статистика\n7. Загрузить тестовые данные\n0. Выход\n> ")

# 02 создание
out = capture(c.seed)
n = c.products.count_documents({})
render("02-products-created.png", TITLE,
       "> 7\n" + (out or "") + f"Добавлено товаров: {n}\n"
       "Повторная вставка NB-001 -> DuplicateKeyError (уникальный индекс sku)")

# 03 каталог
render("03-catalog-result.png", TITLE,
       "> 1\n" + capture(c.show, c.products.find().sort("sku", 1)))

# 04 поиск
render("04-search-result.png", TITLE,
       "> 2\nтекст: ноутбук\n" + capture(c.show, c.search(text="ноутбук")) +
       "\n$ поиск: Смартфоны, в наличии, цена до 30000\n" +
       capture(c.show, c.search(category="Смартфоны", price_max=30000, in_stock=True)))

# 05 обновление и удаление
buf = "> 4\nsku: PR-002\nновая цена: 7990\n"
buf += f"изменено: {c.update_price('PR-002', 7990)}\n> 5\nsku: PH-002\n"
buf += f"удалено: {c.delete('PH-002')}\n\n> 1\n" + capture(c.show, c.products.find().sort("sku", 1))
render("05-update-or-delete-result.png", TITLE, buf)

# 06 проверка в базе
docs = list(c.products.find({"sku": "PR-002"}, {"_id": 0, "created": 0}))
txt = ("> db.products.find({sku: 'PR-002'})\n" + json.dumps(docs[0], ensure_ascii=False, indent=2) +
       f"\n\n> db.products.countDocuments({{}})\n{c.products.count_documents({})}\n\n"
       "> db.products.getIndexes()\n" +
       "\n".join(f"  {k}: {v['key']}" + ("  unique" if v.get("unique") else "")
                 for k, v in c.products.index_information().items()) +
       "\n\n> aggregate по категориям\n" + capture(c.stats))
render("06-database-check.png", "mongosh - catalog_db", txt)
