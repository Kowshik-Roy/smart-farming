document.addEventListener("DOMContentLoaded", function () {
  const ctaButton = document.getElementById("ctaStartBtn");
  const formSection = document.getElementById("mainForm");
  const tabs = document.querySelectorAll(".action-tab");
  const suggestionButton = document.getElementById("suggestionButton");

  if (ctaButton && formSection) {
    ctaButton.addEventListener("click", function () {
      formSection.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  }

  tabs.forEach((tab) => {
    tab.addEventListener("click", function () {
      tabs.forEach((item) => item.classList.remove("action-tab--active"));
      tab.classList.add("action-tab--active");
    });
  });

  if (suggestionButton) {
    suggestionButton.addEventListener("click", function () {
      const resultPanel = document.querySelector(".result-panel");
      if (resultPanel) {
        resultPanel.classList.add("result-panel--active");
      }
    });
  }
});
