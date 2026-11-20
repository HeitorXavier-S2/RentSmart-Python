from abc import ABC, abstractmethod
import csv
from datetime import datetime
import unicodedata

# Função auxiliar para deixar os valores no padrão brasileiro (ex: R$ 1.250,00)
def formatar_moeda(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


# Aqui é uma classe abstrata que serve de molde (base) para todos os tipos de imóvel.
# Ela evita que a gente tenha que repetir os mesmos atributos e cálculos em cada classe filha.
class Imovel(ABC):
    def __init__(self, tipo, valor_base):
        self.tipo = tipo
        self.valor_base = valor_base

    # Método abstrato: obriga cada tipo de imóvel (Casa, Apto, Estúdio) a definir seus próprios adicionais
    @abstractmethod
    def obter_adicionais(self):
        pass

    # Soma todos os itens extras que foram escolhidos para o imóvel
    def calcular_total_adicionais(self):
        total = 0.0
        for _, valor in self.obter_adicionais():
            total += valor
        return total

    # Por padrão, os imóveis não têm desconto (só o Apartamento vai sobrescrever isso)
    def calcular_desconto(self):
        return 0.0

    # Calcula o aluguel mensal final juntando base + adicionais e tirando o desconto (se houver)
    def calcular_aluguel_mensal(self):
        subtotal = self.valor_base + self.calcular_total_adicionais()
        return subtotal - self.calcular_desconto()


# Classe filha que herda de Imovel e aplica as regras específicas de Apartamento
class Apartamento(Imovel):
    def __init__(self, quartos, tem_garagem, possui_criancas):
        # Chama o construtor da classe pai já passando o nome e o aluguel-base de R$ 700,00
        super().__init__("Apartamento", 700.00)
        self.quartos = quartos
        self.tem_garagem = tem_garagem
        self.possui_criancas = possui_criancas

    def obter_adicionais(self):
        adicionais = []
        if self.quartos == 2:
            adicionais.append(("Adicional 2 quartos", 200.00))
        if self.tem_garagem:
            adicionais.append(("Vaga de garagem (1 vaga)", 300.00))
        return adicionais

    # Regra exclusiva do apartamento: 5% de desconto sobre o total (base + adicionais) se não tiver crianças
    def calcular_desconto(self):
        if not self.possui_criancas:
            valor_com_adicionais = self.valor_base + self.calcular_total_adicionais()
            return valor_com_adicionais * 0.05
        return 0.0


# Classe filha que herda de Imovel e aplica as regras específicas de Casa
class Casa(Imovel):
    def __init__(self, quartos, tem_garagem):
        super().__init__("Casa", 900.00)
        self.quartos = quartos
        self.tem_garagem = tem_garagem

    def obter_adicionais(self):
        adicionais = []
        if self.quartos == 2:
            adicionais.append(("Adicional 2 quartos", 250.00))
        if self.tem_garagem:
            adicionais.append(("Vaga de garagem (1 vaga)", 300.00))
        return adicionais


# Classe filha que herda de Imovel e aplica as regras de estacionamento do Estúdio
class Estudio(Imovel):
    def __init__(self, usar_estacionamento, vagas_extras=0):
        super().__init__("Estúdio", 1200.00)
        self.usar_estacionamento = usar_estacionamento
        # Só faz sentido ter vagas extras se o cliente tiver contratado o pacote inicial de 2 vagas
        self.vagas_extras = vagas_extras if usar_estacionamento else 0

    def obter_adicionais(self):
        adicionais = []
        if self.usar_estacionamento:
            adicionais.append(("Pacote estacionamento (2 vagas)", 250.00))
            if self.vagas_extras > 0:
                custo_extras = self.vagas_extras * 60.00
                adicionais.append((f"Vagas extras ({self.vagas_extras}x R$ 60,00)", custo_extras))
        return adicionais


# Classe responsável por juntar o imóvel escolhido com os dados do cliente e a taxa contratual,
# mostrar o resumo na tela e gerar a planilha CSV de 12 meses.
class Orcamento:
    TAXA_CONTRATUAL = 2000.00

    def __init__(self, cliente, imovel, parcelas_taxa):
        self.cliente = cliente
        self.imovel = imovel
        self.parcelas_taxa = parcelas_taxa

    def calcular_parcela_taxa(self):
        return self.TAXA_CONTRATUAL / self.parcelas_taxa

    # Limpa acentos, apóstrofos e espaços do nome para gerar um nome de arquivo seguro no sistema operacional
    def _normalizar_nome_arquivo(self):
        sem_acentos = unicodedata.normalize("NFKD", self.cliente).encode("ASCII", "ignore").decode("ASCII")
        limpo = sem_acentos.replace("'", "").replace("-", "_")
        return "_".join(limpo.lower().strip().split())

    # Mostra todo o detalhamento no terminal alinhado em colunas para facilitar a leitura
    def exibir_resumo(self):
        aluguel_final = self.imovel.calcular_aluguel_mensal()
        desconto = self.imovel.calcular_desconto()
        parcela_taxa = self.calcular_parcela_taxa()
        largura = 56

        print("\n" + "=" * largura)
        print("R.M IMÓVEIS - RESUMO DO ORÇAMENTO".center(largura))
        print("=" * largura)
        print(f"  Cliente             : {self.cliente}")
        print(f"  Categoria do Imóvel : {self.imovel.tipo}")
        print(f"  Aluguel-Base        : {formatar_moeda(self.imovel.valor_base):>30}")
        print("-" * largura)

        adicionais = self.imovel.obter_adicionais()
        if adicionais:
            print("  ADICIONAIS MENSAIS:")
            for descricao, valor in adicionais:
                print(f"   + {descricao:<34} {formatar_moeda(valor):>14}")
        else:
            print("  ADICIONAIS MENSAIS  : Nenhum")

        if desconto > 0:
            print("-" * largura)
            print("  DESCONTOS:")
            print(f"   - Desconto 5% (sem crianças)       -{formatar_moeda(desconto):>14}")

        print("=" * largura)
        print(f"  ALUGUEL MENSAL FINAL                {formatar_moeda(aluguel_final):>16}")
        print("=" * largura)

        # Exibe a taxa separada do aluguel, conforme pedido nas regras da imobiliária
        print("  TAXA CONTRATUAL (COBRADA SEPARADAMENTE DO ALUGUEL)")
        print("-" * largura)
        print(f"  Valor Total da Taxa                 {formatar_moeda(self.TAXA_CONTRATUAL):>16}")
        print(f"  Condição Escolhida: {self.parcelas_taxa}x de {formatar_moeda(parcela_taxa)}")
        print("=" * largura)

    # Cria o arquivo CSV com a projeção mês a mês do primeiro ano de contrato
    def gerar_csv(self):
        aluguel_mensal = self.imovel.calcular_aluguel_mensal()
        parcela_taxa = self.calcular_parcela_taxa()

        # Gera um nome único com o nome do cliente e a data/hora atual para não sobrescrever os anteriores
        cliente_limpo = self._normalizar_nome_arquivo()
        carimbo_tempo = datetime.now().strftime("%d-%m-%Y_%Hh%Mm%Ss")
        nome_arquivo = f"projecao_{cliente_limpo}_{carimbo_tempo}.csv"

        # O encoding 'utf-8-sig' e o separador ';' fazem o arquivo abrir direitinho nas colunas do Excel
        with open(nome_arquivo, mode="w", newline="", encoding="utf-8-sig") as arquivo:
            writer = csv.writer(arquivo, delimiter=";")
            writer.writerow([
                "Mês",
                "Cliente",
                "Categoria",
                "Aluguel Mensal (R$)",
                "Parcela Taxa Contratual (R$)",
                "Total Previsto no Mês (R$)"
            ])

            for mes in range(1, 13):
                # Cobra a parcela da taxa apenas nos primeiros meses escolhidos pelo cliente (1 a 5)
                taxa_mes = parcela_taxa if mes <= self.parcelas_taxa else 0.0
                total_mes = aluguel_mensal + taxa_mes

                writer.writerow([
                    f"Mês {mes:02d}",
                    self.cliente,
                    self.imovel.tipo,
                    f"{aluguel_mensal:.2f}".replace(".", ","),
                    f"{taxa_mes:.2f}".replace(".", ","),
                    f"{total_mes:.2f}".replace(".", ",")
                ])

            # Linha final consolidando o total acumulado nos 12 meses
            writer.writerow([
                "TOTAL (12 MESES)",
                "-",
                "-",
                f"{(aluguel_mensal * 12):.2f}".replace(".", ","),
                f"{self.TAXA_CONTRATUAL:.2f}".replace(".", ","),
                f"{(aluguel_mensal * 12 + self.TAXA_CONTRATUAL):.2f}".replace(".", ",")
            ])

        return nome_arquivo