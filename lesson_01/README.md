# Занятие 1 · MongoDB: документ, BSON и первая коллекция

**Презентация:** https://algorthimization-course-vvodnoe.vercel.app/mdk0401-razrabotka-i-zashchita-baz-dannyh/lessons/02-mongodb-pervyy-dokument/index.html

**Домашнее задание:** [homework_01.md](homework_01.md)

**Предметная область:** заявки в службу технической поддержки.
**База:** `helpdesk`, **коллекция:** `tickets`, **документов:** 5.
Формы документов отличаются: у T-1003 и T-1005 нет поля `assignee`, у T-1004 есть
дополнительное поле `deadline`, у T-1005 — массив `comments`.

## Файлы

| Файл | Что внутри |
|---|---|
| [`seed.json`](seed.json) | массив из пяти документов для загрузки через ADD DATA → Import JSON |
| [`queries.md`](queries.md) | шесть фильтров, числа найденных документов, абзац про цену дубликата |
| [`screenshot.png`](screenshot.png) | Compass с коллекцией и счётчиком найденных документов |

## Как подключиться к серверу через Compass

1. Запустить сервер MongoDB в Docker (стенд курса, папка `stend` репозитория):

   ```bash
   cd stend
   docker compose up -d
   docker compose ps         # статус healthy
   ```

2. Открыть MongoDB Compass, нажать **Add new connection**, ввести строку
   подключения и нажать **Connect**:

   ```
   mongodb://localhost:27017
   ```

## Как загрузить данные

1. В Compass нажать **Create database**: имя базы `helpdesk`, коллекция `tickets`.
2. Открыть коллекцию `tickets` → **ADD DATA** → **Import JSON or CSV file**.
3. Выбрать [`seed.json`](seed.json), формат **JSON**, нажать **Import**.
4. Должно загрузиться 5 документов.

Либо из терминала:

```bash
docker cp seed.json <контейнер>:/seed.json
docker exec <контейнер> mongoimport --db helpdesk --collection tickets --jsonArray --file /seed.json
```

## Как выполнить запросы

В Compass открыть `helpdesk.tickets`, вставить фильтр из [`queries.md`](queries.md)
в поле **Filter** и нажать **Find**. Число найденных документов отображается
справа от списка (`1 – N of N`).

## Как удалить коллекцию

В Compass: наведите курсор на `tickets` в списке слева → значок корзины →
введите имя коллекции → **Drop Collection**.

Из терминала:

```js
use helpdesk
db.tickets.drop()
```

## Сдача

Ветка `hw-01`, коммит с содержательным сообщением, Pull Request в свою `main`
с описанием: предметная область и чем отличаются формы документов.

