from models import Apartamento, Casa, Estudio, Orcamento


# Função de validação para menus numéricos (evita que o programa quebre se o usuário digitar texto ou número inválido)
def pedir_opcao(mensagem, opcoes_validas):
    while True:
        try:
            valor = int(input(mensagem))
            if valor in opcoes_validas:
                return valor
            print(f"Opção inválida. Escolha entre: {opcoes_validas}")
        except ValueError:
            print("Digite apenas números válidos.")


# Função de validação para quantidades inteiras (ex: vagas extras no estúdio)
def pedir_inteiro_positivo(mensagem):
    while True:
        try:
            valor = int(input(mensagem))
            if valor >= 0:
                return valor
            print("O número não pode ser negativo.")
        except ValueError:
            print("Digite um número inteiro válido.")


# Função de validação para perguntas de Sim ou Não, retornando True ou False
def pedir_sim_nao(mensagem):
    while True:
        resposta = input(mensagem).strip().upper()
        if resposta in ("S", "SIM"):
            return True
        if resposta in ("N", "NAO", "NÃO"):
            return False
        print("Responda apenas com S (Sim) ou N (Não).")


# Função principal que conduz o atendimento e monta os objetos
def main():
    print("=== RentSmart - Sistema de Orçamento (R.M Imóveis) ===")
    print("1 - Apartamento (Base: R$ 700,00)")
    print("2 - Casa (Base: R$ 900,00)")
    print("3 - Estúdio (Base: R$ 1.200,00)")

    opcao_imovel = pedir_opcao("\nEscolha a categoria do imóvel (1, 2 ou 3): ", [1, 2, 3])

    # Coleta as características específicas de acordo com o imóvel escolhido e cria o objeto correspondente
    if opcao_imovel == 1:
        quartos = pedir_opcao("Quantidade de quartos (1 ou 2): ", [1, 2])
        garagem = pedir_sim_nao("Incluir 1 vaga de garagem (+R$ 300,00)? [S/N]: ")
        criancas = pedir_sim_nao("O cliente possui crianças? [S/N]: ")
        imovel = Apartamento(quartos, garagem, criancas)

    elif opcao_imovel == 2:
        quartos = pedir_opcao("Quantidade de quartos (1 ou 2): ", [1, 2])
        garagem = pedir_sim_nao("Incluir 1 vaga de garagem (+R$ 300,00)? [S/N]: ")
        imovel = Casa(quartos, garagem)

    else:
        estacionamento = pedir_sim_nao("Incluir pacote de 2 vagas de estacionamento (+R$ 250,00)? [S/N]: ")
        extras = 0
        if estacionamento:
            extras = pedir_inteiro_positivo("Quantas vagas extras além das 2 (+R$ 60,00 cada)? ")
        imovel = Estudio(estacionamento, extras)

    # Pergunta em quantas vezes a taxa de R$ 2.000,00 será parcelada
    parcelas = pedir_opcao(
        "\nEm quantas parcelas deseja pagar a taxa contratual de R$ 2.000,00 (1 a 5)? ",
        [1, 2, 3, 4, 5]
    )

    # Cria o orçamento passando o imóvel montado, exibe o resultado e exporta o CSV
    orcamento = Orcamento(imovel, parcelas)
    orcamento.exibir_resumo()

    caminho_csv = orcamento.gerar_csv()
    print(f"\nProjeção dos 12 meses salva no arquivo '{caminho_csv}'.")


# Garante que o programa só rode quando este arquivo for executado diretamente
if __name__ == "__main__":
    main()