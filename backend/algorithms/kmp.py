"""
Knuth-Morris-Pratt (KMP) Algorithm
Time Complexity: O(n + m) where n is text length and m is pattern length
Uses failure function to avoid redundant comparisons
"""

class KMPAlgorithm:
    def __init__(self):
        self.name = "KMP (Knuth-Morris-Pratt)"
        
    def compute_failure_function(self, pattern):
        """
        Compute the failure function (prefix function) for the pattern.
        failure[i] = length of longest proper prefix of pattern[0..i] 
        which is also a suffix of pattern[0..i]
        """
        m = len(pattern)
        failure = [0] * m
        j = 0
        
        for i in range(1, m):
            while j > 0 and pattern[i] != pattern[j]:
                j = failure[j - 1]
            if pattern[i] == pattern[j]:
                j += 1
            failure[i] = j
            
        return failure
    
    def search(self, text, pattern):
        """
        Search for pattern in text using KMP algorithm.
        Returns list of starting positions where pattern is found.
        """
        if not text or not pattern:
            return []
            
        n = len(text)
        m = len(pattern)
        matches = []
        
        # Compute failure function
        failure = self.compute_failure_function(pattern)
        
        j = 0  # index for pattern
        for i in range(n):  # index for text
            while j > 0 and text[i] != pattern[j]:
                j = failure[j - 1]
            
            if text[i] == pattern[j]:
                j += 1
            
            if j == m:
                # Pattern found at position i - m + 1
                matches.append(i - m + 1)
                j = failure[j - 1]
        
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
