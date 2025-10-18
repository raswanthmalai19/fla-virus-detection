"""
String Matching Algorithms Package

This package contains implementations of classical string matching algorithms
used for virus signature detection.
"""

from .kmp import KMPAlgorithm
from .aho_corasick import AhoCorasickAlgorithm
from .finite_automaton import FiniteAutomaton

__all__ = [
    'KMPAlgorithm',
    'AhoCorasickAlgorithm',
    'FiniteAutomaton'
]
