from models import Apartamento, Casa, Estudio, Orcamento

# Função de validação para exigir nome e sobrenome do cliente
def pedir_nome_completo(mensagem):
    while True:
        nome = " ".join(input(mensagem).strip().split())
        partes = nome.split(" ")
        # Permite letras, hífen (Ana-Clara) e apóstrofo (D'Ávila), exigindo pelo menos nome e sobrenome
        valido = all(parte.replace("-", "").replace("'", "").isalpha() for parte in partes)
        if len(partes) >= 2 and valido:
            return nome.title()
        print("  [!] Por favor, informe pelo menos nome e sobrenome válidos (apenas letras).")


# Função de validação para menus numéricos (evita que o programa quebre se o usuário digitar texto ou número inválido)
def pedir_opcao(mensagem, opcoes_validas):
    while True:
        try:
            valor = int(input(mensagem))
            if valor in opcoes_validas:
                return valor
            print(f"  [!] Opção inválida. Escolha entre: {opcoes_validas}")
        except ValueError:
            print("  [!] Entrada inválida. Digite apenas números.")


# Função de validação para quantidades inteiras (ex: vagas extras no estúdio)
def pedir_inteiro_positivo(mensagem):
    while True:
        try:
            valor = int(input(mensagem))
            if valor >= 0:
                return valor
            print("  [!] O número não pode ser negativo.")
        except ValueError:
            print("  [!] Entrada inválida. Digite um número inteiro.")


# Função de validação para perguntas de Sim ou Não, retornando True ou False
def pedir_sim_nao(mensagem):
    while True:
        resposta = input(mensagem).strip().upper()
        if resposta in ("S", "SIM"):
            return True
        if resposta in ("N", "NAO", "NÃO"):
            return False
        print("  [!] Responda apenas com S (Sim) ou N (Não).")


# Função principal que conduz o atendimento e monta os objetos
def main():
    largura = 56
    print("\n" + "=" * largura)
    print("RENTSMART - SISTEMA DE ORÇAMENTO DE LOCAÇÃO".center(largura))
    print("R.M Imóveis".center(largura))
    print("=" * largura)

    # Mantém o sistema rodando para vários atendimentos seguidos até o usuário escolher sair
    while True:
        print("\n[1/4] IDENTIFICAÇÃO DO CLIENTE")
        print("-" * largura)
        cliente = pedir_nome_completo("  > Nome e sobrenome do cliente: ")

        print("\n[2/4] CATEGORIA DO IMÓVEL")
        print("-" * largura)
        print("  [1] Apartamento  (Base: R$ 700,00)")
        print("  [2] Casa         (Base: R$ 900,00)")
        print("  [3] Estúdio      (Base: R$ 1.200,00)")
        print("-" * largura)

        opcao_imovel = pedir_opcao("  > Escolha uma opção (1, 2 ou 3): ", [1, 2, 3])

        print("\n[3/4] CONFIGURAÇÃO DO IMÓVEL")
        print("-" * largura)

        # Coleta as características específicas de acordo com o imóvel escolhido e cria o objeto correspondente
        if opcao_imovel == 1:
            quartos = pedir_opcao("  > Quantidade de quartos (1 ou 2): ", [1, 2])
            garagem = pedir_sim_nao("  > Incluir 1 vaga de garagem (+R$ 300,00)? [S/N]: ")
            criancas = pedir_sim_nao("  > O cliente possui crianças? [S/N]: ")
            imovel = Apartamento(quartos, garagem, criancas)

        elif opcao_imovel == 2:
            quartos = pedir_opcao("  > Quantidade de quartos (1 ou 2): ", [1, 2])
            garagem = pedir_sim_nao("  > Incluir 1 vaga de garagem (+R$ 300,00)? [S/N]: ")
            imovel = Casa(quartos, garagem)

        else:
            estacionamento = pedir_sim_nao("  > Incluir pacote de 2 vagas (+R$ 250,00)? [S/N]: ")
            extras = 0
            if estacionamento:
                extras = pedir_inteiro_positivo("  > Quantas vagas extras além das 2 (+R$ 60,00 cada)? ")
            imovel = Estudio(estacionamento, extras)

        print("\n[4/4] CONDIÇÃO DA TAXA CONTRATUAL (R$ 2.000,00)")
        print("-" * largura)
        parcelas = pedir_opcao(
            "  > Parcelar em quantas vezes (1 a 5)? ",
            [1, 2, 3, 4, 5]
        )

        # Cria o orçamento passando o cliente, o imóvel montado e as parcelas, exibe o resultado e exporta o CSV
        orcamento = Orcamento(cliente, imovel, parcelas)
        orcamento.exibir_resumo()

        caminho_csv = orcamento.gerar_csv()
        print(f"\n  [OK] Projeção de 12 meses salva em: '{caminho_csv}'\n")

        if not pedir_sim_nao("  > Deseja realizar outro orçamento? [S/N]: "):
            print("\n" + "=" * largura)
            print("Atendimento encerrado. Obrigado por usar o RentSmart!".center(largura))
            print("=" * largura + "\n")
            break

        print("\n" + "=" * largura)
        print("NOVO ORÇAMENTO".center(largura))
        print("=" * largura)


# Garante que o programa só rode quando este arquivo for executado diretamente
if __name__ == "__main__":
    main()