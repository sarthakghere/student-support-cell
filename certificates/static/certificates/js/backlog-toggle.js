document.addEventListener("DOMContentLoaded", function () {
    const backlogYes = document.querySelector("#backlog-yes");
    const backlogSection = document.querySelector("#backlog-section");

    if (backlogYes && backlogSection) {
        backlogYes.addEventListener("change", function () {
            backlogSection.style.display = "block";
        });
    }
});
