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
            elif tipo == "CADEIA":
                valor = valor.strip()
        else:
            nome = declaracao.strip()
            if (tipo == "NUMERO"):
                valor = 0
            else:
                valor = '""'
        
        escopos[-1][nome] = {"tipo": tipo, "valor": valor}

def atribuicao(linha, escopos, num_linha):
    nome, valor = linha.split("=")
    nome = nome.strip()
    valor = valor.strip()
    tipo = None

    variavel_original = procurar_variavel(escopos, nome)
    if variavel_original:
        if valor[0].islower():
            variavel_referencia = procurar_variavel(escopos, valor)
            if variavel_referencia:
                if variavel_referencia["tipo"] == variavel_original["tipo"]:
                    if nome in escopos[-1]:
                        escopos[-1][nome]["valor"] = variavel_referencia["valor"]
                    else:
                        escopos[-1][nome] = {"tipo": variavel_referencia["tipo"], "valor": variavel_referencia["valor"]}
                else:
                    print(f"Erro linha {num_linha} - tipos incompatíveis")
            else:
                print(f"Erro linha {num_linha} - variável não declarada")
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
                print(f"Erro linha {num_linha} - tipos incompatíveis")
    else:
        print(f"Erro linha {num_linha} - variável não declarada")

def procurar_variavel(escopos, nome):
    for escopo in reversed(escopos):
        if nome in escopo:
            return escopo[nome]
    return None

def imprimir_variavel(linha, escopos, num_linha):
    nome = linha.split()[1].strip()
    variavel = procurar_variavel(escopos, nome)
    if variavel:
        print(variavel["valor"])
    else:
        print(f"Erro linha {num_linha} - variável não declarada")
            

def main():
    arquivo = "exemplo3.txt"
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
                print(f"Erro linha {num_linha} - nenhum escopo para fechar")
        elif linha.startswith("NUMERO") or linha.startswith("CADEIA"):
            declarar_variaveis(linha, escopos)
        elif linha.startswith("PRINT") or linha.startswith("print"):
            imprimir_variavel(linha, escopos, num_linha)
        elif "=" in linha:
            atribuicao(linha, escopos, num_linha)
    
main()