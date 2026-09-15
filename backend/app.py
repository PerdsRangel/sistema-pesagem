from flask import Flask, request, jsonify, send_from_directory
from datetime import datetime
from flask_cors import CORS
import os
import webbrowser
import threading
import sys

from database import db
from models.cliente import Cliente
from models.pesagem import Pesagem

from services.impressao_service import (
    gerar_ticket,
    gerar_ticket_escpos,
    imprimir_ticket
)


app = Flask(__name__)

if getattr(sys, "frozen", False):
    FRONTEND_DIR = os.path.join(sys._MEIPASS, "frontend")
else:
    FRONTEND_DIR = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "frontend")
    )

CORS(app)

PASTA_DADOS = os.path.join(
    os.environ.get("PUBLIC", r"C:\Users\Public"),
    "SistemaPesagem"
)

os.makedirs(PASTA_DADOS, exist_ok=True)

BANCO = os.path.join(PASTA_DADOS, "pesagem.db")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + BANCO
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


# =========================================
# BANCO DE DADOS
# =========================================

with app.app_context():

    db.create_all()

    # Atualiza a tabela pesagens caso ela já exista
    # e ainda não possua as novas colunas.

    colunas_novas = {
        "descricao": "VARCHAR(200)",
        "quantidade": "VARCHAR(50)",
        "valor_produto": "FLOAT",
        "total_itens": "FLOAT",
        "quantidade_total_itens": "FLOAT",
        "valor_total": "FLOAT",
        "desconto": "FLOAT",
        "pagamento": "VARCHAR(50)",
        "valor_pagar": "FLOAT",
        "nfe": "VARCHAR(50)"
    }

    colunas_existentes = db.session.execute(
        db.text("PRAGMA table_info(pesagens)")
    ).fetchall()

    nomes_colunas = {
        coluna[1]
        for coluna in colunas_existentes
    }

    for nome, tipo in colunas_novas.items():

        if nome not in nomes_colunas:

            db.session.execute(
                db.text(
                    f"ALTER TABLE pesagens "
                    f"ADD COLUMN {nome} {tipo}"
                )
            )

    db.session.commit()


# =========================================
# HOME
# =========================================

@app.route("/")
def home():
    return send_from_directory(FRONTEND_DIR, "index.html")

@app.route("/<path:filename>")
def frontend_files(filename):
    return send_from_directory(FRONTEND_DIR, filename)


# =========================================
# CLIENTES
# =========================================

@app.route("/api/clientes", methods=["GET"])
def listar_clientes():

    clientes = Cliente.query.order_by(
        Cliente.nome.asc()
    ).all()

    return jsonify([
        cliente.to_dict()
        for cliente in clientes
    ])


@app.route("/api/clientes", methods=["POST"])
def criar_cliente():

    dados = request.get_json()

    nome = dados.get("nome")
    transportadora = dados.get("transportadora")
    placa = dados.get("placa")
    telefone = dados.get("telefone")

    if not nome:

        return jsonify({
            "erro": "O nome do cliente é obrigatório."
        }), 400

    if not placa:

        return jsonify({
            "erro": "A placa é obrigatória."
        }), 400

    novo_cliente = Cliente(
        nome=nome,
        transportadora=transportadora,
        placa=placa.upper(),
        telefone=telefone
    )

    db.session.add(novo_cliente)
    db.session.commit()

    return jsonify({
        "mensagem": "Cliente cadastrado com sucesso!",
        "cliente": novo_cliente.to_dict()
    }), 201

@app.route("/api/clientes/<int:id>", methods=["PUT"])
def editar_cliente(id):
    cliente = Cliente.query.get_or_404(id)

    dados = request.get_json()

    nome = dados.get("nome")
    transportadora = dados.get("transportadora")
    placa = dados.get("placa")
    telefone = dados.get("telefone")

    if not nome:
        return jsonify({
            "erro": "O nome do cliente é obrigatório."
        }), 400

    if not placa:
        return jsonify({
            "erro": "A placa é obrigatória."
        }), 400

    cliente.nome = nome
    cliente.transportadora = transportadora
    cliente.placa = placa.upper()
    cliente.telefone = telefone

    db.session.commit()

    return jsonify({
        "mensagem": "Cliente atualizado com sucesso!",
        "cliente": cliente.to_dict()
    }), 200


