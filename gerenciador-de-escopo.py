# Declara variáveis no escopo atual
def declarar_variaveis (linha, escopos):
    partes = linha.split()
    tipo = partes[0] # A primeira posição do array de partes contém o tipo da variável (NUMERO ou CADEIA)
    declaracoes = " ".join(partes[1:]).split(",") # Separa as declarações individuais de variáveis (a virgula é o separador)

    for declaracao in declaracoes:
        if "=" in declaracao:
            # Se a declaração possuir atribuição, separa o nome e o valor
            nome, valor = declaracao.split("=")
            nome = nome.strip()
            valor = valor.strip()

            # Cast do valor para o tipo correto
            if tipo == "NUMERO":
                if ("." in valor):
                    valor = float(valor)
                else:
                    valor = int(valor)
            elif tipo == "CADEIA":
                valor = valor.strip()
        else:
            # Se não possuir atribuição, declara a variável com valor padrão
            nome = declaracao.strip()
            if (tipo == "NUMERO"):
                valor = 0
            else:
                valor = '""'
        
        # Adiciona a variável ao escopo atual
        escopos[-1][nome] = {"tipo": tipo, "valor": valor}

# Atribuição de valor a uma variável já declarada
def atribuicao(linha, escopos, num_linha):
    nome, valor = linha.split("=")
    nome = nome.strip()
    valor = valor.strip()
    tipo = None

    # Procura a variável a partir do escopo atual
    variavel_original = procurar_variavel(escopos, nome)
    if variavel_original:
        if valor[0].islower(): # Se o valor for uma variável (começar com letra minúscula)
            # Se a variável de referência for encontrada, atribui o valor dela à variável original
            variavel_referencia = procurar_variavel(escopos, valor)
            if variavel_referencia:
                # Se os tipos forem compatíveis, atribui o valor
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
            # Tenta fazer cast do valor para descobrir o tipo
            # Utilizei try/except pois o Python gera erro e para a execução se o cast não for possível
            try:
                float(valor)
                tipo = "NUMERO"
            except ValueError:
                tipo = "CADEIA"

            # Se os tipos forem compatíveis, atribui o valor
            if tipo == variavel_original["tipo"]:
                    if nome in escopos[-1]:
                        escopos[-1][nome]["valor"] = valor
                    else:
                        escopos[-1][nome] = {"tipo": tipo, "valor": valor}
            else:
                print(f"Erro linha {num_linha} - tipos incompatíveis")
    else:
        print(f"Erro linha {num_linha} - variável não declarada")

# Procura uma variável na pilha de escopos (a partir do topo)
def procurar_variavel(escopos, nome):
    for escopo in reversed(escopos):
        if nome in escopo:
            return escopo[nome]
    return None

# Imprime o valor de uma variável
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
    
    # Itera sobre as linhas do código realizando as operações necessárias
    for num_linha, linha in enumerate(linhas, 1):
        linha = linha.strip()
        if linha.startswith("BLOCO"):
            escopos.append({}) # Adiciona um novo escopo
        elif linha.startswith("FIM"):
            if (escopos):
                escopos.pop() # Fecha o escopo atual
            else:
                print(f"Erro linha {num_linha} - nenhum escopo para fechar")
        elif linha.startswith("NUMERO") or linha.startswith("CADEIA"):
            declarar_variaveis(linha, escopos)
        elif linha.startswith("PRINT") or linha.startswith("print"):
            imprimir_variavel(linha, escopos, num_linha)
        elif "=" in linha:
            atribuicao(linha, escopos, num_linha)
    
main()