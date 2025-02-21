document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");
    const horasInput = document.querySelector("input[name='horas']");
    const tipoSelect = document.querySelector("select[name='tipo']");
    const categoriaSelect = document.querySelector("select[name='categoria']");
    const mensagensContainer = document.createElement("div");
    const aproveitamentoInfo = document.getElementById("aproveitamento-info");

    // Adicionar container de mensagens no topo do formulário
    form.insertAdjacentElement("beforebegin", mensagensContainer);

    // Configurações de limite por categoria
    const limites = {
        "Extensão": 90,
        "Ensino": 90,
        "Pesquisa": 90
    };

    // Atualiza o aproveitamento com base na seleção de tipo
    function atualizarHorasAproveitadas() {
        const horas = parseFloat(horasInput.value) || 0;
        const aproveitamento = parseFloat(tipoSelect.options[tipoSelect.selectedIndex]?.dataset.aproveitamento || 100);

        const horasAproveitadas = ((horas * aproveitamento) / 100).toFixed(2);
        aproveitamentoInfo.textContent = `Horas aproveitadas: ${horasAproveitadas}h (Aproveitamento: ${aproveitamento}%)`;

        return { horasAproveitadas: parseFloat(horasAproveitadas), aproveitamento };
    }

    // Exibe mensagens de erro ou sucesso
    function exibirMensagem(mensagem, tipo = "error") {
        mensagensContainer.innerHTML = ""; // Limpa mensagens anteriores
        const alerta = document.createElement("div");
        alerta.className = `alert alert-${tipo === "error" ? "danger" : "success"} text-center`;
        alerta.textContent = mensagem;
        mensagensContainer.appendChild(alerta);

        // Remove mensagem após 3 segundos
        setTimeout(() => mensagensContainer.innerHTML = "", 3000);
    }

    // Reseta o estilo do campo
    function resetarEstiloInput(input) {
        input.classList.remove("is-invalid", "is-valid");
    }

    // Valida as horas informadas
    function validarHoras(horasAproveitadas, categoria) {
        const limite = limites[categoria] || 90;

        if (horasAproveitadas <= 0) {
            return { valido: false, mensagem: "As horas aproveitadas devem ser maiores que zero!" };
        }
        if (horasAproveitadas > limite) {
            return { valido: false, mensagem: `O limite de horas aproveitadas para ${categoria} é ${limite} horas.` };
        }

        return { valido: true };
    }

    //  envio do formulário
    form.addEventListener("submit", (e) => {
        const { horasAproveitadas } = atualizarHorasAproveitadas();
        const categoria = categoriaSelect.value;

        // Resetar estilos
        resetarEstiloInput(horasInput);

        // Realiza validação
        const { valido, mensagem } = validarHoras(horasAproveitadas, categoria);

        if (!valido) {
            exibirMensagem(mensagem, "error");
            horasInput.classList.add("is-invalid");
            e.preventDefault();
            return;
        }

        // Feedback visual
        exibirMensagem("Atividade adicionada com sucesso!", "success");
        horasInput.classList.add("is-valid");
    });

    // atualizar horas aproveitadas em tempo real
    tipoSelect.addEventListener("change", atualizarHorasAproveitadas);
    horasInput.addEventListener("input", atualizarHorasAproveitadas);

    // Atualização dinâmica dos totais
    async function atualizarRelatorio() {
        try {
            const response = await fetch("/api/totais");

            if (!response.ok) {
                throw new Error("Erro ao buscar os dados do relatório.");
            }

            const data = await response.json();

            document.getElementById("total-extensao").textContent = `${data.total_extensao || 0} horas`;
            document.getElementById("total-ensino").textContent = `${data.total_ensino || 0} horas`;
            document.getElementById("total-pesquisa").textContent = `${data.total_pesquisa || 0} horas`;
        } catch (error) {
            console.error("Erro ao atualizar o relatório:", error);
            exibirMensagem("Erro ao carregar o relatório. Tente novamente mais tarde.", "error");
        }
    }

    // Verifica se os elementos de relatório existem e atualiza
    if (document.getElementById("total-extensao")) {
        atualizarRelatorio();
    }
});
