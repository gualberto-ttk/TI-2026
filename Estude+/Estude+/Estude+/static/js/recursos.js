"use strict";

document.addEventListener("DOMContentLoaded", () => {
    if (document.getElementById("focusRelogio")) configurarFocus();
    if (document.getElementById("chatForm")) configurarChat();
    configurarRecompensas();
});

function configurarFocus() {
    const relogio = document.getElementById("focusRelogio");
    const barra = document.getElementById("focusBarra");
    const mensagem = document.getElementById("focusMensagem");
    const estado = document.getElementById("focusEstado");
    const disciplina = document.getElementById("focusDisciplina");
    const iniciar = document.getElementById("focusIniciar");
    const pausar = document.getElementById("focusPausar");
    const reiniciar = document.getElementById("focusReiniciar");
    const progresso = barra?.parentElement;

    let minutos = 25;
    let total = minutos * 60;
    let restante = total;
    let timer = null;
    let rodando = false;
    let concluindo = false;

    function formatarTempo(segundos) {
        const m = String(Math.floor(segundos / 60)).padStart(2, "0");
        const s = String(segundos % 60).padStart(2, "0");
        return `${m}:${s}`;
    }

    function desenhar() {
        const percentual = Math.min(100, Math.max(0, ((total - restante) / total) * 100));

        relogio.textContent = formatarTempo(restante);
        barra.style.width = `${percentual}%`;

        if (progresso) {
            progresso.setAttribute("aria-valuenow", String(Math.round(percentual)));
        }

        document.title = rodando
            ? `${formatarTempo(restante)} | Focus`
            : "Modo Focus | Estude+";
    }

    function atualizarBotoes() {
        iniciar.disabled = rodando || concluindo;
        pausar.disabled = !rodando || concluindo;
        reiniciar.disabled = concluindo;

        iniciar.innerHTML = rodando
            ? '<i class="fa-solid fa-spinner fa-spin"></i> Em andamento'
            : '<i class="fa-solid fa-play"></i> Iniciar';
    }

    function pararTimer() {
        if (timer) clearInterval(timer);
        timer = null;
        rodando = false;
        atualizarBotoes();
    }

    async function concluirSessao() {
        if (concluindo) return;

        concluindo = true;
        pararTimer();
        estado.textContent = "SALVANDO SUA SESSÃO";
        mensagem.textContent = "Registrando seu progresso...";

        try {
            const resposta = await fetch("/focus/concluir", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    minutos,
                    disciplina: disciplina.value.trim() || "Estudo geral"
                })
            });

            const dados = await resposta.json();

            if (!resposta.ok || !dados.sucesso) {
                throw new Error(dados.mensagem || "Não foi possível salvar a sessão.");
            }

            estado.textContent = "SESSÃO CONCLUÍDA";
            mensagem.textContent =
                `Parabéns! +${dados.xp_ganho} XP e +${dados.moedas_ganhas} moedas.`;

            if ("Notification" in window && Notification.permission === "granted") {
                new Notification("Sessão Focus concluída!", {
                    body: mensagem.textContent
                });
            }

            setTimeout(() => {
                restante = total;
                estado.textContent = "PRONTO PARA COMEÇAR";
                mensagem.textContent = "";
                concluindo = false;
                desenhar();
                atualizarBotoes();
            }, 3500);
        } catch (erro) {
            estado.textContent = "ERRO AO SALVAR";
            mensagem.textContent = erro.message;
            concluindo = false;
            atualizarBotoes();
        }
    }

    document.querySelectorAll("[data-minutos]").forEach((botao) => {
        botao.addEventListener("click", () => {
            if (rodando || concluindo) return;

            document.querySelectorAll("[data-minutos]").forEach((item) => {
                item.classList.remove("ativo");
            });

            botao.classList.add("ativo");
            minutos = Number(botao.dataset.minutos);
            total = minutos * 60;
            restante = total;
            estado.textContent = "PRONTO PARA COMEÇAR";
            mensagem.textContent = "";
            desenhar();
        });
    });

    iniciar.addEventListener("click", async () => {
        if (rodando || concluindo) return;

        if (!disciplina.value.trim()) {
            disciplina.focus();
            mensagem.textContent = "Digite o que você vai estudar.";
            return;
        }

        if ("Notification" in window && Notification.permission === "default") {
            Notification.requestPermission().catch(() => {});
        }

        rodando = true;
        estado.textContent = "MANTENHA O FOCO";
        mensagem.textContent = "";
        atualizarBotoes();

        timer = setInterval(() => {
            restante -= 1;
            desenhar();

            if (restante <= 0) {
                restante = 0;
                desenhar();
                concluirSessao();
            }
        }, 1000);
    });

    pausar.addEventListener("click", () => {
        if (!rodando) return;
        pararTimer();
        estado.textContent = "SESSÃO PAUSADA";
        mensagem.textContent = "Quando estiver pronto, clique em Iniciar para continuar.";
    });

    reiniciar.addEventListener("click", () => {
        pararTimer();
        restante = total;
        estado.textContent = "PRONTO PARA COMEÇAR";
        mensagem.textContent = "";
        desenhar();
    });

    desenhar();
    atualizarBotoes();
}

