"""
Aho-Corasick Algorithm
Time Complexity: O(n + m + z) where z is number of matches
Builds a trie with failure links for efficient multi-pattern matching
"""

from collections import deque, defaultdict

class AhoCorasickNode:
    def __init__(self):
        self.children = {}
        self.failure = None
        self.output = []  # Patterns that end at this node

class AhoCorasickAlgorithm:
    def __init__(self):
        self.name = "Aho-Corasick"
        self.root = None
        
    def build_trie(self, patterns):
        """
        Build a trie from the list of patterns.
        """
        self.root = AhoCorasickNode()
        
        for pattern in patterns:
            node = self.root
            for char in pattern:
                if char not in node.children:
                    node.children[char] = AhoCorasickNode()
                node = node.children[char]
            node.output.append(pattern)
    
    def build_failure_links(self):
        """
        Build failure links using BFS for the Aho-Corasick automaton.
        """
        queue = deque()
        
        # All first level nodes have failure link to root
        for child in self.root.children.values():
            child.failure = self.root
            queue.append(child)
        
        # BFS to build failure links
        while queue:
            current = queue.popleft()
            
            for char, child in current.children.items():
                queue.append(child)
                
                # Find failure link
                failure = current.failure
                while failure and char not in failure.children:
                    failure = failure.failure
                
                if failure:
                    child.failure = failure.children[char]
                else:
                    child.failure = self.root
                
                # Add output from failure link
                child.output.extend(child.failure.output)
    
    def search(self, text, patterns):
        """
        Search for multiple patterns in text using Aho-Corasick algorithm.
        Returns dictionary with pattern as key and list of positions as value.
        """
        if not text or not patterns:
            return {}
        
        # Build the automaton
        self.build_trie(patterns)
        self.build_failure_links()
        
        results = defaultdict(list)
        node = self.root
        
        # Process text character by character
        for i, char in enumerate(text):
            # Follow failure links until we find a match or reach root
            while node and char not in node.children:
                node = node.failure
            
            if node:
                node = node.children[char]
            else:
                node = self.root
                continue
            
            # Check for pattern matches at current position
            for pattern in node.output:
                # Position where pattern starts
                start_pos = i - len(pattern) + 1
                results[pattern].append(start_pos)
        
        return dict(results)
    
    def search_multiple_patterns(self, text, patterns):
        """
        Wrapper method for consistency with other algorithms.
        """
        return self.search(text, patterns)
