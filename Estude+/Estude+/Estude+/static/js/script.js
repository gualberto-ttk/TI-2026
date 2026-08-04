"use strict";

/* =========================================================
   UTILITÁRIOS
   ========================================================= */

function salvarLocal(chave, valor) {
    try {
        localStorage.setItem(chave, valor);
    } catch (erro) {
        console.warn("Não foi possível salvar no navegador:", erro);
    }
}

function lerLocal(chave, valorPadrao = "") {
    try {
        return localStorage.getItem(chave) || valorPadrao;
    } catch (erro) {
        return valorPadrao;
    }
}

function removerLocal(chave) {
    try {
        localStorage.removeItem(chave);
    } catch (erro) {
        console.warn("Não foi possível remover a configuração:", erro);
    }
}


/* =========================================================
   MENU RESPONSIVO
   ========================================================= */

function configurarMenuResponsivo() {
    const menu = document.getElementById("menu");
    const botaoMenu = document.getElementById("botaoMenu");

    if (!menu || !botaoMenu) {
        return;
    }

    function atualizarBotaoMenu() {
        const aberto = menu.classList.contains("aberto");
        const icone = botaoMenu.querySelector("i");

        botaoMenu.setAttribute(
            "aria-expanded",
            aberto ? "true" : "false"
        );

        botaoMenu.setAttribute(
            "aria-label",
            aberto ? "Fechar menu" : "Abrir menu"
        );

        botaoMenu.title = aberto
            ? "Fechar menu"
            : "Abrir menu";

        if (icone) {
            icone.className = aberto
                ? "fa-solid fa-xmark"
                : "fa-solid fa-bars";
        }
    }

    function fecharMenu() {
        menu.classList.remove("aberto");
        atualizarBotaoMenu();
    }

    botaoMenu.addEventListener("click", function (evento) {
        evento.preventDefault();
        evento.stopPropagation();

        menu.classList.toggle("aberto");
        atualizarBotaoMenu();
    });

    menu.addEventListener("click", function (evento) {
        evento.stopPropagation();
    });

    menu.querySelectorAll("a").forEach(function (link) {
        link.addEventListener("click", fecharMenu);
    });

    document.addEventListener("click", function (evento) {
        if (
            menu.classList.contains("aberto") &&
            !menu.contains(evento.target) &&
            !botaoMenu.contains(evento.target)
        ) {
            fecharMenu();
        }

        const perfil = document.querySelector(".perfil-site");

        if (
            perfil &&
            perfil.open &&
            !perfil.contains(evento.target)
        ) {
            perfil.removeAttribute("open");
        }
    });

    document.addEventListener("keydown", function (evento) {
        if (evento.key === "Escape") {
            fecharMenu();
        }
    });

    window.addEventListener("resize", function () {
        if (window.innerWidth > 980) {
            fecharMenu();
        }
    });

    atualizarBotaoMenu();
}


/* =========================================================
   TEMA ESCURO
   ========================================================= */

function atualizarIconeTema() {
    const icone = document.getElementById("iconeTema");

    if (!icone) {
        return;
    }

    const temaEscuro =
        document.body.classList.contains("modo-escuro");

    icone.className = temaEscuro
        ? "fa-solid fa-sun"
        : "fa-solid fa-moon";
}

function alternarTema() {
    document.body.classList.toggle("modo-escuro");

    const temaEscuro =
        document.body.classList.contains("modo-escuro");

    salvarLocal(
        "temaEscuro",
        temaEscuro ? "true" : "false"
    );

    atualizarIconeTema();
}

function configurarTema() {
    const botaoTema = document.getElementById("botaoTema");

    if (lerLocal("temaEscuro") === "true") {
        document.body.classList.add("modo-escuro");
    }

    atualizarIconeTema();

    if (!botaoTema) {
        return;
    }

    botaoTema.addEventListener("click", function (evento) {
        evento.preventDefault();
        alternarTema();
    });
}


