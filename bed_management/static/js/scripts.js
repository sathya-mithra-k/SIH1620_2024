document.getElementById('allocation-form').onsubmit = async function(event) {
    event.preventDefault();
    const patientName = document.getElementById('patient_name').value;

    const response = await fetch('/allocate_bed', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ patient_name: patientName }),
    });

    const result = await response.json();
    alert(result.message);
    location.reload(); // Reload the page to show updated bed status
};
