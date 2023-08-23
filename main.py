import re
from datetime import datetime

import pandas as pd

from logs import registrar_log

VALOR = 15
QUANTIDADE = 1


def criar_planilha(nome_arquivo):
    colunas = ["Nomes", "INTEIRA", "MEIA", "TOTAL"]
    dados = pd.DataFrame(columns=colunas)
    dados.to_excel(nome_arquivo, index=False)


def criar_arquivo_log(log_file):
    with open(log_file, "w") as log:
        log.write("Arquivo de Logs:\n\n")


def separa_pares(menu, op):
    texto_limpo = re.sub(r'^\d+-\s*', '', menu[op])
    pares = re.findall(r'(\w+):(I|M)', texto_limpo)
    objetos = [{"nome": nome, "tipo": "INTEIRA" if tipo == "I" else "MEIA"}
               for nome, tipo in pares]

    return objetos


def ler_tabela_e_formatar(dados):
    entries = []

    for index, row in dados.iterrows():
        entry = f"{row['Nomes']}: INTEIRA({row['INTEIRA']}), \
            MEIA({row['MEIA']}), \
            TOTAL({row['TOTAL']})"
        entries.append(entry)

    return "©".join(entries)


def adicionar_pessoa(planilha, pessoas):
    dados = pd.read_excel(planilha)

    for pessoa in pessoas:
        nome, tipo = pessoa['nome'], pessoa['tipo']
        index = dados.index[dados['Nomes'] == nome].tolist()

        if not index:
            novo_registro = {'Nomes': nome,
                             'INTEIRA': 0, 'MEIA': 0, 'TOTAL': 0}
            dados = dados._append(novo_registro, ignore_index=True)
            index = [dados.shape[0] - 1]

        index = index[0]
        dados.loc[index, tipo] += QUANTIDADE
        dados.loc[index, 'TOTAL'] = dados.loc[index, 'INTEIRA'] * \
            VALOR + dados.loc[index, 'MEIA'] * (VALOR/2)
        dados.to_excel(planilha, index=False)

    tabela_formatada = ler_tabela_e_formatar(dados)
    registrar_log(tabela_formatada)

    print("Registro Salvo!\n")


def main():
    nome_arquivo = f'{datetime.now().strftime("%Y-%m")}.xlsx'
    nome_arquivo_log = f'logs-{datetime.now().strftime("%Y-%m")}.txt'

    try:
        dados = pd.read_excel(nome_arquivo)
    except FileNotFoundError:
        criar_planilha(nome_arquivo)
        print(f"Planilha {nome_arquivo} criada.")
        dados = pd.DataFrame(columns=["Nomes", "INTEIRA", "MEIA", "TOTAL"])

    try:
        log = open(nome_arquivo_log, 'r')
        log_lines = log.readlines()
        log.close()
        for line in log_lines:
            if "INTEIRA" in line and "MEIA" in line and "TOTAL" in line:
                elem = re.sub(re.compile(
                    r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{6} - "), "", line)
                for person in elem.split("©"):
                    nome = re.search(r"^(.*?):", person).group(1).strip()

                    numeros = re.findall(r"\((\d+(\.\d+)?)\)", person)
                    valores = [float(numero[0]) for numero in numeros]

                    inteira = valores[0]
                    meia = valores[1]
                    total = valores[2]
                    index = dados.index[dados['Nomes'] == nome].tolist()

                    if not index:
                        novo_registro = {'Nomes': nome,
                                         'INTEIRA': inteira,
                                         'MEIA': meia,
                                         'TOTAL': total}
                        dados = dados.append(novo_registro, ignore_index=True)
                    else:
                        index = index[0]
                        dados.loc[index, 'INTEIRA'] = inteira
                        dados.loc[index, 'MEIA'] = meia
                        dados.loc[index, 'TOTAL'] = total

    except FileNotFoundError:
        criar_arquivo_log(nome_arquivo_log)
        print(f"Arquivo de logs {nome_arquivo_log} criado.")

    while True:
        print("Menu:")
        opcoes = [
            "1- Alexander:M, Manasses:M, Enzo:I",
            "2- Alexander:M, Manasses:M",
            "3- Alexander:M, Enzo:M",
            "4- Manasses:I",
            "5- Nova pessoa + Default",
            "6- Nova pessoa",
            "7- Sair"
        ]
        for op in opcoes:
            print(op)

        opcao = int(input("\nEscolha uma opção: "))-1

        if opcao in range(0, 4):
            adicionar_pessoa(nome_arquivo, separa_pares(opcoes, opcao))
        elif opcao in [4, 5]:
            nova = input("Nome:<Tipo> - ")

            menu = opcoes[:]
            menu[opcao] = menu[0] + ", " + nova if opcao == 4 else nova

            adicionar_pessoa(nome_arquivo, separa_pares(menu, opcao))
        elif opcao == 6:
            print("Saindo do programa.")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
