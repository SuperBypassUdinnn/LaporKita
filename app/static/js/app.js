document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("laporForm");
    const submitBtn = document.getElementById("submitBtn");
    const btnText = document.getElementById("btnText");
    const loadingSpinner = document.getElementById("loadingSpinner");
    const statusMessage = document.getElementById("statusMessage");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        // UI Loading state
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
                // Success UI
                statusMessage.textContent = result.message || "Laporan berhasil diterima dan sedang dianalisis!";
                statusMessage.classList.remove("hidden");
                statusMessage.classList.add("bg-green-100", "text-green-800");
                
                if (result.kode_tiket) {
                    const tiketBox = document.getElementById("tiketBox");
                    const tiketCode = document.getElementById("tiketCode");
                    if (tiketBox && tiketCode) {
                        tiketCode.textContent = result.kode_tiket;
                        tiketBox.classList.remove("hidden");
                    }
                }
                form.reset();
            } else {
                // Error UI
                statusMessage.textContent = result.detail || "Terjadi kesalahan pada sistem.";
                statusMessage.classList.remove("hidden");
                statusMessage.classList.add("bg-red-100", "text-red-800");
            }
        } catch (error) {
            statusMessage.textContent = "Gagal terhubung ke server.";
            statusMessage.classList.remove("hidden");
            statusMessage.classList.add("bg-red-100", "text-red-800");
        } finally {
            // Restore UI
            submitBtn.disabled = false;
            submitBtn.classList.remove("opacity-75", "cursor-not-allowed");
            btnText.textContent = "Kirim Laporan";
            loadingSpinner.classList.add("hidden");
        }
    });
});
