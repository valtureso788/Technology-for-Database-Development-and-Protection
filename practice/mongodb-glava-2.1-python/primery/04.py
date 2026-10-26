# Глава 2.1 · Фильтр — это документ. Точечная нотация
# Пример 4 из 6 · §5 Точечная нотация: поле внутри документа · поле внутри документа
#
# Запуск из папки архива:
#   docker compose run --rm python primery/04.py
#   cd primery, затем python 04.py (Windows) или python3 04.py (macOS, Linux)
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
for doc in vacancies.find({"salary.from": 60000},
                       {"title": 1, "salary": 1, "_id": 0}):
    print(doc)

print("выпускники СПО:", resumes.count_documents({"education.level": "СПО"}))
print("собеседования в Москве:", interviews.count_documents({"company.city": "Москва"}))
