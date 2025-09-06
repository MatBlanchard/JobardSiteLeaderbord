document.addEventListener("DOMContentLoaded", () => {
  function makeDraggable() {
    const draggables = document.querySelectorAll(".draggable");
    const droppables = document.querySelectorAll(".droppable");

    draggables.forEach(el => {
      el.addEventListener("dragstart", e => {
        e.dataTransfer.setData("text/plain", e.target.dataset.id);
        e.dataTransfer.setData("text/html", e.target.outerHTML);
        setTimeout(() => e.target.style.display = "none", 0);
      });

      el.addEventListener("dragend", e => e.target.style.display = "block");
    });

    droppables.forEach(dropzone => {
      dropzone.addEventListener("dragover", e => e.preventDefault());
      dropzone.addEventListener("drop", e => {
        e.preventDefault();
        const html = e.dataTransfer.getData("text/html");
        const id = e.dataTransfer.getData("text/plain");
        if (![...dropzone.children].some(li => li.dataset.id === id)) {
          dropzone.insertAdjacentHTML("beforeend", html);
          makeDraggable(); // rebind events
        }
        document.querySelectorAll(`[data-id="${id}"]`).forEach((el, i) => {
          if (i < document.querySelectorAll(`[data-id="${id}"]`).length - 1) el.remove();
        });
        updateHiddenInputs();

        // 🔥 Appel avec campaignId
        const campaignId = document.getElementById("campaign-id").value;
        saveCampaignItems(campaignId);
      });
    });
  }

  function updateHiddenInputs() {
    document.getElementById("cars-input").value =
      [...document.querySelectorAll("#cars-selected li")].map(li => li.dataset.id).join(",");
    document.getElementById("layouts-input").value =
      [...document.querySelectorAll("#layouts-selected li")].map(li => li.dataset.id).join(",");
  }

  makeDraggable();
  updateHiddenInputs();
});

function saveCampaignItems(campaignId) {
    const selectedCars = Array.from(document.querySelectorAll("#selected-cars li"))
        .map(el => el.dataset.id);

    const selectedLayouts = Array.from(document.querySelectorAll("#selected-layouts li"))
        .map(el => el.dataset.id);

    fetch(`/campaigns/${campaignId}/update_items/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: JSON.stringify({
            cars: selectedCars,
            layouts: selectedLayouts
        })
    }).then(response => response.json())
      .then(data => {
          if (data.success) {
              alert("Campagne mise à jour !");
          }
      });
}