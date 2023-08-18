import re

nome = 'Nova:I'

print(nome.split(':'))
print(nome.split(':')[0], nome.split(':')[1])


nome2 = "1- Alexander:M, Manasses:M, Enzo:I"

novo_texto = re.sub(r'^\d+-\s*', '', nome2)
print(novo_texto)
pares_nome_tipo = re.findall(r'(\w+):(I|M)', novo_texto)
objetos = [{"nome": nome, "tipo": "INTEIRA" if tipo == "I" else "MEIA"} for nome, tipo in pares_nome_tipo]
print(objetos)