## HOW IT WORKS

1. Copy file service.env in current directory

# start app
docker compose up -d

# restart app
docker compose down & docker compose up -d

# stop app
docker compose down

2. Open app by URL: http://localhost/api/bday_time/test


# bday_time
Tg app about bday




# Alembic
alembic revision --autogenerate -m 'initial'
alembic upgrade head
alembic upgrade +1

alembic downgrade -1



# other style options
https://codepen.io/Markshall/pen/ExPxpYX


