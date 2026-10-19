# Amazon Engineering Challenge — Árvores AVL e Rubro-Negra

Protótipo de um índice em memória para **identificadores de encomendas** (cenário de Black Friday), com duas árvores balanceadas implementadas do zero: **AVL** e **Rubro-Negra**. As duas garantem busca, inserção e remoção em **O(log n)**, mesmo quando os IDs chegam em ordem crescente, que é o pior caso de uma árvore binária de busca (ABB/BST) comum.

**Autor:** Mairon Lima de Melo
**Disciplina:** IMD0039 — Estruturas de Dados Básicas II · Trabalho da Unidade II
**Instituição:** Instituto Metrópole Digital — UFRN

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `avl.py` | Árvore AVL: inserção, remoção, busca, percurso, impressão com fator de balanceamento, verificação das propriedades, contagem de rotações |
| `rbtree.py` | Árvore Rubro-Negra: as mesmas operações, impressão com as cores e contagem de rotações e recolorações |
| `main.py` | Menu interativo: escolhe a árvore e executa as operações |
| `testes.py` | Testes do enunciado, com os mesmos dados nas duas árvores |
| `experimentos.py` | Comparação AVL × Rubro-Negra (altura, rotações, comparações por busca) e simulação de carga da Black Friday |
| `make_slides.py` | Gera a apresentação em PDF a partir dos mesmos experimentos (opcional) |

Nenhuma biblioteca pronta de árvore foi usada: o balanceamento das duas estruturas está implementado nos próprios arquivos.

## Requisitos

- **Python 3.8 ou superior**, só com a biblioteca padrão.
- **Versão compilada:** não se aplica. Python é interpretado, e os arquivos `.py` do repositório já são o programa executável.
- Opcional, só para gerar os slides: `pip install reportlab`.

> No Windows, use `python` ou `py` no lugar de `python3` em todos os comandos.

## Como inicializar

```bash
git clone https://github.com/MaironLima/Arvore-Rubro-Negra.git
cd Arvore-Rubro-Negra
python3 main.py
```

O programa pergunta primeiro qual árvore usar:

```
Tipo de árvore — 1) AVL  2) Rubro-Negra: 2
  Usando árvore Rubro-Negra (vazia).
```

## Como usar

```
===== Índice de Encomendas (Rubro-Negra) =====
 1) Inserir ID(s)          5) Imprimir árvore
 2) Remover ID             6) Métricas (altura, rotações...)
 3) Buscar ID              7) Verificar propriedades
 4) Percurso em ordem      8) Experimentos AVL × Rubro-Negra
 9) Trocar tipo de árvore  0) Sair
```

| Opção | O que faz |
|---|---|
| **1** | Insere um ou vários IDs de uma vez (separados por espaço ou vírgula). |
| **2** | Remove um ID. |
| **3** | Informa se o ID está na árvore. |
| **4** | Lista os IDs em ordem crescente. |
| **5** | Desenha a árvore deitada (raiz à esquerda). Rubro-Negra: `[R]` vermelho, `[B]` preto. AVL: `(fb=…)` mostra o fator de balanceamento. |
| **6** | Mostra nº de nós, altura e rotações acumuladas (na RB, também altura negra e recolorações). |
| **7** | Verifica as propriedades da árvore atual. |
| **8** | Roda os experimentos comparativos nas duas árvores. |
| **9** | Troca de árvore (começa uma árvore nova e vazia). |
| **0** | Sai do programa. |

### Exemplo de sessão (Rubro-Negra)

```
Opção: 1
  IDs (separados por espaço): 40 20 60 10 30 50 70 25
Opção: 1
  IDs (separados por espaço): 30
  30: já existe (ignorado)
Opção: 2
  ID: 20
  removido
Opção: 4
  10 25 30 40 50 60 70
Opção: 5
  Legenda: [R] vermelho, [B] preto
    ┌── 70[R]
┌── 60[B]
│   └── 50[R]
40[B]
│   ┌── 30[B]
└── 25[R]
    └── 10[B]
```

Com a AVL, a mesma sequência imprime `40(fb=0)`, `25(fb=0)` etc.

## Decisões de implementação

As regras são as mesmas nas duas árvores, para a comparação ser justa:

- **ID repetido:** a inserção é recusada com aviso e a árvore não muda (os IDs são únicos).
- **Busca ou remoção de ID inexistente:** mostra "ID não encontrado"; nenhuma rotação ou recoloração acontece.
- **Árvore vazia:** altura 0; busca e remoção mostram "não encontrado"; o percurso mostra "(árvore vazia)".
- **Remoção de nó com dois filhos:** usa o sucessor em ordem.
- **Altura:** medida em nós (vazia = 0, um nó = 1).
- **Contagem de rotações:** a rotação dupla da AVL (casos LR e RL) conta como 2.
- **Rubro-Negra:** usa um sentinela NIL único e preto no lugar de ponteiros nulos, o que simplifica os casos de ajuste.
- **Entrada inválida** no menu (letras etc.): o programa pede os números de novo.

## Testes

```bash
python3 testes.py
```

Executa, nas duas árvores e com os mesmos dados:

- inserção de 1000 IDs em ordem crescente, decrescente e não ordenada;
- busca de existentes e de inexistentes;
- remoção de folha, de nó com 1 filho, de nó com 2 filhos e da raiz;
- remoção de inexistente e inserção de repetido;
- operações em árvore vazia e em árvore com um elemento;
- 500 remoções aleatórias em cada cenário.

As propriedades são verificadas após **cada** inserção e remoção. Na AVL: |fb| ≤ 1 e alturas corretas. Na Rubro-Negra: raiz preta, nenhum vermelho com filho vermelho e mesma altura negra em todos os caminhos. Nas duas: ordem de ABB e contagem de nós. O programa termina com código 1 se algum teste falhar.

Cada árvore também tem um autoteste próprio: `python3 avl.py` e `python3 rbtree.py`.

## Experimentos comparativos

```bash
python3 experimentos.py
```

Mostra, para os três cenários de 1000 inserções seguidas de 500 remoções, a altura da AVL, da Rubro-Negra e da ABB comum, as rotações na inserção e na remoção, as comparações médias por busca e o máximo de rotações numa única operação. Também roda uma simulação de carga da Black Friday com cerca de 48 mil operações intercaladas. As sementes aleatórias são fixas, então os resultados são sempre os mesmos e batem com os da apresentação.

## Usando as árvores no seu próprio código

```python
from avl import AVLTree
from rbtree import RBTree

t = RBTree()          # ou AVLTree()
t.insert(42)          # True (inserido) / False (repetido)
t.search(42)          # nó encontrado ou None
t.remove(42)          # True (removido) / False (não existia)
t.inorder()           # lista em ordem crescente
t.height()            # altura em nós (vazia = 0)
t.check()             # AssertionError se alguma propriedade for violada
t.rotations           # rotações acumuladas (RBTree também tem t.recolors)
print(t.pretty())
```
