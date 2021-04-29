import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.state import InstanceState

from simple_loggers import SimpleLogger


class Manager(object):
    """The Database Manager

    :param Base: ``Base`` object created by ``DynamicModel``
    :param dbfile: path of database file
    :param uri: uri of database. SQLite3: ``sqlite:///test.db``, MySQL: ``mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}/{DBNAME}``
    :param echo: turn echo on
    :param drop: drop table before create
    :param logger: a logging object

    :examples:
    >>> from sqlalchemy import Column, Integer
    >>> from sql_manager import DynamicModel, Manager
    >>> columns = {'uid': Column(Interger, primary_key=True), 'name': Column(String(10), comment='the username')}
    >>> Base, Data = DynamicModel('TEST', columns, 'test')
    >>> with Manager(Base, dbfile='test.db') as m:
    >>>     data = Data(uid=1, name='zoro')
    >>>     m.insert(Data, 'uid', data)
    """
    def __init__(self, Base, dbfile=':memory:', uri=None, echo=False, drop=False, logger=None):
        self.Base = Base
        self.drop = drop
        self.uri = uri if uri else f'sqlite:///{dbfile}'
        self.logger = logger or SimpleLogger('Manager')
        self.engine = sqlalchemy.create_engine(self.uri, echo=echo)
        self.engine.logger.level = self.logger.level
        self.session = self.connect()
    
    def __enter__(self):
        self.create_table(drop=self.drop)
        return self

    def __exit__(self, *exc_info):
        self.session.commit()
        self.session.close()
        self.logger.debug('database closed.')

    def connect(self):
        """create a connection
        """
        DBSession = sessionmaker(bind=self.engine)
        return DBSession()

    def create_table(self, drop=False):
        """create all table from Base and Model
        """
        if drop:
            self.Base.metadata.drop_all(self.engine)
        self.Base.metadata.create_all(self.engine)

    def query(self, Meta, key=None, value=None, like=False):
        """query database with key-value

        :param Meta: the meta model
        :param key: the field name
        :param value: the field value
        :returns: a query object of sqlalchemy
        """
        query = self.session.query(Meta)
        if key:
            if key not in Meta.__dict__:
                self.logger.warning(f'unavailable key: {key}')
                return None
            else:
                query = query.filter(Meta.__dict__[key]==value)

        return query

    def delete(self, Meta, key, value):
        """delete row(s) by key-value

        :param Meta: the meta model
        :param key: the field name
        :param value: the field value
        """
        res = self.query(Meta, key, value)
        if res.count():
            self.logger.debug(f'delete {res.count()} row(s)')
            res.delete()
        else:
            self.logger.debug(f'key input not in database: {key}={value}')

    def insert(self, Meta, key, datas, upsert=True):
        """insert data

        :param Meta: the meta model
        :param key: the field name
        :param data: an instance of Meta, or a list of instance
        :param upsert: add when key not exists, update when key exists
        """
        if isinstance(datas, self.Base):
            datas = [datas]

        for data in datas:
            res = self.query(Meta, key, data.__dict__[key])
            if not res.first():
                self.logger.debug(f'>>> insert data: {data}')
                self.session.add(data)
            elif upsert:
                self.logger.debug(f'>>> update data: {data}')
                context = {k: v for k, v in data.__dict__.items() if not isinstance(v, InstanceState)}
                res.update(context)