@app.route("/api/clientes/<int:id>", methods=["DELETE"])
def excluir_cliente(id):
    cliente = Cliente.query.get_or_404(id)

    db.session.delete(cliente)
    db.session.commit()

    return jsonify({
        "mensagem": "Cliente excluído com sucesso!"
    }), 200

# =========================================
# PESAGENS
# =========================================

@app.route("/api/pesagens", methods=["POST"])
def criar_pesagem():

    dados = request.get_json()

    # ======================================
    # TICKET E HORÁRIO MANUAIS
    # ======================================

    ticket = dados.get("ticket")
    horario = dados.get("horario")

    # Validação do ticket
    try:
        ticket = int(ticket)
    except (TypeError, ValueError):
        return jsonify({
            "erro": "Informe um número de ticket válido."
        }), 400

    if ticket <= 0:
        return jsonify({
            "erro": "O número do ticket deve ser maior que zero."
        }), 400


    # Validação do horário
    if not horario:
        return jsonify({
            "erro": "Informe o horário da pesagem."
        }), 400

    try:
        hora_manual = datetime.strptime(
            horario,
            "%H:%M"
        ).time()

    except ValueError:
        return jsonify({
            "erro": "Informe um horário válido."
        }), 400


    data_pesagem = datetime.combine(
        datetime.now().date(),
        hora_manual
    )

    # ======================================
    # DADOS DO CLIENTE
    # ======================================

    cliente = dados.get("cliente")
    transportadora = dados.get("transportadora")
    placa = dados.get("placa")
    telefone = dados.get("telefone")

    # ======================================
    # DADOS DO PRODUTO
    # ======================================

    descricao = dados.get("descricao")

    quantidade = dados.get("quantidade")

    valor_produto = float(
        dados.get("valor_produto", 0)
    )

    total_itens = float(
        dados.get("total_itens", 0)
    )

    quantidade_total_itens = float(
        dados.get("quantidade_total_itens", 0)
    )

    valor_total = float(
        dados.get("valor_total", 0)
    )

    desconto = float(
        dados.get("desconto", 0)
    )

    pagamento = dados.get("pagamento")

    valor_pagar = float(
        dados.get("valor_pagar", 0)
    )

    # ======================================
    # PESAGEM
    # ======================================

    tara = float(
        dados.get("tara", 0)
    )

    peso_bruto = float(
        dados.get("peso_bruto", 0)
    )

    # Calcula automaticamente
    peso_liquido = peso_bruto - tara

    # ======================================
    # NF-E
    # ======================================

    nfe = dados.get("nfe")

    # ======================================
    # VALIDAÇÕES
    # ======================================

    if not cliente:

        return jsonify({
            "erro": "O cliente é obrigatório."
        }), 400

    if not placa:

        return jsonify({
            "erro": "A placa é obrigatória."
        }), 400

    if peso_bruto < tara:

        return jsonify({
            "erro": "O peso bruto não pode ser menor que a tara."
        }), 400

    # ======================================
    # VERIFICAR TICKET
    # ======================================

    ticket_existente = Pesagem.query.filter_by(
        ticket=ticket
    ).first()

    if ticket_existente:

        return jsonify({
            "erro": f"O ticket Nº {ticket} já existe."
        }), 400

    # ======================================
    # CRIA PESAGEM
    # ======================================

    nova_pesagem = Pesagem(

        ticket=ticket,

        # Cliente
        cliente=cliente,
        transportadora=transportadora,
        placa=placa.upper(),
        telefone=telefone,

        # Produto
        descricao=descricao,
        quantidade=quantidade,
        valor_produto=valor_produto,
        total_itens=total_itens,
        quantidade_total_itens=quantidade_total_itens,
        valor_total=valor_total,
        desconto=desconto,
        pagamento=pagamento,
        valor_pagar=valor_pagar,

        # Pesagem
        tara=tara,
        peso_bruto=peso_bruto,
        peso_liquido=peso_liquido,
        data=data_pesagem,

        # NF-e
        nfe=nfe
    )

    db.session.add(nova_pesagem)

    db.session.commit()

    return jsonify({

        "mensagem":
            "Pesagem salva com sucesso!",

        "pesagem":
            nova_pesagem.to_dict()

    }), 201

