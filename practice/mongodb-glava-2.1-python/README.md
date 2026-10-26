# Глава 2.1 · Фильтр — это документ. Точечная нотация — примеры на Python

Архив к «Справочнику по MongoDB»: все примеры главы готовыми программами, учебные базы и стенд в Docker.
Глава: https://maximbytecamp.github.io/mongodb_theory_makarov/temy/09-filtr-i-tochechnaya-notaciya/index.html

Язык: **Python** · драйвер PyMongo · сервер MongoDB 7.

## Что в архиве

```text
mongodb-glava-2.1-python/
  README.md         эта инструкция
  primery/          примеры главы — по программе на пример
    01.py … 06.py
  compose.yaml      стенд в Docker: сервер, базы, mongo-express, Python
  docker/           образ с драйвером Python и скрипт запуска run.sh
  stend/seed/       учебные данные: 12 файлов JSON
  stend/load.ps1    загрузка данных на установленный сервер — Windows
  stend/load.sh     то же — macOS и Linux
requirements.txt  драйвер PyMongo для pip и для образа Docker
```

## Порядок работы

1. **Базы.** Глава **только читает** данные — сбрасывать базы не нужно.
2. **Примеры — по порядку, каждый один раз.** Пример в главе рассчитан на данные, которые оставил
   предыдущий. Если запустить пример дважды или пропустить, числа разойдутся с книгой — тогда
   сбросьте базы и начните с `01.py`.
3. **Сверка.** Что должна напечатать каждая программа — в разделе «Примеры и выводы» ниже.
   Отличаться могут только `_id`, которые выдаёт сервер, текущие дата и время и порядок
   в списке коллекций: сервер отдаёт их имена в произвольном порядке. У документа, который
   создан обновлением с `upsert`, поля тоже могут идти в другом порядке — значения при этом те же.

Подойдёт любой из двух способов. Адрес сервера в обоих — `mongodb://localhost:27017`, код примеров
одинаковый.

| Способ | Что нужно | Когда подходит |
|---|---|---|
| **1. Docker** | Docker Desktop | Compass и сервер не установились или не подключаются; ничего, кроме Docker, ставить не нужно |
| **2. Сервер и Compass** | MongoDB Server, Compass, Python с драйвером | сервер и Compass уже стоят и подключаются |

## Способ 1. Docker

