function abrirMenu() {
    const menu = document.getElementById("menu");
    const botao = document.querySelector(".menu-mobile");

    if (!menu) {
        return;
    }

    menu.classList.toggle("aberto");

    if (botao) {
        botao.setAttribute(
            "aria-expanded",
            menu.classList.contains("aberto")
                ? "true"
                : "false"
        );
    }
}


function fecharMenuMobile() {
    const menu = document.getElementById("menu");
    const botao = document.querySelector(".menu-mobile");

    if (!menu) {
        return;
    }

    menu.classList.remove("aberto");

    if (botao) {
        botao.setAttribute("aria-expanded", "false");
    }
}


function atualizarIconeTema() {
    const icone = document.getElementById("iconeTema");

    if (!icone) {
        return;
    }

    if (document.body.classList.contains("modo-escuro")) {
        icone.className = "fa-solid fa-sun";
    } else {
        icone.className = "fa-solid fa-moon";
    }
}


function modoEscuro() {
    document.body.classList.toggle("modo-escuro");

    const temaAtivo =
        document.body.classList.contains("modo-escuro");

    localStorage.setItem(
        "temaEscuro",
        temaAtivo ? "true" : "false"
    );

    atualizarIconeTema();
}


/* =========================================================
   TAMANHO DA FONTE
   ========================================================= */

function tamanhoFonteAtual() {
    return (
        parseFloat(
            getComputedStyle(document.documentElement).fontSize
        ) || 16
    );
}


function diminuirFonte() {
    const tamanho = Math.max(
        tamanhoFonteAtual() - 2,
        12
    );

    document.documentElement.style.fontSize =
        `${tamanho}px`;

    localStorage.setItem("fonte", String(tamanho));

    selecionarOpcaoAcessibilidade(
        "fonte",
        "menor"
    );
}


function fonteNormal() {
    document.documentElement.style.fontSize = "16px";

    localStorage.setItem("fonte", "16");

    selecionarOpcaoAcessibilidade(
        "fonte",
        "normal"
    );
}


function aumentarFonte() {
    const tamanho = Math.min(
        tamanhoFonteAtual() + 2,
        24
    );

    document.documentElement.style.fontSize =
        `${tamanho}px`;

    localStorage.setItem("fonte", String(tamanho));

    selecionarOpcaoAcessibilidade(
        "fonte",
        "maior"
    );
}


/* =========================================================
   CONTRASTE
   ========================================================= */

function alterarContraste(tipo) {
    document.body.classList.remove(
        "contraste-alto",
        "escala-cinza"
    );

    if (tipo === "alto") {
        document.body.classList.add(
            "contraste-alto"
        );
    }

    if (tipo === "cinza") {
        document.body.classList.add(
            "escala-cinza"
        );
    }

    localStorage.setItem("contraste", tipo);

    selecionarOpcaoAcessibilidade(
        "contraste",
        tipo
    );
}


/* =========================================================
   FONTE DE LEITURA
   ========================================================= */

function alterarFonteLeitura(tipo) {
    const usarFonteAcessivel =
        tipo === "acessivel";

    document.body.classList.toggle(
        "fonte-acessivel",
        usarFonteAcessivel
    );

    localStorage.setItem(
        "fonteLeitura",
        tipo
    );

    selecionarOpcaoAcessibilidade(
        "fonte-leitura",
        tipo
    );
}


/* =========================================================
   ANIMAÇÕES
   ========================================================= */

function alterarAnimacoes(reduzir) {
    const opcao = reduzir
        ? "reduzidas"
        : "normais";

    document.body.classList.toggle(
        "reduzir-animacoes",
        reduzir
    );

    localStorage.setItem(
        "animacoes",
        reduzir ? "1" : "0"
    );

    selecionarOpcaoAcessibilidade(
        "animacoes",
        opcao
    );
}


/* =========================================================
   ESPAÇAMENTO DE LEITURA
   ========================================================= */

function alterarEspacamentoLeitura(tipo) {
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

    localStorage.setItem(
        "espacamentoLeitura",
        tipo
    );

    selecionarOpcaoAcessibilidade(
        "espacamento",
        tipo
    );
}


/* =========================================================
   BOTÕES DA PÁGINA DE ACESSIBILIDADE
   ========================================================= */

function selecionarOpcaoAcessibilidade(
    grupoNome,
    opcaoNome,
    salvar = true
) {
    const grupo = document.querySelector(
        `[data-grupo-acessibilidade="${grupoNome}"]`
    );

    if (!grupo) {
        return;
    }

    const botoes = grupo.querySelectorAll(
        ".opcao-acessibilidade, .opcao-espacamento"
    );

    botoes.forEach(botao => {
        const selecionado =
            botao.dataset.opcao === opcaoNome;

        botao.classList.toggle(
            "ativa",
            selecionado
        );

        botao.setAttribute(
            "aria-pressed",
            selecionado ? "true" : "false"
        );
    });

    if (salvar) {
        localStorage.setItem(
            `opcao-${grupoNome}`,
            opcaoNome
        );
    }
}