/* =========================================================
   ACESSIBILIDADE — OPÇÕES ATIVAS
   ========================================================= */

function marcarOpcaoAtiva(grupoNome, opcaoNome) {
    const grupo = document.querySelector(
        `[data-grupo-acessibilidade="${grupoNome}"]`
    );

    if (!grupo) {
        return;
    }

    const botoes = grupo.querySelectorAll(
        ".opcao-acessibilidade, .opcao-espacamento"
    );

    botoes.forEach(function (botao) {
        const ativo = botao.dataset.opcao === opcaoNome;

        botao.classList.toggle("ativa", ativo);

        botao.setAttribute(
            "aria-pressed",
            ativo ? "true" : "false"
        );
    });
}


/* =========================================================
   TAMANHO DA FONTE
   ========================================================= */

function aplicarTamanhoFonte(opcao, salvar = true) {
    const tamanhos = {
        menor: "14px",
        normal: "16px",
        maior: "18px"
    };

    if (!tamanhos[opcao]) {
        opcao = "normal";
    }

    document.documentElement.style.fontSize =
        tamanhos[opcao];

    marcarOpcaoAtiva("fonte", opcao);

    if (salvar) {
        salvarLocal("estude-fonte", opcao);
    }
}

function diminuirFonte() {
    aplicarTamanhoFonte("menor");
}

function fonteNormal() {
    aplicarTamanhoFonte("normal");
}

function aumentarFonte() {
    aplicarTamanhoFonte("maior");
}


/* =========================================================
   CONTRASTE
   ========================================================= */

function aplicarContraste(tipo, salvar = true) {
    const tiposValidos = [
        "padrao",
        "alto",
        "cinza"
    ];

    if (!tiposValidos.includes(tipo)) {
        tipo = "padrao";
    }

    document.body.classList.remove(
        "contraste-alto",
        "escala-cinza"
    );

    if (tipo === "alto") {
        document.body.classList.add("contraste-alto");
    }

    if (tipo === "cinza") {
        document.body.classList.add("escala-cinza");
    }

    marcarOpcaoAtiva("contraste", tipo);

    if (salvar) {
        salvarLocal("estude-contraste", tipo);
    }
}

function alterarContraste(tipo) {
    aplicarContraste(tipo);
}


/* =========================================================
   FONTE DE LEITURA
   ========================================================= */

function aplicarFonteLeitura(tipo, salvar = true) {
    if (tipo !== "acessivel") {
        tipo = "padrao";
    }

    document.body.classList.toggle(
        "fonte-acessivel",
        tipo === "acessivel"
    );

    marcarOpcaoAtiva("fonte-leitura", tipo);

    if (salvar) {
        salvarLocal("estude-fonte-leitura", tipo);
    }
}

function alterarFonteLeitura(tipo) {
    aplicarFonteLeitura(tipo);
}


/* =========================================================
   MOVIMENTOS E ANIMAÇÕES
   ========================================================= */

function aplicarAnimacoes(tipo, salvar = true) {
    if (tipo !== "reduzidas") {
        tipo = "normais";
    }

    document.body.classList.toggle(
        "reduzir-animacoes",
        tipo === "reduzidas"
    );

    marcarOpcaoAtiva("animacoes", tipo);

    if (salvar) {
        salvarLocal("estude-animacoes", tipo);
    }
}

function alterarAnimacoes(reduzir) {
    aplicarAnimacoes(
        reduzir ? "reduzidas" : "normais"
    );
}


/* =========================================================
   ESPAÇAMENTO DE LEITURA
   ========================================================= */

