from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

# Путь к файлу с товарами
PRODUCTS_FILE = 'products.json'

# Создаём файл, если его нет
if not os.path.exists(PRODUCTS_FILE):
    with open(PRODUCTS_FILE, 'w', encoding='utf-8') as f:
        json.dump([
            {
                "id": 1,
                "name": "Набор клубники 9 шт",
                "price": 990,
                "category": "клубника",
                "image": "/static/images/placeholder.jpg",
                "description": "Свежая клубника в шоколаде",
                "composition": "Клубника, белый и тёмный шоколад",
                "packaging": "Подарочная коробка",
                "shelfLife": "48 часов",
                "delivery": "По городу в течение 3 часов"
            }
        ], f, ensure_ascii=False, indent=2)

# Главная страница — каталог
@app.route('/')
def index():
    return render_template('index.html')

# Страница товара
@app.route('/product')
def product():
    return render_template('product.html')

# Админка
@app.route('/admin')
def admin():
    return render_template('admin.html')

# API: получить все товары
@app.route('/api/products')
def get_products():
    with open(PRODUCTS_FILE, 'r', encoding='utf-8') as f:
        products = json.load(f)
    return jsonify(products)

# API: получить один товар
@app.route('/api/products/<int:id>')
def get_product(id):
    with open(PRODUCTS_FILE, 'r', encoding='utf-8') as f:
        products = json.load(f)
    product = next((p for p in products if p['id'] == id), None)
    return jsonify(product)

# API: добавить/изменить товар
@app.route('/api/products', methods=['POST'])
def save_product():
    data = request.json
    with open(PRODUCTS_FILE, 'r', encoding='utf-8') as f:
        products = json.load(f)

    if 'id' in data and data['id']:
        # Редактируем существующий
        for i, p in enumerate(products):
            if p['id'] == data['id']:
                products[i] = data
                break
    else:
        # Добавляем новый
        new_id = max([p['id'] for p in products]) + 1 if products else 1
        data['id'] = new_id
        products.append(data)

    with open(PRODUCTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(products, f, ensure_ascii=False, indent=2)

    return jsonify(data)

# API: удалить товар
@app.route('/api/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    with open(PRODUCTS_FILE, 'r', encoding='utf-8') as f:
        products = json.load(f)

    products = [p for p in products if p['id'] != id]

    with open(PRODUCTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(products, f, ensure_ascii=False, indent=2)

    return jsonify({"success": True})

# Запуск сервера
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)