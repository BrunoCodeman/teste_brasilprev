from dataclasses import dataclass, field

PERSONALIDADES = ["impulsivo", "exigente", "cauteloso", "aleatorio"]


@dataclass
class Jogador:
    """
    Jogador do banco imobiliário
    """
    personalidade: str
    saldo: float = 300
    propriedades: list = field(default_factory=list)
    posicao: int = 0

    def __str__(self):
        return f"{self.personalidade}: {self.saldo}, {len(self.propriedades)} propriedades"


@dataclass
class Propriedade:
    """
    Propriedade para compra ou aluguel
    """
    valor_compra: float
    valor_aluguel: float
    dono: Jogador = None

    def __str__(self):
        return "Dono: {self.dono}, compra: {self.valor_compra}, aluguel: {self.valor_aluguel}"