Docker Desktop — с [docker.com](https://www.docker.com/products/docker-desktop/); на Linux — Docker Engine.
Перед командами Docker Desktop должен быть запущен. Команды одинаковые в PowerShell, cmd и терминале
macOS/Linux; выполняйте их **из папки архива** — там, где лежит `compose.yaml`.

1. Поднять сервер и загрузить учебные базы:

   ```bash
   docker compose up -d
   ```

2. Запустить пример — путь к файлу пишется от папки архива:

   ```bash
   docker compose run --rm python primery/01.py
   ```

   При первом запуске Docker соберёт образ с драйвером Python — это пара минут.
   Дальше запуск идёт за секунды.

3. Все примеры главы подряд, по порядку, одной командой:

   ```bash
   docker compose run --rm python primery
   ```

   Перед каждой программой печатается её имя: `── primery/01.py ──`.

**Смотреть данные.** Compass не нужен: в браузере откройте http://localhost:8081, логин `student`,
пароль `student` — это mongo-express, в нём видны базы, коллекции и документы. Если Compass
установлен, он подключается к этому же серверу по адресу `mongodb://localhost:27017`.

**Консоль сервера:** `docker compose exec mongo mongosh`.

**Остановить и удалить:**

```bash
docker compose stop        # остановить; данные останутся
docker compose down        # удалить контейнеры; данные останутся
docker compose down -v     # удалить всё вместе с данными
```

Архивы всех глав пользуются одним и тем же сервером и данными: после этой главы можно распаковать
архив следующей и работать там, не удаляя стенд.

## Способ 2. Установленный сервер MongoDB и Compass

Нужны MongoDB Server 7 или 8 и MongoDB Compass — установка по шагам в
[главе 1.0а](https://maximbytecamp.github.io/mongodb_theory_makarov/temy/00a-windows-10-mongodb-7/index.html).
Проверка: Compass подключается к `mongodb://localhost:27017`.

### Шаг 1. Загрузить учебные базы

Windows, PowerShell, из папки архива — нужен `mongoimport` из MongoDB Command Line Database Tools:

```powershell
powershell -ExecutionPolicy Bypass -File stend\load.ps1
```

macOS и Linux (`mongoimport`: `brew tap mongodb/brew && brew install mongodb-database-tools`):

```bash
bash stend/load.sh
```

Скрипт пересоздаёт коллекции целиком, поэтому он же сбрасывает базы: повторный запуск ничего не двоит.

**Без `mongoimport` — через Compass.** Подключитесь к `mongodb://localhost:27017`, нажмите **Create database**,
затем в коллекции **Add data → Import JSON or CSV file** и выберите файл из `stend/seed`. Имя файла
подсказывает, куда класть: `shop.orders.json` — база `shop`, коллекция `orders`. Так загружаются все
12 файлов; пошагово с кадрами — [глава 1.0, §7](https://maximbytecamp.github.io/mongodb_theory_makarov/temy/00-uchebnye-bazy/index.html#s7).

После загрузки в Compass нажмите **Refresh**: в списке должны быть базы `shop`, `hh`, `logs`, `org`
и `sandbox`. В `shop.products` — 21 документ, в `shop.orders` — 120.

### Шаг 2. Драйвер Python и запуск

Python 3.10 или новее — с [python.org](https://www.python.org/downloads/). На Windows в установщике
отметьте **Add python.exe to PATH**.

Windows, PowerShell, из папки архива:

```powershell
python -m pip install -r requirements.txt
cd primery
python 01.py
```

macOS и Linux — драйвер ставится в виртуальное окружение: системный Python не даёт ставить пакеты напрямую.

```bash
python3 -m venv .venv
source .venv/bin/activate          # в каждом новом терминале снова
pip install -r requirements.txt
cd primery
python3 01.py
```

Если `venv` не найден на Linux: `sudo apt install python3-venv`.

Остальные примеры запускаются так же: `02.py`, `03.py` и далее. Если сервер слушает другой адрес,
задайте его переменной `MONGO_URI` — программы глав 1.2–1.8 читают её при подключении.

## Примеры и выводы

| Файл | Параграф главы | Что делает |
|---|---|---|
| `01.py` | §2 Фильтр — это документ | резюме из одного города |
| `02.py` | §3 Несколько условий: все должны выполниться | город и должность |
| `03.py` | §4 Значение должно совпасть точно | тип и регистр значения |
| `04.py` | §5 Точечная нотация: поле внутри документа | поле внутри документа |
| `05.py` | §6 Точка и массивы | массив строк и массив документов |
| `06.py` | §7 Пустой фильтр | пустой фильтр |

### 01.py · §2 Фильтр — это документ

Резюме из одного города.

```text
{'fio': 'Анна Белова', 'position': 'Junior Python-разработчик'}
{'fio': 'Пётр Ковалёв', 'position': 'Junior Python-разработчик'}
{'fio': 'Игорь Самойлов', 'position': 'Backend-разработчик C#'}
{'fio': 'Ксения Лапина', 'position': 'Тестировщик'}
{'fio': 'Ольга Пирогова', 'position': 'Аналитик данных'}
```

### 02.py · §3 Несколько условий: все должны выполниться

Город и должность.

```text
город: 5
город и должность: 2
{'fio': 'Анна Белова', 'salary': 65000}
{'fio': 'Пётр Ковалёв', 'salary': 70000}
```

### 03.py · §4 Значение должно совпасть точно

Тип и регистр значения.

```text
salary 70000 числом:  1
salary '70000' строкой: 0
is_open True:           8
is_open 'true':         0
город с маленькой:      0
```

### 04.py · §5 Точечная нотация: поле внутри документа

Поле внутри документа.

```text
{'title': 'Junior Python-разработчик', 'salary': {'from': 60000, 'to': 90000}}
выпускники СПО: 4
собеседования в Москве: 27
```

### 05.py · §6 Точка и массивы

Массив строк и массив документов.

```text
знают Python: 6
{'fio': 'Пётр Ковалёв'}
{'fio': 'Алина Дроздова'}
```

### 06.py · §7 Пустой фильтр

Пустой фильтр.

```text
всего резюме: 9
всего собеседований: 60
```

## Частые ошибки

| Что видно | Причина | Что сделать |
|---|---|---|
| `port is already allocated`, `address already in use` на `docker compose up -d` | порт 27017 занят: уже работает установленный MongoDB или стенд `mongodb-practice` | остановите тот сервер или создайте рядом с `compose.yaml` файл `.env` со строкой `MONGO_PORT=27018`: в PowerShell — `Set-Content .env "MONGO_PORT=27018"`, в bash — `echo "MONGO_PORT=27018" > .env`. Программы в Docker это не затрагивает, Compass подключайте к `localhost:27018` |
| `Cannot connect to the Docker daemon`, `error during connect` | Docker Desktop не запущен | запустите Docker Desktop и дождитесь зелёного статуса Engine running |
| `ServerSelectionTimeoutError`, `Connection refused`, `No server available` | сервер не запущен | Docker: `docker compose up -d`; способ 2 — запустите службу MongoDB |
| `Файл не найден: …` | путь написан не от папки архива или команда выполнена в другой папке | перейдите в папку, где лежит `compose.yaml`, и пишите путь `primery/01.py` |
| числа в выводе не совпадают с README | пример запускали дважды, пропустили или базы не сброшены | сбросьте базы и запустите примеры с первого по порядку |

В PowerShell не используйте `echo … > .env`: Windows PowerShell 5 пишет такой файл в UTF-16, и Docker
Compose его не прочитает.
