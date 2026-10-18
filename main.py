"""Menu interativo da Árvore Rubro-Negra — índice de IDs de encomendas."""
import math
import random
import sys

from rbtree import RBTree

MENU = """
===== Índice de Encomendas (Árvore Rubro-Negra) =====
 1) Inserir ID(s)          5) Imprimir árvore
 2) Remover ID             6) Métricas (altura, rotações...)
 3) Buscar ID              7) Verificar propriedades
 4) Percurso em ordem      8) Executar experimentos
 0) Sair
"""


def read_ints(prompt):
    while True:
        try:
            return [int(x) for x in input(prompt).replace(",", " ").split()]
        except ValueError:
            print("  Digite apenas números inteiros.")


def experiments(n=1000):
    cenarios = [("Crescente", list(range(1, n + 1))),
                ("Decrescente", list(range(n, 0, -1))),
                ("Não ordenada", random.Random(42).sample(range(1, 100_000), n))]
    print(f"\n{'Cenário':<14}{'Altura':>8}{'Alt.negra':>11}{'Rotações':>10}{'Recolor.':>10}")
    for nome, ids in cenarios:
        t = RBTree()
        for k in ids:
            t.insert(k)
        bh = t.check()
        print(f"{nome:<14}{t.height():>8}{bh:>11}{t.rotations:>10}{t.recolors:>10}")
    print(f"Limite teórico 2·log2(n+1) = {2 * math.log2(n + 1):.1f}")


def main():
    t = RBTree()
    while True:
        print(MENU)
        op = input("Opção: ").strip()
        if op == "1":
            for k in read_ints("  IDs (separados por espaço): "):
                print(f"  {k}: " + ("inserido" if t.insert(k) else "já existe (ignorado)"))
        elif op == "2":
            for k in read_ints("  ID: ")[:1]:
                print("  removido" if t.remove(k) else "  ID não encontrado")
        elif op == "3":
            for k in read_ints("  ID: ")[:1]:
                print("  encontrado" if t.search(k) else "  ID não encontrado")
        elif op == "4":
            print("  " + (" ".join(map(str, t.inorder())) or "(árvore vazia)"))
        elif op == "5":
            print(t.pretty())
        elif op == "6":
            print(f"  nós = {t.size}  altura = {t.height()}  altura negra = {t.check()}"
                  f"  rotações = {t.rotations}  recolorações = {t.recolors}")
        elif op == "7":
            try:
                t.check()
                print("  OK: todas as propriedades da Rubro-Negra são válidas")
            except AssertionError as e:
                print(f"  ERRO: {e}")
        elif op == "8":
            experiments()
        elif op == "0":
            return
        else:
            print("  Opção inválida.")


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        sys.exit(0)