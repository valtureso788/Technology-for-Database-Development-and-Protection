# Глава 2.1 · Фильтр — это документ. Точечная нотация
# Пример 6 из 6 · §7 Пустой фильтр · пустой фильтр
#
# Запуск из папки архива:
#   docker compose run --rm python primery/06.py
#   cd primery, затем python 06.py (Windows) или python3 06.py (macOS, Linux)
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
print("всего резюме:", resumes.count_documents({}))
print("всего собеседований:", interviews.count_documents({}))
