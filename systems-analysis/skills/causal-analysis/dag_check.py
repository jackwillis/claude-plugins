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
# d-separation, vendored from networkx 3.6.1 (BSD-3) and adapted to the DAG
# shim above. See module docstring for the full license and citations.
# ---------------------------------------------------------------------------

def _as_set(G, s):
    return {s} if s in G else set(s)


def is_d_separator(G, x, y, z):
    """Return whether node sets `x` and `y` are d-separated by `z` in DAG `G`."""
    x = _as_set(G, x)
    y = _as_set(G, y)
    z = _as_set(G, z)

    intersection = x & y or x & z or y & z
    if intersection:
        raise CausalError(f"sets are not disjoint, intersection {intersection}")
    set_v = x | y | z
    if set_v - G.nodes:
        raise NodeNotFound(f"nodes not in graph: {set_v - G.nodes}")
    if not is_directed_acyclic_graph(G):
        raise CausalError("graph should be directed acyclic")

    forward_deque = deque()
    forward_visited = set()
    backward_deque = deque(x)
    backward_visited = set()
    ancestors_or_z = set().union(*[ancestors(G, n) for n in x]) | z | x

    while forward_deque or backward_deque:
        if backward_deque:
            node = backward_deque.popleft()
            backward_visited.add(node)
            if node in y:
                return False
            if node in z:
                continue
            backward_deque.extend(G.pred[node].keys() - backward_visited)
            forward_deque.extend(G.succ[node].keys() - forward_visited)
        if forward_deque:
            node = forward_deque.popleft()
            forward_visited.add(node)
            if node in y:
                return False
            if node in ancestors_or_z:
                backward_deque.extend(G.pred[node].keys() - backward_visited)
            if node not in z:
                forward_deque.extend(G.succ[node].keys() - forward_visited)
    return True


def _reachable(G, x, a, z):
    """Modified Bayes-Ball: nodes in `a` d-connected to `x` given `z`."""
    def _pass(e, v, f, n):
        is_element_of_A = n in a
        collider_if_in_Z = v not in z or (e and not f)
        return is_element_of_A and collider_if_in_Z

    queue = deque()
    for node in x:
        if bool(G.pred[node]):
            queue.append((True, node))
        if bool(G.succ[node]):
            queue.append((False, node))
    processed = list(queue)

    while queue:
        e, v = queue.popleft()
        preds = ((False, n) for n in G.pred[v])
        succs = ((True, n) for n in G.succ[v])
        for f, n in chain(preds, succs):
            if (f, n) not in processed and _pass(e, v, f, n):
                queue.append((f, n))
                processed.append((f, n))

    return {w for (_, w) in processed}


def find_minimal_d_separator(G, x, y, included=None, restricted=None):
    """Return a minimal d-separator of `x` and `y` within `restricted`,
    containing `included`, or None if no d-separator exists."""
    if not is_directed_acyclic_graph(G):
        raise CausalError("graph should be directed acyclic")

    x = _as_set(G, x)
    y = _as_set(G, y)
    included = set() if included is None else _as_set(G, included)
    restricted = set(G) if restricted is None else _as_set(G, restricted)

    set_y = x | y | included | restricted
    if set_y - G.nodes:
        raise NodeNotFound(f"nodes not in graph: {set_y - G.nodes}")
    if not included <= restricted:
        raise CausalError(f"included {included} must be within restricted {restricted}")
    intersection = x & y or x & included or y & included
    if intersection:
        raise CausalError(f"x, y, included not disjoint: {intersection}")

    nodeset = x | y | included
    anc = nodeset.union(*[ancestors(G, n) for n in nodeset])
    z_init = restricted & (anc - (x | y))
    x_closure = _reachable(G, x, anc, z_init)
    if x_closure & y:
        return None
    z_updated = z_init & (x_closure | included)
    y_closure = _reachable(G, y, anc, z_updated)
    return z_updated & (y_closure | included)


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

    # Task 2: vendored d-separation (vectors adapted from networkx 3.6.1
    # networkx/algorithms/tests/test_d_separation.py, BSD-3).
    path = DAG([(0, 1), (1, 2)])
    _check("path dsep {1}", is_d_separator(path, {0}, {2}, {1}), True)
    _check("path dsep {}", is_d_separator(path, {0}, {2}, set()), False)

    fork = DAG([(0, 1), (0, 2)])
    _check("fork dsep {0}", is_d_separator(fork, {1}, {2}, {0}), True)
    _check("fork dsep {}", is_d_separator(fork, {1}, {2}, set()), False)

    collider = DAG([(0, 2), (1, 2)])
    _check("collider dsep {}", is_d_separator(collider, {0}, {1}, set()), True)
    _check("collider open on {2}", is_d_separator(collider, {0}, {1}, {2}), False)

    asia = DAG([
        ("asia", "tuberculosis"), ("smoking", "cancer"), ("smoking", "bronchitis"),
        ("tuberculosis", "either"), ("cancer", "either"), ("either", "xray"),
        ("either", "dyspnea"), ("bronchitis", "dyspnea"),
    ])
    _check("asia dsep", is_d_separator(
        asia, {"asia", "smoking"}, {"dyspnea", "xray"}, {"bronchitis", "either"}), True)

    large = DAG([("A", "B"), ("C", "B"), ("B", "D"), ("D", "E"), ("B", "F"), ("G", "E")])
    _check("large_collider not sep {}", is_d_separator(large, {"B"}, {"E"}, set()), False)
    zmin = find_minimal_d_separator(large, "B", "E")
    _check("large_collider min sep", zmin, {"D"})
    _check("large_collider min is sep", is_d_separator(large, "B", "E", zmin), True)

    cf = DAG([("A", "B"), ("B", "C"), ("B", "D"), ("D", "C")])
    _check("chain_fork min sep", find_minimal_d_separator(cf, "A", "C"), {"B"})

    nosep = DAG([("A", "B")])
    _check("no separating set", find_minimal_d_separator(nosep, "A", "B"), None)

    nosep2 = DAG([("A", "B"), ("C", "A"), ("C", "B")])
    _check("no sep (confounded)", find_minimal_d_separator(nosep2, "A", "B"), None)

    print("ALL SELFTESTS PASSED")


def main(argv):
    if "--selftest" in argv:
        run_selftest()
        return
    print("not yet implemented", file=sys.stderr)
    sys.exit(2)


if __name__ == "__main__":
    main(sys.argv[1:])
