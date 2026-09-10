from database import db
from datetime import datetime


class Pesagem(db.Model):
    __tablename__ = "pesagens"

    id = db.Column(db.Integer, primary_key=True)

    ticket = db.Column(db.Integer, unique=True, nullable=False)

    # ==========================================
    # DADOS DO CLIENTE
    # ==========================================

    cliente = db.Column(db.String(150), nullable=False)
    transportadora = db.Column(db.String(150), nullable=True)
    placa = db.Column(db.String(20), nullable=False)
    telefone = db.Column(db.String(30), nullable=True)

    # ==========================================
    # DADOS DO PRODUTO / VENDA
    # ==========================================

    descricao = db.Column(db.String(200), nullable=True)

    quantidade = db.Column(db.String(50), nullable=True)

    valor_produto = db.Column(db.Float, nullable=True)

    total_itens = db.Column(db.Float, nullable=True)

    quantidade_total_itens = db.Column(db.Float, nullable=True)

    valor_total = db.Column(db.Float, nullable=True)

    desconto = db.Column(db.Float, nullable=True)

    pagamento = db.Column(db.String(50), nullable=True)

    valor_pagar = db.Column(db.Float, nullable=True)

    # ==========================================
    # PESAGEM
    # ==========================================

    tara = db.Column(db.Float, nullable=False)

    peso_bruto = db.Column(db.Float, nullable=False)

    peso_liquido = db.Column(db.Float, nullable=False)

    # ==========================================
    # NOTA FISCAL
    # ==========================================

    nfe = db.Column(db.String(50), nullable=True)

    # ==========================================
    # DATA
    # ==========================================

    data = db.Column(
        db.DateTime,
        default=datetime.now
    )

    # ==========================================
    # CONVERTER PARA JSON
    # ==========================================

    def to_dict(self):
        return {
            "id": self.id,
            "ticket": self.ticket,

            # Cliente
            "cliente": self.cliente,
            "transportadora": self.transportadora,
            "placa": self.placa,
            "telefone": self.telefone,

            # Produto / venda
            "descricao": self.descricao,
            "quantidade": self.quantidade,
            "valor_produto": self.valor_produto,
            "total_itens": self.total_itens,
            "quantidade_total_itens": self.quantidade_total_itens,
            "valor_total": self.valor_total,
            "desconto": self.desconto,
            "pagamento": self.pagamento,
            "valor_pagar": self.valor_pagar,

            # Pesagem
            "tara": self.tara,
            "peso_bruto": self.peso_bruto,
            "peso_liquido": self.peso_liquido,

            # NF-e
            "nfe": self.nfe,

            # Data
            "data": self.data.strftime("%d/%m/%Y %H:%M")
        }