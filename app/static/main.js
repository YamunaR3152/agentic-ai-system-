let currentTaskId = null;
let polling = false;

async function runTask() {
    const query = document.getElementById("query").value.trim();
    if (!query) return alert("Enter a query");

    document.getElementById("statusBox").innerText = "Submitting task...";
    document.getElementById("final").value = "";

    const res = await fetch("/submit-task", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query })
    });

    const data = await res.json();
    currentTaskId = data.task_id;

    if (!polling) {
        polling = true;
        pollStatus();
    }
}

async function pollStatus() {
    if (!currentTaskId) {
        polling = false;
        return;
    }

    try {
        const res = await fetch(`/task-status/${currentTaskId}`);
        const data = await res.json();

        if (data.type === "status") {
            document.getElementById("statusBox").innerText = data.message;
        }

        if (data.type === "final") {
            document.getElementById("statusBox").innerText = "✅ Task complete";
            document.getElementById("final").value = data.message;
            polling = false;
            return;
        }

        setTimeout(pollStatus, 1000);

    } catch (err) {
        document.getElementById("statusBox").innerText = "⚠️ Connection issue. Retrying...";
        setTimeout(pollStatus, 2000);
    }
}
