const API = "/api/v1/";

function login() {
    const username = document.getElementById("username")?.value;
    const password = document.getElementById("password")?.value;

    fetch(API + "auth/login/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username: username,
            password: password
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.access) {
            localStorage.setItem("access", data.access);
            localStorage.setItem("refresh", data.refresh);
            window.location.href = "/dashboard/";
        } else {
            document.getElementById("msg").innerText = data.error || "Login failed";
        }
    })
    .catch(() => {
        document.getElementById("msg").innerText = "Server error";
    });
}

function authHeader() {
    return {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + localStorage.getItem("access")
    };
}

function loadEmployees() {
    fetch(API + "employees/", {
        method: "GET",
        headers: authHeader()
    })
    .then(res => res.json())
    .then(data => {
        const table = document.getElementById("employeeTable");
        if (!table) return;
        table.innerHTML = "";

        data.forEach(emp => {
            table.innerHTML += `
                <tr>
                    <td>${emp.id}</td>
                    <td>${emp.employee_code || ""}</td>
                    <td>${emp.first_name || ""}</td>
                    <td>${emp.email || ""}</td>
                </tr>
            `;
        });
    });
}

function checkIn() {
    const emp = document.getElementById("employee_id")?.value;

    fetch(API + "attendance/check-in/", {
        method: "POST",
        headers: authHeader(),
        body: JSON.stringify({ employee: emp })
    })
    .then(res => res.json())
    .then(data => {
        const msg = document.getElementById("attendanceMsg");
        if (msg) msg.innerText = data.error || "Check-in successful";
    });
}

function checkOut() {
    const emp = document.getElementById("employee_id")?.value;

    fetch(API + "attendance/check-out/", {
        method: "POST",
        headers: authHeader(),
        body: JSON.stringify({ employee: emp })
    })
    .then(res => res.json())
    .then(data => {
        const msg = document.getElementById("attendanceMsg");
        if (msg) msg.innerText = data.error || "Check-out successful";
    });
}

function applyLeave() {
    fetch(API + "leaves/apply/", {
        method: "POST",
        headers: authHeader(),
        body: JSON.stringify({
            employee: document.getElementById("emp_id")?.value,
            leave_type: document.getElementById("leave_type")?.value,
            start_date: document.getElementById("start")?.value,
            end_date: document.getElementById("end")?.value,
            reason: document.getElementById("reason")?.value
        })
    })
    .then(res => res.json())
    .then(data => {
        const msg = document.getElementById("leaveMsg");
        if (msg) msg.innerText = data.error || "Leave applied successfully";
    });
}

function loadLeaveHistory() {
    fetch(API + "leaves/history/", {
        method: "GET",
        headers: authHeader()
    })
    .then(res => res.json())
    .then(data => {
        const table = document.getElementById("leaveHistoryTable");
        if (!table) return;
        table.innerHTML = "";

        data.forEach(item => {
            table.innerHTML += `
                <tr>
                    <td>${item.id}</td>
                    <td>${item.employee}</td>
                    <td>${item.leave_type}</td>
                    <td>${item.start_date}</td>
                    <td>${item.end_date}</td>
                    <td>${item.status}</td>
                </tr>
            `;
        });
    });
}