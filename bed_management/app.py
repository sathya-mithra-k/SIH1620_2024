from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Sample data structure for beds
beds = [
    {"id": 1, "block": "A", "floor": 1, "status": "available", "patient": None},
    {"id": 2, "block": "A", "floor": 1, "status": "occupied", "patient": "John Doe"},
    {"id": 3, "block": "B", "floor": 2, "status": "available", "patient": None},
    {"id": 4, "block": "B", "floor": 2, "status": "under_maintenance", "patient": None},
]

# Home page to view beds
@app.route('/')
def home():
    return render_template('index.html', beds=beds)

# API to allocate a bed to a patient
@app.route('/allocate_bed', methods=['POST'])
def allocate_bed():
    patient_name = request.json['patient_name']
    
    # Find the first available bed
    for bed in beds:
        if bed['status'] == 'available':
            bed['status'] = 'occupied'
            bed['patient'] = patient_name
            return jsonify({"message": "Bed allocated", "bed_id": bed['id']})
    
    return jsonify({"message": "No available beds"}), 400

# API to view bed details
@app.route('/bed/<int:bed_id>')
def view_bed(bed_id):
    bed = next((b for b in beds if b['id'] == bed_id), None)
    if bed:
        return jsonify(bed)
    return jsonify({"message": "Bed not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
