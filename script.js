console.log("Hello, JavaScript is linked!");

document.addEventListener("DOMContentLoaded", function() {
    const chakra = document.querySelector(".chakra");
    const numSpokes = 24;

    for (let i = 0; i < numSpokes; i++) {
        const spoke = document.createElement("div");
        spoke.classList.add("spoke");
        spoke.style.transform = `rotate(${i * (360 / numSpokes)}deg)`;
        chakra.appendChild(spoke);
    }
});
