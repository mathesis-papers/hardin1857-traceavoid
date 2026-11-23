# Hardin's trace-avoiding array recurrences and Barker's formulas

The note counts labeled binary arrays with unequal ordinary traces at
horizontally and vertically neighboring contiguous 2 by 2 blocks. It proves
the recurrences in OEIS A185761–A185768, Barker's four generating functions
and width-two closed form, and a width-six generating function. It also gives
transposition symmetry for A185769, rationality for every fixed width and
divisibility by eight. The width-seven, width-eight and width-nine recurrences
start at indices 19, 25 and 37, respectively.

Marko Riedel's 23 December 2016 forbidden-word enumeration already implies
the width-two recurrence, generating function and closed form. The note
gives the explicit four-to-one array encoding and a uniform alternative
proof extending the enumeration to widths three through nine.
Howroyd's 9 January 2025 array-counting argument in
[A183774](https://oeis.org/A183774/internal) is a later antecedent;
the note gives the reversible alternating-complement map yielding
`a_2(n) = 8*A183774(n-1)` for `n >= 1`.

## Files

- `note.tex`: the main LaTeX source, with its bibliography included.
- `metadata.json`: title, creators, problem identifiers, license and source link.
- `verify.py`: standard-library Python 3 exact integer checks.
- `LICENSE`: CC BY 4.0 license notice.

The corresponding readable document is `note.pdf`.

## Build

Use Tectonic 0.17.0:

```sh
tectonic --untrusted note.tex
```

Alternatively use a LaTeX distribution with `geometry`, `amsmath`, `amssymb`,
`amsthm`, `booktabs`, `array`, `fontenc`, `lmodern`, `microtype`, `hyperref`
and `fancyvrb`:

```sh
pdflatex -interaction=nonstopmode -halt-on-error note.tex
pdflatex -interaction=nonstopmode -halt-on-error note.tex
```

No separate bibliography database, BibTeX invocation, figures or shell escape
is needed.

## Exact integer certificates

```sh
python3 verify.py
python3 verify.py --output certificates.json
```

The final line is `ALL_CHECKS_OK`. Every admissible ordered row pair is a
state. The program checks the full continuation-vector identity for each
width, the boundary scalar identities, and the displayed generating-function
numerators. The written proof shows why those finite identities imply the
recurrences for all lengths; this is stronger than matching a finite prefix.
Independent cell enumeration covers heights two and three at widths two
through six and height two at widths seven through nine. Additional scalar
recurrence equalities are checked through index 51, and the transposition
comparison covers all heights and widths from two through nine. The three
state classes and their outgoing multiplicities in the width-two quotient
are also checked exactly.

The regenerated `certificates.json` records exact state and edge counts,
coefficients, starting indices, and distinct continuation vectors. Its expected
SHA256 is recorded in `certificate-sha256.txt`.

## Scientific sources and scope

The posing sources are the name and formula fields of
OEIS [A185761](https://oeis.org/A185761),
[A185762](https://oeis.org/A185762), [A185763](https://oeis.org/A185763),
[A185764](https://oeis.org/A185764), [A185765](https://oeis.org/A185765),
[A185766](https://oeis.org/A185766), [A185767](https://oeis.org/A185767),
[A185768](https://oeis.org/A185768),
and the parent table [A185769](https://oeis.org/A185769).
The exact revisions and attributions are in the bibliography.
The prior width-two proof is Riedel's
[answer 2070074](https://math.stackexchange.com/a/2070074),
[revision 3](https://math.stackexchange.com/revisions/2070074/3),
23 December 2016, 23:49 UTC.

The note links each corresponding fixed-revision `.lean` file and states the
scope of its `result` declaration. Those declarations state the literal array
recurrences; the first four also state their generating functions, and the
width-two declaration also states its real closed form. The width-six
generating function, width-seven through width-nine recurrences and parent-table
consequences have written proofs in the note. The transfer and finite arithmetic
identities are independently specified by `verify.py`. The linked Lean
declarations do not cover widths seven through nine.

## Creators and license

Haobo Ma (ChronoAI Pte Ltd, Singapore), followed by Wenlin Zhang
(National University of Singapore; ChronoAI Pte Ltd, Singapore).
CC BY 4.0, identifier `cc-by-4.0`.
