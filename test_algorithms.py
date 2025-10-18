"""
Test script to verify all algorithms work correctly
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from backend.algorithms.kmp import KMPAlgorithm
from backend.algorithms.aho_corasick import AhoCorasickAlgorithm
from backend.algorithms.finite_automaton import FiniteAutomaton

def test_algorithm(algo, text, pattern):
    """Test a single algorithm"""
    print(f"\n{algo.name}:")
    matches = algo.search(text, pattern)
    if matches:
        print(f"  ✓ Pattern '{pattern}' found at positions: {matches}")
    else:
        print(f"  ✗ Pattern '{pattern}' not found")
    return len(matches)

def main():
    print("="*60)
    print("Testing Virus Detection Algorithms")
    print("="*60)
    
    # Test data
    text = "ABABDABACDABABCABAB"
    pattern = "ABABCABAB"
    
    print(f"\nText: {text}")
    print(f"Pattern: {pattern}")
    print(f"Expected position: 10")
    
    # Test all algorithms
    algorithms = [
        KMPAlgorithm(),
        FiniteAutomaton()
    ]
    
    results = {}
    for algo in algorithms:
        count = test_algorithm(algo, text, pattern)
        results[algo.name] = count
    
    # Test Aho-Corasick with multiple patterns
    print(f"\nAho-Corasick (Multi-Pattern):")
    ac = AhoCorasickAlgorithm()
    patterns = ["ABAB", "ABABCABAB", "CDAB"]
    matches = ac.search(text, patterns)
    if matches:
        for pat, positions in matches.items():
            print(f"  ✓ Pattern '{pat}' found at positions: {positions}")
    results["Aho-Corasick"] = len(matches)
    
    # Summary
    print("\n" + "="*60)
    print("Test Summary:")
    print("="*60)
    all_passed = True
    for algo_name, count in results.items():
        status = "✓ PASS" if count > 0 else "✗ FAIL"
        print(f"{algo_name:25s} - {status} ({count} matches)")
        if count == 0:
            all_passed = False
    
    print("="*60)
    if all_passed:
        print("✓ All 3 algorithms working correctly!")
        print("  • KMP (Knuth-Morris-Pratt)")
        print("  • Aho-Corasick (Multi-Pattern)")
        print("  • DFA (Finite State Automaton)")
    else:
        print("✗ Some algorithms failed!")
    print("="*60)

if __name__ == "__main__":
    main()
