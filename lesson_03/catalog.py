"""Каталог товаров на MongoDB: создание, просмотр, поиск, обновление, удаление.

Запуск:  python catalog.py          (нужен MongoDB на localhost:27017)
Проверка без сервера:  CATALOG_MOCK=1 python catalog.py --demo
"""
import os
import sys
from datetime import datetime, timezone

URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017")

if os.environ.get("CATALOG_MOCK"):
    import mongomock
    client = mongomock.MongoClient()
else:
    from pymongo import MongoClient
    client = MongoClient(URI, serverSelectionTimeoutMS=3000)

products = client["catalog_db"]["products"]


def init():
    """Уникальный SKU и индекс по категории."""
    products.create_index("sku", unique=True)
    products.create_index("category")


def create(sku, title, category, price, qty, specs=None):
    doc = {
        "sku": sku, "title": title, "category": category,
        "price": float(price), "qty": int(qty),
        "specs": specs or [], "created": datetime.now(timezone.utc),
    }
    return products.insert_one(doc).inserted_id


def seed():
    items = [
        ("NB-001", "Ноутбук Lenovo IdeaPad 3", "Ноутбуки", 42990, 8, ["15.6\"", "8 ГБ"]),
        ("NB-002", "Ноутбук ASUS VivoBook 15", "Ноутбуки", 51490, 5, ["15.6\"", "16 ГБ"]),
        ("PH-001", "Смартфон Xiaomi Redmi Note 13", "Смартфоны", 18990, 20, ["6.67\"", "128 ГБ"]),
        ("PH-002", "Смартфон Samsung Galaxy A55", "Смартфоны", 32990, 0, ["6.6\"", "256 ГБ"]),
        ("PR-001", "Мышь Logitech MX Master 3S", "Периферия", 9490, 12, ["Bluetooth"]),
        ("PR-002", "Клавиатура Keychron K2", "Периферия", 8990, 3, ["Bluetooth"]),
    ]
    for item in items:
        try:
            create(*item)
        except Exception as exc:  # дубликат SKU при повторном запуске
            print("пропуск", item[0], "-", type(exc).__name__)


def show(cursor):
    n = 0
    for p in cursor:
        n += 1
        print(f"{p['sku']:8} {p['title']:34} {p['category']:11} {p['price']:>9.2f} р.  на складе: {p['qty']}")
    print(f"всего: {n}")


def search(text=None, category=None, price_min=None, price_max=None, in_stock=False):
    query = {}
    if text:
        query["title"] = {"$regex": text, "$options": "i"}
    if category:
        query["category"] = category
    price = {}
    if price_min is not None:
        price["$gte"] = price_min
    if price_max is not None:
        price["$lte"] = price_max
    if price:
        query["price"] = price
    if in_stock:
        query["qty"] = {"$gt": 0}
    return products.find(query).sort("price", 1)


def update_price(sku, new_price):
    return products.update_one({"sku": sku}, {"$set": {"price": float(new_price)}}).modified_count


def add_stock(sku, delta):
    return products.update_one({"sku": sku}, {"$inc": {"qty": int(delta)}}).modified_count


def delete(sku):
    return products.delete_one({"sku": sku}).deleted_count


def stats():
    pipeline = [{"$group": {"_id": "$category", "count": {"$sum": 1},
                            "avg_price": {"$avg": "$price"}}},
                {"$sort": {"_id": 1}}]
    for row in products.aggregate(pipeline):
        print(f"{row['_id']:11} товаров: {row['count']}  средняя цена: {row['avg_price']:.2f}")


def demo():
    init()
    seed()
    print("\n== Весь каталог ==")
    show(products.find().sort("sku", 1))
    print("\n== Поиск: 'ноутбук' ==")
    show(search(text="ноутбук"))
    print("\n== Смартфоны в наличии до 30000 ==")
    show(search(category="Смартфоны", price_max=30000, in_stock=True))
    print("\n== Обновление цены PR-002 ->", 7990, "==")
    print("изменено:", update_price("PR-002", 7990))
    print("пополнение склада PR-001 +10, изменено:", add_stock("PR-001", 10))
    print("\n== Удаление PH-002 ==")
    print("удалено:", delete("PH-002"))
    print("\n== Итог ==")
    show(products.find().sort("sku", 1))
    print("\n== Статистика по категориям ==")
    stats()


def menu():
    init()
    actions = {
        "1": ("Показать все", lambda: show(products.find().sort("sku", 1))),
        "2": ("Поиск по названию", lambda: show(search(text=input("текст: ")))),
        "3": ("Добавить товар", lambda: print("id:", create(
            input("sku: "), input("название: "), input("категория: "),
            input("цена: "), input("количество: ")))),
        "4": ("Изменить цену", lambda: print("изменено:", update_price(
            input("sku: "), input("новая цена: ")))),
        "5": ("Удалить товар", lambda: print("удалено:", delete(input("sku: ")))),
        "6": ("Статистика", stats),
        "7": ("Загрузить тестовые данные", seed),
    }
    while True:
        print("\n" + "\n".join(f"{k}. {v[0]}" for k, v in actions.items()) + "\n0. Выход")
        choice = input("> ").strip()
        if choice == "0":
            return
        if choice in actions:
            try:
                actions[choice][1]()
            except Exception as exc:
                print("ошибка:", exc)


if __name__ == "__main__":
    demo() if "--demo" in sys.argv else menu()
