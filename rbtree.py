"""Árvore Rubro-Negra (CLRS, cap. 13) com contadores de rotações e recolorações.

Decisões:
- valores repetidos: inserção recusada (retorna False), árvore inalterada;
- busca/remoção de valor inexistente: retorna None/False, árvore inalterada;
- folhas são um sentinela NIL único (sempre preto).
"""
RED, BLACK = "R", "B"


class Node:
    __slots__ = ("key", "color", "left", "right", "parent")

    def __init__(self, key, color, nil=None):
        self.key, self.color = key, color
        self.left = self.right = self.parent = nil


class RBTree:
    def __init__(self):
        self.NIL = Node(None, BLACK)
        self.root = self.NIL
        self.rotations = 0
        self.recolors = 0
        self.size = 0

    # ---------- utilidades ----------
    def _paint(self, n, color):
        if n is not self.NIL and n.color != color:
            self.recolors += 1
        n.color = color

    def _rotate_left(self, x):
        y = x.right
        x.right = y.left
        if y.left is not self.NIL:
            y.left.parent = x
        self._replace_child(x, y)
        y.left, x.parent = x, y
        self.rotations += 1

    def _rotate_right(self, x):
        y = x.left
        x.left = y.right
        if y.right is not self.NIL:
            y.right.parent = x
        self._replace_child(x, y)
        y.right, x.parent = x, y
        self.rotations += 1

    def _replace_child(self, old, new):
        new.parent = old.parent
        if old.parent is self.NIL:
            self.root = new
        elif old is old.parent.left:
            old.parent.left = new
        else:
            old.parent.right = new

    # ---------- busca ----------
    def search(self, key):
        n = self.root
        while n is not self.NIL and n.key != key:
            n = n.left if key < n.key else n.right
        return None if n is self.NIL else n

    # ---------- inserção ----------
    def insert(self, key):
        parent, cur = self.NIL, self.root
        while cur is not self.NIL:
            if key == cur.key:
                return False  # repetido: recusado
            parent, cur = cur, (cur.left if key < cur.key else cur.right)
        z = Node(key, RED, self.NIL)
        z.parent = parent
        if parent is self.NIL:
            self.root = z
        elif key < parent.key:
            parent.left = z
        else:
            parent.right = z
        self.size += 1
        self._insert_fixup(z)
        return True

    def _insert_fixup(self, z):
        while z.parent.color == RED:
            g = z.parent.parent
            left_side = z.parent is g.left
            uncle = g.right if left_side else g.left
            if uncle.color == RED:  # caso 1: só recoloração
                self._paint(z.parent, BLACK)
                self._paint(uncle, BLACK)
                self._paint(g, RED)
                z = g
                continue
            if left_side:
                if z is z.parent.right:  # caso 2: triângulo -> linha
                    z = z.parent
                    self._rotate_left(z)
                self._paint(z.parent, BLACK)  # caso 3: linha
                self._paint(g, RED)
                self._rotate_right(g)
            else:
                if z is z.parent.left:
                    z = z.parent
                    self._rotate_right(z)
                self._paint(z.parent, BLACK)
                self._paint(g, RED)
                self._rotate_left(g)
        self._paint(self.root, BLACK)

    # ---------- remoção ----------
    def _transplant(self, u, v):
        if u.parent is self.NIL:
            self.root = v
        elif u is u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def remove(self, key):
        z = self.search(key)
        if z is None:
            return False  # inexistente: nada muda
        y, y_color = z, z.color
        if z.left is self.NIL:
            x = z.right
            self._transplant(z, z.right)
        elif z.right is self.NIL:
            x = z.left
            self._transplant(z, z.left)
        else:  # dois filhos: sucessor em ordem
            y = z.right
            while y.left is not self.NIL:
                y = y.left
            y_color = y.color
            x = y.right
            if y.parent is z:
                x.parent = y
            else:
                self._transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self._transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color  # herda a posição, não conta como recoloração de ajuste
        self.size -= 1
        if y_color == BLACK:
            self._delete_fixup(x)
        return True

    def _delete_fixup(self, x):
        while x is not self.root and x.color == BLACK:
            left_side = x is x.parent.left
            w = x.parent.right if left_side else x.parent.left
            rot_a = self._rotate_left if left_side else self._rotate_right
            rot_b = self._rotate_right if left_side else self._rotate_left
            near = (lambda n: n.left) if left_side else (lambda n: n.right)
            far = (lambda n: n.right) if left_side else (lambda n: n.left)
            if w.color == RED:  # caso 1: irmão vermelho
                self._paint(w, BLACK)
                self._paint(x.parent, RED)
                rot_a(x.parent)
                w = x.parent.right if left_side else x.parent.left
            if near(w).color == BLACK and far(w).color == BLACK:  # caso 2
                self._paint(w, RED)
                x = x.parent
            else:
                if far(w).color == BLACK:  # caso 3
                    self._paint(near(w), BLACK)
                    self._paint(w, RED)
                    rot_b(w)
                    w = x.parent.right if left_side else x.parent.left
                self._paint(w, x.parent.color)  # caso 4
                self._paint(x.parent, BLACK)
                self._paint(far(w), BLACK)
                rot_a(x.parent)
                x = self.root
        self._paint(x, BLACK)

    # ---------- percursos / visualização ----------
    def inorder(self):
        out, stack, n = [], [], self.root
        while stack or n is not self.NIL:
            while n is not self.NIL:
                stack.append(n)
                n = n.left
            n = stack.pop()
            out.append(n.key)
            n = n.right
        return out

    def height(self, n=None):
        """Altura em nós (árvore vazia = 0)."""
        n = self.root if n is None else n
        if n is self.NIL:
            return 0
        return 1 + max(self.height(n.left), self.height(n.right))

    def pretty(self):
        lines = []

        def go(n, prefix, is_left):
            if n is self.NIL:
                return
            go(n.right, prefix + ("│   " if is_left else "    "), False)
            lines.append(prefix + ("└── " if is_left else "┌── ") + f"{n.key}[{n.color}]")
            go(n.left, prefix + ("    " if is_left else "│   "), True)

        if self.root is not self.NIL:
            go(self.root.right, "", False)
            lines.append(f"{self.root.key}[{self.root.color}]")
            go(self.root.left, "", True)
        return "\n".join(lines) or "(árvore vazia)"

    def snapshot(self, n=None):
        n = self.root if n is None else n
        if n is self.NIL:
            return None
        return (n.key, n.color, self.snapshot(n.left), self.snapshot(n.right))

    # ---------- verificação das propriedades ----------
    def check(self):
        """Retorna a altura negra; levanta AssertionError se alguma propriedade falhar."""
        assert self.root.color == BLACK, "raiz não é preta"
        assert self.NIL.color == BLACK

        def go(n, lo, hi):
            if n is self.NIL:
                return 1
            assert (lo is None or n.key > lo) and (hi is None or n.key < hi), "ordem BST"
            if n.color == RED:
                assert n.left.color == BLACK and n.right.color == BLACK, "vermelho com filho vermelho"
            bl, br = go(n.left, lo, n.key), go(n.right, n.key, hi)
            assert bl == br, "altura negra diferente"
            return bl + (n.color == BLACK)

        bh = go(self.root, None, None)
        assert self.inorder() == sorted(self.inorder()) and len(self.inorder()) == self.size
        return bh


if __name__ == "__main__":
    import random

    t = RBTree()
    assert t.search(1) is None and not t.remove(1) and t.check() == 1
    keys = random.Random(1).sample(range(10_000), 2_000)
    for k in keys:
        assert t.insert(k)
        t.check()
    assert not t.insert(keys[0])
    for k in keys[::2]:
        assert t.remove(k)
        t.check()
    assert t.inorder() == sorted(keys[1::2])
    print("ok", t.height(), t.rotations, t.recolors)
