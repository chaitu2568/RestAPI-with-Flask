from flask import Flask,jsonify,request,render_template

app=Flask(__name__)


stores=[
    {
    'name':'My First Store',
    'items':[
    {
    'name':'My first item',
    'price':19.99
    }
    ]
    }
]

@app.route('/store',methods=['POST'])
def create_store():
    request_item=request.get_json()
    new_item={
        'name':request_item['name'],
        'items':[]
    }
    stores.append(new_item)
    return jsonify(new_item)

@app.route('/store/<string:name>/')
def get_store(name):
    for store in stores:
        if store['name']==name:
            return jsonify(store)
    return jsonify({'message':'store not found'})


@app.route('/store')
def get_stores():
    return jsonify({'stores':stores})

@app.route('/store/<string:name>/item',methods=['POST'])
def create_item_in_store(name):
    request_item=request.get_json()
    for store in stores:
        if store['name']==name:
            new_item={
                'name':request_item['name'],
                'price':request_item['price']
            }
            store['items'].append(new_item)
            return jsonify(new_item)
    return jsonify({'message':'store item not found'})

@app.route('/store/<string:name>/item')
def get_items_in_store(name):
    for store in stores:
        if store['name']==name:
            return jsonify({'items':store['items']})
    return jsonify({'message':'there are no items in store'})

@app.route('/')
def home():
    return render_template('index.html')

app.run(port=4999)
