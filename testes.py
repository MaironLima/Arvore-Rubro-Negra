"""Testes exigidos no enunciado, executados com os MESMOS dados nas duas árvores.

Uso: python3 testes.py   (termina com código 1 se algum teste falhar)
"""
import random
import sys

from experimentos import TREES, scenarios


def casos(cls):
    """Cada caso retorna (descrição, passou?)."""
    r = []

    # inserção crescente, decrescente e não ordenada, verificando após cada inserção
    for nome, ks in scenarios(1000):
        t = cls()
        ok = True
        for k in ks:
            ok &= t.insert(k)
            t.check()
        r.append((f"Inserção {nome.lower()} (1000 IDs)", ok and t.inorder() == sorted(ks)))

    t = cls()
    for k in [40, 20, 60, 10, 30, 50, 70, 25, 35, 65]:
        t.insert(k)

    # busca
    r.append(("Busca de existentes (25, 40, 70)", all(t.search(k) for k in (25, 40, 70))))
    r.append(("Busca de inexistentes (0, 33, 99)", not any(t.search(k) for k in (0, 33, 99))))

    # remoções com diferentes configurações de filhos
    def remove_ok(k):
        before = t.inorder()
        ok = t.remove(k)
        t.check()
        return ok and t.inorder() == [x for x in before if x != k]

    def n_children(k, n="root"):
        n = t.snapshot() if n == "root" else n
        if n[0] == k:
            return (n[2] is not None) + (n[3] is not None)
        return n_children(k, n[2] if k < n[0] else n[3])

    for desc, k, filhos in [("folha", 35, 0), ("nó com 1 filho", 70, 1), ("nó com 2 filhos", 20, 2)]:
        r.append((f"Remoção de {desc} ({k})", n_children(k) == filhos and remove_ok(k)))
    r.append(("Remoção da raiz", remove_ok(t.snapshot()[0])))

    # remoção de inexistente
    snap, rot = t.snapshot(), t.rotations
    r.append(("Remoção de inexistente (999)", not t.remove(999) and t.snapshot() == snap and t.rotations == rot))

    # inserção repetida
    size, snap = t.size, t.snapshot()
    r.append(("Inserção de ID repetido (25)", not t.insert(25) and t.size == size and t.snapshot() == snap))

    # árvore vazia
    e = cls()
    r.append(("Árvore vazia: busca, remoção, percurso, altura",
              e.search(1) is None and not e.remove(1) and e.inorder() == [] and e.height() == 0
              and e.pretty() == "(árvore vazia)"))

    # árvore com um elemento
    u = cls()
    u.insert(7)
    u.check()
    ok = u.height() == 1 and u.search(7) and u.remove(7) and u.size == 0 and u.height() == 0
    r.append(("Árvore com 1 elemento: inserir, buscar, remover", bool(ok)))

    # remoções aleatórias com verificação após cada uma
    for nome, ks in scenarios(1000):
        t = cls()
        for k in ks:
            t.insert(k)
        for k in random.Random(7).sample(ks, 500):
            t.remove(k)
            t.check()
        r.append((f"500 remoções após inserção {nome.lower()}", t.size == 500))
    return r


def main():
    falhas = 0
    for label, cls in TREES:
        print(f"\n=== {label} ===")
        for desc, ok in casos(cls):
            print(f"  [{'OK' if ok else 'FALHOU'}] {desc}")
            falhas += not ok
    print(f"\n{'Todos os testes passaram.' if not falhas else f'{falhas} teste(s) falharam.'}")
    print("Propriedades verificadas com check() após cada inserção e remoção "
          "(AVL: |fb| ≤ 1 e alturas; RB: raiz preta, sem vermelho-vermelho, mesma altura negra).")
    return falhas


if __name__ == "__main__":
    sys.exit(1 if main() else 0)