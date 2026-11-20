# RentSmart - Sistema de Orçamento de Locação

O **RentSmart** é uma aplicação de linha de comando desenvolvida em Python para apoiar o atendimento interno de corretores e atendentes da **R.M Imóveis**. O objetivo do sistema é padronizar o cálculo de orçamentos de locação residencial, reduzir erros manuais durante o atendimento e gerar automaticamente uma projeção financeira de 12 meses em formato CSV pronta para envio ao cliente ou arquivo interno.

---

## Funcionalidades Principais

* **Atendimento contínuo em terminal:** Permite realizar vários orçamentos em sequência sem precisar reiniciar o programa, identificando cada cliente por nome e sobrenome.
* **Cálculo automatizado por categoria de imóvel:** Aplica automaticamente valores-base, adicionais específicos e descontos conforme as regras da imobiliária.
* **Separação da taxa contratual:** Exibe a taxa fixa de contrato (R$ 2.000,00) e seu parcelamento de forma independente do valor recorrente do aluguel mensal.
* **Validação de entradas:** Impede que erros de digitação (como texto em campos numéricos, opções fora do menu ou nomes inválidos) interrompam a execução. Aceita inclusive nomes compostos com hífen ou apóstrofo.
* **Exportação automática para CSV:** Gera uma planilha mensal com os 12 meses do primeiro ano de contrato mais o total acumulado. Cada arquivo recebe um nome único com o nome normalizado do cliente e a data/hora no padrão brasileiro (`projecao_nome_cliente_DD-MM-AAAA_HHhMMmSSs.csv`), evitando sobrescrever orçamentos anteriores.

---

## Regras de Negócio Implementadas

| Categoria | Aluguel-Base | Adicionais Disponíveis | Desconto Aplicável |
| :--- | :--- | :--- | :--- |
| **Apartamento** | R$ 700,00 | 2 quartos (+R$ 200,00)<br>1 vaga de garagem (+R$ 300,00) | 5% sobre o aluguel com adicionais caso não haja crianças |
| **Casa** | R$ 900,00 | 2 quartos (+R$ 250,00)<br>1 vaga de garagem (+R$ 300,00) | Não se aplica |
| **Estúdio** | R$ 1.200,00 | Pacote de 2 vagas (+R$ 250,00)<br>Vaga extra (+R$ 60,00 cada) | Não se aplica |

* **Taxa contratual:** Valor fixo de **R$ 2.000,00**, com opção de parcelamento de **1x a 5x**, cobrada separadamente do aluguel mensal.

---

## Estrutura do Projeto e Arquitetura (POO)

O código foi dividido em dois módulos principais utilizando apenas bibliotecas nativas do Python (`abc`, `csv`, `datetime` e `unicodedata`), sem necessidade de instalar dependências externas:

```text
RentSmart-Python/
├── main.py       # Interface de terminal, validações de entrada e fluxo de atendimento
├── models.py     # Classes de domínio, regras de cálculo e exportação para CSV
├── LICENSE       # Licença MIT
└── README.md     # Documentação do projeto
```

### Modelagem Orientada a Objetos (`models.py`)

* **`Imovel` (Classe Abstrata):** Define a estrutura comum a todos os imóveis (`tipo`, `valor_base`) e os métodos gerais de soma de adicionais, desconto e cálculo final do aluguel mensal. Obriga as subclasses a implementarem o método abstrato `obter_adicionais()`.
* **`Apartamento`, `Casa` e `Estudio` (Herança e Polimorfismo):** Herdam de `Imovel` e implementam suas próprias regras de adicionais. A classe `Apartamento` também sobrescreve `calcular_desconto()` para aplicar a regra exclusiva dos 5%.
* **`Orcamento` (Composição):** Recebe o nome do cliente, uma instância de `Imovel` e o número de parcelas da taxa contratual. É responsável por calcular a parcela da taxa, formatar o resumo no terminal e exportar o arquivo CSV compatível com o Excel em português (codificação `utf-8-sig` e delimitador `;`).

---

## Como Executar

### Pré-requisitos
* Python 3.8 ou superior instalado na máquina.

### Passo a passo

1. Clone este repositório:
   ```bash
   git clone https://github.com/HeitorXavier-S2/RentSmart-Python.git
   ```

2. Acesse a pasta do projeto:
   ```bash
   cd RentSmart-Python
   ```

3. Execute a aplicação:
   ```bash
   python main.py
   ```

---

## Exemplo de Uso

### Saída no Terminal

```text
========================================================
           R.M IMÓVEIS - RESUMO DO ORÇAMENTO            
========================================================
  Cliente             : Maria José
  Categoria do Imóvel : Apartamento
  Aluguel-Base        :                      R$ 700,00
--------------------------------------------------------
  ADICIONAIS MENSAIS:
   + Adicional 2 quartos                     R$ 200,00
   + Vaga de garagem (1 vaga)                R$ 300,00
========================================================
  ALUGUEL MENSAL FINAL                     R$ 1.200,00
========================================================
  TAXA CONTRATUAL (COBRADA SEPARADAMENTE DO ALUGUEL)
--------------------------------------------------------
  Valor Total da Taxa                      R$ 2.000,00
  Condição Escolhida: 5x de R$ 400,00
========================================================

  [OK] Projeção de 12 meses salva em: 'projecao_maria_jose_20-11-2026_13h08m11s.csv'
```

### Estrutura do CSV Gerado

| Mês | Cliente | Categoria | Aluguel Mensal (R$) | Parcela Taxa Contratual (R$) | Total Previsto no Mês (R$) |
| :--- | :--- | :--- | ---: | ---: | ---: |
| Mês 01 | Maria José | Apartamento | 1200,00 | 400,00 | 1600,00 |
| Mês 02 | Maria José | Apartamento | 1200,00 | 400,00 | 1600,00 |
| ... | ... | ... | ... | ... | ... |
| Mês 06 | Maria José | Apartamento | 1200,00 | 0,00 | 1200,00 |
| ... | ... | ... | ... | ... | ... |
| Mês 12 | Maria José | Apartamento | 1200,00 | 0,00 | 1200,00 |
| **TOTAL (12 MESES)** | - | - | **14400,00** | **2000,00** | **16400,00** |

---

## Autor

Desenvolvido por **Heitor Resende Pires Xavier** ([@HeitorXavier-S2](https://github.com/HeitorXavier-S2)) como projeto acadêmico de Programação Orientada a Objetos em Python.

## Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE).
