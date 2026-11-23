import argparse
from itertools import product
import json
from pathlib import Path

RECURRENCES = {
    2: (1, 4),
    3: (1, 6, 1),
    4: (1, 10, 3, -5, 1),
    5: (1, 17, 9, -22, -1, 1, -6),
    6: (1, 30, 24, -95, -15, 64, -116, 16, 16),
    7: (1, 54, 60, -400, -155, 924, -1220, -76, 1725, -642, -412, -88, 100, 40),
    8: (1, 98, 145, -1606, -1043, 9813, -11042, -14222, 67346, -40216,
        -64047, 36082, 29210, 8981, -23650, -12520, 7365, 448, -196),
    9: (1, 179, 341, -6316, -6138, 92272, -87872, -479803, 1815915, -852208,
        -6873004, 8175787, 6036792, -5492010, -12389568, 3504328, 38808492,
        -4735254, -36745560, -36433267, 12744011, 28480781, 9986028, -2174189,
        -3904760, -845298, -118044, -60864, -3296, -32),
}
STARTS = {2: 3, 3: 4, 4: 7, 5: 10, 6: 13, 7: 19, 8: 25, 9: 37}
SHIFTS = {2: 1, 3: 2, 4: 3, 5: 3, 6: 5, 7: 6, 8: 7, 9: 8}
NUMERATORS = {
    2: (0, 16, 24),
    3: (0, 40, 80, 8),
    4: (0, 104, 264, 0, -128, 56, -8),
    5: (0, 264, 864, -344, -1992, -552, 40, 344, 648, 144),
    6: (0, 680, 2776, -3864, -21744, -11000, 16832, 50208, 38368,
        -61872, -23144, 27200, -4160),
}


def transition_graph(width):
    rows = list(product((0, 1), repeat=width))
    traces = {}
    for upper in rows:
        for lower in rows:
            trace = tuple(upper[column] + lower[column + 1] for column in range(width - 1))
            if all(left != right for left, right in zip(trace, trace[1:])):
                traces[upper, lower] = trace
    states = list(traces)
    indices = {pair: index for index, pair in enumerate(states)}
    next_rows = {}
    for upper, lower in states:
        next_rows.setdefault(upper, []).append(lower)
    edges = []
    for upper, middle in states:
        successors = []
        for lower in next_rows.get(middle, []):
            target = (middle, lower)
            if target in indices and all(
                left != right for left, right in zip(traces[upper, middle], traces[target])
            ):
                successors.append(indices[target])
        edges.append(successors)
    return states, edges


def direct_count(height, width):
    total = 0
    for entries in product((0, 1), repeat=height * width):
        block_traces = [
            [entries[row * width + column] + entries[(row + 1) * width + column + 1]
             for column in range(width - 1)]
            for row in range(height - 1)
        ]
        horizontal = all(
            block_traces[row][column] != block_traces[row][column + 1]
            for row in range(height - 1) for column in range(width - 2)
        )
        vertical = all(
            block_traces[row][column] != block_traces[row + 1][column]
            for row in range(height - 2) for column in range(width - 1)
        )
        total += horizontal and vertical
    return total


def check_width(width):
    states, edges = transition_graph(width)
    coefficients = RECURRENCES[width]
    degree = len(coefficients)
    vectors = [[1] * len(states)]
    for exponent in range(1, 51):
        vectors.append([sum(vectors[-1][target] for target in successors) for successors in edges])
    counts = [0] + [sum(vector) for vector in vectors]
    shift = None
    for candidate in range(11):
        residual = [
            vectors[candidate + degree][state]
            - sum(coefficient * vectors[candidate + degree - lag][state]
                  for lag, coefficient in enumerate(coefficients, 1))
            for state in range(len(states))
        ]
        if not any(residual):
            shift = candidate
            break
    assert shift is not None, ('No continuation identity', width)
    assert shift == SHIFTS[width], (width, shift)
    for index in range(STARTS[width], len(counts)):
        assert counts[index] == sum(
            coefficient * counts[index - lag]
            for lag, coefficient in enumerate(coefficients, 1)
        ), (width, index)
    denominator = [1] + [-coefficient for coefficient in coefficients]
    product_coefficients = [
        sum(denominator[lag] * counts[index - lag]
            for lag in range(min(index, degree) + 1))
        for index in range(len(counts))
    ]
    while product_coefficients[-1] == 0:
        product_coefficients.pop()
    if width in NUMERATORS:
        assert tuple(product_coefficients) == NUMERATORS[width]
    assert len(product_coefficients) <= STARTS[width]
    for height in range(2, min(3, 18 // width) + 1):
        assert direct_count(height, width) == counts[height - 1], (height, width)
    if width == 2:
        classes = [(2, 4), (2, 6), (4, 10)]
        labels = [classes.index((vectors[1][state], vectors[2][state]))
                  for state in range(len(states))]
        quotient = [[0, 2, 0], [1, 0, 1], [1, 2, 1]]
        assert [labels.count(label) for label in range(3)] == [4, 8, 4]
        for state, targets in enumerate(edges):
            assert [sum(labels[target] == label for target in targets)
                    for label in range(3)] == quotient[labels[state]]
    distinct_vectors = sorted(set(
        tuple(vectors[exponent][state] for exponent in range(shift + degree + 1))
        for state in range(len(states))
    ))
    for vector in distinct_vectors:
        assert vector[-1] == sum(
            coefficient * vector[-1 - lag]
            for lag, coefficient in enumerate(coefficients, 1)
        )
    return {
        'width': width,
        'oeis': 'A' + str(185759 + width),
        'states': len(states),
        'edges': sum(map(len, edges)),
        'degree': degree,
        'shift': shift,
        'vector_identity_exponent': shift + degree,
        'vector_identity_residual': 0,
        'recurrence_start': STARTS[width],
        'recurrence_coefficients': list(coefficients),
        'denominator': denominator,
        'numerator': product_coefficients,
        'initial_counts': counts[1:STARTS[width]],
        'counts_through_12': counts[1:13],
        'distinct_continuation_vectors': distinct_vectors,
        'direct_enumeration_max_height': min(3, 18 // width),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    arguments = parser.parse_args()
    results = [check_width(width) for width in RECURRENCES]
    for left in results:
        for right in results:
            assert left['counts_through_12'][right['width'] - 2] == right['counts_through_12'][left['width'] - 2]
    print('Exact continuation identities: widths 2 through 9.')
    print('For each width, every admissible ordered row pair is a state.')
    for result in results:
        print('width={width} states={states} edges={edges} degree={degree} shift={shift} residual={vector_identity_residual} recurrence_start={recurrence_start}'.format(**result))
    print('Generating-function numerator identities: widths 2 through 9.')
    print('Independent cell enumeration: widths 2 through 6 at heights 2 and 3; widths 7 through 9 at height 2.')
    print('Scalar recurrence comparisons: through index 51 for every width.')
    print('Width-two equitable quotient: all state classes and outgoing multiplicities.')
    print('Transpose symmetry: all height/width pairs from 2 through 9.')
    print('ALL_CHECKS_OK')
    if arguments.output:
        arguments.output.write_text(json.dumps({'schema_version': 1, 'results': results}, indent=2) + '\n')


if __name__ == '__main__':
    main()
