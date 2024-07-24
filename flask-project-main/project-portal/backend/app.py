from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///requests.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class ProjectRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(100), nullable=False)
    entry_number = db.Column(db.String(20), nullable=False)
    request_type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    submission_date = db.Column(db.DateTime, default=datetime.utcnow)
    additional_remarks = db.Column(db.Text)
    urgency = db.Column(db.String(20), nullable=False)
    estimated_duration = db.Column(db.Integer, nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/requests', methods=['GET'])
def handle_requests():
    requests = ProjectRequest.query.all()
    requests_list = [
        {
            'student_name': r.student_name,
            'entry_number': r.entry_number,
            'request_type': r.request_type,
            'description': r.description,
            'submission_date': r.submission_date.strftime('%Y-%m-%d %H:%M:%S'),
            'additional_remarks': r.additional_remarks or 'None',
            'urgency': r.urgency,
            'estimated_duration': r.estimated_duration
        }
        for r in requests
    ]
    return jsonify(requests_list)

@app.route('/requests', methods=['POST'])
def add_request():
    data = request.json
    new_request = ProjectRequest(
        student_name=data['student_name'],
        entry_number=data['entry_number'],
        request_type=data['request_type'],
        description=data['description'],
        additional_remarks=data.get('additional_remarks'),
        urgency=data['urgency'],
        estimated_duration=data['estimated_duration']
    )
    db.session.add(new_request)
    db.session.commit()
    return jsonify({'message': 'Request added successfully!'}), 201

if __name__ == '__main__':
    app.run(debug=True)