function definirOpcaoVisualFonte() {
    const tamanho = Number(
        localStorage.getItem("fonte") || 16
    );

    if (tamanho < 16) {
        return "menor";
    }

    if (tamanho > 16) {
        return "maior";
    }

    return "normal";
}


function restaurarSelecoesVisuaisSalvas() {
    const opcoes = {
        fonte:
            localStorage.getItem("opcao-fonte") ||
            definirOpcaoVisualFonte(),

        contraste:
            localStorage.getItem("opcao-contraste") ||
            localStorage.getItem("contraste") ||
            "padrao",

        "fonte-leitura":
            localStorage.getItem("opcao-fonte-leitura") ||
            localStorage.getItem("fonteLeitura") ||
            "padrao",

        animacoes:
            localStorage.getItem("opcao-animacoes") ||
            (
                localStorage.getItem("animacoes") === "1"
                    ? "reduzidas"
                    : "normais"
            ),

        espacamento:
            localStorage.getItem("opcao-espacamento") ||
            localStorage.getItem("espacamentoLeitura") ||
            "padrao"
    };

    Object.entries(opcoes).forEach(
        ([grupo, opcao]) => {
            selecionarOpcaoAcessibilidade(
                grupo,
                opcao,
                false
            );
        }
    );
}


function configurarBotoesAcessibilidade() {
    const grupos = document.querySelectorAll(
        "[data-grupo-acessibilidade]"
    );

    grupos.forEach(grupo => {
        const nomeGrupo =
            grupo.dataset.grupoAcessibilidade;

        const botoes = grupo.querySelectorAll(
            ".opcao-acessibilidade, .opcao-espacamento"
        );

        botoes.forEach(botao => {
            botao.setAttribute(
                "aria-pressed",
                botao.classList.contains("ativa")
                    ? "true"
                    : "false"
            );

            botao.addEventListener("click", () => {
                selecionarOpcaoAcessibilidade(
                    nomeGrupo,
                    botao.dataset.opcao
                );
            });
        });
    });

    restaurarSelecoesVisuaisSalvas();
}


/* =========================================================
   RESTAURAR ACESSIBILIDADE
   ========================================================= */

function restaurarAcessibilidade() {
    const configuracoes = [
        "fonte",
        "contraste",
        "fonteLeitura",
        "animacoes",
        "espacamentoLeitura",
        "opcao-fonte",
        "opcao-contraste",
        "opcao-fonte-leitura",
        "opcao-animacoes",
        "opcao-espacamento"
    ];

    configuracoes.forEach(configuracao => {
        localStorage.removeItem(configuracao);
    });

    document.documentElement.style.fontSize = "16px";

    document.body.classList.remove(
        "contraste-alto",
        "escala-cinza",
        "fonte-acessivel",
        "reduzir-animacoes",
        "espacamento-confortavel",
        "espacamento-amplo"
    );

    restaurarBotoesAcessibilidade();
}


function restaurarBotoesAcessibilidade() {
    const valoresPadrao = {
        fonte: "normal",
        contraste: "padrao",
        "fonte-leitura": "padrao",
        animacoes: "normais",
        espacamento: "padrao"
    };

    Object.entries(valoresPadrao).forEach(
        ([grupo, opcao]) => {
            localStorage.removeItem(
                `opcao-${grupo}`
            );

            selecionarOpcaoAcessibilidade(
                grupo,
                opcao,
                false
            );
        }
    );
}


/* =========================================================
   MOSTRAR E OCULTAR SENHA
   ========================================================= */

