"""Experimentos comparativos AVL × Rubro-Negra.

Usado pelo menu (main.py, opção 8) e pela geração dos slides (make_slides.py),
para que os números da apresentação sejam exatamente os do programa.
Todas as sequências usam sementes fixas: os resultados são reproduzíveis.
"""
import math
import random

from avl import AVLTree
from rbtree import RBTree

TREES = [("AVL", AVLTree), ("Rubro-Negra", RBTree)]


def scenarios(n=1000):
    return [("Crescente", list(range(1, n + 1))),
            ("Decrescente", list(range(n, 0, -1))),
            ("Não ordenada", random.Random(42).sample(range(1, 100_000), n))]


def bst_height(keys):
    """Altura de uma ABB comum (sem balanceamento) com as mesmas inserções."""
    left, right, root, h = {}, {}, None, 0
    for k in keys:
        if root is None:
            root, h = k, 1
            continue
        n, d = root, 1
        while True:
            d += 1
            side = left if k < n else right
            if n in side:
                n = side[n]
            else:
                side[n] = k
                break
        h = max(h, d)
    return h


def avg_comparisons(t):
    """Nº médio de nós visitados para encontrar uma chave existente (profundidade média)."""
    total = 0
    stack = [(t.snapshot(), 1)]
    while stack:
        n, d = stack.pop()
        if n:
            total += d
            stack += [(n[2], d + 1), (n[3], d + 1)]
    return total / t.size if t.size else 0


def _apply(t, op, k, stats):
    before = t.rotations
    ok = {"i": t.insert, "r": t.remove, "s": t.search}[op](k)
    stats["max_rot"] = max(stats["max_rot"], t.rotations - before)
    return ok


def run(n=1000, check_each=True):
    """Para cada cenário: n inserções e depois n/2 remoções aleatórias, nas duas árvores."""
    out = []
    for name, keys in scenarios(n):
        removals = random.Random(7).sample(keys, n // 2)
        row = {"cenario": name, "bst": bst_height(keys)}
        for label, cls in TREES:
            t = cls()
            st = {"max_rot": 0}
            for k in keys:
                assert _apply(t, "i", k, st)
                if check_each:
                    t.check()
            ins = {"altura": t.height(), "rot": t.rotations, "max_rot": st["max_rot"],
                   "recolor": getattr(t, "recolors", None), "comp": avg_comparisons(t)}
            r0, c0 = t.rotations, getattr(t, "recolors", 0)
            st = {"max_rot": 0}
            for k in removals:
                assert _apply(t, "r", k, st)
                if check_each:
                    t.check()
            rem = {"altura": t.height(), "rot": t.rotations - r0, "max_rot": st["max_rot"],
                   "recolor": getattr(t, "recolors", c0) - c0 if hasattr(t, "recolors") else None}
            row[label] = {"ins": ins, "rem": rem}
        out.append(row)
    return out


def black_friday_ops(n=20_000, centers=10, window=2_000, seed=3):
    """Carga simulada: IDs sequenciais por centro de distribuição chegando intercalados
    ("quase em ordem"); encomendas antigas despachadas (removidas) e consultas aleatórias."""
    r = random.Random(seed)
    seq, ops, live = [0] * centers, [], []
    for _ in range(n):
        c = r.randrange(centers)
        seq[c] += 1
        k = c * 1_000_000 + seq[c]
        ops.append(("i", k))
        live.append(k)
        if len(live) > window:
            ops.append(("r", live.pop(r.randrange(len(live) // 4))))
        if r.random() < 0.5:
            ops.append(("s", r.choice(live)))
    return ops


def black_friday():
    ops = black_friday_ops()
    res = {"ops": len(ops), "ins": sum(o == "i" for o, _ in ops),
           "rem": sum(o == "r" for o, _ in ops), "busca": sum(o == "s" for o, _ in ops)}
    for label, cls in TREES:
        t, st = cls(), {"max_rot": 0}
        for i, (op, k) in enumerate(ops):
            _apply(t, op, k, st)
            if i % 1000 == 0:
                t.check()
        t.check()
        res[label] = {"altura": t.height(), "rot": t.rotations, "max_rot": st["max_rot"],
                      "recolor": getattr(t, "recolors", None), "comp": avg_comparisons(t)}
    return res


def print_report(n=1000):
    print(f"\n=== {n} inserções e depois {n // 2} remoções (propriedades verificadas após cada operação) ===")
    print(f"{'Cenário':<14}{'Árvore':<13}{'Alt.':>5}{'Rot.ins':>9}{'Comp.méd':>10}"
          f"{'Alt.após rem':>14}{'Rot.rem':>9}{'Máx rot/op':>12}")
    for row in run(n):
        for label, _ in TREES:
            i, r = row[label]["ins"], row[label]["rem"]
            print(f"{row['cenario']:<14}{label:<13}{i['altura']:>5}{i['rot']:>9}{i['comp']:>10.2f}"
                  f"{r['altura']:>14}{r['rot']:>9}{max(i['max_rot'], r['max_rot']):>12}")
        print(f"{'':<14}{'ABB comum':<13}{row['bst']:>5}")
    print(f"Limites teóricos: AVL ≈ 1,44·log2(n+2) = {1.44 * math.log2(n + 2):.1f} | "
          f"RB = 2·log2(n+1) = {2 * math.log2(n + 1):.1f}")
    bf = black_friday()
    print(f"\n=== Simulação Black Friday: {bf['ops']} operações "
          f"({bf['ins']} inserções, {bf['rem']} remoções, {bf['busca']} buscas) ===")
    for label, _ in TREES:
        d = bf[label]
        print(f"{label:<13} altura={d['altura']:<3} rotações={d['rot']:<6} máx rot/op={d['max_rot']}"
              f"  comp.méd={d['comp']:.2f}" + (f"  recolorações={d['recolor']}" if d["recolor"] is not None else ""))


if __name__ == "__main__":
    print_report()