@app.route("/api/pesagens/<int:id>", methods=["DELETE"])
def excluir_pesagem(id):
    pesagem = Pesagem.query.get_or_404(id)

    db.session.delete(pesagem)
    db.session.commit()

    return jsonify({
        "mensagem": "Pesagem excluída com sucesso!"
    }), 200

# =========================================
# LISTAR PESAGENS
# =========================================

@app.route("/api/pesagens", methods=["GET"])
def listar_pesagens():

    pesagens = Pesagem.query.order_by(
        Pesagem.id.desc()
    ).all()

    return jsonify([

        pesagem.to_dict()

        for pesagem in pesagens

    ])

# =========================================
# BUSCAR UMA PESAGEM
# =========================================

@app.route("/api/pesagens/<int:id>", methods=["GET"])
def buscar_pesagem(id):

    pesagem = Pesagem.query.get_or_404(id)

    return jsonify({
        "pesagem": pesagem.to_dict()
    })


# =========================================
# TICKET - VISUALIZAÇÃO
# =========================================

@app.route(
    "/api/pesagens/<int:id>/ticket",
    methods=["GET"]
)
def visualizar_ticket(id):

    pesagem = Pesagem.query.get_or_404(id)

    ticket = gerar_ticket(pesagem)

    html = """

    <html>

        <head>

            <meta charset="UTF-8">

            <title>Ticket</title>

            <style>

                body {

                    background-color: #eeeeee;

                    display: flex;

                    justify-content: center;

                    padding: 30px;

                }

                pre {

                    background-color: white;

                    padding: 20px;

                    font-family:
                        "Courier New",
                        monospace;

                    font-size: 16px;

                    box-shadow:
                        0 0 10px
                        rgba(0,0,0,0.2);

                }

            </style>

        </head>

        <body>

            <pre>TICKET_AQUI</pre>

        </body>

    </html>

    """

    html = html.replace(
        "TICKET_AQUI",
        ticket
    )

    return html


# =========================================
# TICKET - ESC/POS
# =========================================

@app.route(
    "/api/pesagens/<int:id>/ticket/escpos",
    methods=["GET"]
)
def gerar_ticket_escpos_rota(id):

    pesagem = Pesagem.query.get_or_404(id)

    comandos = gerar_ticket_escpos(
        pesagem
    )

    return jsonify({

        "mensagem":
            "Comandos ESC/POS gerados com sucesso!",

        "tamanho":
            len(comandos),

        "dados":
            list(comandos)

    })


# =========================================
# IMPRESSÃO - ELGIN i9
# =========================================

@app.route(
    "/api/pesagens/<int:id>/imprimir",
    methods=["POST"]
)
def imprimir_pesagem(id):

    pesagem = Pesagem.query.get_or_404(id)

    try:

        imprimir_ticket(pesagem)

        return jsonify({

            "mensagem":
                "Ticket enviado para a impressora!",

            "pesagem":
                pesagem.to_dict()

        })

    except Exception as e:

        return jsonify({

            "erro":
                "Não foi possível imprimir o ticket.",

            "detalhes":
                str(e)

        }), 500


# =========================================
# INICIAR SERVIDOR
# =========================================

def abrir_navegador():
    webbrowser.open("http://127.0.0.1:5000")


if __name__ == "__main__":

    threading.Timer(1.5, abrir_navegador).start()

    app.run(
        debug=False,
        host="127.0.0.1",
        port=5000
    )