function generatePassword() {
    fetch('/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            username: document.getElementById('username').value,
            type: document.getElementById('type').value,
            length: document.getElementById('length').value
        })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById('result').value = data.password;
        loadPasswords();
    });
}

function loadPasswords() {
    fetch('/passwords')
    .then(res => res.json())
    .then(data => {
        const list = document.getElementById('savedPasswords');
        list.innerHTML = '';
        data.forEach(p => {
            const li = document.createElement('li');
            li.textContent = p.username + " → " + p.password;
            list.appendChild(li);
        });
    });
}

window.onload = loadPasswords;