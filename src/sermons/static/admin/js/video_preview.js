document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".video-preview").forEach(function (container) {
        container.addEventListener("click", function () {
            const embedUrl = container.getAttribute("data-embed");

            const iframe = document.createElement("iframe");
            iframe.setAttribute("src", embedUrl);
            iframe.setAttribute("width", "300");
            iframe.setAttribute("height", "170");
            iframe.setAttribute("frameborder", "0");
            iframe.setAttribute("allowfullscreen", "true");
            iframe.setAttribute("referrerpolicy", "strict-origin-when-cross-origin");

            container.innerHTML = "";
            container.appendChild(iframe);
        });
    });
});