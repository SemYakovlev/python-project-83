#!/usr/bin/env bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
make install && psql -a -d $DATABASE_URL -f database.sql

##!/usr/bin/env bash
#
## Скачиваем и устанавливаем uv
#curl -LsSf https://astral.sh/uv/install.sh | sh
#source $HOME/.local/bin/env
#
## Устанавливаем зависимости проекта
#make install
#
## ЭКСПОРТИРУЕМ переменные из .env файла, если он существует локально
#if [ -f .env ]; then
#  export $(cat .env | xargs)
#fi
#
## Теперь проверяем, что DATABASE_URL точно заполнена (локально или на Render)
#if [ -n "$DATABASE_URL" ]; then
#  psql -a -d "$DATABASE_URL" -f database.sql
#fi