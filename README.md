# A simple database manager with sqlalchemy

### Installation
```bash
python3 -m pip install sql_manager
```

### Basic Usage
```python
from sqlalchemy import Column, Integer, String
from sql_manager import DynamicModel, Manager

# create model
columns = {
    'uid': Column(Integer, primary_key=True, comment='the unique identity'),
    'name': Column(String(10), comment='the username', default='zoro')}

Data = DynamicModel('OnePiece', columns, 'user')

print(Data.get_table())
'''
+------+---------------------+-------------+-----------------------+
| Key  | Comment             | Type        | Default               |
+------+---------------------+-------------+-----------------------+
| uid  | the unique identity | INTEGER     | None                  |
| name | the username        | VARCHAR(10) | ColumnDefault('zoro') |
+------+---------------------+-------------+-----------------------+
'''

data = Data(uid=1, name='luffy')
print(data)
'''
OnePiece <{'uid': 1, 'name': 'luffy'}>
'''

# insert one data
with Manager(Data, dbfile='test.db') as m:
    data = Data(uid=1, name='luffy')
    m.insert(Data, 'uid', data)
'''
[2021-06-21 16:10:48 Manager insert DEBUG MainThread:95] >>> insert data: OnePiece <{'uid': 2, 'name': 'luffy'}>
[2021-06-21 16:10:48 Manager __exit__ DEBUG MainThread:34] database closed.
'''

# insert multiple datas
with Manager(Data, dbfile='test.db') as m:
    datas = [Data(uid=uid, name=name) for uid, name in zip([2, 3, 4], ['sanji', 'chopper', 'nami'])]
    m.insert(Data, 'uid', datas)
'''
[2021-06-21 16:19:08 Manager insert DEBUG MainThread:95] >>> insert data: OnePiece <{'uid': 2, 'name': 'sanji'}>
[2021-06-21 16:19:08 Manager insert DEBUG MainThread:95] >>> insert data: OnePiece <{'uid': 3, 'name': 'chopper'}>
[2021-06-21 16:19:08 Manager insert DEBUG MainThread:95] >>> insert data: OnePiece <{'uid': 4, 'name': 'nami'}>
[2021-06-21 16:19:08 Manager __exit__ DEBUG MainThread:34] database closed.
'''

# query, delete
with Manager(Data, dbfile='test.db') as m:
    res = m.query(Data, 'uid', 1)
    print(res.all())
    m.delete(Data, 'uid', 2)    
'''
[OnePiece <{'uid': 1, 'name': 'luffy'}>]
[2021-06-21 16:19:36 Manager delete DEBUG MainThread:76] delete 1 row(s)
[2021-06-21 16:19:36 Manager __exit__ DEBUG MainThread:34] database closed.
'''


# other origin methods
with Manager(Data, dbfile='test.db') as m:
    query = m.session.query(Data)
    res = query.filter(Data.name.like('%op%')).limit(1)
    print(res)
    print(res.all())
'''
SELECT user.uid AS user_uid, user.name AS user_name 
FROM user 
WHERE user.name LIKE ?
 LIMIT ? OFFSET ?
[OnePiece <{'uid': 3, 'name': 'chopper'}>]
[2021-06-21 16:24:07 Manager __exit__ DEBUG MainThread:34] database closed.
''' 
```

### Document
https://sql-manager.readthedocs.io/en/latest/
