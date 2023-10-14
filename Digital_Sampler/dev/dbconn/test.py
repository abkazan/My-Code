import sqlalchemy

# TODO These arguments as dummies THEY WILL NOT WORK :D
url = sqlalchemy.engine.URL.create (
    drivername = "mysql",
    username = "root",
    password = "admin",
    host = 'cs506-team-35.cs.wisc.edu',
    port = '3306',
    database = "sample_lib"
)

try:
    _engine = sqlalchemy.create_engine(url)
except Exception as exe:
    exe.args = (f'Issues creating database engine with url "{url}"', *exe.args)
    raise

_meta = sqlalchemy.MetaData()

try:
    _table = sqlalchemy.Table('sample', _meta, autoload_with = _engine)
except Exception as exe:
    exe.args = (f'Issues with table lookup for table sample', *exe.args)
    raise