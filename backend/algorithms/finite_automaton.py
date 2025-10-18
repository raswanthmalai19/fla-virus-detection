"""
Finite State Automaton (FSA) for Pattern Matching
Time Complexity: O(n * |Σ|) preprocessing, O(n) matching
Constructs a DFA (Deterministic Finite Automaton) for pattern recognition
"""

class FiniteAutomaton:
    def __init__(self):
        self.name = "Finite State Automaton"
        
    def compute_transition_function(self, pattern, alphabet):
        """
        Compute the transition function (DFA) for the pattern.
        Returns a 2D dictionary representing state transitions.
        """
        m = len(pattern)
        tf = [{} for _ in range(m + 1)]
        
        for state in range(m + 1):
            for char in alphabet:
                # Find the longest prefix of pattern that is also a suffix of pattern[0:state] + char
                k = min(m, state + 1)
                while k > 0:
                    if pattern[:k] == (pattern[:state] + char)[-k:]:
                        break
                    k -= 1
                tf[state][char] = k
        
        return tf
    
    def get_alphabet(self, text, pattern):
        """
        Extract unique characters from text and pattern to form alphabet.
        """
        return set(text + pattern)
    
    def search(self, text, pattern):
        """
        Search for pattern in text using Finite Automaton.
        Returns list of starting positions where pattern is found.
        """
        if not text or not pattern:
            return []
        
        n = len(text)
        m = len(pattern)
        matches = []
        
        # Get alphabet and build transition function
        alphabet = self.get_alphabet(text, pattern)
        tf = self.compute_transition_function(pattern, alphabet)
        
        # Start from state 0 and process text
        state = 0
        for i in range(n):
            if text[i] in tf[state]:
                state = tf[state][text[i]]
            else:
                state = 0
                
            # If we reach the final state, pattern is found
            if state == m:
                matches.append(i - m + 1)
        
        return matches
    
    def search_multiple_patterns(self, text, patterns):
        """
        Search for multiple patterns in text.
        Returns dictionary with pattern as key and list of positions as value.
        """
        results = {}
        for pattern in patterns:
            positions = self.search(text, pattern)
            if positions:
                results[pattern] = positions
        return results
    
    def visualize_automaton(self, pattern):
        """
        Generate a simple visualization of the automaton states.
        Returns a string representation of the DFA.
        """
        m = len(pattern)
        alphabet = set(pattern)
        tf = self.compute_transition_function(pattern, alphabet)
        
        visualization = f"Automaton for pattern: '{pattern}'\n"
        visualization += f"States: 0 to {m} (final state: {m})\n\n"
        
        for state in range(m + 1):
            visualization += f"State {state}: "
            if state < m:
                visualization += f"[{pattern[:state]}] -> "
            else:
                visualization += "[ACCEPT] -> "
            
            transitions = []
            for char in sorted(alphabet):
                next_state = tf[state].get(char, 0)
                transitions.append(f"'{char}' -> {next_state}")
            
            visualization += ", ".join(transitions) + "\n"
        
        return visualization