function aplicarEspacamento(tipo, salvar = true) {
    const tiposValidos = [
        "padrao",
        "confortavel",
        "amplo"
    ];

    if (!tiposValidos.includes(tipo)) {
        tipo = "padrao";
    }

    document.body.classList.remove(
        "espacamento-confortavel",
        "espacamento-amplo"
    );

    if (tipo === "confortavel") {
        document.body.classList.add(
            "espacamento-confortavel"
        );
    }

    if (tipo === "amplo") {
        document.body.classList.add(
            "espacamento-amplo"
        );
    }

    marcarOpcaoAtiva("espacamento", tipo);

    if (salvar) {
        salvarLocal("estude-espacamento", tipo);
    }
}

function alterarEspacamentoLeitura(tipo) {
    aplicarEspacamento(tipo);
}


/* =========================================================
   RESTAURAR ACESSIBILIDADE
   ========================================================= */

function restaurarAcessibilidade() {
    [
        "estude-fonte",
        "estude-contraste",
        "estude-fonte-leitura",
        "estude-animacoes",
        "estude-espacamento",
        "fonte",
        "contraste",
        "fonteLeitura",
        "animacoes",
        "espacamentoLeitura"
    ].forEach(function (chave) {
        removerLocal(chave);
    });

    aplicarTamanhoFonte("normal", false);
    aplicarContraste("padrao", false);
    aplicarFonteLeitura("padrao", false);
    aplicarAnimacoes("normais", false);
    aplicarEspacamento("padrao", false);
}

function restaurarBotoesAcessibilidade() {
    restaurarAcessibilidade();
}


/* =========================================================
   CONFIGURAR CLIQUES DOS BOTÕES
   ========================================================= */

function configurarBotoesAcessibilidade() {
    const grupos = document.querySelectorAll(
        "[data-grupo-acessibilidade]"
    );

    grupos.forEach(function (grupo) {
        const nomeGrupo =
            grupo.dataset.grupoAcessibilidade;

        const botoes = grupo.querySelectorAll(
            ".opcao-acessibilidade, .opcao-espacamento"
        );

        botoes.forEach(function (botao) {
            /*
             * Remove o onclick do HTML para evitar
             * que a mesma função seja executada duas vezes.
             */
            botao.removeAttribute("onclick");

            botao.addEventListener("click", function (evento) {
                evento.preventDefault();
                evento.stopPropagation();

                const opcao = botao.dataset.opcao;

                if (nomeGrupo === "fonte") {
                    aplicarTamanhoFonte(opcao);
                }

                if (nomeGrupo === "contraste") {
                    aplicarContraste(opcao);
                }

                if (nomeGrupo === "fonte-leitura") {
                    aplicarFonteLeitura(opcao);
                }

                if (nomeGrupo === "animacoes") {
                    aplicarAnimacoes(opcao);
                }

                if (nomeGrupo === "espacamento") {
                    aplicarEspacamento(opcao);
                }
            });
        });
    });

    const botaoRestaurar = document.querySelector(
        ".botao-restaurar-acessibilidade"
    );

    if (botaoRestaurar) {
        botaoRestaurar.removeAttribute("onclick");

        botaoRestaurar.addEventListener(
            "click",
            function (evento) {
                evento.preventDefault();
                restaurarAcessibilidade();
            }
        );
    }
}


/* =========================================================
   CARREGAR PREFERÊNCIAS
   ========================================================= */

function carregarAcessibilidade() {
    const fonte = lerLocal(
        "estude-fonte",
        "normal"
    );

    const contraste = lerLocal(
        "estude-contraste",
        "padrao"
    );

    const fonteLeitura = lerLocal(
        "estude-fonte-leitura",
        "padrao"
    );

    const animacoes = lerLocal(
        "estude-animacoes",
        "normais"
    );

    const espacamento = lerLocal(
        "estude-espacamento",
        "padrao"
    );

    aplicarTamanhoFonte(fonte, false);
    aplicarContraste(contraste, false);
    aplicarFonteLeitura(fonteLeitura, false);
    aplicarAnimacoes(animacoes, false);
    aplicarEspacamento(espacamento, false);
}


/* =========================================================
   MOSTRAR E OCULTAR SENHA
   ========================================================= */

