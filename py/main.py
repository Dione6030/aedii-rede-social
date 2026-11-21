"""
Atividade Final - AED II - Rede Social
Ponto de partida em Python. Leia o README.md na raiz do repositório.

Este arquivo apenas carrega os dados. Todo o resto é com você:
crie suas próprias estruturas (hash, AVL, heap, grafo, ordenação)
em quantos arquivos quiser dentro desta pasta.
"""
from aedlib import social_inicializar_tabela_hash, social_mapeia_ids, social_recomendacoes  # biblioteca base do projeto (obrigatória - não remova)


def main():
    print("Iniciando sistema da Rede Social...")
    # Na 1ª execução, lê os CSVs e gera o backup_tabela.json.
    # Nas próximas, carrega instantaneamente do JSON.
    tabela_usuarios = social_inicializar_tabela_hash()
    id_para_nome, maior_id = social_mapeia_ids(tabela_usuarios)
    print(f"Base carregada com sucesso! ({tabela_usuarios.quantidade_itens} usuários prontos)\n")

    while True:
        print("-" * 40)
        entrada = input("Digite o @username para buscar (ou 'sair' para encerrar): ").strip()

        if entrada.lower() == "sair":
            print("Encerrando o sistema...")
            break

        if not entrada:
            continue

        # Chama o método da sua classe TabelaHash para exibir os dados
        ficha = tabela_usuarios.social_buscar(entrada)
        
        if ficha is not None:
            # Garante que o @ apareça no título mesmo se você digitou sem ele
            user_exibicao = entrada if entrada.startswith("@") else f"@{entrada}"

            print("\n" + "=" * 40)
            print(f" PERFIL ENCONTRADO: {user_exibicao}")
            print("=" * 40)
            print(f" Nome Completo         : {ficha[0]}")
            print(f" Data Cadastro         : {ficha[1]}")
            print(f" Seguidores            : {len(ficha[2])}")
            print(f" Seguindo              : {len(ficha[3])}")
            print(f" Total de Posts        : {ficha[4]}")
            
            recomendacoes = social_recomendacoes(ficha, tabela_usuarios, id_para_nome, maior_id, limite=5)
            print("\n")
            print(" Sugestão de amizade:")
            if len(recomendacoes) == 0:
                print("     Nenhuma sugestão disponivel no momento")
            else:
                for recomendado in recomendacoes:
                    print(f"     - {recomendado[0]} ({recomendado[1]} amigos em comum)")
            print("=" * 40 + "\n")
        else:
            print(f"\n[!] Usuário '{entrada}' não encontrado na base.\n")

    # TODO: construir as estruturas e implementar os comandos descritos no README.


if __name__ == "__main__":
    main()
