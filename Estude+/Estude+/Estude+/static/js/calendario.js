(function () {
    "use strict";

    const pagina = document.querySelector(".calendario-pagina");

    if (!pagina) {
        return;
    }

    const grade = document.getElementById("gradeCalendario");
    const tituloMes = document.getElementById("tituloMes");
    const mesAnterior = document.getElementById("mesAnterior");
    const proximoMes = document.getElementById("proximoMes");
    const irParaHoje = document.getElementById("irParaHoje");
    const modal = document.getElementById("modalCalendario");
    const abrirNovoEvento = document.getElementById("abrirNovoEvento");
    const formEvento = document.getElementById("formEvento");
    const tituloModal = document.getElementById("tituloModalCalendario");
    const etiquetaModal = document.getElementById("etiquetaModalCalendario");
    const botaoSalvarTexto = formEvento?.querySelector(".botao-salvar-evento span");
    const eventos = Array.from(document.querySelectorAll(".calendario-evento"));
    const filtros = Array.from(document.querySelectorAll("[data-filtro]"));
    const hojeTexto = pagina.dataset.hoje;
    const hoje = hojeTexto ? new Date(`${hojeTexto}T12:00:00`) : new Date();

    let anoExibido = Number(grade?.dataset.ano) || hoje.getFullYear();
    let mesExibido = (Number(grade?.dataset.mes) || hoje.getMonth() + 1) - 1;
    let dataSelecionada = hojeTexto || "";

    const nomesMeses = [
        "janeiro", "fevereiro", "março", "abril", "maio", "junho",
        "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"
    ];

    const nomesMesesCurtos = [
        "JAN", "FEV", "MAR", "ABR", "MAI", "JUN",
        "JUL", "AGO", "SET", "OUT", "NOV", "DEZ"
    ];

    function doisDigitos(valor) {
        return String(valor).padStart(2, "0");
    }

    function dataISO(ano, mes, dia) {
        return `${ano}-${doisDigitos(mes + 1)}-${doisDigitos(dia)}`;
    }

    function eventosPorData(data) {
        return eventos.filter((evento) => evento.dataset.data === data);
    }

    function renderizarCalendario() {
        if (!grade || !tituloMes) {
            return;
        }

        grade.innerHTML = "";
        tituloMes.textContent = `${nomesMeses[mesExibido]} de ${anoExibido}`;

        const primeiroDia = new Date(anoExibido, mesExibido, 1).getDay();
        const totalDias = new Date(anoExibido, mesExibido + 1, 0).getDate();
        const totalAnterior = new Date(anoExibido, mesExibido, 0).getDate();
        const totalCelulas = 42;

        for (let indice = 0; indice < totalCelulas; indice += 1) {
            let dia;
            let mes = mesExibido;
            let ano = anoExibido;
            let outroMes = false;

            if (indice < primeiroDia) {
                dia = totalAnterior - primeiroDia + indice + 1;
                mes -= 1;
                outroMes = true;
            } else if (indice >= primeiroDia + totalDias) {
                dia = indice - primeiroDia - totalDias + 1;
                mes += 1;
                outroMes = true;
            } else {
                dia = indice - primeiroDia + 1;
            }

            if (mes < 0) {
                mes = 11;
                ano -= 1;
            }

            if (mes > 11) {
                mes = 0;
                ano += 1;
            }

            const data = dataISO(ano, mes, dia);
            const itens = eventosPorData(data);
            const botao = document.createElement("button");
            botao.type = "button";
            botao.className = "calendario-dia";
            botao.dataset.data = data;

            if (outroMes) {
                botao.classList.add("outro-mes");
            }

            if (data === hojeTexto) {
                botao.classList.add("hoje");
            }

            if (data === dataSelecionada) {
                botao.classList.add("selecionado");
            }

            const numero = document.createElement("span");
            numero.className = "calendario-dia-numero";
            numero.textContent = dia;
            botao.appendChild(numero);

            const areaEventos = document.createElement("span");
            areaEventos.className = "calendario-dia-eventos";

            itens.slice(0, 2).forEach((evento) => {
                const mini = document.createElement("span");
                mini.className = `calendario-mini-evento ${evento.dataset.prioridade || "media"}`;
                mini.textContent = evento.querySelector("h3")?.textContent.trim() || "Atividade";
                areaEventos.appendChild(mini);
            });

            if (itens.length > 2) {
                const mais = document.createElement("span");
                mais.className = "calendario-mais-eventos";
                mais.textContent = `+${itens.length - 2} atividades`;
                areaEventos.appendChild(mais);
            }

            botao.appendChild(areaEventos);

            botao.addEventListener("click", () => {
                dataSelecionada = data;
                document.getElementById("eventoData").value = data;
                renderizarCalendario();
                filtrarPorData(data);
            });

            grade.appendChild(botao);
        }
    }

    function abrirModalNovo(data = "") {
        if (!modal || !formEvento) {
            return;
        }

        formEvento.reset();
        formEvento.action = "/calendario/criar";
        document.getElementById("eventoPrioridade").value = "media";
        document.getElementById("eventoData").value = data || dataSelecionada || hojeTexto;
        tituloModal.textContent = "Planejar estudo";
        etiquetaModal.textContent = "NOVA ATIVIDADE";
        botaoSalvarTexto.textContent = "Salvar atividade";
        modal.classList.add("aberto");
        modal.setAttribute("aria-hidden", "false");
        document.body.classList.add("modal-aberto");
        setTimeout(() => document.getElementById("eventoTitulo")?.focus(), 50);
    }

    function abrirModalEdicao(botao) {
        if (!modal || !formEvento) {
            return;
        }

        const id = botao.dataset.id;
        formEvento.action = `/calendario/${encodeURIComponent(id)}/editar`;
        document.getElementById("eventoTitulo").value = botao.dataset.titulo || "";
        document.getElementById("eventoData").value = botao.dataset.data || "";
        document.getElementById("eventoHorario").value = botao.dataset.horario || "";
        document.getElementById("eventoDisciplina").value = botao.dataset.disciplina || "";
        document.getElementById("eventoDescricao").value = botao.dataset.descricao || "";
        document.getElementById("eventoPrioridade").value = botao.dataset.prioridade || "media";
        tituloModal.textContent = "Editar atividade";
        etiquetaModal.textContent = "ATUALIZAR PLANEJAMENTO";
        botaoSalvarTexto.textContent = "Salvar alterações";
        modal.classList.add("aberto");
        modal.setAttribute("aria-hidden", "false");
        document.body.classList.add("modal-aberto");
        setTimeout(() => document.getElementById("eventoTitulo")?.focus(), 50);
    }

    function fecharModal() {
        modal?.classList.remove("aberto");
        modal?.setAttribute("aria-hidden", "true");
        document.body.classList.remove("modal-aberto");
    }

    function filtrarPorData(data) {
        eventos.forEach((evento) => {
            evento.hidden = evento.dataset.data !== data;
        });

        filtros.forEach((botao) => botao.classList.remove("ativo"));
    }

    function aplicarFiltro(tipo) {
        dataSelecionada = "";
        renderizarCalendario();

        eventos.forEach((evento) => {
            const concluido = evento.dataset.concluido === "true";
            evento.hidden =
                (tipo === "pendentes" && concluido) ||
                (tipo === "concluidas" && !concluido);
        });
    }

    function atualizarResumo() {
        const concluidas = eventos.filter((evento) => evento.dataset.concluido === "true").length;
        const hojeTotal = eventos.filter((evento) => evento.dataset.data === hojeTexto).length;
        document.getElementById("totalAtividades").textContent = eventos.length;
        document.getElementById("totalConcluidas").textContent = concluidas;
        document.getElementById("totalPendentes").textContent = eventos.length - concluidas;
        document.getElementById("totalHoje").textContent = hojeTotal;
    }

    function formatarDatas() {
        document.querySelectorAll("[data-data-formatar]").forEach((elemento) => {
            const [ano, mes] = elemento.dataset.dataFormatar.split("-").map(Number);
            elemento.textContent = nomesMesesCurtos[mes - 1] || "";
        });
    }

    mesAnterior?.addEventListener("click", () => {
        mesExibido -= 1;
        if (mesExibido < 0) {
            mesExibido = 11;
            anoExibido -= 1;
        }
        renderizarCalendario();
    });

    proximoMes?.addEventListener("click", () => {
        mesExibido += 1;
        if (mesExibido > 11) {
            mesExibido = 0;
            anoExibido += 1;
        }
        renderizarCalendario();
    });

    irParaHoje?.addEventListener("click", () => {
        anoExibido = hoje.getFullYear();
        mesExibido = hoje.getMonth();
        dataSelecionada = hojeTexto;
        eventos.forEach((evento) => {
            evento.hidden = false;
        });
        filtros.forEach((botao) => botao.classList.remove("ativo"));
        filtros[0]?.classList.add("ativo");
        renderizarCalendario();
    });

    abrirNovoEvento?.addEventListener("click", () => abrirModalNovo());

    document.querySelectorAll("[data-fechar-modal]").forEach((botao) => {
        botao.addEventListener("click", fecharModal);
    });

    document.querySelectorAll(".editar-evento").forEach((botao) => {
        botao.addEventListener("click", () => abrirModalEdicao(botao));
    });

    filtros.forEach((botao) => {
        botao.addEventListener("click", () => {
            filtros.forEach((item) => item.classList.remove("ativo"));
            botao.classList.add("ativo");
            aplicarFiltro(botao.dataset.filtro);
        });
    });

    document.addEventListener("keydown", (evento) => {
        if (evento.key === "Escape") {
            fecharModal();
        }
    });

    renderizarCalendario();
    atualizarResumo();
    formatarDatas();
})();