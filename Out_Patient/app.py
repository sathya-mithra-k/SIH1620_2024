from flask import Flask, jsonify, request
import heapq
from collections import deque

app = Flask(__name__)


docs = []
doc_patients = {}
normal_queue = deque()
emergency_queue = []
patient_token_counter = 0
patient_tokens = {}

def num_doc(tot_doctors):
    global docs, doc_patients
    docs = [f"doctor_{i+1}" for i in range(tot_doctors)]
    doc_patients = {doc: [] for doc in docs}

def ticket_generation(patient_name):
    global patient_token_counter, patient_tokens
    patient_token_counter += 1
    token = patient_token_counter
    patient_tokens[token] = patient_name
    return token

def assign_patient():
    available_doctors = [doc for doc in docs if len(doc_patients[doc]) == 0]

    while emergency_queue and available_doctors:
        _, token = heapq.heappop(emergency_queue)
        patient_name = patient_tokens[token]
        doctor = available_doctors.pop(0)
        doc_patients[doctor].append(patient_name)

    while normal_queue and available_doctors:
        token = normal_queue.popleft()
        patient_name = patient_tokens[token]
        doctor = available_doctors.pop(0)
        doc_patients[doctor].append(patient_name)

def complete_visit(doctor, token):
    if token in patient_tokens:
        patient_name = patient_tokens[token]
        if patient_name in doc_patients[doctor]:
            doc_patients[doctor].remove(patient_name)
            del patient_tokens[token]
            assign_patient()
            return f"Visit completed for Patient '{patient_name}' (Token {token}) with {doctor}."
        else:
            return f"Patient '{patient_name}' (Token {token}) not found with {doctor}."
    else:
        return f"Token {token} not found."

def get_display():
    doc_patient_assignments = {doctor: patients for doctor, patients in doc_patients.items()}
    waiting_normal = [patient_tokens[token] for token in normal_queue]
    waiting_emergency = [patient_tokens[token] for _, token in emergency_queue]
    
    return {
        "Doctor-Patient Assignments": doc_patient_assignments,
        "Waiting in Regular Queue": waiting_normal,
        "Waiting in Emergency Queue": waiting_emergency
    }

@app.route('/init', methods=['POST'])
def init():
    tot_doctors = int(request.json.get('tot_doctors', 0))
    num_doc(tot_doctors)
    return jsonify({"message": f"Initialized doctors: {docs}"})

@app.route('/add_patient', methods=['POST'])
def add_patient():
    patient_name = request.json.get('patient_name')
    is_emergency = request.json.get('is_emergency', False)
    
    token = ticket_generation(patient_name)
    if is_emergency:
        heapq.heappush(emergency_queue, (1, token))
        message = f"Patient '{patient_name}' with token {token} added to the emergency queue."
    else:
        normal_queue.append(token)
        message = f"Patient '{patient_name}' with token {token} added to the regular queue."
    
    assign_patient()
    return jsonify({"message": message, "display": get_display()})

@app.route('/complete', methods=['POST'])
def complete():
    doctor = request.json.get('doctor')
    token = int(request.json.get('token'))
    
    message = complete_visit(doctor, token)
    return jsonify({"message": message, "display": get_display()})

@app.route('/display', methods=['GET'])
def display():
    return jsonify(get_display())

if __name__ == '__main__':
    app.run(debug=True)
