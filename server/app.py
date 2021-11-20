from flask import Flask, render_template, Response, jsonify,request
import time
import datetime
import sys
from pymongo import MongoClient
import datetime
from pytz import timezone



datetime.datetime.now(timezone('Asia/Seoul'))
now = datetime.datetime.now()
client = MongoClient("mongodb+srv://root:toor@cluster0.50yj2.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
Refri_db = client['Refrigerator']
Recipe_db = client['Recipe']
Refri_col = Refri_db["post"]
Recipe_col = Recipe_db["post"]
class_name=['bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot']
class_list ={"bowl":"그릇","banana": "바나나","apple": "사과","sandwich": "샌드위치","orange": "오렌지","broccoli": "브로콜리","carrot": "당근"}



def get_ingredients():
    cursor = Refri_col.find()
    col_list = []
    for document in cursor:
            col_list.append(document['name'])
    return col_list


def get_makeable_recipe(detect_list):
    cursor = Recipe_col.find()
    conv_detect_list=[]
    intersection=[]
    collect_res={}
    name_list=[]
    for item in detect_list:
        conv_detect_list.append(class_list[item])
    for document in cursor:
        col_list=[]
        item_list = document["ingredients"]["주재료"]
        for item in item_list:
            for key,val in item.items():
                col_list.append(key)
            
        intersection = list(set(col_list) & set(conv_detect_list))
        if len(intersection) > 0:
            col_list.append(len(col_list))
            col_list.append(len(intersection))
            col_list.append(document["picture"])
            collect_res[document["name"]] = col_list
    print(collect_res)
    collect_res = sorted(collect_res.items(),reverse=False, key=lambda item:(int(item[1][-3]) - int(item[1][-2])))
    
    for item in collect_res:
        tmp=[]
        tmp.append(item[0])
        tmp.append(item[1][-1])
        name_list.append(tmp)
    return name_list

def get_recipe_info(name):
    cursor = Recipe_col.find({"name":name},{"_id":0})
    res = {}
    for document in cursor:
        res = document
    return res

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
@app.route('/')
def index():
    return "hello"



@app.route("/get_data")
def get_data():
    get_list = get_ingredients()
    return jsonify(get_list)



@app.route("/get_makeable_recipe")
def get_makeable():
    detect_list = get_ingredients()
    get_list = get_makeable_recipe(detect_list)
    return jsonify(get_list)


@app.route("/get_recipe")
def get_recipe():
    if request.args.get("name"):
        name = request.args.get("name")
        print(name)
        get_list = get_recipe_info(name)
        return jsonify(get_list)
    else:
        return "Input recipe name, please"
    

if __name__ == '__main__':
    app.run(host='0.0.0.0') 