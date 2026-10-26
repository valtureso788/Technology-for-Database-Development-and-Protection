# Technology-for-Database-Development-and-Protection

Репозиторий с работами по курсу «Технология разработки и защиты баз данных»
(MongoDB): домашние задания, практика и учебный стенд.

## Требования

| Что | Зачем |
|---|---|
| **Docker Desktop** | запуск MongoDB в контейнере |
| **MongoDB Compass** | графический клиент для запросов и данных |
| **git** | контроль версий |

Проверка Docker:

```bash
docker --version
docker compose version
```

## Запуск стенда

```bash
cd stend
docker compose up -d      # поднять MongoDB
docker compose ps         # статус должен быть healthy
```

Строка подключения для Compass: `mongodb://localhost:27017`.

Сброс к исходному состоянию:

```bash
docker compose down -v
docker compose up -d
```

Подробнее: [`stend/SETUP.md`](stend/SETUP.md).

## Структура

```
stend/          стенд: docker-compose.yml и тестовые данные (seed/)
lesson_01/      Занятие 1: MongoDB, документ, BSON
lesson_02/      Занятие 2: embedding и referencing
lesson_03/      Занятие 3: проектирование «Каталог товаров»
lesson_04/      Занятие 4: план запроса (explain) и индексы — выполнено
lesson_05/      Занятие 5: скрипт подбора
lesson_06/      Занятие 6: практикум «Аналитик»
lesson_07/      Занятие 7: практикум «Индексы»
practice/       дополнительная практика и стенды
  mongodb-glava-2.1-python/   примеры на Python (глава 2.1)
  mongodb-practice/           практический стенд (Python, Go, C++, Ruby)
  mongodb-practice-main/      базовая версия практического стенда
lectures/       конспекты занятий
materials/      материалы и скрипты к занятиям
docs/git/       инструкция по работе с git в VS Code
```

## Статус заданий

| Занятие | Задание | Статус |
|---|---|---|
| 1–3 | `lesson_01` … `lesson_03` | по шаблону |
| 4 | [`lesson_04`](lesson_04/README.md) — отчёт и 6 планов `plan-*.json` | выполнено |
| 5–7 | `lesson_05` … `lesson_07` | по шаблону |

## Работа с репозиторием

Каждое задание — отдельная ветка `hw-XX` и Pull Request в `main`.
