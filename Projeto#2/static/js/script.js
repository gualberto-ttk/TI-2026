function aumentarFonte(){
    let tamanho = parseFloat(
        getComputedStyle(document.body).fontSize
    )

    document.body.style.fontSize = (tamanho + 2) + "px"
}

function diminuirFonte(){
    let tamanho = parseFloat(
        getComputedStyle(document.body).fontSize
    )

    if(tamanho > 12){
        document.body.style.fontSize = (tamanho - 2) + "px"
    }
}

function modoEscuro(){
    document.body.classList.toggle("modo-escuro")

    localStorage.setItem(
        "modoEscuro",
        document.body.classList.contains("modo-escuro")
    )
}

if(localStorage.getItem("modoEscuro") === "true"){
    document.body.classList.add("modo-escuro")
}

document.querySelectorAll(".card, .card-serie").forEach(card => {
    card.addEventListener("mousemove", evento => {
        const posicao = card.getBoundingClientRect()
        const x = evento.clientX - posicao.left
        const y = evento.clientY - posicao.top

        card.style.background = `
            radial-gradient(
                circle at ${x}px ${y}px,
                rgba(37, 99, 235, 0.12),
                rgba(255, 255, 255, 0.88) 45%
            )
        `
    })

    card.addEventListener("mouseleave", () => {
        card.style.background = ""
    })
})