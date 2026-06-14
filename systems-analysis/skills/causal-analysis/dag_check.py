#!/usr/bin/env python3
"""Deterministic DAG checks for the causal-analysis skill.

Reads a JSON DAG spec from stdin and prints an identifiability report:
backdoor paths, a valid adjustment set (or "not identifiable"), node
classification, and validation of any proposed adjustment set.

No runtime dependencies (Python 3 standard library only).

----------------------------------------------------------------------
The d-separation routines (`is_d_separator`, `find_minimal_d_separator`,
`_reachable`) are vendored and lightly adapted from NetworkX 3.6.1
(networkx/algorithms/d_separation.py), distributed under the 3-clause BSD
license, and reproduced here without the networkx runtime dependency:

  Copyright (c) 2004-2025, NetworkX Developers
  Aric Hagberg <hagberg@lanl.gov>
  Dan Schult <dschult@colgate.edu>
  Pieter Swart <swart@lanl.gov>
  All rights reserved.

  Redistribution and use in source and binary forms, with or without
  modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright notice,
      this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of the NetworkX Developers nor the names of its
      contributors may be used to endorse or promote products derived from
      this software without specific prior written permission.
  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
  AND ANY EXPRESS OR IMPLIED WARRANTIES ARE DISCLAIMED. IN NO EVENT SHALL THE
  COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DAMAGES ARISING IN ANY WAY
  OUT OF THE USE OF THIS SOFTWARE.

Algorithms: Bayes-ball / reachability (Shachter 1998); minimal d-separator in
linear time (van der Zander & Liskiewicz 2020); d-separation (Pearl 2009).
----------------------------------------------------------------------
"""

import json
import sys
from collections import deque
from itertools import chain


class CausalError(Exception):
    """Invalid graph or query (e.g. cyclic graph, non-disjoint node sets)."""


class NodeNotFound(Exception):
    """A referenced node is not present in the graph."""


class DAG:
    """Minimal directed-graph shim exposing exactly what the vendored
    d-separation routines need: `pred`, `succ`, `nodes`, membership, iteration."""

    def __init__(self, edges, nodes=None):
        self.succ = {}
        self.pred = {}
        self.nodes = set()
        if nodes:
            for n in nodes:
                self._add_node(n)
        for u, v in edges:
            self._add_node(u)
            self._add_node(v)
            self.succ[u][v] = {}
            self.pred[v][u] = {}

    def _add_node(self, n):
        if n not in self.nodes:
            self.nodes.add(n)
            self.succ[n] = {}
            self.pred[n] = {}

    def __contains__(self, n):
        return n in self.nodes

    def __iter__(self):
        return iter(self.nodes)


def ancestors(G, node):
    """All strict ancestors of `node` (excludes `node`)."""
    seen = set()
    stack = [node]
    while stack:
        n = stack.pop()
        for p in G.pred[n]:
            if p not in seen:
                seen.add(p)
                stack.append(p)
    return seen


def descendants(G, node):
    """All strict descendants of `node` (excludes `node`)."""
    seen = set()
    stack = [node]
    while stack:
        n = stack.pop()
        for c in G.succ[n]:
            if c not in seen:
                seen.add(c)
                stack.append(c)
    return seen


def is_directed_acyclic_graph(G):
    """True iff `G` has no directed cycle (DFS three-coloring)."""
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {n: WHITE for n in G.nodes}

    def visit(n):
        color[n] = GRAY
        for m in G.succ[n]:
            if color[m] == GRAY:
                return False
            if color[m] == WHITE and not visit(m):
                return False
        color[n] = BLACK
        return True

    return all(visit(n) for n in G.nodes if color[n] == WHITE)


# ---------------------------------------------------------------------------
# Selftest harness (vectors added across tasks).
# ---------------------------------------------------------------------------

def _check(name, got, expected):
    if got != expected:
        raise AssertionError(f"{name}: expected {expected!r}, got {got!r}")
    print(f"ok  {name}")


def run_selftest():
    # Task 1: shim + helpers
    g = DAG([("A", "B"), ("B", "C"), ("B", "D"), ("D", "C")])
    _check("ancestors(C)", ancestors(g, "C"), {"A", "B", "D"})
    _check("descendants(A)", descendants(g, "A"), {"B", "C", "D"})
    _check("isolated node preserved", "X" in DAG([("A", "B")], nodes=["X"]), True)
    _check("acyclic", is_directed_acyclic_graph(g), True)
    _check("cyclic", is_directed_acyclic_graph(DAG([("A", "B"), ("B", "A")])), False)
    print("ALL SELFTESTS PASSED")


def main(argv):
    if "--selftest" in argv:
        run_selftest()
        return
    print("not yet implemented", file=sys.stderr)
    sys.exit(2)


if __name__ == "__main__":
    main(sys.argv[1:])
