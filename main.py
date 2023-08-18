import re
from datetime import datetime

import pandas as pd

VALOR = 15
QUANTIDADE = 1


def criar_planilha(nome_arquivo):
    colunas = ["Nomes", "INTEIRA", "MEIA", "TOTAL"]
    dados = pd.DataFrame(columns=colunas)
    dados.to_excel(nome_arquivo, index=False)


def registrar_log(dados):
    nome_arquivo_log = f'logs-{datetime.now().strftime("%Y-%m")}.txt'

    try:
        with open(nome_arquivo_log, 'a') as log:
            pass
    except FileNotFoundError:
        with open(nome_arquivo_log, "w") as log:
            log.write("Arquivo de Logs:\n")

    log_entry = f"{datetime.now()} - {dados}"
    with open(nome_arquivo_log, "a") as log:
        log.write(log_entry + "\n")
    

def separa_pares(menu, op):
    texto_limpo = re.sub(r'^\d+-\s*', '', menu[op])
    pares = re.findall(r'(\w+):(I|M)', texto_limpo)
    objetos = [{"nome": nome, "tipo": "INTEIRA" if tipo == "I" else "MEIA"}
               for nome, tipo in pares]

    return objetos


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

        registrar_log(dados.loc[index])

    print("Registro Salvo!\n")


def main():
    nome_arquivo = f'{datetime.now().strftime("%Y-%m")}.xlsx'

    try:
        dados = pd.read_excel(nome_arquivo)
    except FileNotFoundError:
        criar_planilha(nome_arquivo)
        print(f"Planilha {nome_arquivo} criada.")

    while True:
        print("Menu:")
        opcoes = [
            "1- Alexander:M, Manasses:M, Enzo:I",
            "2- Alexander:M, Manasses:M",
            "3- Alexander:M, Enzo:M",
            "4- Manasses:I",
            "5- Nova pessoa + Default",
            "6- Nova pessoa",
            "7- Sair"]
        for op in opcoes:
            print(op)

        opcao = int(input("\nEscolha uma opção: "))-1

        if opcao in range(0, 3):
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
