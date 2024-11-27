# app.py

from flask import Flask, request, jsonify, abort
from models import Ad, ads_db

app = Flask(__name__)

# Создание нового объявления
@app.route('/ads', methods=['POST'])
def create_ad():
    data = request.get_json()
    
    # Проверка наличия всех обязательных полей
    if not data or not data.get('title') or not data.get('description') or not data.get('owner'):
        abort(400, description="Missing required fields")
    
    ad = Ad(
        title=data['title'],
        description=data['description'],
        owner=data['owner']
    )
    
    # Сохраняем объявление в базу данных (в памяти)
    ads_db[ad.id] = ad
    
    return jsonify(ad.to_dict()), 201

# Получение всех объявлений
@app.route('/ads', methods=['GET'])
def get_ads():
    return jsonify([ad.to_dict() for ad in ads_db.values()])

# Получение конкретного объявления по ID
@app.route('/ads/<ad_id>', methods=['GET'])
def get_ad(ad_id):
    ad = ads_db.get(ad_id)
    if ad is None:
        abort(404, description="Ad not found")
    return jsonify(ad.to_dict())

# Удаление объявления
@app.route('/ads/<ad_id>', methods=['DELETE'])
def delete_ad(ad_id):
    ad = ads_db.pop(ad_id, None)
    if ad is None:
        abort(404, description="Ad not found")
    return jsonify({'message': 'Ad deleted successfully'}), 200

# Обработчик ошибок
@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': str(error)}), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': str(error)}), 404

if __name__ == '__main__':
    app.run(debug=True)
