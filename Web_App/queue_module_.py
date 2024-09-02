import heapq   # initialize  heap queue algorithm
from collections import deque  # provides a double-ended queue

#initializing the required data structure
docs = []                      # stores the names of doctors in a list
doc_patients = {}              #stores the data of assigned patients to their doctor 
normal_queue = deque()         # INITIALIZE THE NORMAL_QUEUE
emergency_queue = []           # INITIALIZE THE _EMERGENCY_QUEUE
patient_token_counter = 0      #  GENERATES A NEW TOKEN TO THE NEXT PATIENT (INCREMENT)
patient_tokens = {}            # STORES THE TOKEN VALUE AS THE PATIENT NAME (INCREMENT)


#  CREATES AN LIST WHERE THE NUM OF DOCTOR IS THE NUMBER OF ELEMENTS 
def num_doc(tot_doctors):                            
    global docs, doc_patients
    docs = [f"doctor_{i+1}" for i in range(tot_doctors)]
    doc_patients = {doc: [] for doc in docs}
    # print(f"Initialized doctors: {docs}")


# ADDS THE TOKEN TO TOKEN COUNTER WHEN PATIENT_NAME IS ENTERED 
def ticket_generation(patient_name):
    global patient_token_counter, patient_tokens
    patient_token_counter += 1
    token = patient_token_counter
    patient_tokens[token] = patient_name
    return token
#add error case


def assign_patient():

    # this line creates a list of available doctors by reading the doc_patient dictionary
    available_doctors = [doc for doc in docs if len(doc_patients[doc]) == 0]
    
    # Process emergency cases first
    while emergency_queue and available_doctors:
        _, token = heapq.heappop(emergency_queue)
        patient_name = patient_tokens[token]
        doctor = available_doctors.pop(0)
        doc_patients[doctor].append(patient_name)
        print(f"EMERGENCY: Patient '{patient_name}' (Token {token}) is assigned to {doctor}.")
        display()  # Display current assignments after adding a patient

    # Process normal cases next
    while normal_queue and available_doctors:
        token = normal_queue.popleft()
        patient_name = patient_tokens[token]
        doctor = available_doctors.pop(0)
        doc_patients[doctor].append(patient_name)
        print(f"Patient '{patient_name}' (Token {token}) is assigned to {doctor}.")
        display()  # Display current assignments after adding a patient


# removes the patient form the queue after the visit is over 
def complete_visit(doctor, token):
    if token in patient_tokens:
        patient_name = patient_tokens[token]
        if patient_name in doc_patients[doctor]:
            doc_patients[doctor].remove(patient_name)
            del patient_tokens[token]
            # Reassign patients after completion
            assign_patient()
            return f"Visit completed for Patient '{patient_name}' (Token {token}) with {doctor}."
        else:
            return f"Patient '{patient_name}' (Token {token}) not found with {doctor}."
    else:
        return f"Token {token} not found."

# a function for displaying the details of the patient assign list
def display():

    doc_patient_assignments = {doctor: patients for doctor, patients in doc_patients.items()}
    
    # Display waiting patients in the queue
    waiting_normal = [patient_tokens[token] for token in normal_queue]
    waiting_emergency = [patient_tokens[token] for _, token in emergency_queue]
    
    return {
        "Doctor-Patient Assignments": doc_patient_assignments,
        "Waiting in Regular Queue": waiting_normal,
        "Waiting in Emergency Queue": waiting_emergency
    }



# def add_patients_dynamically():
#     while True:
#         patient_name = input("Enter the patient's name (or type 'stop' to finish): ")
#         if patient_name.lower() == 'stop':
#             break

#         is_emergency = input("Is this an emergency patient? (yes/no): ").lower()
#         if is_emergency == 'yes':
#             add_patient(patient_name, is_emergency=True)
#         else:
#             add_patient(patient_name)

# # Start the dynamic patient addition
# add_patients_dynamically()


# the main method the should be modified 

# if __name__ == "__main__":
#     tot_doctors = int(input("Enter the number of doctors: "))
#     num_doc(tot_doctors)

#     # Adding patients
#     add_patient("Patient_1")
#     add_patient("Patient_2")
#     add_patient("Patient_3", is_emergency=True)  # Emergency patient
#     add_patient("Patient_4",) 
#     add_patient("Patient_5", is_emergency=True)  # Emergency patient

#     # Completing visits
#     token_for_patient_2 = next(token for token, name in patient_tokens.items() if name == "Patient_2")
#     complete("doctor_2", token_for_patient_2)

#     token_for_patient_3 = next(token for token, name in patient_tokens.items() if name == "Patient_3")
#     complete("doctor_3", token_for_patient_3)



# FUNCTION TO ADD PATIENT TO NORMAL OR EMERGENCY QUEUE 
def add_patient(patient_name, is_emergency=False):
    token = ticket_generation(patient_name)
    if is_emergency:
        heapq.heappush(emergency_queue, (1, token))
        print(f"Patient '{patient_name}' with token {token} added to the emergency queue.")
    else:
        normal_queue.append(token)
        print(f"Patient '{patient_name}' with token {token} added to the regular queue.")
    assign_patient()
