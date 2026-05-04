function redirectToPage(element) {
    const targetUrl = element.getAttribute('data-url');
    if (targetUrl){
        window.location.href = targetUrl;
    }
  }

function pillClass(status) {
    return { Active: 'pill-active', Locked: 'pill-locked', Inactive: 'pill-inactive' }[status] || '';
}

function renderTable(data) {
    const body = document.getElementById('dgBody');
    body.innerHTML = data.map(u => `
    <tr>
        <td><input type="checkbox"/></td>
        <td>
        <div class="u-cell">
            <div class="u-avatar" style="background:${u.color};color:${u.colorText}">${u.initials}</div>
            <div>
            <div class="u-name">${u.name}</div>
            <div class="u-email">${u.email}</div>
            </div>
        </div>
        </td>
        <td><span class="pill ${u.role === 'Admin' ? 'pill-admin' : 'pill-user'}">${u.role}</span></td>
        <td><span class="pill ${pillClass(u.status)}">${u.status}</span></td>
        <td style="color:var(--text2)">${u.last}</td>
        <td style="color:${u.tfa ? 'var(--success)' : 'var(--danger)'}">${u.tfa ? '✓ On' : '✗ Off'}</td>
        <td>
        <span class="act-link">Edit</span>
        <span class="act-link danger">${u.status === 'Locked' ? 'Unlock' : 'Lock'}</span>
        </td>
    </tr>
    `).join('');
    document.getElementById('dgCount').textContent = `Showing ${data.length} of ${USERS.length} users`;
}

function filterTable() {
    const q      = document.getElementById('dgSearch').value.toLowerCase();
    const role   = document.getElementById('dgRole').value;
    const status = document.getElementById('dgStatus').value;
    const filtered = USERS.filter(u =>
    (!q      || u.name.toLowerCase().includes(q) || u.email.toLowerCase().includes(q)) &&
    (!role   || u.role   === role) &&
    (!status || u.status === status)
    );
    renderTable(filtered);
}

function toggleAll(master) {
    document.querySelectorAll('#dgBody input[type=checkbox]').forEach(cb => cb.checked = master.checked);
}
/* ── Sample user data (replace with API call to GET /api/users) ── */
const USERS = [
    { name: 'Juan Dela Cruz', email: 'juan@example.com',  role: 'Admin', status: 'Active',   last: 'Today, 2:14 PM',     tfa: true,  initials: 'JD', color: 'var(--accent-bg)', colorText: 'var(--accent)' },
    { name: 'Maria Reyes',    email: 'maria@example.com', role: 'User',  status: 'Active',   last: 'Apr 16, 9:00 AM',    tfa: true,  initials: 'MR', color: 'var(--success-bg)', colorText: 'var(--success)' },
    { name: 'Carlo Santos',   email: 'carlo@example.com', role: 'User',  status: 'Locked',   last: 'Apr 15, 6:33 PM',    tfa: false, initials: 'CS', color: 'var(--danger-bg)',  colorText: 'var(--danger)' },
    { name: 'Ana Lim',        email: 'ana@example.com',   role: 'User',  status: 'Inactive', last: 'Apr 10, 11:20 AM',   tfa: false, initials: 'AL', color: 'var(--warning-bg)', colorText: 'var(--warning)' },
    { name: 'Ben Torres',     email: 'ben@example.com',   role: 'Admin', status: 'Active',   last: 'Today, 8:01 AM',     tfa: true,  initials: 'BT', color: 'var(--accent-bg)', colorText: 'var(--accent)' },
];

// FOR OTP; DONT MODIFY
document.addEventListener("DOMContentLoaded", () => {
    const userInputs = document.querySelectorAll(".otp-input");
    const verifyButton = document.getElementById("otpBtn");
    const alertBox = document.getElementById("otpAlert");

    userInputs.forEach((input, index) => {
        input.addEventListener("input", () => {
            if (input.value &&  index < userInputs.length - 1 ){
                userInputs[index + 1].focus();
            }
            const otpCode = Array.from(userInputs).map(input => input.value).join("");
            if (otpCode.length === userInputs.length) {
                verifyButton.disabled = false;
            }
        });
    });
    verifyButton.addEventListener("click", () => {
        const otpCode = Array.from(userInputs).map(input => input.value).join("");
        fetch("OTPValidate/",{
            method: "POST",
            headers: {"Content-Type" : "application/x-www-form-urlencoded"},
            body: `OTPCode=${otpCode}`
        })
        .then(result => result.json())
        .then(data => {
            if (data.valid){
                alertBox.style.display = "block";
                alertBox.className = "alert alert-success";
                alertBox.textContent = "OTP verified successfully!";
            } else {
                alertBox.style.display = "block";
                alertBox.className = "alert alert-danger";
                alertBox.textContent = data.message;
            }
        });
    });
});