from flask import Flask, request, jsonify, send_from_directory, redirect, 
url_for
from flask_sqlalchemy import SQLAlchemy
import os
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///calendar.db'
db = SQLAlchemy(app)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    territory = db.Column(db.String(20), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    time = db.Column(db.String(5), nullable=False)
    details = db.Column(db.JSON, nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return send_from_directory(os.getcwd(), 'templates/index.html')

@app.route('/geocode', methods=['POST'])
def geocode_address():
    data = request.json
    address = data['address']
    city = data['city']
    postal_code = data['postalCode']
    
    # Use the OpenCage Geocoding API
    api_key = '73115f1ed34b4fffbd79f38e2af45e16'
    full_address = f"{address}, {city}, {postal_code}"
    url = f"https://api.opencagedata.com/geocode/v1/json?q={full_address}&key={api_key}"
    
    response = requests.get(url)
    if response.status_code == 200:
        results = response.json()['results']
        if results:
            coordinates = results[0]['geometry']
            latitude = coordinates['lat']
            longitude = coordinates['lng']
            
            # Determine the territory based on the coordinates
            territory = determine_territory(latitude, longitude)
            if territory:
                return jsonify({'redirectUrl': url_for(territory)})
            return jsonify({'error': 'Territory not found'}), 404
    return jsonify({'error': 'Geocoding failed'}), 500

def determine_territory(lat, lng):
    # Example implementation: map coordinates to a territory
    # Replace with actual logic
    if 46.0 <= lat <= 47.0 and -123.0 <= lng <= -122.0:
        return 'zone1'
    elif 45.0 <= lat < 46.0 and -124.0 <= lng <= -123.0:
        return 'zone2'
    # Add other territory conditions here
    return None

@app.route('/zone1')
def zone1():
    return send_from_directory(os.getcwd(), 'templates/zone1.html')

@app.route('/zone2')
def zone2():
    return send_from_directory(os.getcwd(), 'templates/zone2.html')

@app.route('/book/zone1', methods=['POST'])
def book_appointment_zone1():
    data = request.json
    date = data['date']
    if Appointment.query.filter_by(date=date, territory='zone1').count() >= 5:
        return jsonify({'error': 'Slot full'}), 400
    new_appointment = Appointment(date=date, time='all-day', details=data['details'], territory='zone1')
    db.session.add(new_appointment)
    db.session.commit()
    return jsonify({'message': 'Appointment booked'})

@app.route('/book/zone2', methods=['POST'])
def book_appointment_zone2():
    data = request.json
    date = data['date']
    if Appointment.query.filter_by(date=date, territory='zone2').count() >= 5:
        return jsonify({'error': 'Slot full'}), 400
    new_appointment = Appointment(date=date, time='all-day', details=data['details'], territory='zone2')
    db.session.add(new_appointment)
    db.session.commit()
    return jsonify({'message': 'Appointment booked'})

@app.route('/appointments/zone1', methods=['GET'])
def get_appointments_zone1():
    appointments = Appointment.query.filter_by(territory='zone1').all()
    return jsonify([{'date': a.date, 'time': a.time, 'details': a.details} for a in appointments])

@app.route('/appointments/zone2', methods=['GET'])
def get_appointments_zone2():
    appointments = Appointment.query.filter_by(territory='zone2').all()
    return jsonify([{'date': a.date, 'time': a.time, 'details': a.details} for a in appointments])

if __name__ == '__main__':
app.run(debug=True, host='127.0.0.1', port=5002)