function configurarChat() {
    const form = document.getElementById("chatForm");
    const input = document.getElementById("chatInput");
    const area = document.getElementById("chatMensagens");
    const enviarBotao = document.getElementById("chatEnviar");
    const limparBotao = document.getElementById("chatLimpar");
    const contador = document.getElementById("chatContador");

    let enviando = false;
    let ultimaPergunta = "";

    function rolarParaFim() {
        area.scrollTop = area.scrollHeight;
    }

    function escaparTexto(texto) {
        return String(texto ?? "");
    }

    function criarMensagem(texto, tipo, carregando = false) {
        const balao = document.createElement("div");
        balao.className = `chat-balao ${tipo}${carregando ? " chat-carregando" : ""}`;

        if (tipo === "bot") {
            const avatar = document.createElement("span");
            avatar.className = "chat-avatar";
            avatar.innerHTML = '<i class="fa-solid fa-robot"></i>';
            balao.appendChild(avatar);
        }

        const conteudo = document.createElement("div");
        conteudo.className = "chat-conteudo";

        const autor = document.createElement("small");
        autor.textContent = tipo === "bot" ? "ESTUDEBOT" : "VOCÊ";

        const textoElemento = document.createElement("div");
        textoElemento.className = "chat-texto";
        textoElemento.textContent = escaparTexto(texto);

        conteudo.append(autor, textoElemento);

        if (tipo === "bot" && !carregando) {
            conteudo.appendChild(criarBotaoCopiar(textoElemento));
        }

        balao.appendChild(conteudo);
        area.appendChild(balao);
        rolarParaFim();
        return balao;
    }

    function criarBotaoCopiar(textoElemento) {
        const botao = document.createElement("button");
        botao.type = "button";
        botao.className = "chat-copiar";
        botao.innerHTML = '<i class="fa-regular fa-copy"></i> Copiar';

        botao.addEventListener("click", async () => {
            try {
                await navigator.clipboard.writeText(textoElemento.textContent);
                botao.innerHTML = '<i class="fa-solid fa-check"></i> Copiado';
                setTimeout(() => {
                    botao.innerHTML = '<i class="fa-regular fa-copy"></i> Copiar';
                }, 1600);
            } catch {
                botao.textContent = "Não foi possível copiar";
            }
        });

        return botao;
    }

    function alternarCarregamento(ativo) {
        enviando = ativo;
        input.disabled = ativo;
        enviarBotao.disabled = ativo;
        enviarBotao.innerHTML = ativo
            ? '<i class="fa-solid fa-spinner fa-spin"></i>'
            : '<i class="fa-solid fa-paper-plane"></i>';
    }

    function ajustarTextarea() {
        input.style.height = "auto";
        input.style.height = `${Math.min(input.scrollHeight, 150)}px`;
        contador.textContent = `${input.value.length}/8000`;
    }

    async function enviar(texto) {
        const mensagem = String(texto || "").trim();
        if (!mensagem || enviando) return;

        ultimaPergunta = mensagem;
        criarMensagem(mensagem, "usuario");
        input.value = "";
        ajustarTextarea();
        alternarCarregamento(true);

        const carregando = criarMensagem("Pensando em uma resposta...", "bot", true);

        try {
            const resposta = await fetch("/chatbot/perguntar", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ mensagem })
            });

            let dados = {};
            try {
                dados = await resposta.json();
            } catch {
                dados = {};
            }

            carregando.remove();

            if (!resposta.ok || dados.sucesso === false) {
                throw new Error(
                    dados.mensagem || "Não consegui obter uma resposta agora."
                );
            }

            criarMensagem(
                dados.resposta || dados.mensagem || "Não consegui responder.",
                "bot"
            );
        } catch (erro) {
            carregando.remove();
            criarMensagem(
                erro.message ||
                "Não foi possível conectar ao assistente. Tente novamente.",
                "bot"
            );
        } finally {
            alternarCarregamento(false);
            input.focus();
        }
    }

    form.addEventListener("submit", (evento) => {
        evento.preventDefault();
        enviar(input.value);
    });

    input.addEventListener("input", ajustarTextarea);

    input.addEventListener("keydown", (evento) => {
        if (evento.key === "Enter" && !evento.shiftKey) {
            evento.preventDefault();
            form.requestSubmit();
        }
    });

    document.querySelectorAll(".chat-sugestoes button").forEach((botao) => {
        botao.addEventListener("click", () => {
            enviar(botao.textContent.trim());
        });
    });

    document.querySelectorAll("[data-copiar-resposta]").forEach((botao) => {
        const conteudo = botao.closest(".chat-conteudo");
        const texto = conteudo?.querySelector(".chat-texto");

        if (!texto) return;

        botao.addEventListener("click", async () => {
            await navigator.clipboard.writeText(texto.textContent);
            botao.innerHTML = '<i class="fa-solid fa-check"></i> Copiado';
            setTimeout(() => {
                botao.innerHTML = '<i class="fa-regular fa-copy"></i> Copiar';
            }, 1600);
        });
    });

    limparBotao?.addEventListener("click", async () => {
        const confirmar = window.confirm(
            "Deseja apagar todo o histórico desta conversa?"
        );

        if (!confirmar) return;

        limparBotao.disabled = true;

        try {
            const resposta = await fetch("/chatbot/limpar", {
                method: "POST",
                headers: { "Content-Type": "application/json" }
            });

            if (!resposta.ok) {
                throw new Error("Não foi possível limpar a conversa.");
            }

            area.innerHTML = "";
            criarMensagem(
                "Conversa limpa! Pode enviar uma nova pergunta.",
                "bot"
            );
        } catch (erro) {
            criarMensagem(erro.message, "bot");
        } finally {
            limparBotao.disabled = false;
        }
    });

    ajustarTextarea();
    rolarParaFim();
}

function configurarRecompensas() {
    document.querySelectorAll("[data-form-recompensa]").forEach((formulario) => {
        formulario.addEventListener("submit", (evento) => {
            const botao = formulario.querySelector("button[type='submit']");

            if (!botao || botao.disabled) {
                evento.preventDefault();
                return;
            }

            const card = formulario.closest(".loja-card");
            const nome = card?.querySelector("h2")?.textContent?.trim() || "este item";
            const preco = card?.dataset.preco || "";

            const confirmar = window.confirm(
                `Desbloquear "${nome}" por ${preco} moedas?`
            );

            if (!confirmar) {
                evento.preventDefault();
                return;
            }

            botao.disabled = true;
            botao.innerHTML =
                '<i class="fa-solid fa-spinner fa-spin"></i> Processando...';
        });
    });
}
