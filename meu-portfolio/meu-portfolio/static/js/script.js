document.addEventListener("DOMContentLoaded", function() {
    const menu = document.querySelector(".menu-toggle");
    const lista = document.querySelector(".nav-list");

    if (menu && lista) {
        menu.addEventListener("click", function() {
            lista.classList.toggle("active");

            if (menu.getAttribute("aria-expanded") === "true") {
                menu.setAttribute("aria-expanded", "false");
            } else {
                menu.setAttribute("aria-expanded", "true");
            }
        });
    }

    const tema = document.getElementById("theme-toggle");

    if (localStorage.getItem("theme") === "light") {
        document.body.classList.add("light-mode");

        if (tema) {
            tema.textContent = "☀️";
        }
    }

    if (tema) {
        tema.addEventListener("click", function() {
            document.body.classList.toggle("light-mode");

            if (document.body.classList.contains("light-mode")) {
                tema.textContent = "☀️";
                localStorage.setItem("theme", "light");
            } else {
                tema.textContent = "🌙";
                localStorage.setItem("theme", "dark");
            }
        });
    }

    const saudacao = document.getElementById("saudacao-dinamica");

    if (saudacao) {
        const hora = new Date().getHours();

        if (hora >= 5 && hora < 12) {
            saudacao.textContent = "BOM DIA!";
        } else if (hora >= 12 && hora < 18) {
            saudacao.textContent = "BOA TARDE!";
        } else {
            saudacao.textContent = "BOA NOITE!";
        }
    }

    const ano = document.getElementById("current-year");

    if (ano) {
        ano.textContent = new Date().getFullYear();
    }

    const formulario = document.getElementById("contact-form");

    if (formulario) {
        formulario.addEventListener("submit", function(event) {
            event.preventDefault();

            const nome = document.getElementById("nome").value.trim();
            const email = document.getElementById("email").value.trim();
            const mensagem = document.getElementById("mensagem").value.trim();
            const consentimento = document.getElementById("consentimento").checked;

            if (nome === "" || email === "" || mensagem === "") {
                alert("Preencha todos os campos!");
                return;
            }

            if (!email.includes("@") || !email.includes(".")) {
                alert("Digite um e-mail válido!");
                return;
            }

            if (mensagem.length < 20) {
                alert("A mensagem precisa ter pelo menos 20 caracteres!");
                return;
            }

            if (!consentimento) {
                alert("Você precisa aceitar o termo de consentimento!");
                return;
            }

            alert("Mensagem enviada com sucesso!");
            formulario.reset();
        });
    }
});