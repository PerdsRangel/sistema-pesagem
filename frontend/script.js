const API_URL = "http://127.0.0.1:5000";


document.addEventListener("DOMContentLoaded", () => {

    const form =
        document.getElementById("pesagemForm");

    const clienteInput =
        document.getElementById("cliente");

    const transportadoraInput =
        document.getElementById("transportadora");

    const placaInput =
        document.getElementById("placa");

    const telefoneInput =
        document.getElementById("telefone");

    const descricaoInput =
        document.getElementById("descricao");

    const quantidadeInput =
        document.getElementById("quantidade");

    const valorProdutoInput =
        document.getElementById("valorProduto");

    const totalItensInput =
        document.getElementById("totalItens");

    const quantidadeTotalItensInput =
        document.getElementById("quantidadeTotalItens");

    const valorTotalInput =
        document.getElementById("valorTotal");

    const descontoInput =
        document.getElementById("desconto");

    const pagamentoInput =
        document.getElementById("pagamento");

    const valorPagarInput =
        document.getElementById("valorPagar");

    const taraInput =
        document.getElementById("tara");

    const pesoBrutoInput =
        document.getElementById("pesoBruto");

    const pesoLiquidoInput =
        document.getElementById("pesoLiquido");

    const nfeInput =
        document.getElementById("nfe");

    const btnLimpar =
        document.getElementById("btnLimpar");

    const btnImprimir =
        document.getElementById("btnImprimir");

    const btnSalvar =
        document.getElementById("btnSalvar");

    const mensagem =
        document.getElementById("mensagem");

    const tabela =
        document.getElementById("tabelaPesagens");


    // =========================================
    // CADASTRO DE CLIENTE
    // =========================================

    const btnNovoCliente =
        document.getElementById("btnNovoCliente");

    const formNovoCliente =
        document.getElementById("formNovoCliente");

    const btnCancelarCliente =
        document.getElementById("btnCancelarCliente");

    const btnCadastrarCliente =
        document.getElementById("btnCadastrarCliente");

    const novoClienteNome =
        document.getElementById("novoClienteNome");

    const novoClienteTransportadora =
        document.getElementById("novoClienteTransportadora");

    const novoClientePlaca =
        document.getElementById("novoClientePlaca");

    const novoClienteTelefone =
        document.getElementById("novoClienteTelefone");


    // =========================================
    // PESAGEM SELECIONADA
    // =========================================

    let pesagemSelecionada = null;


    // =========================================
    // PROTEÇÃO CONTRA SUBMIT DO FORM
    // =========================================

    form.addEventListener("submit", (event) => {

        event.preventDefault();

    });


    // =========================================
    // MENSAGEM
    // =========================================

    function mostrarMensagem(texto) {

        mensagem.textContent = texto;

    }


    // =========================================
    // ABRIR CADASTRO DE CLIENTE
    // =========================================

    btnNovoCliente.addEventListener(
        "click",
        () => {

            formNovoCliente.style.display = "block";

            novoClienteNome.focus();

        }
    );


    // =========================================
    // CANCELAR CADASTRO DE CLIENTE
    // =========================================

    btnCancelarCliente.addEventListener(
        "click",
        () => {

            formNovoCliente.style.display = "none";

            novoClienteNome.value = "";
            novoClienteTransportadora.value = "";
            novoClientePlaca.value = "";
            novoClienteTelefone.value = "";

        }
    );


    // =========================================
    // CARREGAR CLIENTES
    // =========================================

    async function carregarClientes() {

        try {

            const resposta =
                await fetch(
                    `${API_URL}/api/clientes`
                );


            if (!resposta.ok) {

                throw new Error(
                    "Erro ao buscar clientes."
                );

            }


            const clientes =
                await resposta.json();


            clienteInput.innerHTML = `
                <option value="">
                    Selecione um cliente
                </option>
            `;


            clientes.forEach((cliente) => {

                const option =
                    document.createElement("option");


                option.value =
                    cliente.id;


                option.textContent =
                    cliente.nome;


                option.dataset.nome =
                    cliente.nome;


                option.dataset.transportadora =
                    cliente.transportadora || "";


                option.dataset.placa =
                    cliente.placa || "";


                option.dataset.telefone =
                    cliente.telefone || "";


                clienteInput.appendChild(option);

            });


        } catch (erro) {

            console.error(
                "Erro ao carregar clientes:",
                erro
            );


            mostrarMensagem(
                "❌ Não foi possível carregar os clientes."
            );

        }

    }


    // =========================================
    // CADASTRAR CLIENTE
    // =========================================

    btnCadastrarCliente.addEventListener(
        "click",
        async () => {

            const nome =
                novoClienteNome.value.trim();

            const transportadora =
                novoClienteTransportadora.value.trim();

            const placa =
                novoClientePlaca.value.trim();

            const telefone =
                novoClienteTelefone.value.trim();


            // -----------------------------
            // VALIDAÇÃO
            // -----------------------------

            if (!nome) {

                mostrarMensagem(
                    "❌ Informe o nome do cliente."
                );

                novoClienteNome.focus();

                return;

            }


            if (!placa) {

                mostrarMensagem(
                    "❌ Informe a placa do caminhão."
                );

                novoClientePlaca.focus();

                return;

            }


            // -----------------------------
            // ENVIA PARA O BACKEND
            // -----------------------------

            try {

                const resposta =
                    await fetch(
                        `${API_URL}/api/clientes`,
                        {

                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body: JSON.stringify({

                                nome:
                                    nome,

                                transportadora:
                                    transportadora,

                                placa:
                                    placa.toUpperCase(),

                                telefone:
                                    telefone

                            })

                        }
                    );


                const resultado =
                    await resposta.json();


                console.log(
                    "RESPOSTA AO CADASTRAR CLIENTE:",
                    resultado
                );


                // -----------------------------
                // ERRO
                // -----------------------------

                if (!resposta.ok) {

                    mostrarMensagem(
                        `❌ ${
                            resultado.erro ||
                            "Erro ao cadastrar cliente."
                        }`
                    );

                    return;

                }


                // -----------------------------
                // SUCESSO
                // -----------------------------

                mostrarMensagem(
                    `✅ Cliente "${resultado.cliente.nome}" cadastrado com sucesso!`
                );


                // Fecha formulário

                formNovoCliente.style.display =
                    "none";


                // Limpa formulário

                novoClienteNome.value = "";
                novoClienteTransportadora.value = "";
                novoClientePlaca.value = "";
                novoClienteTelefone.value = "";


                // Recarrega clientes

                await carregarClientes();


                // Seleciona automaticamente
                // o cliente recém-cadastrado

                clienteInput.value =
                    resultado.cliente.id;


                // Atualiza transportadora,
                // placa e telefone

                clienteInput.dispatchEvent(
                    new Event("change")
                );


            } catch (erro) {

                console.error(
                    "Erro ao cadastrar cliente:",
                    erro
                );


                mostrarMensagem(
                    "❌ Não foi possível conectar ao servidor."
                );

            }

        }
    );


    // =========================================
    // SELECIONAR CLIENTE
    // =========================================

    clienteInput.addEventListener(
        "change",
        () => {

            const option =
                clienteInput.options[
                    clienteInput.selectedIndex
                ];


            if (
                !option ||
                !option.value
            ) {

                transportadoraInput.value = "";
                placaInput.value = "";
                telefoneInput.value = "";

                return;

            }


            transportadoraInput.value =
                option.dataset.transportadora || "";


            placaInput.value =
                option.dataset.placa || "";


            telefoneInput.value =
                option.dataset.telefone || "";

        }
    );


    // =========================================
    // CALCULAR PESO LÍQUIDO
    // =========================================

    function calcularPesoLiquido() {

        const tara =
            parseFloat(taraInput.value) || 0;


        const pesoBruto =
            parseFloat(pesoBrutoInput.value) || 0;


        const pesoLiquido =
            pesoBruto - tara;


        pesoLiquidoInput.value =
            pesoLiquido.toFixed(3);

    }


    taraInput.addEventListener(
        "input",
        calcularPesoLiquido
    );


    pesoBrutoInput.addEventListener(
        "input",
        calcularPesoLiquido
    );


    // =========================================
    // SALVAR PESAGEM
    // =========================================

    btnSalvar.addEventListener(
        "click",
        async () => {

            console.log("SALVAR FOI CHAMADO");


            const clienteSelecionado =
                clienteInput.options[
                    clienteInput.selectedIndex
                ];


            if (
                !clienteSelecionado ||
                !clienteSelecionado.value
            ) {

                mostrarMensagem(
                    "❌ Selecione um cliente."
                );

                return;

            }


            // -----------------------------
            // PESOS
            // -----------------------------

            const tara =
                parseFloat(taraInput.value);


            const pesoBruto =
                parseFloat(pesoBrutoInput.value);


            if (
                isNaN(tara) ||
                isNaN(pesoBruto)
            ) {

                mostrarMensagem(
                    "❌ Informe a tara e o peso bruto."
                );

                return;

            }


            if (pesoBruto < tara) {

                mostrarMensagem(
                    "❌ O peso bruto não pode ser menor que a tara."
                );

                return;

            }


            // -----------------------------
            // DADOS
            // -----------------------------

            const dados = {

                cliente:
                    clienteSelecionado.dataset.nome,

                transportadora:
                    transportadoraInput.value,

                placa:
                    placaInput.value,

                telefone:
                    telefoneInput.value,


                descricao:
                    descricaoInput.value,

                quantidade:
                    quantidadeInput.value,

                valor_produto:
                    parseFloat(
                        valorProdutoInput.value
                    ) || 0,

                total_itens:
                    parseFloat(
                        totalItensInput.value
                    ) || 0,

                quantidade_total_itens:
                    parseFloat(
                        quantidadeTotalItensInput.value
                    ) || 0,

                valor_total:
                    parseFloat(
                        valorTotalInput.value
                    ) || 0,

                desconto:
                    parseFloat(
                        descontoInput.value
                    ) || 0,

                pagamento:
                    pagamentoInput.value,

                valor_pagar:
                    parseFloat(
                        valorPagarInput.value
                    ) || 0,


                tara:
                    tara,

                peso_bruto:
                    pesoBruto,


                nfe:
                    nfeInput.value

            };


            // =================================
            // ENVIA PARA O BACKEND
            // =================================

            try {

                const resposta =
                    await fetch(
                        `${API_URL}/api/pesagens`,
                        {

                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body:
                                JSON.stringify(dados)

                        }
                    );


                const resultado =
                    await resposta.json();


                console.log(
                    "RESPOSTA AO SALVAR:",
                    resultado
                );


                if (!resposta.ok) {

                    mostrarMensagem(
                        `❌ ${
                            resultado.erro ||
                            "Erro ao salvar a pesagem."
                        }`
                    );

                    return;

                }


                // Guarda a pesagem recém-criada

                pesagemSelecionada =
                    resultado.pesagem;


                mostrarMensagem(
                    `✅ Pesagem salva! Ticket Nº ${
                        resultado.pesagem.ticket
                    }`
                );


                // Atualiza o histórico

                await carregarPesagens();


            } catch (erro) {

                console.error(erro);


                mostrarMensagem(
                    "❌ Não foi possível conectar ao servidor."
                );

            }

        }
    );


    // =========================================
    // LIMPAR
    // =========================================

    btnLimpar.addEventListener(
        "click",
        () => {

            form.reset();


            transportadoraInput.value = "";
            placaInput.value = "";
            telefoneInput.value = "";


            pesoLiquidoInput.value =
                "0.000";


            descontoInput.value =
                "0";


            pesagemSelecionada =
                null;


            mensagem.textContent = "";

        }
    );


    // =========================================
    // IMPRIMIR
    // =========================================

    btnImprimir.addEventListener(
        "click",
        async () => {

            if (!pesagemSelecionada) {

                mostrarMensagem(
                    "⚠️ Selecione uma pesagem no histórico antes de imprimir."
                );

                return;

            }


            mostrarMensagem(
                `🖨️ Enviando ticket Nº ${
                    pesagemSelecionada.ticket
                } para a Elgin i9...`
            );


            try {

                const resposta =
                    await fetch(
                        `${API_URL}/api/pesagens/${pesagemSelecionada.id}/imprimir`,
                        {
                            method: "POST"
                        }
                    );


                const resultado =
                    await resposta.json();


                if (!resposta.ok) {

                    mostrarMensagem(
                        `❌ ${
                            resultado.detalhes ||
                            resultado.erro ||
                            "Erro ao imprimir."
                        }`
                    );

                    return;

                }


                mostrarMensagem(
                    `✅ Ticket Nº ${
                        pesagemSelecionada.ticket
                    } enviado para a Elgin i9!`
                );


            } catch (erro) {

                console.error(erro);


                mostrarMensagem(
                    "❌ Não foi possível conectar ao servidor."
                );

            }

        }
    );


    // =========================================
    // CARREGAR HISTÓRICO
    // =========================================

    async function carregarPesagens() {

        try {

            const resposta =
                await fetch(
                    `${API_URL}/api/pesagens`
                );


            const pesagens =
                await resposta.json();


            tabela.innerHTML = "";


            if (pesagens.length === 0) {

                tabela.innerHTML = `
                    <tr>
                        <td colspan="8">
                            Nenhuma pesagem cadastrada.
                        </td>
                    </tr>
                `;

                return;

            }


            pesagens.forEach((pesagem) => {

                tabela.innerHTML += `

                    <tr>

                        <td>
                            ${pesagem.ticket}
                        </td>

                        <td>
                            ${pesagem.cliente}
                        </td>

                        <td>
                            ${pesagem.placa}
                        </td>

                        <td>
                            ${Number(
                                pesagem.tara
                            ).toFixed(3)}
                        </td>

                        <td>
                            ${Number(
                                pesagem.peso_bruto
                            ).toFixed(3)}
                        </td>

                        <td>
                            ${Number(
                                pesagem.peso_liquido
                            ).toFixed(3)}
                        </td>

                        <td>
                            ${pesagem.data}
                        </td>

                        <td>
                            <button
                                type="button"
                                class="btn-selecionar"
                                data-id="${pesagem.id}"
                            >
                                Selecionar
                            </button>
                                                
                            <button
                                type="button"
                                class="btn-excluir-pesagem"
                                data-id="${pesagem.id}"
                            >
                                🗑️ Excluir
                            </button>
                        </td>

                    </tr>

                `;

            });


        } catch (erro) {

            console.error(
                "Erro ao carregar pesagens:",
                erro
            );

        }

    }


    // =========================================
    // CLICAR EM "SELECIONAR"
    // =========================================

    tabela.addEventListener("click", async (event) => {

    const botaoSelecionar =
        event.target.closest(".btn-selecionar");

    const botaoExcluir =
        event.target.closest(".btn-excluir-pesagem");


    // Selecionar pesagem
    if (botaoSelecionar) {

        const id =
            botaoSelecionar.dataset.id;

        await selecionarPesagem(id);

        return;
    }


    // Excluir pesagem
    if (botaoExcluir) {

        const id =
            botaoExcluir.dataset.id;

        await excluirPesagem(id);

    }

    });


    // =========================================
    // SELECIONAR PESAGEM
    // =========================================

    async function selecionarPesagem(id) {

        try {

            mostrarMensagem(
                "🔄 Carregando pesagem..."
            );


            const resposta =
                await fetch(
                    `${API_URL}/api/pesagens/${id}`
                );


            if (!resposta.ok) {

                throw new Error(
                    "Erro ao buscar pesagem."
                );

            }


            const resultado =
                await resposta.json();


            const pesagem =
                resultado.pesagem ||
                resultado;


            // Guarda a pesagem selecionada

            pesagemSelecionada =
                pesagem;


            // =================================
            // CLIENTE
            // =================================

            let clienteEncontrado =
                false;


            for (
                const option of clienteInput.options
            ) {

                if (
                    option.dataset.nome ===
                    pesagem.cliente
                ) {

                    clienteInput.value =
                        option.value;

                    clienteEncontrado =
                        true;

                    break;

                }

            }


            if (clienteEncontrado) {

                clienteInput.dispatchEvent(
                    new Event("change")
                );

            } else {

                transportadoraInput.value =
                    pesagem.transportadora || "";

                placaInput.value =
                    pesagem.placa || "";

                telefoneInput.value =
                    pesagem.telefone || "";

            }


            // =================================
            // PRODUTO
            // =================================

            descricaoInput.value =
                pesagem.descricao || "";


            quantidadeInput.value =
                pesagem.quantidade || "";


            valorProdutoInput.value =
                pesagem.valor_produto ?? 0;


            totalItensInput.value =
                pesagem.total_itens ?? 0;


            quantidadeTotalItensInput.value =
                pesagem.quantidade_total_itens ?? 0;


            valorTotalInput.value =
                pesagem.valor_total ?? 0;


            descontoInput.value =
                pesagem.desconto ?? 0;


            pagamentoInput.value =
                pesagem.pagamento || "";


            valorPagarInput.value =
                pesagem.valor_pagar ?? 0;


            // =================================
            // PESAGEM
            // =================================

            taraInput.value =
                pesagem.tara ?? 0;


            pesoBrutoInput.value =
                pesagem.peso_bruto ?? 0;


            pesoLiquidoInput.value =
                pesagem.peso_liquido ?? 0;


            // =================================
            // NF-E
            // =================================

            nfeInput.value =
                pesagem.nfe || "";


            mostrarMensagem(
                `✅ Pesagem Nº ${
                    pesagem.ticket
                } selecionada.`
            );


            // Volta para o formulário

            form.scrollIntoView({
                behavior: "smooth",
                block: "start"
            });


        } catch (erro) {

            console.error(
                "Erro ao selecionar pesagem:",
                erro
            );


            mostrarMensagem(
                "❌ Não foi possível carregar essa pesagem."
            );

        }

    }

    async function excluirPesagem(id) {

    const confirmou = confirm(
        "⚠️ Tem certeza que deseja excluir esta pesagem?\n\n" +
        "Essa ação não poderá ser desfeita."
    );


    if (!confirmou) {
        return;
    }


    try {

        mostrarMensagem("🗑️ Excluindo pesagem...");


        const resposta = await fetch(
            `${API_URL}/api/pesagens/${id}`,
            {
                method: "DELETE"
            }
        );


        const resultado =
            await resposta.json();


        if (!resposta.ok) {

            mostrarMensagem(
                `❌ ${
                    resultado.erro ||
                    "Erro ao excluir pesagem."
                }`
            );

            return;
        }


        // Se a pesagem excluída estava selecionada,
        // limpamos a seleção.
        if (
            pesagemSelecionada &&
            pesagemSelecionada.id == id
        ) {

            pesagemSelecionada = null;

        }


        mostrarMensagem(
            "✅ Pesagem excluída com sucesso!"
        );


        // Atualiza a tabela
        await carregarPesagens();


    } catch (erro) {

        console.error(
            "Erro ao excluir pesagem:",
            erro
        );


        mostrarMensagem(
            "❌ Não foi possível conectar ao servidor."
        );

    }

}

    // =========================================
    // INICIALIZAÇÃO
    // =========================================

    carregarClientes();

    carregarPesagens();

});