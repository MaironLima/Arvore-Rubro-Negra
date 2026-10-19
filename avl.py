"""Árvore AVL com contador de rotações (mesma interface de rbtree.RBTree).

Decisões (iguais às da Rubro-Negra, para comparação justa):
- valores repetidos: inserção recusada (retorna False), árvore inalterada;
- busca/remoção de valor inexistente: retorna None/False, árvore inalterada;
- remoção com dois filhos usa o sucessor em ordem;
- altura medida em nós (árvore vazia = 0, folha = 1);
- rotação dupla conta como 2 rotações.
"""


class Node:
    __slots__ = ("key", "left", "right", "h")

    def __init__(self, key):
        self.key, self.left, self.right, self.h = key, None, None, 1


def _h(n):
    return n.h if n else 0


def _bf(n):
    """Fator de balanceamento = altura(esq) - altura(dir)."""
    return _h(n.left) - _h(n.right)


def _update(n):
    n.h = 1 + max(_h(n.left), _h(n.right))


class AVLTree:
    def __init__(self):
        self.root = None
        self.rotations = 0
        self.size = 0

    # ---------- rotações ----------
    def _rot_right(self, y):
        x = y.left
        y.left, x.right = x.right, y
        _update(y); _update(x)
        self.rotations += 1
        return x

    def _rot_left(self, x):
        y = x.right
        x.right, y.left = y.left, x
        _update(x); _update(y)
        self.rotations += 1
        return y

    def _rebalance(self, n):
        """Atualiza a altura e aplica a rotação necessária (LL, LR, RR, RL)."""
        _update(n)
        bf = _bf(n)
        if bf > 1:  # pesado à esquerda
            if _bf(n.left) < 0:  # caso LR: rotação dupla
                n.left = self._rot_left(n.left)
            return self._rot_right(n)  # caso LL
        if bf < -1:  # pesado à direita
            if _bf(n.right) > 0:  # caso RL: rotação dupla
                n.right = self._rot_right(n.right)
            return self._rot_left(n)  # caso RR
        return n

    # ---------- busca ----------
    def search(self, key):
        n = self.root
        while n and n.key != key:
            n = n.left if key < n.key else n.right
        return n

    # ---------- inserção ----------
    def insert(self, key):
        if self.search(key):
            return False  # repetido: recusado
        self.root = self._insert(self.root, key)
        self.size += 1
        return True

    def _insert(self, n, key):
        if n is None:
            return Node(key)
        if key < n.key:
            n.left = self._insert(n.left, key)
        else:
            n.right = self._insert(n.right, key)
        return self._rebalance(n)

    # ---------- remoção ----------
    def remove(self, key):
        if not self.search(key):
            return False  # inexistente: nada muda
        self.root = self._remove(self.root, key)
        self.size -= 1
        return True

    def _remove(self, n, key):
        if key < n.key:
            n.left = self._remove(n.left, key)
        elif key > n.key:
            n.right = self._remove(n.right, key)
        else:
            if n.left is None or n.right is None:  # 0 ou 1 filho
                return n.left or n.right
            s = n.right  # dois filhos: sucessor em ordem
            while s.left:
                s = s.left
            n.key = s.key
            n.right = self._remove(n.right, s.key)
        return self._rebalance(n)

    # ---------- percursos / visualização ----------
    def inorder(self):
        out, stack, n = [], [], self.root
        while stack or n:
            while n:
                stack.append(n)
                n = n.left
            n = stack.pop()
            out.append(n.key)
            n = n.right
        return out

    def height(self):
        return _h(self.root)

    def pretty(self):
        lines = []

        def go(n, prefix, is_left):
            if n is None:
                return
            go(n.right, prefix + ("│   " if is_left else "    "), False)
            lines.append(prefix + ("└── " if is_left else "┌── ") + f"{n.key}(fb={_bf(n)})")
            go(n.left, prefix + ("    " if is_left else "│   "), True)

        if self.root:
            go(self.root.right, "", False)
            lines.append(f"{self.root.key}(fb={_bf(self.root)})")
            go(self.root.left, "", True)
        return "\n".join(lines) or "(árvore vazia)"

    def snapshot(self, n="root"):
        n = self.root if n == "root" else n
        if n is None:
            return None
        return (n.key, _bf(n), self.snapshot(n.left), self.snapshot(n.right))

    # ---------- verificação das propriedades ----------
    def check(self):
        """Retorna a altura; levanta AssertionError se alguma propriedade falhar."""

        def go(n, lo, hi):
            if n is None:
                return 0
            assert (lo is None or n.key > lo) and (hi is None or n.key < hi), "ordem BST"
            hl, hr = go(n.left, lo, n.key), go(n.right, n.key, hi)
            assert abs(hl - hr) <= 1, f"desbalanceado em {n.key} (fb={hl - hr})"
            assert n.h == 1 + max(hl, hr), "altura armazenada incorreta"
            return n.h

        h = go(self.root, None, None)
        assert len(self.inorder()) == self.size
        return h


if __name__ == "__main__":
    import random

    t = AVLTree()
    assert t.search(1) is None and not t.remove(1) and t.check() == 0
    keys = random.Random(1).sample(range(10_000), 2_000)
    for k in keys:
        assert t.insert(k)
        t.check()
    assert not t.insert(keys[0])
    for k in keys[::2]:
        assert t.remove(k)
        t.check()
    assert t.inorder() == sorted(keys[1::2])
    print("ok", t.height(), t.rotations)