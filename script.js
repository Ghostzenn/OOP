let notified = new Set();

document.addEventListener("click", () => {
    if ("Notification" in window && Notification.permission !== "granted") {
        Notification.requestPermission();
    }
}, { once: true });

function notify(title, message) {

    if ("Notification" in window && Notification.permission === "granted") {
        new Notification(title, {
            body: message,
            icon: "https://cdn-icons-png.flaticon.com/512/1827/1827392.png"
        });
    }

    else {
        alert(title + "\n" + message);
    }
}

function parseDate(value) {
    return new Date(value.replace(" ", "T"));
}

function checkTasks() {

    const rows = document.querySelectorAll("tr[data-id]");
    const now = new Date();

    rows.forEach(row => {

        const id = row.dataset.id;
        const title = row.dataset.title;
        const deadlineStr = row.dataset.deadline;

        if (!deadlineStr) return;

        const deadline = parseDate(deadlineStr);
        if (isNaN(deadline.getTime())) return;

        const diff = deadline - now;

        if (diff <= 300000 && diff > 60000 && !notified.has("5min-" + id)) {
            notified.add("5min-" + id);
            notify("5 Minutes Left", title);
        }

        else if (diff <= 60000 && diff > 0 && !notified.has("1min-" + id)) {
            notified.add("1min-" + id);
            notify("1 Minute Left", title);
        }

        else if (diff <= 0 && !notified.has("overdue-" + id)) {
            notified.add("overdue-" + id);
            notify("Task is Overdue!", title);
        }

    });
}

setInterval(checkTasks, 1000);

function editTask(btn) {

    let deadline = btn.dataset.deadline;

    if (deadline) {
        deadline = deadline.replace(" ", "T").slice(0, 16);
    }

    document.getElementById("task_id").value = btn.dataset.id;
    document.getElementById("title").value = btn.dataset.title;
    document.getElementById("category").value = btn.dataset.category;
    document.getElementById("deadline").value = deadline;

    window.scrollTo({ top: 0, behavior: "smooth" });
}
