"""
Atividade Final - AED II - Rede Social
Ponto de partida em Python. Leia o README.md na raiz do repositório.

Este arquivo apenas carrega os dados. Todo o resto é com você:
crie suas próprias estruturas (hash, AVL, heap, grafo, ordenação)
em quantos arquivos quiser dentro desta pasta.
"""
from aedlib import social_inicializar_tabela_hash, social_mapeia_ids, social_recomendacoes, social_obter_comunidades  # biblioteca base do projeto (obrigatória - não remova)

def buscar_perfil(tabela_usuarios, id_para_nome, maior_id):
    entrada = input("Digite o @username para buscar: ").strip()
    if not entrada:
        return

    # Chama o método da sua classe TabelaHash para exibir os dados
    ficha = tabela_usuarios.social_buscar(entrada)

    if ficha is not None:
        # Garante que o @ apareça no título mesmo se você digitou sem ele
        user_exibicao = entrada if entrada.startswith("@") else f"@{entrada}"

        print("\n" + "=" * 40)
        print(f" PERFIL ENCONTRADO: {user_exibicao}")
        print("=" * 40)
        print(f" Nome Completo  : {ficha[0]}")
        print(f" Data Cadastro  : {ficha[1]}")
        print(f" Seguidores     : {len(ficha[2])}")
        print(f" Seguindo       : {len(ficha[3])}")
        print(f" Total de Posts : {ficha[4]}")

        recomendacoes = social_recomendacoes(ficha, tabela_usuarios, id_para_nome, maior_id, limite=5)
        print("\n Sugestão de amizade:")
        if len(recomendacoes) == 0:
            print("   Nenhuma sugestão disponível no momento")
        else:
            for recomendado in recomendacoes:
                print(f"   - {recomendado[0]} ({recomendado[1]} amigos em comum)")
        print("=" * 40 + "\n")
    else:
        print(f"\n[!] Usuário '{entrada}' não encontrado na base.\n")


def exibir_comunidades(id_para_nome, tabela_usuarios):
    comunidades = social_obter_comunidades(id_para_nome, tabela_usuarios)

    print("\n" + "=" * 40)
    print(f" COMUNIDADES DA REDE")
    print("=" * 40)

    if len(comunidades) == 0:
        print(" Nenhuma comunidade encontrada.")
    else:
        isolados = 0
        for i in range(len(comunidades)):
            nome_lider = comunidades[i][0]
            tamanho = comunidades[i][1]
            if tamanho >= 2:
                print(f" {i + 1}ª Comunidade | Representante: {nome_lider} | Membros: {tamanho}")
            else:
                isolados += 1

    total_reais = len(comunidades) - isolados
    print("-" * 40)
    print(f" Total de comunidades    : {total_reais}")
    print(f" Usuários isolados       : {isolados}")
    print("=" * 40 + "\n")


def main():
    print("Iniciando sistema da Rede Social...")
    # Na 1ª execução, lê os CSVs e gera o backup_tabela.json.
    # Nas próximas, carrega instantaneamente do JSON.
    tabela_usuarios = social_inicializar_tabela_hash()
    id_para_nome, maior_id = social_mapeia_ids(tabela_usuarios)
    print(f"Base carregada com sucesso! ({tabela_usuarios.quantidade_itens} usuários prontos)\n")

    while True:
        print("-" * 40)
        print(" 1 - Buscar perfil de usuário")
        print(" 2 - Listar comunidades da rede")
        print(" 0 - Sair")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "0":
            print("Encerrando o sistema...")
            break
        elif opcao == "1":
            buscar_perfil(tabela_usuarios, id_para_nome, maior_id)
        elif opcao == "2":
            exibir_comunidades(id_para_nome, tabela_usuarios)
        else:
            print("\n[!] Opção inválida.\n")

    # TODO: construir as estruturas e implementar os comandos descritos no README.


if __name__ == "__main__":
    main()
