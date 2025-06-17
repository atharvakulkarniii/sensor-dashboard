from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta, timezone
from sqlalchemy.sql import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sensor_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

THRESHOLD = 200

class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(50))
    value = db.Column(db.Float)
    timestamp = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/receive', methods=['POST'])
def receive_data():
    data = request.get_json()
    timestamp = datetime.fromisoformat(data['timestamp']) if 'timestamp' in data else datetime.now(timezone.utc)
    entry = SensorData(location=data['location'], value=data['value'], timestamp=timestamp)
    db.session.add(entry)
    db.session.commit()
    return jsonify({'status': 'success'})

@app.route('/data')
def latest_data():
    latest = SensorData.query.order_by(SensorData.timestamp.desc()).first()
    if latest:
        return jsonify({
            "location": latest.location,
            "value": latest.value,
            "timestamp": latest.timestamp.isoformat()
        })
    return jsonify({'status': 'no data'}), 404

@app.route('/history/readings')
def reading_history():
    week_ago = datetime.now(timezone.utc) - timedelta(days=7)
    readings = SensorData.query.filter(SensorData.timestamp >= week_ago).all()
    grouped = {}
    for r in readings:
        day = r.timestamp.strftime('%a %d-%m')
        grouped.setdefault(day, []).append(r.value)
    return jsonify([{ "day": k, "average": sum(v)/len(v) } for k, v in grouped.items()])

@app.route('/history/alerts')
def alert_history():
    week_ago = datetime.now(timezone.utc) - timedelta(days=7)
    alerts = db.session.query(
        func.date(SensorData.timestamp),
        func.count()
    ).filter(
        SensorData.timestamp >= week_ago,
        SensorData.value > THRESHOLD
    ).group_by(func.date(SensorData.timestamp)).all()
    return jsonify({str(date): count for date, count in alerts})

@app.route('/history/alert-events')
def alert_events():
    alerts = SensorData.query.filter(SensorData.value > THRESHOLD).order_by(SensorData.timestamp).all()
    return jsonify([
        {
            "timestamp": alert.timestamp.isoformat(),
            "value": alert.value
        } for alert in alerts
    ])

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
