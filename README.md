# Q6 K33 Factorization

This repository contains a constructive certificate for a 1-factorization of the 6-dimensional hypercube `Q_6` whose Hamilton-pair auxiliary graph is exactly `K_{3,3}`.

The construction resolves the remaining `(k,l)=(3,3)` case from Natalie C. Behague's work on semi-perfect 1-factorizations of the hypercube.

Archived release DOI: [10.5281/zenodo.19854804](https://doi.org/10.5281/zenodo.19854804)

## Main Files

- `q6_k33_paper.tex`: LaTeX short-paper draft.
- `q6_k33_solution.json`: machine-readable certificate listing the six matchings as edge sets.
- `verify_q6_k33.py`: verifier for the JSON certificate.
- `q6_k33_selfcheck.py`: self-contained verifier with the compact certificate table hard-coded.

## Verification

Run the JSON verifier:

```bash
python verify_q6_k33.py q6_k33_solution.json
```

Run the self-contained verifier:

```bash
python q6_k33_selfcheck.py
```

Both checks should report that the Hamilton-pair graph is exactly the complete bipartite graph with parts `{0,1,5}` and `{2,3,4}`.

## Citation Background

Natalie C. Behague, *Semi-perfect 1-factorizations of the hypercube*, Discrete Mathematics 342(6) (2019), 1696-1702. DOI: 10.1016/j.disc.2019.01.035; arXiv:1811.06389.
