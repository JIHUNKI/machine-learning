from pymongo import MongoClient
from face_attendence import rectangle_detect

client = MongoClient('mongodb+srv://root:1234@cluster0.jywxwoy.mongodb.net/?retryWrites=true&w=majority')

db = client.information


# post = {"name":"기지훈","idnumber":"939393-2299292" }
# db.ID.insert_one(post)

# file_name = rectangle_detect('./image/id_4.jpg')
# with open(f'{file_name}.txt', 'r', encoding='UTF-8') as f:
#     text = f.read()
#     doc = {
#         "filename":f'{file_name}.txt',
#         "id_info": text
#     }
#     db.ID.insert_one(doc)

all_id = list (db.ID.find({},{'_id':False}))
print(all_id)

user = db.ID.find_one({"name":"기지훈"},{"_id": False})
print(user)