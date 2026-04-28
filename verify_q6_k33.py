from __future__ import annotations

import json
import sys
from pathlib import Path


N = 6
V = 1 << N


def parity(x: int) -> int:
    return x.bit_count() & 1


def is_q6_edge(u: int, v: int) -> bool:
    diff = u ^ v
    return diff != 0 and (diff & (diff - 1)) == 0


def cycle_lengths(edges: list[tuple[int, int]]) -> list[int]:
    adj = [[] for _ in range(V)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    if any(len(xs) != 2 for xs in adj):
        raise AssertionError("the union of two matchings is not 2-regular")

    seen = [False] * V
    lengths: list[int] = []
    for start in range(V):
        if seen[start]:
            continue
        length = 0
        prev = -1
        cur = start
        while not seen[cur]:
            seen[cur] = True
            length += 1
            nxts = adj[cur]
            nxt = nxts[0] if nxts[0] != prev else nxts[1]
            prev, cur = cur, nxt
        lengths.append(length)
    return sorted(lengths, reverse=True)


def verify(path: Path) -> None:
    data = json.loads(path.read_text())
    left = tuple(data["partition"]["left"])
    right = tuple(data["partition"]["right"])
    matchings = {
        int(color): [tuple(edge) for edge in edges]
        for color, edges in data["matchings"].items()
    }

    if sorted(matchings) != list(range(N)):
        raise AssertionError("expected colors 0..5")
    if sorted(left + right) != list(range(N)):
        raise AssertionError("partition is not a 3+3 split of colors 0..5")

    all_edges: set[tuple[int, int]] = set()
    for color, edges in matchings.items():
        if len(edges) != V // 2:
            raise AssertionError(f"color {color} does not contain 32 edges")
        covered: set[int] = set()
        for u, v in edges:
            if not (0 <= u < V and 0 <= v < V):
                raise AssertionError(f"vertex out of range in color {color}: {(u, v)}")
            if parity(u) == parity(v):
                raise AssertionError(f"edge does not cross bipartition in color {color}: {(u, v)}")
            if not is_q6_edge(u, v):
                raise AssertionError(f"not a Q6 edge in color {color}: {(u, v)}")
            e = (u, v) if u < v else (v, u)
            if e in all_edges:
                raise AssertionError(f"duplicate edge: {e}")
            all_edges.add(e)
            covered.add(u)
            covered.add(v)
        if covered != set(range(V)):
            raise AssertionError(f"color {color} is not a perfect matching")

    expected_edges = {
        (u, u ^ (1 << d)) if u < (u ^ (1 << d)) else (u ^ (1 << d), u)
        for u in range(V)
        for d in range(N)
    }
    if all_edges != expected_edges:
        raise AssertionError("the six matchings do not partition E(Q6)")

    all_pair_lengths: dict[str, list[int]] = {}
    hamilton_pairs: set[tuple[int, int]] = set()
    for a in range(N):
        for b in range(a + 1, N):
            lengths = cycle_lengths(matchings[a] + matchings[b])
            all_pair_lengths[f"{a}-{b}"] = lengths
            if lengths == [V]:
                hamilton_pairs.add((a, b))

    wanted = {
        (a, b) if a < b else (b, a)
        for a in left
        for b in right
    }
    if hamilton_pairs != wanted:
        raise AssertionError(
            f"Hamilton-pair graph mismatch: got {sorted(hamilton_pairs)}, wanted {sorted(wanted)}"
        )

    print("valid Q6 1-factorization")
    print("partition:", {"left": left, "right": right})
    print("Hamilton pairs:", sorted(hamilton_pairs))
    print("all pair cycle lengths:", all_pair_lengths)
    print("auxiliary graph is exactly K_{3,3}")


def main() -> None:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("q6_k33_solution.json")
    verify(path)


if __name__ == "__main__":
    main()
