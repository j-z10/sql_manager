# A simple database manager with sqlalchemy

### Installation
```bash
python3 -m pip install sql_manager
```

### Basic Usage
```python
from sqlalchemy import Column, Integer
from sql_manager import DynamicModel, Manager

# create model
columns = {
    'uid': Column(Interger, primary_key=True),
    'name': Column(String(10), comment='the username')}
Base, Data = DynamicModel('TEST', columns, 'test')

# insert data
with Manager(Base, dbfile='test.db') as m:
    data = Data(uid=1, name='zoro')
    m.insert(Data, 'uid', data)

# query, delete
with Manager(Base, dbfile='test.db') as m:
    res = m.query(Data, 'uid', 1)
    print(res.all())
    m.delete(Data, 'uid', 1)    

# other origin methods
with Manager(Base, dbfile='test.db') as m:
    query = m.session.query(Data)
    query.filter(Data.name.like('%zo%')).limit(1)
```

### Document
https://sql-manager.readthedocs.io/en/latest/
