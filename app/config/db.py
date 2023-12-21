from urllib.parse import quote_plus
from os.path import dirname, abspath, join

BASEDIR = abspath(dirname(dirname(__file__)))


class DB:
    def sqlite_uri(self):
        db_path = join(BASEDIR, 'db', 'data.sqlite')
        return f'sqlite:///{db_path}'

    def postgres_uri(self):
        dialect = 'postgresql'
        host = 'postgres'
        # host = '52.74.252.162'
        user = 'fedb'
        db = 'fedbproduction'
        port = '5432'
        password = 'FeSys2357.!'
        db_uri = f'{dialect}://{user}:{quote_plus(password)}@{host}:{port}/{db}'
        return db_uri
