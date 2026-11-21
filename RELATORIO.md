# Relatório

**Autores:** Dione e Ítalo

---

## Parte da tabela hash

### 1. O que foi feito

Criamos uma classe que recebe um tamanho baseado na quantidade de usuários, garantindo que ele seja **pelo menos 30% maior** que a quantidade original. Com isso, buscamos dar a cada usuário a sua própria linha na tabela hash (o que ainda não é totalmente garantido). Como o algoritmo usa **encadeamento separado**, dois usuários ainda podem cair na mesma linha, mas as informações de cada um ficam separadas, de modo que podem ser pesquisadas sem que uma afete a outra.

O cálculo que decide em qual linha cada usuário fica é baseado no **DJB2**, que usa deslocamento de bits para um cálculo mais rápido. No nosso código, o processo é:

1. Lê o nome de cada usuário na coluna `usuario`;
2. Separa as letras do nome;
3. Transforma cada letra em um número, multiplica por 33 e combina os resultados;
4. O valor final define a linha do usuário.

Ainda é possível haver mais de um usuário por linha, mas isso é difícil de acontecer.

Depois que a tabela é organizada, é gerado um arquivo JSON com os dados. A busca lê esses dados "crus" para utilizá-los em cálculos e na API.

### 2. Como foi feito

- **Estrutura:** as funções principais para criar a tabela hash ficam em um arquivo separado, `tabelaHash.py`, chamado pelo `aedlib` para organizar os dados. A classe é iniciada com um tamanho específico, guarda a quantidade de itens da tabela e monta o vetor de listas com as informações dos usuários.
- **Função hash (`função_hash`):** optamos pelo algoritmo DJB2. O cálculo começa com um valor inicial (2381) e, para cada letra do nome de usuário, multiplica o valor acumulado por 33 e soma o código da letra. Para que a multiplicação seja mais rápida, os bits são deslocados em 5 casas (o que equivale a multiplicar por 32) e o valor anterior é somado, completando o ×33. O resultado, ajustado ao tamanho da tabela (resto da divisão), é o número da linha onde as informações do usuário serão guardadas.
- **Inserção:** a função de inserir percorre cada informação espalhada pelos CSVs, relacionando-as pelos IDs que aparecem. Cada usuário é guardado como um par chave-valor: a chave é o nome de usuário e o valor é a lista com suas informações. Formato e exemplo:
  - `[@nome_de_usuario, [Nome, data_de_cadastro, seguidores, seguidos, posts, ID]]`
  - `[@pedrinho1, ["Pedrinho", "20/10/2020", 5, 10, 354, 4821]]`
- **Salvamento:** o tamanho, a quantidade de itens e a tabela (percorrida por um laço de repetição que lê cada linha) são guardados no `backupTabela.json` pela função `salvar_json`. O arquivo é criado na primeira vez em que o `main.py` é executado.
- **Reaproveitamento:** nas execuções seguintes, os dados são lidos direto do JSON, sem precisar criar a tabela hash do zero a cada consulta.
- **Busca:** a função de busca procura pelo nome de usuário e, se o "@" (arroba) for esquecido, ela o completa. Em seguida, usa o código hash para ir direto à linha do JSON onde ficam as informações do usuário. Como pode haver mais de um usuário na mesma linha, ela confere qual deles é o usuário buscado pelo nome de usuário.

### 3. Escolhas tomadas e por quê

- **Função hash DJB2 (Daniel J. Bernstein):** é uma das mais populares e simples. Basicamente multiplica o número de cada letra por 33 e combina os valores para selecionar a linha.
- **Encadeamento separado para colisões:** usuários podem ficar na mesma linha, mas ficam em listas diferentes dentro da mesma posição da tabela.
- **Tamanho 26003:** é o número primo mais próximo de 130% da quantidade de dados que temos, o que nos dá uma folga. Números compostos costumam deixar mais linhas vazias enquanto outras ficam superlotadas, já tamanhos primos tendem a distribuir melhor os dados entre as linhas.
- **JSON:** Só usei para carregar o arquivo, pesquisei como fazia para criar uma função para salvar as informações em um JSON até perceber que JSON não estáva proibido de usar, foi a melhor forma que eu encontrei para deixar a tabela organizada e funcional, a outra forma era usar os CSVs, que ia aumentar o tempo de carregamento.

### 4. Complexidade

| Operação | Complexidade | Justificativa |
|---|---|---|
| Busca | O(1) | Usa o código hash para ir direto à linha onde as informações estão (ou vão ficar). |
| Função hash | O(1) | Calcula a linha diretamente, sem percorrer a tabela. |
| Criação da tabela | O(n) | Passa linha por linha, mesmo as vazias, para gerar o JSON. Não é um problema, pois isso só precisa ser feito uma vez. |

### 5. Testes

#### Teste 1 — Primeira execução (criando o JSON do zero)

**Objetivo:** verificar a criação do `backupTabela.json` na primeira vez que o `main.py` é executado.

![Teste 1 — Primeira execução](imgs/teste1.png)

*Figura 1 — Primeira execução, com a criação do JSON do zero.*

#### Teste 2 — Segunda execução (usando o JSON pronto)

**Objetivo:** verificar que, nas execuções seguintes, os dados são carregados do JSON já existente.

![Teste 2 — Segunda execução](imgs/teste2.png)

*Figura 2 — Segunda execução, utilizando o JSON pronto.*

#### Teste 3 — Busca de usuários na mesma linha do JSON

**Objetivo:** verificar que usuários que caem na mesma linha continuam sendo pesquisados de forma independente.

![Teste 3 — Busca dos usuários na mesma linha](imgs/teste3.png)

*Figura 3 — Busca dos usuário que compartilham a mesma linha.*

![Teste 4 — Mostra usuários na mesma linha pelo json](imgs/teste4.png)

*Figura 4 — mostra os usuários que compartilha a mesma linha no json.*
