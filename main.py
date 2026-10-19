"""Menu interativo — índice de IDs de encomendas com Árvore AVL ou Rubro-Negra.

Autor: Mairon Lima de Melo — IMD0039 Estruturas de Dados Básicas II (IMD/UFRN)
"""
import sys

from avl import AVLTree
from experimentos import print_report
from rbtree import RBTree

TIPOS = {"1": ("AVL", AVLTree), "2": ("Rubro-Negra", RBTree)}

MENU = """
===== Índice de Encomendas ({nome}) =====
 1) Inserir ID(s)          5) Imprimir árvore
 2) Remover ID             6) Métricas (altura, rotações...)
 3) Buscar ID              7) Verificar propriedades
 4) Percurso em ordem      8) Experimentos AVL × Rubro-Negra
 9) Trocar tipo de árvore  0) Sair
"""


def read_ints(prompt):
    while True:
        try:
            return [int(x) for x in input(prompt).replace(",", " ").split()]
        except ValueError:
            print("  Digite apenas números inteiros.")


def escolher_arvore():
    while True:
        op = input("Tipo de árvore — 1) AVL  2) Rubro-Negra: ").strip()
        if op in TIPOS:
            nome, cls = TIPOS[op]
            print(f"  Usando árvore {nome} (vazia).")
            return nome, cls()
        print("  Opção inválida.")


def metricas(t):
    txt = f"  nós = {t.size}  altura = {t.height()}  rotações = {t.rotations}"
    if isinstance(t, RBTree):
        txt += f"  altura negra = {t.check()}  recolorações = {t.recolors}"
    return txt


def main():
    nome, t = escolher_arvore()
    while True:
        print(MENU.format(nome=nome))
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
            print("  Legenda: " + ("[R] vermelho, [B] preto" if isinstance(t, RBTree)
                                   else "fb = fator de balanceamento (altura esq. − altura dir.)"))
            print(t.pretty())
        elif op == "6":
            print(metricas(t))
        elif op == "7":
            try:
                t.check()
                print(f"  OK: todas as propriedades da {nome} são válidas")
            except AssertionError as e:
                print(f"  ERRO: {e}")
        elif op == "8":
            print_report()
        elif op == "9":
            nome, t = escolher_arvore()
        elif op == "0":
            return
        else:
            print("  Opção inválida.")


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        sys.exit(0)