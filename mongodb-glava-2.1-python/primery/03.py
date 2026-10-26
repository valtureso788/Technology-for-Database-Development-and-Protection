# Глава 2.1 · Фильтр — это документ. Точечная нотация
# Пример 3 из 6 · §4 Значение должно совпасть точно · тип и регистр значения
#
# Запуск из папки архива:
#   docker compose run --rm python primery/03.py
#   cd primery, затем python 03.py (Windows) или python3 03.py (macOS, Linux)
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
print("salary 70000 числом: ", resumes.count_documents({"salary": 70000}))
print("salary '70000' строкой:", resumes.count_documents({"salary": "70000"}))
print("is_open True:          ", vacancies.count_documents({"is_open": True}))
print("is_open 'true':        ", vacancies.count_documents({"is_open": "true"}))
print("город с маленькой:     ", resumes.count_documents({"city": "ярославль"}))
