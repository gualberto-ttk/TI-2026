/* =========================================== CHATBOT PREMIUM - AÇÕES
DAS RESPOSTAS Acrescente ao final do recursos.js
=========================================== */

function adicionarAcoesMensagem(blocoResposta, textoOriginal){

    const acoes=document.createElement("div");
    acoes.className="chat-acoes";

    const copiar=document.createElement("button");
    copiar.innerHTML='<i class="fa-solid fa-copy"></i> Copiar';

    copiar.onclick=async()=>{
        try{
            await navigator.clipboard.writeText(textoOriginal);
            copiar.innerHTML='<i class="fa-solid fa-check"></i> Copiado';
            setTimeout(()=>{
                copiar.innerHTML='<i class="fa-solid fa-copy"></i> Copiar';
            },1800);
        }catch(e){
            alert("Não foi possível copiar.");
        }
    };

    const gostei=document.createElement("button");
    gostei.innerHTML='<i class="fa-solid fa-thumbs-up"></i>';

    gostei.onclick=()=>{
        gostei.style.background="#22c55e";
        gostei.style.color="#fff";
    };

    const ruim=document.createElement("button");
    ruim.innerHTML='<i class="fa-solid fa-thumbs-down"></i>';

    ruim.onclick=()=>{
        ruim.style.background="#ef4444";
        ruim.style.color="#fff";
    };

    const regenerar=document.createElement("button");
    regenerar.innerHTML='<i class="fa-solid fa-rotate-right"></i> Regenerar';

    regenerar.onclick=()=>{
        const campo=document.getElementById("chatInput");
        if(!campo) return;

        const ultimaPergunta=document.querySelectorAll(".chat-balao.usuario");
        if(!ultimaPergunta.length) return;

        campo.value=ultimaPergunta[ultimaPergunta.length-1].innerText.trim();

        document.getElementById("chatForm").requestSubmit();
    };

    acoes.appendChild(copiar);
    acoes.appendChild(gostei);
    acoes.appendChild(ruim);
    acoes.appendChild(regenerar);

    blocoResposta.appendChild(acoes);

}

/* Dentro da função adicionarMensagem() do recursos.js, logo após criar
a resposta da IA, chame:

adicionarAcoesMensagem( balao.querySelector(“.chat-texto”) || balao,
texto );

*/
