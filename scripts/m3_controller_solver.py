"""Earliest target hit over the fixed, ordered, pre-edge Controller trace samples."""
from itertools import groupby

import z3

from predicates import parse


class FiniteTraceSolver:
    def __init__(self, samples, timeout_ms):
        if not samples or not samples[0] or timeout_ms <= 0:
            raise ValueError("expected sampled atoms and a positive query timeout")
        names = samples[0].keys()
        if any(row.keys() != names for row in samples):
            raise ValueError("inconsistent sampled atom columns")
        self.index = z3.Int("sample_index")
        self.solver = z3.Optimize()
        self.solver.set(timeout=timeout_ms)
        self.solver.add(self.index >= 0, self.index < len(samples))
        self.minimum = self.solver.minimize(self.index)
        self.atoms = {"true": z3.BoolVal(True), "false": z3.BoolVal(False)}
        for name in names:
            intervals = []
            offset = 0
            for value, rows in groupby(samples, key=lambda row: row[name]):
                if value not in (0, 1):
                    raise ValueError(f"non-binary sample for {name}")
                end = offset + sum(1 for _ in rows)
                if value:
                    if end == offset + 1:
                        intervals.append(self.index == offset)
                    else:
                        intervals.append(z3.And(self.index >= offset, self.index < end))
                offset = end
            self.atoms[name] = z3.Or(*intervals)

    def _condition(self, node):
        if isinstance(node, str):
            return self.atoms[node]
        if node[0] == "not":
            return z3.Not(self._condition(node[1]))
        left, right = self._condition(node[1]), self._condition(node[2])
        return z3.And(left, right) if node[0] == "and" else z3.Or(left, right)

    def first_hit(self, expr):
        """Return a zero-based sample index; None means UNSAT on these samples."""
        self.solver.push()
        try:
            self.solver.add(self._condition(parse(expr)))
            status = self.solver.check()
            if status == z3.unsat:
                return None
            if status != z3.sat:
                raise RuntimeError(f"unknown trace obligation: {self.solver.reason_unknown()}")
            index = self.solver.model().eval(self.index).as_long()
            if not all(z3.eq(bound, z3.IntVal(index)) for bound in
                       (self.minimum.lower(), self.minimum.upper())):
                raise RuntimeError("unknown optimum: solver did not certify the first hit")
            return index
        finally:
            self.solver.pop()
