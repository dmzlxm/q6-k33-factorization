# Q6 K33 Construction Artifact

This directory contains a short-paper draft and verification files for an
explicit 1-factorization of `Q_6` whose auxiliary graph is exactly `K_{3,3}`.

Archived artifact DOI: <https://doi.org/10.5281/zenodo.19854804>

## Files

- `q6_k33_paper.tex`: LaTeX short-paper draft.
- `q6_k33_discrete_math.tex`: Elsevier/Discrete Mathematics submission draft
  using the `elsarticle` class.
- `q6_k33_cover_letter.md`: cover letter draft.
- `q6_k33_highlights.txt`: highlights draft.
- `q6_k33_note.md`: readable working note with the same construction.
- `q6_k33_solution.json`: machine-readable certificate listing the six
  matchings as edge sets.
- `verify_q6_k33.py`: independent verifier for `q6_k33_solution.json`.
- `q6_k33_selfcheck.py`: self-contained verifier with the compact certificate
  table hard-coded.
- `q6_search.py` and `q6_beam.py`: search scripts used to find the construction.

## Verification

Run the JSON verifier:

```powershell
& 'C:\Users\zmd\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' .\verify_q6_k33.py .\q6_k33_solution.json
```

Run the self-contained verifier:

```powershell
& 'C:\Users\zmd\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' .\q6_k33_selfcheck.py
```

Both should report that the Hamilton-pair graph is exactly the complete
bipartite graph with parts `{0,1,5}` and `{2,3,4}`.

## Before Sharing Or Submitting

- Check the author metadata, AI-use statement, funding statement, and cover
  letter against the target journal's current submission system.
- Compile the TeX file in a LaTeX environment with `amsmath`, `amsthm`,
  `booktabs`, `hyperref`, `longtable`, and Elsevier's `elsarticle` class.
- Re-run both verifiers after any edit to the certificate table.
- Do a final literature check for independent solutions posted after Behague's
  paper and before submission.
