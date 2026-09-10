const API_URL = "http://127.0.0.1:5000";


document.addEventListener("DOMContentLoaded", () => {

    const formCliente = document.getElementById("formCliente");

    const tituloFormulario =
        document.getElementById("tituloFormulario");

    const nomeInput =
        document.getElementById("nome");

    const transportadoraInput =
        document.getElementById("transportadora");

    const placaInput =
        document.getElementById("placa");

    const telefoneInput =
        document.getElementById("telefone");

    const btnNovoCliente =
        document.getElementById("btnNovoCliente");

    const btnCancelar =
        document.getElementById("btnCancelar");

    const btnSalvar =
        document.getElementById("btnSalvar");

    const pesquisaInput =
        document.getElementById("pesquisa");

    const tabela =
        document.getElementById("tabelaClientes");

    const mensagem =
        document.getElementById("mensagem");


    let clientes = [];

    let clienteEditando = null;


    // =====================================================
    // MENSAGEM
    // =====================================================

    function mostrarMensagem(texto) {

        mensagem.textContent = texto;

    }


    // =====================================================
    // ABRIR FORMULÁRIO PARA NOVO CLIENTE
    // =====================================================

    btnNovoCliente.addEventListener("click", () => {

        clienteEditando = null;

        tituloFormulario.textContent =
            "➕ Novo Cliente";

        btnSalvar.textContent =
            "💾 Salvar Cliente";

        limparFormulario();

        formCliente.style.display = "block";

        nomeInput.focus();

    });


    // =====================================================
    // CANCELAR
    // =====================================================

    btnCancelar.addEventListener("click", () => {

        fecharFormulario();

    });


    function fecharFormulario() {

        formCliente.style.display = "none";

        clienteEditando = null;

        limparFormulario();

    }


    function limparFormulario() {

        nomeInput.value = "";
        transportadoraInput.value = "";
        placaInput.value = "";
        telefoneInput.value = "";

    }


    // =====================================================
    // CARREGAR CLIENTES
    // =====================================================

    async function carregarClientes() {

        try {

            const resposta =
                await fetch(`${API_URL}/api/clientes`);

            if (!resposta.ok) {

                throw new Error(
                    "Erro ao buscar clientes."
                );

            }

            clientes = await resposta.json();

            renderizarClientes(clientes);

        } catch (erro) {

            console.error(
                "Erro ao carregar clientes:",
                erro
            );

            tabela.innerHTML = `
                <tr>
                    <td colspan="6">
                        ❌ Não foi possível carregar os clientes.
                    </td>
                </tr>
            `;

        }

    }


    // =====================================================
    // MOSTRAR CLIENTES NA TABELA
    // =====================================================

    function renderizarClientes(lista) {

        tabela.innerHTML = "";


        if (lista.length === 0) {

            tabela.innerHTML = `
                <tr>
                    <td colspan="6">
                        Nenhum cliente encontrado.
                    </td>
                </tr>
            `;

            return;

        }


        lista.forEach((cliente) => {

            const linha =
                document.createElement("tr");


            linha.innerHTML = `

                <td>${cliente.id}</td>

                <td>${cliente.nome || ""}</td>

                <td>${cliente.transportadora || ""}</td>

                <td>${cliente.placa || ""}</td>

                <td>${cliente.telefone || ""}</td>

                <td>

                    <button
                        type="button"
                        class="btn-editar"
                        data-id="${cliente.id}"
                    >
                        ✏️ Editar
                    </button>

                    <button
                        type="button"
                        class="btn-excluir"
                        data-id="${cliente.id}"
                    >
                        🗑️ Excluir
                    </button>

                </td>

            `;


            tabela.appendChild(linha);

        });

    }


    // =====================================================
    // PESQUISA
    // =====================================================

    pesquisaInput.addEventListener("input", () => {

        const texto =
            pesquisaInput.value
                .trim()
                .toLowerCase();


        if (!texto) {

            renderizarClientes(clientes);

            return;

        }


        const resultados =
            clientes.filter((cliente) => {

                const nome =
                    (cliente.nome || "")
                        .toLowerCase();

                const placa =
                    (cliente.placa || "")
                        .toLowerCase();

                const transportadora =
                    (cliente.transportadora || "")
                        .toLowerCase();


                return (
                    nome.includes(texto) ||
                    placa.includes(texto) ||
                    transportadora.includes(texto)
                );

            });


        renderizarClientes(resultados);

    });


    // =====================================================
    // BOTÕES DA TABELA
    // =====================================================

    tabela.addEventListener("click", (event) => {

        const botaoEditar =
            event.target.closest(".btn-editar");

        const botaoExcluir =
            event.target.closest(".btn-excluir");


        if (botaoEditar) {

            const id =
                Number(botaoEditar.dataset.id);

            editarCliente(id);

        }


        if (botaoExcluir) {

            const id =
                Number(botaoExcluir.dataset.id);

            excluirCliente(id);

        }

    });


    // =====================================================
    // EDITAR CLIENTE
    // =====================================================

    function editarCliente(id) {

        const cliente =
            clientes.find(
                (item) => item.id === id
            );


        if (!cliente) {

            mostrarMensagem(
                "❌ Cliente não encontrado."
            );

            return;

        }


        clienteEditando = id;


        tituloFormulario.textContent =
            "✏️ Editar Cliente";


        btnSalvar.textContent =
            "💾 Atualizar Cliente";


        nomeInput.value =
            cliente.nome || "";

        transportadoraInput.value =
            cliente.transportadora || "";

        placaInput.value =
            cliente.placa || "";

        telefoneInput.value =
            cliente.telefone || "";


        formCliente.style.display =
            "block";


        nomeInput.focus();


        formCliente.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });

    }


    // =====================================================
    // SALVAR / ATUALIZAR
    // =====================================================

    btnSalvar.addEventListener("click", async () => {

        const nome =
            nomeInput.value.trim();

        const transportadora =
            transportadoraInput.value.trim();

        const placa =
            placaInput.value.trim();

        const telefone =
            telefoneInput.value.trim();


        if (!nome) {

            mostrarMensagem(
                "❌ Informe o nome do cliente."
            );

            nomeInput.focus();

            return;

        }


        if (!placa) {

            mostrarMensagem(
                "❌ Informe a placa do caminhão."
            );

            placaInput.focus();

            return;

        }


        const dados = {

            nome: nome,

            transportadora: transportadora,

            placa: placa.toUpperCase(),

            telefone: telefone

        };


        try {

            let resposta;


            // -------------------------------------------------
            // EDITAR
            // -------------------------------------------------

            if (clienteEditando !== null) {

                resposta =
                    await fetch(
                        `${API_URL}/api/clientes/${clienteEditando}`,
                        {
                            method: "PUT",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body: JSON.stringify(dados)
                        }
                    );

            }


            // -------------------------------------------------
            // NOVO CLIENTE
            // -------------------------------------------------

            else {

                resposta =
                    await fetch(
                        `${API_URL}/api/clientes`,
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body: JSON.stringify(dados)
                        }
                    );

            }


            const resultado =
                await resposta.json();


            if (!resposta.ok) {

                mostrarMensagem(
                    `❌ ${
                        resultado.erro ||
                        "Erro ao salvar cliente."
                    }`
                );

                return;

            }


            if (clienteEditando !== null) {

                mostrarMensagem(
                    "✅ Cliente atualizado com sucesso!"
                );

            } else {

                mostrarMensagem(
                    "✅ Cliente cadastrado com sucesso!"
                );

            }


            fecharFormulario();

            await carregarClientes();

        } catch (erro) {

            console.error(
                "Erro ao salvar cliente:",
                erro
            );

            mostrarMensagem(
                "❌ Não foi possível conectar ao servidor."
            );

        }

    });


    // =====================================================
    // EXCLUIR CLIENTE
    // =====================================================

    async function excluirCliente(id) {

        const cliente =
            clientes.find(
                (item) => item.id === id
            );


        if (!cliente) {

            return;

        }


        const confirmou =
            confirm(
                `Tem certeza que deseja excluir o cliente "${cliente.nome}"?`
            );


        if (!confirmou) {

            return;

        }


        try {

            const resposta =
                await fetch(
                    `${API_URL}/api/clientes/${id}`,
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
                        "Erro ao excluir cliente."
                    }`
                );

                return;

            }


            mostrarMensagem(
                "✅ Cliente excluído com sucesso!"
            );


            await carregarClientes();

        } catch (erro) {

            console.error(
                "Erro ao excluir cliente:",
                erro
            );

            mostrarMensagem(
                "❌ Não foi possível conectar ao servidor."
            );

        }

    }


    // =====================================================
    // INICIAR
    // =====================================================

    carregarClientes();

});