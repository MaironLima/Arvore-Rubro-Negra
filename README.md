# Amazon Engineering Challenge — Árvore Rubro-Negra

Protótipo de um índice em memória para **identificadores de encomendas** (cenário de Black Friday), implementado com uma **Árvore Rubro-Negra**. Garante busca, inserção e remoção em **O(log n)**, mesmo quando os IDs chegam em ordem crescente, que é o pior caso de uma árvore binária de busca (ABB/BST) comum.

Trabalho da Unidade II — IMD0039 Estruturas de Dados Básicas II (IMD/UFRN).

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `rbtree.py` | Implementação da Árvore Rubro-Negra (inserção, remoção, busca, percurso, impressão, verificação das propriedades) com autoteste |
| `main.py` | Menu interativo para usar a árvore |
| `make_slides.py` | Gera a apresentação `apresentacao_rubro_negra.pdf` (opcional) |

## Requisitos

- **Python 3.8 ou superior** (só a biblioteca padrão para `rbtree.py` e `main.py`).
- Para gerar os slides: `pip install reportlab`.

Para conferir a versão do Python:

```bash
python3 --version
```

> No Windows, use `python` ou `py` no lugar de `python3` em todos os comandos.

## Como inicializar

```bash
git clone https://github.com/MaironLima/Arvore-Rubro-Negra.git
cd Arvore-Rubro-Negra
python3 main.py
```

Não há etapa de compilação nem dependências para instalar.

## Como usar

Ao executar, aparece o menu:

```
===== Índice de Encomendas (Árvore Rubro-Negra) =====
 1) Inserir ID(s)          5) Imprimir árvore
 2) Remover ID             6) Métricas (altura, rotações...)
 3) Buscar ID              7) Verificar propriedades
 4) Percurso em ordem      8) Executar experimentos
 0) Sair
```

| Opção | O que faz |
|---|---|
| **1** | Insere um ou vários IDs de uma vez (separados por espaço ou vírgula). |
| **2** | Remove um ID. |
| **3** | Informa se o ID está na árvore. |
| **4** | Lista os IDs em ordem crescente. |
| **5** | Desenha a árvore deitada (raiz à esquerda, filhos à direita para cima). `[R]` = vermelho, `[B]` = preto. |
| **6** | Mostra nº de nós, altura, altura negra e os totais acumulados de rotações e recolorações. |
| **7** | Verifica as 5 propriedades da Rubro-Negra e a ordem de ABB. |
| **8** | Roda os experimentos com 1000 IDs (crescente, decrescente, não ordenada) e mostra altura, rotações e recolorações. |
| **0** | Sai do programa. |

### Exemplo de sessão

```
Opção: 1
  IDs (separados por espaço): 40 20 60 10 30 50 70 25
  40: inserido
  ...
Opção: 1
  IDs (separados por espaço): 30
  30: já existe (ignorado)
Opção: 2
  ID: 20
  removido
Opção: 4
  10 25 30 40 50 60 70
Opção: 5
    ┌── 70[R]
┌── 60[B]
│   └── 50[R]
40[B]
│   ┌── 30[B]
└── 25[R]
    └── 10[B]
```

### Comportamento em casos especiais

- **ID repetido:** a inserção é recusada com aviso e a árvore não muda (os IDs são únicos).
- **Busca ou remoção de ID inexistente:** mostra "ID não encontrado"; nenhuma rotação ou recoloração acontece.
- **Árvore vazia:** busca e remoção mostram "não encontrado", o percurso mostra "(árvore vazia)" e a altura é 0.
- **Entrada inválida** (letras etc.): o programa pede os números de novo.

## Testes

O `rbtree.py` tem um autoteste que insere 2000 IDs aleatórios e remove metade, verificando todas as propriedades depois de **cada** operação, além de cobrir árvore vazia, busca/remoção de inexistente e inserção de repetido:

```bash
python3 rbtree.py
```

Se tudo estiver correto, imprime uma linha começando com `ok`. Se alguma propriedade for violada, o programa para com `AssertionError` e indica qual foi.

## Usando a árvore no seu próprio código

```python
from rbtree import RBTree

t = RBTree()
t.insert(42)          # True (inserido) / False (repetido)
t.search(42)          # nó encontrado ou None
t.remove(42)          # True (removido) / False (não existia)
t.inorder()           # lista em ordem crescente
t.height()            # altura em nós (vazia = 0)
t.check()             # altura negra; AssertionError se violar alguma propriedade
t.rotations, t.recolors
print(t.pretty())
```

## Gerar a apresentação (opcional)

```bash
pip install reportlab
python3 make_slides.py
```

Gera `apresentacao_rubro_negra.pdf` com as métricas calculadas na hora pela própria implementação.