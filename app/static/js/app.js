document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("laporForm");
    const submitBtn = document.getElementById("submitBtn");
    const btnText = document.getElementById("btnText");
    const loadingSpinner = document.getElementById("loadingSpinner");
    const statusMessage = document.getElementById("statusMessage");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        submitBtn.disabled = true;
        submitBtn.classList.add("opacity-75", "cursor-not-allowed");
        btnText.textContent = "Sedang diproses AI...";
        loadingSpinner.classList.remove("hidden");
        
        statusMessage.classList.add("hidden");
        statusMessage.classList.remove("bg-green-100", "text-green-800", "bg-red-100", "text-red-800");

        const formData = new FormData(form);

        try {
            const response = await fetch("/submit-laporan", {
                method: "POST",
                body: formData
            });

            const result = await response.json();

            if (response.ok) {
                statusMessage.textContent = result.message || "Laporan berhasil diterima dan sedang dianalisis!";
                statusMessage.classList.remove("hidden");
                statusMessage.classList.add("bg-green-100", "text-green-800");
                form.reset();
            } else {
                statusMessage.textContent = result.detail || "Terjadi kesalahan pada sistem.";
                statusMessage.classList.remove("hidden");
                statusMessage.classList.add("bg-red-100", "text-red-800");
            }
        } catch (error) {
            statusMessage.textContent = "Gagal terhubung ke server.";
            statusMessage.classList.remove("hidden");
            statusMessage.classList.add("bg-red-100", "text-red-800");
        } finally {
            submitBtn.disabled = false;
            submitBtn.classList.remove("opacity-75", "cursor-not-allowed");
            btnText.textContent = "Kirim Laporan";
            loadingSpinner.classList.add("hidden");
        }
    });

    const trackBtn = document.getElementById("trackBtn");
    const ticketInput = document.getElementById("ticketCodeInput");
    const trackingResult = document.getElementById("trackingResult");

    trackBtn.addEventListener("click", async () => {
        const code = ticketInput.value.trim();
        if (!code) return;

        trackBtn.textContent = "Mencari...";
        try {
            const response = await fetch(`/track-ticket/${code}`);
            const data = await response.json();

            if (response.ok) {
                trackingResult.classList.remove("hidden");
                trackingResult.innerHTML = `
                    <div class="space-y-1">
                        <p><strong>Status AI:</strong> <span class="px-2 py-0.5 rounded text-xs bg-blue-100 text-blue-800">${data.status_ai}</span></p>
                        <p><strong>Dinas Tujuan:</strong> ${data.dinas_tujuan}</p>
                        <p><strong>Urgensi:</strong> ${data.urgensi}</p>
                        <p><strong>Progress Penanganan:</strong> <span class="text-indigo-600 font-semibold">${data.status_proses}</span></p>
                    </div>
                `;
            } else {
                alert(data.detail || "Tiket tidak ditemukan.");
            }
        } catch (err) {
            alert("Gagal terhubung ke server.");
        } finally {
            trackBtn.textContent = "Cari";
        }
    });
});