function alternarSenha(idCampo, botao) {
    const campo = document.getElementById(idCampo);

    if (!campo || !botao) {
        return;
    }

    const icone = botao.querySelector("i");
    const mostrar = campo.type === "password";

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
        mostrar
            ? "Ocultar senha"
            : "Mostrar senha"
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

    const chaveRascunho =
        `rascunho-${window.location.pathname}`;

    const campos = Array.from(
        formulario.querySelectorAll(
            "input, textarea"
        )
    );

    function contarPalavras() {
        const texto = conteudo.value.trim();

        const quantidade = texto
            ? texto.split(/\s+/).length
            : 0;

        if (contador) {
            contador.textContent =
                quantidade === 1
                    ? "1 palavra"
                    : `${quantidade} palavras`;
        }
    }

    function salvarRascunho() {
        const dados = {};

        campos.forEach(campo => {
            dados[campo.name] = campo.value;
        });

        localStorage.setItem(
            chaveRascunho,
            JSON.stringify(dados)
        );

        contarPalavras();
    }

    campos.forEach(campo => {
        campo.addEventListener(
            "input",
            salvarRascunho
        );
    });

    const rascunhoSalvo =
        localStorage.getItem(chaveRascunho);

    const camposVazios = campos.every(
        campo => !campo.value
    );

    if (rascunhoSalvo && camposVazios) {
        try {
            const dados =
                JSON.parse(rascunhoSalvo);

            campos.forEach(campo => {
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
            localStorage.removeItem(
                chaveRascunho
            );
        }
    }

    formulario.addEventListener(
        "submit",
        () => {
            localStorage.removeItem(
                chaveRascunho
            );
        }
    );

    contarPalavras();
}


/* =========================================================
   ANIMAÇÕES AO ROLAR A PÁGINA
   ========================================================= */

function revelarElementos() {
    const elementos =
        document.querySelectorAll(".revelar");

    if (!elementos.length) {
        return;
    }

    const reduzirMovimentos =
        document.body.classList.contains(
            "reduzir-animacoes"
        ) ||
        window.matchMedia(
            "(prefers-reduced-motion: reduce)"
        ).matches;

    if (
        reduzirMovimentos ||
        !("IntersectionObserver" in window)
    ) {
        elementos.forEach(elemento => {
            elemento.classList.add("visivel");
        });

        return;
    }

    const observador = new IntersectionObserver(
        entradas => {
            entradas.forEach(entrada => {
                if (entrada.isIntersecting) {
                    entrada.target.classList.add(
                        "visivel"
                    );

                    observador.unobserve(
                        entrada.target
                    );
                }
            });
        },
        {
            threshold: 0.12,
            rootMargin: "0px 0px -30px 0px"
        }
    );

    elementos.forEach(elemento => {
        observador.observe(elemento);
    });
}


/* =========================================================
   CONTADORES DA PÁGINA INICIAL
   ========================================================= */

function prepararContadores() {
    const contadores =
        document.querySelectorAll("[data-contador]");

    if (!contadores.length) {
        return;
    }

    function animarContador(elemento) {
        if (elemento.dataset.animado === "true") {
            return;
        }

        elemento.dataset.animado = "true";

        const total = Number(
            elemento.dataset.contador || 0
        );

        const inicio = performance.now();
        const duracao = 900;

        function atualizar(tempoAtual) {
            const progresso = Math.min(
                (tempoAtual - inicio) / duracao,
                1
            );

            elemento.textContent = String(
                Math.round(total * progresso)
            );

            if (progresso < 1) {
                requestAnimationFrame(atualizar);
            }
        }

        requestAnimationFrame(atualizar);
    }

    if (!("IntersectionObserver" in window)) {
        contadores.forEach(animarContador);
        return;
    }

    const observador = new IntersectionObserver(
        entradas => {
            entradas.forEach(entrada => {
                if (entrada.isIntersecting) {
                    animarContador(entrada.target);

                    observador.unobserve(
                        entrada.target
                    );
                }
            });
        },
        {
            threshold: 0.5
        }
    );

    contadores.forEach(contador => {
        observador.observe(contador);
    });
}


/* =========================================================
   CARREGAR CONFIGURAÇÕES SALVAS
   ========================================================= */

function carregarConfiguracoes() {
    const temaEscuro =
        localStorage.getItem("temaEscuro");

    if (temaEscuro === "true") {
        document.body.classList.add(
            "modo-escuro"
        );
    }

    const fonte =
        localStorage.getItem("fonte");

    if (fonte) {
        document.documentElement.style.fontSize =
            `${fonte}px`;
    }

    const contraste =
        localStorage.getItem("contraste") ||
        "padrao";

    alterarContraste(contraste);

    const fonteLeitura =
        localStorage.getItem("fonteLeitura") ||
        "padrao";

    alterarFonteLeitura(fonteLeitura);

    const reduzirAnimacoes =
        localStorage.getItem("animacoes") === "1";

    alterarAnimacoes(reduzirAnimacoes);

    const espacamento =
        localStorage.getItem(
            "espacamentoLeitura"
        ) || "padrao";

    alterarEspacamentoLeitura(espacamento);

    atualizarIconeTema();
}


/* =========================================================
   EVENTOS GERAIS
   ========================================================= */

function configurarEventosGerais() {
    const linksMenu = document.querySelectorAll(
        "#menu a"
    );

    linksMenu.forEach(link => {
        link.addEventListener(
            "click",
            fecharMenuMobile
        );
    });

    window.addEventListener("resize", () => {
        if (window.innerWidth > 980) {
            fecharMenuMobile();
        }
    });

    document.addEventListener("click", evento => {
        const menu = document.getElementById("menu");
        const botao = document.querySelector(
            ".menu-mobile"
        );

        if (
            !menu ||
            !menu.classList.contains("aberto")
        ) {
            return;
        }

        const clicouNoMenu =
            menu.contains(evento.target);

        const clicouNoBotao =
            botao && botao.contains(evento.target);

        if (!clicouNoMenu && !clicouNoBotao) {
            fecharMenuMobile();
        }
    });
}


/* =========================================================
   INICIALIZAÇÃO
   ========================================================= */

document.addEventListener(
    "DOMContentLoaded",
    () => {
        carregarConfiguracoes();
        configurarBotoesAcessibilidade();
        configurarEventosGerais();
        prepararEditor();
        revelarElementos();
        prepararContadores();
    }
);