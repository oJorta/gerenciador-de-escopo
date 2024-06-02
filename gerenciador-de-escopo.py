def declarar_variaveis (linha, escopos, num_linha):
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
            elif tipo == "CADEIA":
                valor = valor.strip()
        else:
            nome = declaracao.strip()
            if (tipo == "NUMERO"):
                valor = 0
            else:
                valor = '""'
        
        escopos[-1][nome] = {"tipo": tipo, "valor": valor}

def processar_atribuicao(linha, escopos, num_linha):
    nome, valor = linha.split("=")
    nome = nome.strip()
    valor = valor.strip()
    tipo = None

    variavel_original = procurar_variavel(escopos, nome, num_linha)
    if variavel_original:
        if valor[0].islower():
            variavel_referencia = procurar_variavel(escopos, valor, num_linha)
            if variavel_referencia:
                if variavel_referencia["tipo"] == variavel_original["tipo"]:
                    if nome in escopos[-1]:
                        escopos[-1][nome]["valor"] = variavel_referencia["valor"]
                    else:
                        escopos[-1][nome] = {"tipo": variavel_referencia["tipo"], "valor": variavel_referencia["valor"]}
                else:
                    print(f"Erro linha {num_linha}, tipos incompatíveis")
            else:
                print(f"Erro linha {num_linha}, variável não declarada")
        else:
            try:
                float(valor)
                tipo = "NUMERO"
            except ValueError:
                tipo = "CADEIA"
            if tipo == variavel_original["tipo"]:
                    if nome in escopos[-1]:
                        escopos[-1][nome]["valor"] = valor
                    else:
                        escopos[-1][nome] = {"tipo": tipo, "valor": valor}
            else:
                print(f"Erro linha {num_linha}, tipos incompatíveis")
    else:
        print(f"Erro linha {num_linha}, variável não declarada")

def procurar_variavel(escopos, nome, num_linha):
    for escopo in reversed(escopos):
        if nome in escopo:
            return escopo[nome]
    print(f"Erro linha {num_linha}, variável não declarada")
    return None

def imprimir_variavel(linha, escopos, num_linha):
    nome = linha.split()[1].strip()
    variavel = procurar_variavel(escopos, nome, num_linha)
    if variavel:
        print(variavel["valor"])
            

def main():
    arquivo = "exemplo2.txt"
    codigo = open(arquivo, "r").read()
    
    escopos = []
    linhas = codigo.strip().split("\n")
    
    for num_linha, linha in enumerate(linhas, 1):
        linha = linha.strip()
        if linha.startswith("BLOCO"):
            escopos.append({})
        elif linha.startswith("FIM"):
            if (escopos):
                escopos.pop()
            else:
                print(f"Erro linha {num_linha}, nenhum escopo para fechar")
        elif linha.startswith("NUMERO") or linha.startswith("CADEIA"):
            declarar_variaveis(linha, escopos, num_linha)
        elif linha.startswith("PRINT") or linha.startswith("print"):
            imprimir_variavel(linha, escopos, num_linha)
        elif "=" in linha:
            processar_atribuicao(linha, escopos, num_linha)
    
main()