from sqlalchemy import Column
from sqlalchemy.orm.state import InstanceState
from sqlalchemy.ext.declarative import declarative_base



def as_dict(self):
    """convert columns to ``dict``
    """
    return {k: v for k, v in self.__dict__.items() if not isinstance(v, InstanceState)}


def DynamicModel(name, columns, tablename='data'):
    """Create a Base Model

    :param name: name of model
    :param columns: dict of sqlalchemy columns, eg. {'id': Column(...)}
    :param tablename: name of table
    
    :returns: (Base, Model)
    """
    Base = declarative_base()

    map_data = {
        '__tablename__': tablename,
        'as_dict': as_dict
    }

    return Base, type(name, (Base,), dict(columns, **map_data))
