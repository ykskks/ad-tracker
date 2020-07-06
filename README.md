# 手順

### set up environment
```
docker-compose up --build -d
docker-compose exec app bash
```

### set up DB
```
psql
>> psql: could not connect to server: No such file or directory
        Is the server running locally and accepting
        connections on Unix domain socket "/var/run/postgresql/.s.PGSQL.5432"?

pg_ctlcluster 11 main start
sudo -u postgres psql

CREATE DATABASE adtracker;
CREATE USER test WITH PASSWORD 'test';
ALTER ROLE test SET client_encoding TO 'utf8';
ALTER ROLE test SET default_transaction_isolation TO 'read committed';
ALTER ROLE test SET timezone TO 'Japan';
GRANT ALL PRIVILEGES ON DATABASE adtracker TO test;
\q
```

```
python manage.py migrate
python manage.py createsuperuser
```

```
python manage.py cron
```
を実行すればDBに登録されてる全てのAdvertiser idに対してad一覧を取得し、そのうちDBに保存されてないadを保存する。
