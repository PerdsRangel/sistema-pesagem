from database import db


class Cliente(db.Model):
    __tablename__ = "clientes"

    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(
        db.String(150),
        nullable=False
    )

    transportadora = db.Column(
        db.String(150),
        nullable=True
    )

    placa = db.Column(
        db.String(20),
        nullable=False
    )

    telefone = db.Column(
        db.String(30),
        nullable=True
    )

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "transportadora": self.transportadora,
            "placa": self.placa,
            "telefone": self.telefone
        }