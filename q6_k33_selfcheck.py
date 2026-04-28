from __future__ import annotations


N = 6
V = 1 << N
LEFT = (0, 1, 5)
RIGHT = (2, 3, 4)

# For each even-parity vertex v, COLORS[v][d] is the color of the edge
# from v to v xor 2^d.
COLORS = {
    0: (4, 5, 0, 1, 3, 2),
    3: (1, 0, 3, 2, 4, 5),
    5: (2, 0, 1, 5, 4, 3),
    6: (2, 3, 4, 1, 0, 5),
    9: (2, 4, 0, 5, 1, 3),
    10: (3, 4, 5, 2, 1, 0),
    12: (3, 4, 0, 5, 2, 1),
    15: (3, 2, 0, 4, 1, 5),
    17: (2, 0, 1, 5, 3, 4),
    18: (3, 1, 2, 4, 0, 5),
    20: (2, 5, 0, 1, 4, 3),
    23: (4, 3, 5, 2, 1, 0),
    24: (2, 0, 5, 4, 3, 1),
    27: (3, 0, 4, 1, 5, 2),
    29: (4, 5, 3, 0, 1, 2),
    30: (0, 3, 5, 1, 2, 4),
    33: (0, 1, 5, 4, 3, 2),
    34: (0, 5, 2, 1, 4, 3),
    36: (4, 0, 3, 2, 5, 1),
    39: (1, 0, 2, 3, 4, 5),
    40: (1, 3, 0, 4, 2, 5),
    43: (4, 0, 2, 3, 5, 1),
    45: (3, 1, 5, 2, 0, 4),
    46: (4, 5, 2, 3, 1, 0),
    48: (0, 2, 4, 3, 1, 5),
    51: (3, 5, 1, 0, 4, 2),
    53: (0, 3, 2, 4, 1, 5),
    54: (5, 2, 1, 0, 4, 3),
    57: (0, 3, 5, 1, 2, 4),
    58: (1, 4, 3, 0, 5, 2),
    60: (3, 2, 5, 1, 4, 0),
    63: (5, 1, 4, 2, 0, 3),
}


def parity(v: int) -> int:
    return v.bit_count() & 1


def build_matchings() -> dict[int, list[tuple[int, int]]]:
    evens = [v for v in range(V) if parity(v) == 0]
    if sorted(COLORS) != evens:
        raise AssertionError("COLORS must have exactly the even vertices")

    matchings = {c: [] for c in range(N)}
    odd_seen = {c: set() for c in range(N)}
    for v in evens:
        row = COLORS[v]
        if sorted(row) != list(range(N)):
            raise AssertionError(f"colors at even vertex {v} are not a permutation")
        for d, c in enumerate(row):
            w = v ^ (1 << d)
            if parity(w) != 1:
                raise AssertionError("edge does not go to odd side")
            matchings[c].append((v, w))
            odd_seen[c].add(w)

    odds = {v for v in range(V) if parity(v) == 1}
    for c in range(N):
        if len(matchings[c]) != V // 2:
            raise AssertionError(f"color {c} has wrong number of edges")
        if odd_seen[c] != odds:
            raise AssertionError(f"color {c} does not cover every odd vertex once")
    return matchings


def cycle_lengths(edges: list[tuple[int, int]]) -> list[int]:
    adj = [[] for _ in range(V)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    if any(len(xs) != 2 for xs in adj):
        raise AssertionError("union is not 2-regular")

    seen = [False] * V
    lengths = []
    for start in range(V):
        if seen[start]:
            continue
        prev = -1
        cur = start
        length = 0
        while not seen[cur]:
            seen[cur] = True
            length += 1
            a, b = adj[cur]
            prev, cur = cur, a if a != prev else b
        lengths.append(length)
    return sorted(lengths, reverse=True)


def main() -> None:
    matchings = build_matchings()
    wanted = {tuple(sorted((a, b))) for a in LEFT for b in RIGHT}
    got = set()
    lengths = {}

    for a in range(N):
        for b in range(a + 1, N):
            key = (a, b)
            xs = cycle_lengths(matchings[a] + matchings[b])
            lengths[f"{a}-{b}"] = xs
            if xs == [V]:
                got.add(key)

    if got != wanted:
        raise AssertionError(f"Hamilton graph mismatch: got {sorted(got)}, wanted {sorted(wanted)}")

    print("self-contained check passed")
    print("partition:", {"left": LEFT, "right": RIGHT})
    print("Hamilton pairs:", sorted(got))
    print("cycle lengths:", lengths)


if __name__ == "__main__":
    main()
