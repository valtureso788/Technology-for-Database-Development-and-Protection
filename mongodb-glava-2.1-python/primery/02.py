# Глава 2.1 · Фильтр — это документ. Точечная нотация
# Пример 2 из 6 · §3 Несколько условий: все должны выполниться · город и должность
#
# Запуск из папки архива:
#   docker compose run --rm python primery/02.py
#   cd primery, затем python 02.py (Windows) или python3 02.py (macOS, Linux)
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
filtr = {"city": "Ярославль",
         "position": "Junior Python-разработчик"}

print("город:", resumes.count_documents({"city": "Ярославль"}))
print("город и должность:", resumes.count_documents(filtr))

for doc in resumes.find(filtr, {"fio": 1, "salary": 1, "_id": 0}):
    print(doc)
