from flask import Flask, request, jsonify, send_from_directory, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
import requests
import geopandas as gpd
from shapely.geometry import Point

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

territories = gpd.read_file('territories.geojson')

@app.route('/')
def home():
    return send_from_directory(os.getcwd(), 'templates/index.html')

@app.route('/geocode', methods=['POST'])
def geocode_address():
    data = request.json
    address = data['address']
    city = data['city']
    postal_code = data['postalCode']
    
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
            
            territory = determine_territory(latitude, longitude)
            if territory:
                return jsonify({'redirectUrl': url_for(territory)})
            return jsonify({'error': 'Territory not found'}), 404
    return jsonify({'error': 'Geocoding failed'}), 500

def determine_territory(lat, lng):
    point = Point(lng, lat)
    for _, row in territories.iterrows():
        if row['geometry'].contains(point):
            territory_name = row['name'].replace(" ", "").lower()  # Normalize the territory name
            if territory_name == 'south18':
                return 'zone18'
            return territory_name
    return None

@app.route('/zone1')
def zone1():
    return send_from_directory(os.getcwd(), 'templates/zone1.html')

@app.route('/book/zone1', methods=['POST'])
def book_appointment_zone1():
    data = request.json
    date = data['date']
    details = data['details']
    if Appointment.query.filter_by(date=date, territory='zone1').count() >= 5:
        return jsonify({'error': 'Slot full'}), 400
    new_appointment = Appointment(date=date, time='all-day', details=details, territory='zone1')
    db.session.add(new_appointment)
    db.session.commit()
    return jsonify({'message': 'Appointment booked'})

@app.route('/appointments/zone1', methods=['GET'])
def get_appointments_zone1():
    appointments = Appointment.query.filter_by(territory='zone1').all()
    return jsonify([{'date': a.date, 'time': a.time, 'details': a.details} for a in appointments])

@app.route('/zone2')
def zone2():
    return send_from_directory(os.getcwd(), 'templates/zone2.html')

@app.route('/book/zone2', methods=['POST'])
def book_appointment_zone2():
    data = request.json
    date = data['date']
    details = data['details']
    if Appointment.query.filter_by(date=date, territory='zone2').count() >= 5:
        return jsonify({'error': 'Slot full'}), 400
    new_appointment = Appointment(date=date, time='all-day', details=details, territory='zone2')
    db.session.add(new_appointment)
    db.session.commit()
    return jsonify({'message': 'Appointment booked'})

@app.route('/appointments/zone2', methods=['GET'])
def get_appointments_zone2():
    appointments = Appointment.query.filter_by(territory='zone2').all()
    return jsonify([{'date': a.date, 'time': a.time, 'details': a.details} for a in appointments])

@app.route('/zone3')
def zone3():
    return send_from_directory(os.getcwd(), 'templates/zone3.html')

@app.route('/book/zone3', methods=['POST'])
def book_appointment_zone3():
    data = request.json
    date = data['date']
    details = data['details']
    if Appointment.query.filter_by(date=date, territory='zone3').count() >= 5:
        return jsonify({'error': 'Slot full'}), 400
    new_appointment = Appointment(date=date, time='all-day', details=details, territory='zone3')
    db.session.add(new_appointment)
    db.session.commit()
    return jsonify({'message': 'Appointment booked'})

@app.route('/appointments/zone3', methods=['GET'])
def get_appointments_zone3():
    appointments = Appointment.query.filter_by(territory='zone3').all()
    return jsonify([{'date': a.date, 'time': a.time, 'details': a.details} for a in appointments])

@app.route('/zone4')
def zone4():
    return send_from_directory(os.getcwd(), 'templates/zone4.html')

@app.route('/book/zone4', methods=['POST'])
def book_appointment_zone4():
    data = request.json
    date = data['date']
    details = data['details']
    if Appointment.query.filter_by(date=date, territory='zone4').count() >= 5:
        return jsonify({'error': 'Slot full'}), 400
    new_appointment = Appointment(date=date, time='all-day', details=details, territory='zone4')
    db.session.add(new_appointment)
    db.session.commit()
    return jsonify({'message': 'Appointment booked'})

@app.route('/appointments/zone4', methods=['GET'])
def get_appointments_zone4():
    appointments = Appointment.query.filter_by(territory='zone4').all()
    return jsonify([{'date': a.date, 'time': a.time, 'details': a.details} for a in appointments])

@app.route('/zone5')
def zone5():
    return send_from_directory(os.getcwd(), 'templates/zone5.html')

@app.route('/book/zone5', methods=['POST'])
def book_appointment_zone5():
    data = request.json
    date = data['date']
    details = data['details']
    if Appointment.query.filter_by(date=date, territory='zone5').count() >= 5:
        return jsonify({'error': 'Slot full'}), 400
    new_appointment = Appointment(date=date, time='all-day', details=details, territory='zone5')
    db.session.add(new_appointment)
    db.session.commit()
    return jsonify({'message': 'Appointment booked'})

