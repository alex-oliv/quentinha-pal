from datetime import datetime

def registrar_log(dados):
    nome_arquivo_log = f'logs-{datetime.now().strftime("%Y-%m")}.txt'

    try:
        with open(nome_arquivo_log, 'a') as log:
            pass
    except FileNotFoundError:
        with open(nome_arquivo_log, "w") as log:
            log.write("Arquivo de Logs:\n\n")

    log_entry = f"{datetime.now()} - {dados}"
    with open(nome_arquivo_log, "a") as log:
        log.write(log_entry + "\n")