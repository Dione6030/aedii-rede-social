"""
Atividade Final - AED II - Rede Social
Ponto de partida em Python. Leia o README.md na raiz do repositório.

Este arquivo apenas carrega os dados. Todo o resto é com você:
crie suas próprias estruturas (hash, AVL, heap, grafo, ordenação)
em quantos arquivos quiser dentro desta pasta.
"""
from aedlib import social_inicializar_tabela_hash  # biblioteca base do projeto (obrigatória - não remova)


def main():
    print("Iniciando sistema da Rede Social...")
    # Na 1ª execução, lê os CSVs e gera o backup_tabela.json.
    # Nas próximas, carrega instantaneamente do JSON.
    tabela_usuarios = social_inicializar_tabela_hash()
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
            print(f" Nome Completo  : {ficha[0]}")
            print(f" Data Cadastro  : {ficha[1]}")
            print(f" Seguidores     : {len(ficha[2])}")
            print(f" Seguindo       : {len(ficha[3])}")
            print(f" Total de Posts : {ficha[4]}")
            print("=" * 40 + "\n")
        else:
            print(f"\n[!] Usuário '{entrada}' não encontrado na base.\n")

    # TODO: construir as estruturas e implementar os comandos descritos no README.


if __name__ == "__main__":
    main()