@app.route('/appointments/zone5', methods=['GET'])
def get_appointments_zone5():
    appointments = Appointment.query.filter_by(territory='zone5').all()
    return jsonify([{'date': a.date, 'time': a.time, 'details': a.details} for a in appointments])

@app.route('/zone6')
def zone6():
    return send_from_directory(os.getcwd(), 'templates/zone6.html')

@app.route('/book/zone6', methods=['POST'])
def book_appointment_zone6():
    data = request.json
    date = data['date']
    details = data['details']
    if Appointment.query.filter_by(date=date, territory='zone6').count() >= 5:
        return jsonify({'error': 'Slot full'}), 400
    new_appointment = Appointment(date=date, time='all-day', details=details, territory='zone6')
    db.session.add(new_appointment)
    db.session.commit()
    return jsonify({'message': 'Appointment booked'})

@app.route('/appointments/zone6', methods=['GET'])
def get_appointments_zone6():
    appointments = Appointment.query.filter_by(territory='zone6').all()
    return jsonify([{'date': a.date, 'time': a.time, 'details': a.details} for a in appointments])

@app.route('/zone7')
def zone7():
    return send_from_directory(os.getcwd(), 'templates/zone7.html')

@app.route('/book/zone7', methods=['POST'])
def book_appointment_zone7():
    data = request.json
    date = data['date']
    details = data['details']
    if Appointment.query.filter_by(date=date, territory='zone7').count() >= 5:
        return jsonify({'error': 'Slot full'}), 400
    new_appointment = Appointment(date=date, time='all-day', details=details, territory='zone7')
    db.session.add(new_appointment)
    db.session.commit()
    return jsonify({'message': 'Appointment booked'})

@app.route('/appointments/zone7', methods=['GET'])
def get_appointments_zone7():
    appointments = Appointment.query.filter_by(territory='zone7').all()
    return jsonify([{'date': a.date, 'time': a.time, 'details': a.details} for a in appointments])

@app.route('/zone8')
def zone8():
    return send_from_directory(os.getcwd(), 'templates/zone8.html')

@app.route('/book/zone8', methods=['POST'])
def book_appointment_zone8():
    data = request.json
    date = data['date']
    details = data['details']
    if Appointment.query.filter_by(date=date, territory='zone8').count() >= 5:
        return jsonify({'error': 'Slot full'}), 400
    new_appointment = Appointment(date=date, time='all-day', details=details, territory='zone8')
    db.session.add(new_appointment)
    db.session.commit()
    return jsonify({'message': 'Appointment booked'})

@app.route('/appointments/zone8', methods=['GET'])
def get_appointments_zone8():
    appointments = Appointment.query.filter_by(territory='zone8').all()
    return jsonify([{'date': a.date, 'time': a.time, 'details': a.details} for a in appointments])

@app.route('/zone9')
def zone9():
    return send_from_directory(os.getcwd(), 'templates/zone9.html')

@app.route('/book/zone9', methods=['POST'])
def book_appointment_zone9():
    data = request.json
    date = data['date']
    details = data['details']
    if Appointment.query.filter_by(date=date, territory='zone9').count() >= 5:
        return jsonify({'error': 'Slot full'}), 400
    new_appointment = Appointment(date=date, time='all-day', details=details, territory='zone9')
    db.session.add(new_appointment)
    db.session.commit()
    return jsonify({'message': 'Appointment booked'})

@app.route('/appointments/zone9', methods=['GET'])
def get_appointments_zone9():
    appointments = Appointment.query.filter_by(territory='zone9').all()
    return jsonify([{'date': a.date, 'time': a.time, 'details': a.details} for a in appointments])

@app.route('/zone10')
def zone10():
    return send_from_directory(os.getcwd(), 'templates/zone10.html')

@app.route('/book/zone10', methods=['POST'])
def book_appointment_zone10():
    data = request.json
    date = data['date']
    details = data['details']
    if Appointment.query.filter_by(date=date, territory='zone10').count() >= 5:
        return jsonify({'error': 'Slot full'}), 400
    new_appointment = Appointment(date=date, time='all-day', details=details, territory='zone10')
    db.session.add(new_appointment)
    db.session.commit()
    return jsonify({'message': 'Appointment booked'})

@app.route('/appointments/zone10', methods=['GET'])
def get_appointments_zone10():
    appointments = Appointment.query.filter_by(territory='zone10').all()
    return jsonify([{'date': a.date, 'time': a.time, 'details': a.details} for a in appointments])

@app.route('/zone11')
def zone11():
    return send_from_directory(os.getcwd(), 'templates/zone11.html')

