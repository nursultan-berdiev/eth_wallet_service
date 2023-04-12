# Краткое описание проекта
Проект представляет собой веб-приложение для управления кошельками пользователей. 
Написан на Python 3.11 с использованием фреймворков 

`Django==4.2`
`DjangoRestFramework==3.14.0`
`web3.py==6.1.0`

и библиотеки DRF_SPECTACULAR для создания документации к API.

## Запуск сервиса
Для запуска сервиса необходимо установить Docker и Docker Compose. 

Для клонирования репозитория выполните команду:

`git clone https://github.com/nursultan-berdiev/eth_wallet_service.git`

Перейдите в директорию проекта выполнив команду:

`cd eth_wallet_service`

Если вы на Unix системах обновите разрешения файлов локально:

`chmod +x backend/entrypoint.sh`

В файле .env.dev укажите замените yourapikeyplaceherewhithoutquotes в API_KEY на полученный в https://infura.io/ без кавычек и пробелов

`ETH_API_KEY=yourapikeyplaceherewhithoutquotes`

Затем выполните команду в корневой директории проекта. 

`docker-compose up -d --build` 

Это построит и запустит сервисы backend и db в фоновом режиме, и веб-сервер будет доступен по адресу 

`http://127.0.0.1:8000/`.

## Запуск тестов
Для запуска тестов необходимо выполнить команду 

`docker-compose exec backend pytest` 

в корневой директории проекта.

## Документация к API
Для доступа к документации к API необходимо перейти по адресу 

`http://127.0.0.1:8000/api/schema/swagger-ui/` 

или 

`http://127.0.0.1:8000/api/schema/redoc/`

в зависимости от того, какую документацию вы хотите увидеть.

Документация создана с помощью библиотеки DRF_SPECTACULAR.
