from abc import ABC, abstractmethod
from typing import List, Optional

class Instrumento(ABC):
    """
    Classe base para todos os instrumentos
    """
    def __init__(self, marca: str, modelo: str, preco: float, num_cordas: int):
        self.marca = marca
        self.modelo = modelo
        self.preco = preco
        self.num_cordas = num_cordas

    @abstractmethod
    def info(self) -> str:
        pass

class Baixo(Instrumento):
    """
    Classe que representa um Baixo, herda de Instrumento
    """
    def __init__(self, marca: str, modelo: str, preco: float, num_cordas: int, fretless: bool):
        super().__init__(marca, modelo, preco, num_cordas)
        self.fretless = fretless

    def info(self) -> str:
        return f"Baixo {self.marca} {self.modelo}, {self.num_cordas} cordas, {'fretless' if self.fretless else 'com trastes'}"

class Guitarra(Instrumento):
    """
    Classe que representa uma Guitarra, herda de Instrumento
    """
    def __init__(self, marca: str, modelo: str, preco: float, num_cordas: int, tipo_captador: str):
        super().__init__(marca, modelo, preco, num_cordas)
        self.tipo_captador = tipo_captador

    def info(self) -> str:
        return f"Guitarra {self.marca} {self.modelo}, {self.num_cordas} cordas, captador {self.tipo_captador}"

class Violao(Instrumento):
    """
    Classe que representa um Violão, herda de Instrumento
    """
    def __init__(self, marca: str, modelo: str, preco: float, num_cordas: int, tipo_corpo: str):
        super().__init__(marca, modelo, preco, num_cordas)
        self.tipo_corpo = tipo_corpo

    def info(self) -> str:
        return f"Violão {self.marca} {self.modelo}, {self.num_cordas} cordas, corpo {self.tipo_corpo}"

class Funcionario:
    """
    Classe que representa um funcionário da empresa.
    Relação de Associação com Loja (um funcionário pode ser associado a uma loja)
    """
    def __init__(self, nome_completo: str, cpf: str, salario: float, cargo: str):
        self.nome_completo = nome_completo
        self.cpf = cpf
        self.salario = salario
        self.cargo = cargo
        self.loja_atual: Optional['Loja'] = None

    def mudar_loja(self, nova_loja: 'Loja'):
        """
        Método para remanejar o funcionário para outra loja
        """
        if self.loja_atual:
            self.loja_atual.remover_funcionario(self)
        nova_loja.adicionar_funcionario(self)
        self.loja_atual = nova_loja

class Loja:
    """
    Classe que representa uma loja da franquia.
    Relação de Composição com Instrumento (a loja é composta por instrumentos)
    Relação de Associação com Funcionario (a loja tem funcionários associados)
    """
    def __init__(self, localizacao: str):
        self.localizacao = localizacao
        self.funcionarios: List[Funcionario] = []
        self.estoque: List[Instrumento] = []
        self.loja_mais_proxima: Optional['Loja'] = None  # Relação de Agregação com outra Loja

    def adicionar_funcionario(self, funcionario: Funcionario):
        """
        Adiciona um funcionário ao quadro da loja
        """
        self.funcionarios.append(funcionario)
        funcionario.loja_atual = self

    def remover_funcionario(self, funcionario: Funcionario):
        """
        Remove um funcionário do quadro da loja
        """
        self.funcionarios.remove(funcionario)
        funcionario.loja_atual = None

    def adicionar_instrumento(self, instrumento: Instrumento):
        """
        Adiciona um instrumento ao estoque da loja
        """
        self.estoque.append(instrumento)

    def remover_instrumento(self, instrumento: Instrumento):
        """
        Remove um instrumento do estoque da loja
        """
        self.estoque.remove(instrumento)

    def consultar_instrumentos(self) -> dict:
        """
        Retorna a quantidade de instrumentos de cada tipo disponíveis na loja
        """
        instrumentos_por_tipo = {'Baixo': 0, 'Guitarra': 0, 'Violão': 0}
        for instrumento in self.estoque:
            if isinstance(instrumento, Baixo):
                instrumentos_por_tipo['Baixo'] += 1
            elif isinstance(instrumento, Guitarra):
                instrumentos_por_tipo['Guitarra'] += 1
            elif isinstance(instrumento, Violao):
                instrumentos_por_tipo['Violão'] += 1
        return instrumentos_por_tipo

    def consultar_funcionarios_por_cargo(self) -> dict:
        """
        Retorna a quantidade de funcionários por cargo na loja.
        """
        funcionarios_por_cargo = {}
        for funcionario in self.funcionarios:
            if funcionario.cargo in funcionarios_por_cargo:
                funcionarios_por_cargo[funcionario.cargo] += 1
            else:
                funcionarios_por_cargo[funcionario.cargo] = 1
        return funcionarios_por_cargo

def main():
    # Cria algumas lojas
    loja1 = Loja("São Paulo")
    loja2 = Loja("Rio de Janeiro")
    loja3 = Loja("Xique-Xique")

    # Define a loja mais próxima (Agregação)
    loja1.loja_mais_proxima = loja2
    loja2.loja_mais_proxima = loja3
    loja3.loja_mais_proxima = loja1

    # Cria alguns funcionários
    func1 = Funcionario("Pinho", "123.456.789-00", 2500.0, "Vendedor")
    func2 = Funcionario("Padre Kelmon", "987.654.321-00", 3000.0, "Gerente")
    func3 = Funcionario("Tokar", "456.789.123-00", 2000.0, "Caixa")

    # Adiciona funcionários às lojas (Associação)
    loja1.adicionar_funcionario(func1)
    loja1.adicionar_funcionario(func2)
    loja2.adicionar_funcionario(func3)

    # Cria alguns instrumentos
    baixo1 = Baixo("Fender", "Jazz Bass", 5000.0, 4, False)
    guitarra1 = Guitarra("Gibson", "Les Paul", 7000.0, 6, "Humbucker")
    violao1 = Violao("Yamaha", "C40", 800.0, 6, "Clássico")

    # Adiciona instrumentos ao estoque da loja (Composição)
    loja1.adicionar_instrumento(baixo1)
    loja1.adicionar_instrumento(guitarra1)
    loja2.adicionar_instrumento(violao1)

    # Consulta instrumentos na loja1
    instrumentos_loja1 = loja1.consultar_instrumentos()
    print("Instrumentos disponíveis na loja 1:")
    for tipo, quantidade in instrumentos_loja1.items():
        print(f"{tipo}: {quantidade}")

    # Consulta funcionários por cargo na loja1
    funcionarios_loja1 = loja1.consultar_funcionarios_por_cargo()
    print("\nFuncionários na loja 1 por cargo:")
    for cargo, quantidade in funcionarios_loja1.items():
        print(f"{cargo}: {quantidade}")

    # Mudar o quadro de funcionários (Remanejamento)
    loja1.remover_funcionario(func2)
    loja2.adicionar_funcionario(func2)

    # Mudar o estoque (Venda de um instrumento)
    loja1.remover_instrumento(baixo1)

    # Após mudanças, consultar novamente
    print("\nApós mudanças:")
    instrumentos_loja1 = loja1.consultar_instrumentos()
    print("Instrumentos disponíveis na loja 1:")
    for tipo, quantidade in instrumentos_loja1.items():
        print(f"{tipo}: {quantidade}")

    funcionarios_loja1 = loja1.consultar_funcionarios_por_cargo()
    print("\nFuncionários na loja 1 por cargo:")
    for cargo, quantidade in funcionarios_loja1.items():
        print(f"{cargo}: {quantidade}")

if __name__ == "__main__":
    main()
