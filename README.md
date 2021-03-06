# FastSearch
Задание:

Написать поисковую систему по текстам документов

Данные хранятся в базе данных, а поисковый индекс в ElasticSearch

Структура БД:
* id - уникальный для каждого документа;
* rubrics - массив рубрик;
* text - текст документа;
* created_date - дата создания документа.
Структура Индекса:
* iD - уникальный для каждого документа;
* text - текст документа (в задании было текст из структуры БД)

Необходимые методы
* сервис должен принимать на вход произвольный текстовый запрос, искать по тексту документа в индексе и возвращать первые 20 документов со всем полями БД, упорядоченные по дате создания;
* удалять документ из БД и индекса по полю  id.

Реализация:
* БД - Postgresql
* Полнотекстовый поиск - ElasticSearch
* сервер на FastAPI + uvicorn

Сервис работает в Docker
Гайд по поднятию:
1. В файле config.py указать параметры: ip внешнего интерфейса (остальные параметры можно оставить по-умолчанию)
2. зайти в папку deployESPostgres и вызвать команду: docker-compose up -d
3. в основной папке проекта (FastSearch) docker-compose up

Данные сначала импортируются в БД и Elastic, а затем запустится сервер (port 8000)

Документацию в формате OpenAPI можно получить пройдя по ссылке http://yourip:8000/docs

Тесты реализованы с помощью pytest

В процессе сборки образа происходит загрузка данных в Elastic и Postgres.
В дальнейшем можно добавить Docker volumes, чтобы каждый раз не импортировать данные.