function alternarSenha(idCampo, botao) {
    const campo = document.getElementById(idCampo);

    if (!campo || !botao) {
        return;
    }

    const mostrar = campo.type === "password";
    const icone = botao.querySelector("i");

    campo.type = mostrar
        ? "text"
        : "password";

    if (icone) {
        icone.className = mostrar
            ? "fa-regular fa-eye-slash"
            : "fa-regular fa-eye";
    }

    botao.setAttribute(
        "aria-label",
        mostrar ? "Ocultar senha" : "Mostrar senha"
    );
}


/* =========================================================
   EDITOR DO CADERNO
   ========================================================= */

function prepararEditor() {
    const formulario =
        document.getElementById("formCaderno");

    const conteudo =
        document.getElementById("conteudo");

    const contador =
        document.getElementById("contadorPalavras");

    if (!formulario || !conteudo) {
        return;
    }

    const chave =
        `rascunho-${window.location.pathname}`;

    const campos = Array.from(
        formulario.querySelectorAll(
            "input[name], textarea[name]"
        )
    );

    function contarPalavras() {
        const texto = conteudo.value.trim();

        const total = texto
            ? texto.split(/\s+/).filter(Boolean).length
            : 0;

        if (contador) {
            contador.textContent =
                total === 1
                    ? "1 palavra"
                    : `${total} palavras`;
        }
    }

    function salvarRascunho() {
        const dados = {};

        campos.forEach(function (campo) {
            dados[campo.name] = campo.value;
        });

        salvarLocal(
            chave,
            JSON.stringify(dados)
        );

        contarPalavras();
    }

    campos.forEach(function (campo) {
        campo.addEventListener(
            "input",
            salvarRascunho
        );
    });

    const rascunhoSalvo = lerLocal(chave);

    const formularioVazio = campos.every(function (campo) {
        return !campo.value;
    });

    if (rascunhoSalvo && formularioVazio) {
        try {
            const dados = JSON.parse(rascunhoSalvo);

            campos.forEach(function (campo) {
                if (
                    Object.prototype.hasOwnProperty.call(
                        dados,
                        campo.name
                    )
                ) {
                    campo.value =
                        dados[campo.name] || "";
                }
            });
        } catch (erro) {
            removerLocal(chave);
        }
    }

    formulario.addEventListener("submit", function () {
        removerLocal(chave);
    });

    contarPalavras();
}


/* =========================================================
   CONTEÚDO VISÍVEL
   ========================================================= */

function revelarElementos() {
    const elementos = document.querySelectorAll(
        ".revelar"
    );

    elementos.forEach(function (elemento) {
        elemento.classList.add("visivel");
        elemento.style.opacity = "1";
        elemento.style.visibility = "visible";
    });
}


/* =========================================================
   INICIALIZAÇÃO
   ========================================================= */

function iniciarSite() {
    revelarElementos();
    configurarTema();
    configurarMenuResponsivo();
    carregarAcessibilidade();
    configurarBotoesAcessibilidade();
    prepararEditor();
    revelarElementos();
}

/*
 * Deixa as funções disponíveis para botões que ainda
 * possuam onclick no HTML.
 */
window.diminuirFonte = diminuirFonte;
window.fonteNormal = fonteNormal;
window.aumentarFonte = aumentarFonte;
window.alterarContraste = alterarContraste;
window.alterarFonteLeitura = alterarFonteLeitura;
window.alterarAnimacoes = alterarAnimacoes;
window.alterarEspacamentoLeitura =
    alterarEspacamentoLeitura;
window.restaurarAcessibilidade =
    restaurarAcessibilidade;
window.restaurarBotoesAcessibilidade =
    restaurarBotoesAcessibilidade;
window.alternarSenha = alternarSenha;

if (document.readyState === "loading") {
    document.addEventListener(
        "DOMContentLoaded",
        iniciarSite
    );
} else {
    iniciarSite();
}