"""padrão aedlib 2.6"""
import json

class TabelaDispersaSocial:
    def __init__(self, tamanho=26003):
        # [SOCIAL-26] Constrói a classe de tabela hash por encadeamento com uma folga de mais ou menos 30%
        self.tamanho = tamanho
        self.quantidade_itens = 0
        # Cria "gavetas" vazias para receber as listas de Usuários
        self.tabela = [[] for _ in range(self.tamanho)]
    
    # Baseado em DJB2
    def social_funcao_hash(self, chave):
        # [SOCIAL-26] algoritmo que faz qualquer letra dar o valor mais diferente possível, tentando garantir que cada usuário tenha uma "gaveta" na tabela só para ele.
        
        hash_valor = 5381 # Número primo inicial padrão
        # Tira o "arroba" para calculo mais eficiente
        limpa_texto = str(chave)[1:] if str(chave).startswith('@') else str(chave)
        
        for caractere in limpa_texto:
            # Multiplica de forma rápida por 32 e soma com valor inicial
            hash_valor = ((hash_valor << 5) + hash_valor) + ord(caractere)
        
        return hash_valor % self.tamanho
    
    def social_inserir_dados(self, chave, indice_campo, valor_campo):
        # [SOCIAL-26] Insere os usuários com fichas fixas só esperando para serem preenchidas com suas respectivas informações, para evitar ficar dando .append sem ordem nenhuma
        
        # Mapeamento mental dos campos da ficha:
        # 0: nome | 1: data_cadastro | 2: seguidores | 3: seguidos | 4: posts | 5: ID do usuário
        
        indice = self.social_funcao_hash(chave)
        gaveta = self.tabela[indice]
        
        # Procura se já tem alguma coisa do usuário
        for registro in gaveta:
            if registro[0] == chave:
                ficha = registro[1]
                # acrescenta só o valor no seu respectivo campo da ficha
                ficha[indice_campo] = valor_campo
                return
            
        # Se não tem nada desse usuário ainda
        nova_ficha = [None, None, None, None, None, None]
        nova_ficha[indice_campo] = valor_campo # Preenche o respectivo campo
        
        gaveta.append([chave, nova_ficha]) # Abre uma gaveta com a ficha do respectivo usuário
        self.quantidade_itens += 1
    
    def social_buscar(self, username):
        # [SOCIAL-26] Retorna a lista bruta dos dados para maior liberdade na representação dos dados em api ou no terminal.
        
        # Só para garantir que vai funcionar mesmo se esquecer o "arroba"
        if not str(username).startswith('@'):
            username = '@' + str(username)
        
        indice = self.social_funcao_hash(username)
        gaveta = self.tabela[indice]
        
        for registro in gaveta:
            if registro[0] == username:
                return registro[1] # Retorna a lista: [nome, data, seguidores, seguidos, posts]
        
        return None # Se o usuário não encontrado (erro aparecerá na api)
    
    def social_salvar_json(self, caminho_arquivo="backupTabela.json"):
        # [SOCIAL-26] Salva tudo em um arquivo json
        
        def social_converte_valor(valor):
            # [SOCIAL-26] É uma função auxiliar só para traduzir umas coisas do python para json
            if valor is None:
                return "null" # Em json o valor vazio é null, enquanto que no py é none
            if isinstance(valor, (int, float)):
                return str(valor) # Números ficam sem aspas no JSON (ex: 540)
            if isinstance(valor, list):
                # Para deixar os seguidores em um formato de lista dentro das fichas
                elementos = ", ".join(social_converte_valor(x) for x in valor) 
                return f"[{elementos}]"
            
            # Se for texto (string), protege aspas internas e envolve com aspas duplas
            texto_seguro = str(valor).replace('"', '\\"')
            return f'"{texto_seguro}"'
        
        with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
            # Escreve o cabeçalho do objeto JSON
            arquivo.write("{\n")
            arquivo.write(f'  "tamanho": {self.tamanho},\n')
            arquivo.write(f'  "quantidade_itens": {self.quantidade_itens},\n')
            arquivo.write('  "gavetas": [\n')
        
            for i, gaveta in enumerate(self.tabela):
                itens_formatados = []
                
                for registro in gaveta:
                    chave = social_converte_valor(registro[0]) # @username
                    ficha = registro[1]                        # lista: [nome, data, seg, seg, posts]
                    
                    # Junta os itens da ficha em uma variável
                    campos_str = ", ".join(social_converte_valor(item) for item in ficha)
                    
                    # Monta a estrutura completa: ["@username", ["Nome", "Data", 10, 20, 30]]
                    itens_formatados.append(f'[{chave}, [{campos_str}]]')
                    
                
                # Se a "gaveta" estava vazia, itens_formatados é [] (espaço em branco), gerando apenas "    []"
                linha = f"    [{','.join(itens_formatados)}]"
                
                # Garante que toda linha vai ter uma "vírgula" para o json não quebrar
                if i < self.tamanho - 1:
                    linha += ","

                arquivo.write(linha + "\n")
            arquivo.write("  ]\n")
            arquivo.write("}\n")
    
    def social_carregar_json_manual(self, caminho_arquivo="backupTabela.json"):
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
            
        self.tamanho = dados["tamanho"]
        self.quantidade_itens = dados["quantidade_itens"]
        self.tabela = dados["gavetas"]