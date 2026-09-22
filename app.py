from flask import Flask, request, jsonify

app = Flask(__name__)

menu = [
    {"id": 1, "name": "Плов",      "category": "main",  "price": 40, "available": True},
    {"id": 2, "name": "Шурбо",     "category": "soup",  "price": 30, "available": True},
    {"id": 3, "name": "Самбуса",   "category": "snack", "price": 10, "available": False},
    {"id": 4, "name": "Чай",       "category": "drink", "price": 5,  "available": True},
    {"id": 5, "name": "Кофе",      "category": "drink", "price": 15, "available": False},
]

@app.route('/menu', methods=["GET"])
def show_menu():
    filtered_list = menu.copy()

    max_price = request.args.get('max_price')
    if max_price:
        max_price = int(max_price)
        new_list = []
        
        for dish in filtered_list:
            if dish['price'] <= max_price:
                new_list.append(dish)

        filtered_list = new_list



    available = request.args.get('available')
    if available:
        new_list = []      

        if available == 'true':
            for dish in filtered_list:
                if dish['available'] == True:
                    new_list.append(dish)


        elif available == 'false':
            for dish in filtered_list:
                if dish['available'] == False:
                    new_list.append(dish)

        filtered_list = new_list      


    return jsonify(filtered_list)

@app.route('/menu', methods=['POST'])
def add_dish():
    data = request.get_json()
    if not data or not 'name' in data or not 'category' in data or not 'price' in data or not 'available' in data:
        return "Не забудьте заполнить все поля!", 400

    new_id = max(dish['id'] for dish in menu) + 1
    new_dish = {
        'id' : new_id,
        'name' : data['name'],
        'category' : data['category'],
        'price' : data['price'],
        'available' : data['available']
    }

    menu.append(new_dish)

    return jsonify(new_dish)


    

@app.route('/menu/<int:id>', methods=['GET'])
def show_dish(id):
    for dish in menu:
        if dish['id'] == id:
            return jsonify(dish)
        
    return f"Нет блюда с id:{id}", 404


@app.route('/menu/category/<name>', methods=['GET'])
def show_category(name):
    selected_dish_list = []
    for dish in menu:
        if dish['category'] == name:
            selected_dish_list.append(dish)

    if not selected_dish_list:
        return f'Нет категории {name}', 404
    else:
        return jsonify(selected_dish_list)


  

if __name__ == "__main__":
    app.run(debug=True)