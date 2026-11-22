"""padrão aedlib 2.6"""

from heap import MaxHeap

def social_explora_comunidade(id_inicial, visitados, ids_para_nomes, tabela):
    # [SOCIAL-26] Explora todos os seguidos e seguidores a partir de um ID inicial
    
    fila = [id_inicial]
    visitados[id_inicial] = True # Marca como visitado para não ficar repetindo
    
    inicio_fila = 0
    tamanho_comunidade = 0
    menor_id = id_inicial
    
    while inicio_fila < len(fila):
        atual_id = fila[inicio_fila]
        inicio_fila += 1
        tamanho_comunidade += 1
        
        # O menor ID define o nome da comunidade
        if atual_id < menor_id:
            menor_id = atual_id
        
        nome_usuario = ids_para_nomes[atual_id]
        if nome_usuario is None:
            continue
        
        ficha = tabela.social_buscar(nome_usuario)
        if ficha is None:
            continue
        
        # Pega quem segue o usuário e quem o usuário segue para colocar na comunidade
        seguidores = ficha[2] if ficha[2] is not None else []
        seguidos = ficha[3] if ficha[3] is not None else []
        
        # Insere todos os seguidos e seguidores na comunidade
        for vizinho_id in seguidores:
            if 0 <= vizinho_id < len(visitados) and not visitados[vizinho_id] and not None:
                visitados[vizinho_id] = True # Marca como visitado para não repitir se passar por ele na tabela
                fila.append(vizinho_id)
        
        for vizinho_id in seguidos:
            if 0 <= vizinho_id < len(visitados) and not visitados[vizinho_id] and not None:
                visitados[vizinho_id] = True
                fila.append(vizinho_id)
        
    return [tamanho_comunidade, menor_id]

def social_encontrar_comunidades(ids_para_nomes, tabela):
    # [SOCIAL-26] Le todos os IDs da rede e agrupa cada comunidade encontrada
    
    total_usuarios = len(ids_para_nomes)
    visitados = [False] * total_usuarios # Na lista de visitados, ninguém foi visitado ainda
    comunidades = [] # A lista de comunidades fica aqui como [[@usuário_com_menor_ID, quant_usuarios], ...]
    
    for usuario in range(total_usuarios):
        # Ignora os espaços vazios da tabela
        if ids_para_nomes[usuario] is None:
            continue
        
        if not visitados[usuario]:
            dados_comunidade = social_explora_comunidade(usuario, visitados, ids_para_nomes, tabela)
            comunidades.append(dados_comunidade)
    
    return comunidades

def social_ordenar_comunidades(comunidades):
    # [SOCIAL-26] Extrai as comunidades da maior para a menor
    heap = MaxHeap()
    
    for comunidade in comunidades:
        tamanho = comunidade[0]
        menor_id = comunidade[1]
        heap.social_inserir(tamanho, menor_id)
        
    comunidades_ordenadas = []
    while not heap.social_esta_vazio():
        maior = heap.social_remover_maior()
        comunidades_ordenadas.append(maior)
        
    return comunidades_ordenadas