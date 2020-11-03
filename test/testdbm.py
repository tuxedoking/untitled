import dbm

db = dbm.open('Bookmark', 'c')
print(dbm.whichdb('Bookmark'))
#db['MyBlog'] = 'jonathanlife.sinaapp.com'
try:
    print(db['MyBlog2'])
except KeyError as err:
    print(err)
#保存，关闭
db.close()