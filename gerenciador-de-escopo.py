def declarar_variaveis (linha, escopos):
    partes = linha.split()
    tipo = partes[0]
    declaracoes = " ".join(partes[1:]).split(",")

    for declaracao in declaracoes:
        if "=" in declaracao:
            nome, valor = declaracao.split("=")
            nome = nome.strip()
            valor = valor.strip()

            if tipo == "NUMERO":
                if ("." in valor):
                    valor = float(valor)
                else:
                    valor = int(valor)
        else:
            nome = declaracao.strip()
            if (tipo == "NUMERO"):
                valor = 0
            else:
                valor = '""'
        
        escopos[-1][nome] = {"tipo": tipo, "valor": valor}

def processar_atribuicao(linha, escopos):
    nome, valor = linha.split("=")
    nome = nome.strip()
    valor = valor.strip()

    variavel = procurar_variavel(escopos, nome)

    if variavel:
        if valor[0].islower():
            variavel_ref = procurar_variavel(escopos, valor)
            atribuir_valor(escopos, nome, variavel_ref["valor"], variavel_ref["tipo"])
        else:
            atribuir_valor(escopos, nome, valor, variavel["tipo"])
    else:
        print("Erro: variável não declarada")

def atribuir_valor(escopos, nome, valor, tipo_valor):
    for escopo in reversed(escopos):
        if nome in escopo:
            if escopo[nome]["tipo"] != tipo_valor:
                print("Erro: tipos incompatíveis")
                return
            escopo[nome]["valor"] = valor
            return
    print("Erro: variável não declarada")

def procurar_variavel(escopos, nome):
    for escopo in reversed(escopos):
        if nome in escopo:
            return escopo[nome]
    print("Erro: variável não declarada")
    return None

def imprimir_variavel(linha, escopos):
    nome = linha.split()[1].strip()
    variavel = procurar_variavel(escopos, nome)
    if variavel:
        print(variavel["valor"])
            

def main():
    arquivo = "exemplo1.txt"
    codigo = open(arquivo, "r").read()
    
    escopos = []
    linhas = codigo.strip().split("\n")
    
    for linha in linhas:
        linha = linha.strip()
        if linha.startswith("BLOCO"):
            escopos.append({})
        elif linha.startswith("FIM"):
            if (escopos):
                escopos.pop()
            else:
                print("Erro: nenhum escopo para fechar")
        elif linha.startswith("NUMERO") or linha.startswith("CADEIA"):
            declarar_variaveis(linha, escopos)
        elif linha.startswith("PRINT"):
            imprimir_variavel(linha, escopos)
        elif "=" in linha:
            processar_atribuicao(linha, escopos)
    
main()