@app.route('/book/zone11', methods=['POST'])
def book_appointment_zone11():
    data = request.json
    date = data['date']
    details = data['details']
    if Appointment.query.filter_by(date=date, territory='zone11').count() >= 5:
        return jsonify({'error': 'Slot full'}), 400
    new_appointment = Appointment(date=date, time='all-day', details=details, territory='zone11')
    db.session.add(new_appointment)
    db.session.commit()
    return jsonify({'message': 'Appointment booked'})

@app.route('/appointments/zone11', methods=['GET'])
def get_appointments_zone11():
    appointments = Appointment.query.filter_by(territory='zone11').all()
    return jsonify([{'date': a.date, 'time': a.time, 'details': a.details} for a in appointments])

@app.route('/zone12')
def zone12():
    return send_from_directory(os.getcwd(), 'templates/zone12.html')

@app.route('/book/zone12', methods=['POST'])
def book_appointment_zone12():
    data = request.json
    date = data['date']
    details = data['details']
    if Appointment.query.filter_by(date=date, territory='zone12').count() >= 5:
        return jsonify({'error': 'Slot full'}), 400
    new_appointment = Appointment(date=date, time='all-day', details=details, territory='zone12')
    db.session.add(new_appointment)
    db.session.commit()
    return jsonify({'message': 'Appointment booked'})

@app.route('/appointments/zone12', methods=['GET'])
def get_appointments_zone12():
    appointments = Appointment.query.filter_by(territory='zone12').all()
    return jsonify([{'date': a.date, 'time': a.time, 'details': a.details} for a in appointments])

@app.route('/zone14')
def zone14():
    return send_from_directory(os.getcwd(), 'templates/zone14.html')

@app.route('/book/zone14', methods=['POST'])
def book_appointment_zone14():
    data = request.json
    date = data['date']
    details = data['details']
    if Appointment.query.filter_by(date=date, territory='zone14').count() >= 5:
        return jsonify({'error': 'Slot full'}), 400
    new_appointment = Appointment(date=date, time='all-day', details=details, territory='zone14')
    db.session.add(new_appointment)
    db.session.commit()
    return jsonify({'message': 'Appointment booked'})

@app.route('/appointments/zone14', methods=['GET'])
def get_appointments_zone14():
    appointments = Appointment.query.filter_by(territory='zone14').all()
    return jsonify([{'date': a.date, 'time': a.time, 'details': a.details} for a in appointments])

@app.route('/zone15')
def zone15():
    return send_from_directory(os.getcwd(), 'templates/zone15.html')

@app.route('/book/zone15', methods=['POST'])
def book_appointment_zone15():
    data = request.json
    date = data['date']
    details = data['details']
    if Appointment.query.filter_by(date=date, territory='zone15').count() >= 5:
        return jsonify({'error': 'Slot full'}), 400
    new_appointment = Appointment(date=date, time='all-day', details=details, territory='zone15')
    db.session.add(new_appointment)
    db.session.commit()
    return jsonify({'message': 'Appointment booked'})

@app.route('/appointments/zone15', methods=['GET'])
def get_appointments_zone15():
    appointments = Appointment.query.filter_by(territory='zone15').all()
    return jsonify([{'date': a.date, 'time': a.time, 'details': a.details} for a in appointments])

@app.route('/zone16')
def zone16():
    return send_from_directory(os.getcwd(), 'templates/zone16.html')

@app.route('/book/zone16', methods=['POST'])
def book_appointment_zone16():
    data = request.json
    date = data['date']
    details = data['details']
    if Appointment.query.filter_by(date=date, territory='zone16').count() >= 5:
        return jsonify({'error': 'Slot full'}), 400
    new_appointment = Appointment(date=date, time='all-day', details=details, territory='zone16')
    db.session.add(new_appointment)
    db.session.commit()
    return jsonify({'message': 'Appointment booked'})

@app.route('/appointments/zone16', methods=['GET'])
def get_appointments_zone16():
    appointments = Appointment.query.filter_by(territory='zone16').all()
    return jsonify([{'date': a.date, 'time': a.time, 'details': a.details} for a in appointments])

@app.route('/zone18')
def zone18():
    return send_from_directory(os.getcwd(), 'templates/zone18.html')

@app.route('/book/zone18', methods=['POST'])
def book_appointment_zone18():
    data = request.json
    date = data['date']
    details = data['details']
    if Appointment.query.filter_by(date=date, territory='zone18').count() >= 5:
        return jsonify({'error': 'Slot full'}), 400
    new_appointment = Appointment(date=date, time='all-day', details=details, territory='zone18')
    db.session.add(new_appointment)
    db.session.commit()
    return jsonify({'message': 'Appointment booked'})

@app.route('/appointments/zone18', methods=['GET'])
def get_appointments_zone18():
    appointments = Appointment.query.filter_by(territory='zone18').all()
    return jsonify([{'date': a.date, 'time': a.time, 'details': a.details} for a in appointments])

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5005)

