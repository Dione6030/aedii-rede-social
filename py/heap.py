"""padrão aedlib 2.6"""

class MaxHeap:
    def __init__(self):
        # [SOCIAL-26] inicia nossa classe vazia
        self.dados = [] # aqui vai fica [quant_amigos_em_comum, id_do_usuário_recomendado]
    
    def social_esta_vazio(self):
        # [SOCIAL-26] tratamento de erros, caso peça mais recomendações do "amigos de amigos" do usuário (Ex: pedro segue 2 pessoas, essas duas seguem outras duas, mas aí pede um Top5 de recomendação, evitando um indexError)
        return len(self.dados) == 0
    
    def social_tamanho(self):
        # [SOCIAl-26] serve para classe saber quantas recomendações o usuário tem no total.
        return len(self.dados)
    
    def social_inserir(self, amigos_em_comum, id_usuario):
        # [SOCIAL-26] insere os IDs dos usuários que serão recomendados
        self.dados.append([amigos_em_comum, id_usuario])
        
        self.social_subir(len(self.dados) -1)
    
    def social_subir(self, indice):
        # [SOCIAL-26] organiza a arvore para que o usuário com mais amigos em comum esteja no topo da arvore de recomendados
        while indice > 0:
            topo = (indice - 1) // 2
            
            # Compara a quantidade de amigos em comum do topo com do mais a baixo
            if self.dados[indice][0] > self.dados[topo][0]:
                # Troca a posição no ranking
                self.dados[indice], self.dados[topo] = self.dados[topo], self.dados[indice]
                indice = topo # continua a verificação
            else:
                break # se ninguém tem mais amigos em comum, tá pronto.
    
    def social_descer(self, indice):
        # [SOCIAL-26] reorganiza a lista quando a melhor recomendação é retirada da lista para selecionar os próximos
        total = len(self.dados)
        
        while True:
            # Deixa a lista no formato de arvore
            maior = indice # Raiz, ou com mais amigos em comum, o próximo que deve sair
            esq = 2 * indice + 1
            dir = 2 * indice + 2
            
            # Checa se o usuario a esquerda tem mais amigos em comum
            if esq < total and self.dados[esq] > self.dados[maior]:
                maior = esq
            
            # Checa se o usuario a direita tem mais amigos em comum
            if dir < total and self.dados[dir] > self.dados[maior]:
                maior = dir
            
            # Se o da raiz já é maior que outros, desce para fazer a comparação com os de baixo.
            if maior != indice:
                self.dados[indice], self.dados[maior] = self.dados[maior], self.dados[indice]
                indice = maior
            
            else:
                break # O maior já é o maior
    
    def social_remover_maior(self):
        # [SOCIAL-26] Entrega o maior candidato para o usuário seguir e o retira da lista.
        if len(self.dados) == 0:
            return None
        if len(self.dados) == 1:
            return self.dados.pop()
        
        # Guarda o melhor candidato
        topo = self.dados[0]
        
        # Manda o ultimo elemento para raiz
        self.dados[0] = self.dados.pop()
        
        # Reorganiza para ter os melhores topos
        self.social_descer(0)
        
        return topo

def social_contar_amigos_comuns(usuario_id, maior_id, ids_para_nomes, tabela):
    # [SOCIAL-26] serve para contar quantos amigos tal usuario tem em comum
    nome_do_usuario = ids_para_nomes[usuario_id]
    ficha_do_usuario = tabela.social_buscar(nome_do_usuario)
    seguidos = ficha_do_usuario[3]
    
    # Inicia o vetor de frequencia
    frequencia = [0] * (maior_id + 1)
    
    # vamos ver quem o usuário está seguindo
    for id_amigo in seguidos:
        nome_do_amigo = ids_para_nomes[id_amigo]
        if nome_do_amigo is None:
            continue
        
        ficha_do_amigo = tabela.social_buscar(nome_do_amigo)
        seguidos_do_amigo = ficha_do_amigo[3]
        
        # vamos ver quem os está sendo seguido pelo seguido do usuáario
        for id_candidato in seguidos_do_amigo:
            # Para não recomendar o próprio usuário nem quem ele já segue
            if id_candidato != usuario_id and id_candidato not in seguidos:
                frequencia[id_candidato] += 1
    
    return frequencia