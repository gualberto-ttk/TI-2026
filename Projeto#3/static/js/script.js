function abrirMenu(){
    const menu = document.getElementById("menu")

    if(menu){
        menu.classList.toggle("ativo")
    }
}

function atualizarIconeTema(){
    const icone = document.getElementById("iconeTema")

    if(!icone){
        return
    }

    if(document.body.classList.contains("modo-escuro")){
        icone.className = "fa-solid fa-sun"
    }else{
        icone.className = "fa-solid fa-moon"
    }
}

function modoEscuro(){
    document.body.classList.toggle("modo-escuro")

    localStorage.setItem(
        "temaEscuro",
        document.body.classList.contains("modo-escuro")
    )

    atualizarIconeTema()
}

function mostrarSenha(id, botao){
    const campo = document.getElementById(id)

    if(!campo){
        return
    }

    const icone = botao.querySelector("i")

    if(campo.type === "password"){
        campo.type = "text"

        if(icone){
            icone.className = "fa-regular fa-eye-slash"
        }
    }else{
        campo.type = "password"

        if(icone){
            icone.className = "fa-regular fa-eye"
        }
    }
}

function aumentarFonte(){
    const tamanhoAtual = parseFloat(
        getComputedStyle(document.documentElement).fontSize
    )

    const novoTamanho = Math.min(tamanhoAtual + 2, 24)

    document.documentElement.style.fontSize = novoTamanho + "px"

    localStorage.setItem("tamanhoFonte", novoTamanho)
}

function diminuirFonte(){
    const tamanhoAtual = parseFloat(
        getComputedStyle(document.documentElement).fontSize
    )

    const novoTamanho = Math.max(tamanhoAtual - 2, 12)

    document.documentElement.style.fontSize = novoTamanho + "px"

    localStorage.setItem("tamanhoFonte", novoTamanho)
}

document.addEventListener("DOMContentLoaded", function(){
    const temaSalvo = localStorage.getItem("temaEscuro")
    const fonteSalva = localStorage.getItem("tamanhoFonte")

    if(temaSalvo === "true"){
        document.body.classList.add("modo-escuro")
    }

    if(fonteSalva){
        document.documentElement.style.fontSize = fonteSalva + "px"
    }

    atualizarIconeTema()

    document.querySelectorAll("#menu a").forEach(link => {
        link.addEventListener("click", function(){
            const menu = document.getElementById("menu")

            if(menu){
                menu.classList.remove("ativo")
            }
        })
    })
})
function alternarConteudos(botao){
    const card = botao.closest(".card-disciplina")

    if(!card){
        return
    }

    const aberto = card.classList.toggle("aberto")
    const icone = botao.querySelector("i")

    if(aberto){
        botao.childNodes[botao.childNodes.length - 1].textContent =
            " Ocultar conteúdos"

        if(icone){
            icone.className = "fa-solid fa-chevron-up"
        }
    }else{
        botao.childNodes[botao.childNodes.length - 1].textContent =
            " Ver conteúdos"

        if(icone){
            icone.className = "fa-solid fa-book-reader"
        }
    }
}
function alternarConteudos(botao){
    const card = botao.closest(".card-disciplina")

    if(!card){
        return
    }

    const aberto = card.classList.toggle("aberto")
    const texto = botao.querySelector("span")
    const icone = botao.querySelector("i")

    if(aberto){
        texto.textContent = "Ocultar conteúdos"
        icone.className = "fa-solid fa-chevron-up"
    }else{
        texto.textContent = "Ver conteúdos"
        icone.className = "fa-solid fa-book-reader"
    }
}

function salvarAnotacao(chave){
    const campo = document.getElementById("resposta")
    const mensagem = document.getElementById("mensagemAnotacao")

    if(!campo){
        return
    }

    localStorage.setItem(
        "anotacao-" + chave,
        campo.value
    )

    if(mensagem){
        mensagem.textContent = "Anotação salva!"
    }
}

document.addEventListener("DOMContentLoaded", function(){
    const campo = document.getElementById("resposta")

    if(campo){
        const partes = window.location.pathname.split("/")
        const chave = partes.slice(-5).join("-")
        const anotacao = localStorage.getItem("anotacao-" + chave)

        if(anotacao){
            campo.value = anotacao
        }
    }
})