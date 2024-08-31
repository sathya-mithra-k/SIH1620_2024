function updateDisplay(data) {
    $('#doctor_assignments').html('');
    $.each(data["Doctor-Patient Assignments"], function(doctor, patients) {
        $('#doctor_assignments').append('<div><strong>' + doctor + ':</strong> ' + patients.join(', ') + '</div>');
    });

    $('#regular_queue').html('');
    $.each(data["Waiting in Regular Queue"], function(index, patient) {
        $('#regular_queue').append('<div>' + patient + '</div>');
    });

    $('#emergency_queue').html('');
    $.each(data["Waiting in Emergency Queue"], function(index, patient) {
        $('#emergency_queue').append('<div>' + patient + '</div>');
    });
}

function refreshDisplay() {
    $.ajax({
        url: '/display',
        type: 'GET',
        success: function(data) {
            updateDisplay(data);
        }
    });
}

$(document).ready(function() {
    $('#init_btn').click(function() {
        var tot_doctors = $('#tot_doctors').val();
        $.ajax({
            url: '/init',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ tot_doctors: tot_doctors }),
            success: function(response) {
                alert(response.message);
                refreshDisplay();
            }
        });
    });

    $('#add_patient_btn').click(function() {
        var patient_name = $('#patient_name').val();
        var is_emergency = $('#is_emergency').is(':checked');
        $.ajax({
            url: '/add_patient',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ patient_name: patient_name, is_emergency: is_emergency }),
            success: function(response) {
                alert(response.message);
                refreshDisplay();
            }
        });
    });

    $('#complete_visit_btn').click(function() {
        var doctor_name = $('#doctor_name').val();
        var patient_token = $('#patient_token').val();
        $.ajax({
            url: '/complete',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ doctor: doctor_name, token: patient_token }),
            success: function(response) {
                alert(response.message);
                refreshDisplay();
            }
        });
    });

    refreshDisplay();
});
