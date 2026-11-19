Nomes: Dione e Ítalo


Parte da tabela hash:
    O que foi feito:
        Fizemos uma classe que recebe um número de tamanho baseado na quantidade usuários, garanti que ele seria pelo menos 30% maior que a quantidade original para garantir que cada usuário tenha sua própria linha na lista da tabela hash (o que ainda não é tão garantido), como fiz um algoritmo por "Encadeamento separado", eles ainda tem chance de ficar na mesma linha, mas suas informações ainda ficam seperadas de forma que elas podem ser pesquisadas sem uma afetar a outra.

        O algoritmo de calculo para decidir quem fica em qual linha foi baseado no DJB2, que usa o deslocamento de bits para um calculo mais rápido, no meu código, ele lê cada nome de usuário na coluna "usuario", separa suas letras, transforma em um número que é multiplicado por 33 e juntado para formar a sua linha, ainda é possível haver mais de 1 usuário em cada linha, mas ainda é difícil.

        Depois de organizado a tabela, é gerado um arquivo json com os dados, onde a busca pega os dados "crus" para utilizá-los em calculos e na api.

    Como foi feito:
        Colocamos a classe responsável pela tabela em um arquivo separado chamado tabelaHash.py, que é chamada pelo aedlib para organizar os dados, todos os dados organizados são colocados em um arquivo JSON chamado "backupTabela.json", que é criado na primeira vez em que o "main.py" é ligado, após isso, os dados sempre pode ser visualizados sem precisar ficar "criando" uma tabela hash do zero toda vez que for fazer uma consulta.
    
    Escolhas tomadas e por quê:
        Optamos por usar a função hash do Daniel J. Bernstein, que é o mais famosinho e simples, que só multiplica o número de cada letra por 33 e depois junta para selecionar a linha, simples.
        Tratamos as colisões com "Encadeamento separado", podem ficar na mesma linha, mas ainda serão listas diferentes dentro da mesma lista.
        E escolhi 26003 pois era o numero primo mais próximo de 130% da quantidade de dados que temos, assim, temos uma folga e números compostos tem o habito de terem mais linhas vazias enquanto outra linhas ficam super-lotadas, enquanto tamanhos de números primos tem mais capacidade de dar linhas melhores distribuídas

    Complexidade:
        O(1) nas buscas e na função hash, pois ele pega pelo código hash da linha exata de onde estão ou vão ficar informações.
        O(n) na criação  da tabela, já que ele passa linha por linha mesmo que ela fique vazia para criar o json, mas não é um problema por ele só ter que fazer uma vez...
    
    Testes:
        Iniciando pela primeira vez (criando o json do zero):

        Iniciando pela segunda vez (pegando o json pronto):

        Testando busca por usuários na mesma linha do json:
        