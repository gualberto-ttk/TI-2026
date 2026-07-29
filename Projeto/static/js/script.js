document.addEventListener("DOMContentLoaded", function () {

    // Confirmação antes de excluir uma vaga
    const botoesExcluir = document.querySelectorAll(".btn-excluir");

    botoesExcluir.forEach(function (botao) {
        botao.addEventListener("click", function (evento) {
            const confirmar = confirm("Tem certeza que deseja excluir esta vaga?");

            if (!confirmar) {
                evento.preventDefault();
            }
        });
    });


    // Aumentar o tamanho da fonte
    const botaoAumentar = document.getElementById("aumentar-fonte");

    if (botaoAumentar) {
        botaoAumentar.addEventListener("click", function () {
            document.body.style.fontSize = "18px";
        });
    }


    // Voltar ao tamanho normal da fonte
    const botaoNormal = document.getElementById("fonte-normal");

    if (botaoNormal) {
        botaoNormal.addEventListener("click", function () {
            document.body.style.fontSize = "16px";
        });
    }


    // Diminuir o tamanho da fonte
    const botaoDiminuir = document.getElementById("diminuir-fonte");

    if (botaoDiminuir) {
        botaoDiminuir.addEventListener("click", function () {
            document.body.style.fontSize = "14px";
        });
    }


    // Ativar e desativar o alto contraste
    const botaoContraste = document.getElementById("alto-contraste");

    if (botaoContraste) {
        botaoContraste.addEventListener("click", function () {
            document.body.classList.toggle("alto-contraste");
        });
    }


    // Mostrar mensagem quando o formulário for enviado
    const formulario = document.querySelector("form");

    if (formulario) {
        formulario.addEventListener("submit", function () {
            const botaoEnviar = formulario.querySelector("button[type='submit']");

            if (botaoEnviar) {
                botaoEnviar.innerText = "Salvando...";
                botaoEnviar.disabled = true;
            }
        });
    }

});