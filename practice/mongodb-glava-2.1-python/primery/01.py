# Глава 2.1 · Фильтр — это документ. Точечная нотация
# Пример 1 из 6 · §2 Фильтр — это документ · резюме из одного города
#
# Запуск из папки архива:
#   docker compose run --rm python primery/01.py
#   cd primery, затем python 01.py (Windows) или python3 01.py (macOS, Linux)
# Что должно получиться — в README.md, раздел «Примеры и выводы».

import os
from pymongo import MongoClient

client = MongoClient(os.environ.get("MONGO_URI", "mongodb://localhost:27017/"))
db = client["hh"]
resumes = db["resumes"]
vacancies = db["vacancies"]
companies = db["companies"]
interviews = db["interviews"]
box = client["sandbox"]["products"]        # песочница: здесь можно менять

# ── пример из главы ───────────────────────────────────────────
for doc in resumes.find({"city": "Ярославль"},
                     {"fio": 1, "position": 1, "_id": 0}):
    print(doc)
