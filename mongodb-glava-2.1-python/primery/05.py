# Глава 2.1 · Фильтр — это документ. Точечная нотация
# Пример 5 из 6 · §6 Точка и массивы · массив строк и массив документов
#
# Запуск из папки архива:
#   docker compose run --rm python primery/05.py
#   cd primery, затем python 05.py (Windows) или python3 05.py (macOS, Linux)
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
print("знают Python:", resumes.count_documents({"skills": "Python"}))

for doc in resumes.find({"experience.role": "стажёр"},
                     {"fio": 1, "_id": 0}):
    print(doc)
