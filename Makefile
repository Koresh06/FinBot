DC = docker compose
EXEC = docker exec -it
LOGS = docker logs
APP_CONTAINER = main-app
BOT_CONTAINER = finance_bot

# Запуск приложения через Poetry (локально)
start:
	poetry run python -m src.main


.PHONY: all # make all - Запускает и собирает оба сервиса (бот и приложение) в фоне
all:
	${DC} -f up --build -d

.PHONY: start # make start - Запустить контейнеры
start:
	${DC} start

.PHONY: down # make down - Удалить контенеры
down:
	${DC} down -v

.PHONY: stop # make stop - Остановить контенеры
stop:
	${DC} stop

.PHONY: logs # make stop - Смотреть все логи
logs:
	${DC} logs

.PHONY: app-down # make app-down - Остановить и удалить контейнер приложения
app-down:
	${DC} -f ${APP_FILE} down

.PHONY: app-shell # make app-shell - Зайти в контейнер с приложением (shell bash)
app-shell:
	${EXEC} ${APP_CONTAINER} bash

.PHONY: app-logs # make app-logs - Смотреть логи контейнера с приложением: в реальном времени (-f)
app-logs:
	${LOGS} ${APP_CONTAINER}

.PHONY: bot-shell # make bot-shell - Зайти в контейнер с ботом (shell bash)
bot-shell:
	${EXEC} ${BOT_CONTAINER} bash

.PHONY: bot-logs # make bot-logs - Смотреть логи контейнера с ботом: в реальном времени (-f)
bot-logs:
	${LOGS} ${BOT_CONTAINER}

.PHONY: bot-down # make bot-down - Остановить и удалить контейнер бота
bot-down:
	${DC} -f ${BOT_FILE} down
