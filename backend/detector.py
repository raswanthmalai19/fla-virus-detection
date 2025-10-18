"""
Main Virus Detection Engine
Coordinates all algorithms and manages signature database
"""

import os
import sys

# Add algorithms directory to path
sys.path.append(os.path.dirname(__file__))

from algorithms.kmp import KMPAlgorithm
from algorithms.aho_corasick import AhoCorasickAlgorithm
from algorithms.finite_automaton import FiniteAutomaton

class VirusDetector:
    def __init__(self, signature_file="data/virus_signatures.txt"):
        self.signature_file = signature_file
        self.signatures = {}
        self.load_signatures()
        
        # Initialize all algorithms
        self.algorithms = {
            "KMP": KMPAlgorithm(),
            "Aho-Corasick": AhoCorasickAlgorithm(),
            "DFA": FiniteAutomaton()
        }
    
    def load_signatures(self):
        """
        Load virus signatures from database file.
        Format: SIGNATURE_ID|SIGNATURE_NAME|PATTERN|THREAT_LEVEL
        """
        if not os.path.exists(self.signature_file):
            print(f"Warning: Signature file not found: {self.signature_file}")
            return
        
        with open(self.signature_file, 'r') as f:
            for line in f:
                line = line.strip()
                # Skip comments and empty lines
                if not line or line.startswith('#'):
                    continue
                
                try:
                    parts = line.split('|')
                    if len(parts) == 4:
                        sig_id, sig_name, pattern, threat_level = parts
                        self.signatures[pattern] = {
                            "id": sig_id,
                            "name": sig_name,
                            "pattern": pattern,
                            "threat_level": threat_level
                        }
                except Exception as e:
                    print(f"Error parsing signature: {line} - {e}")
    
    def hex_to_string(self, hex_string):
        """
        Convert hex string to ASCII string for matching.
        """
        try:
            bytes_obj = bytes.fromhex(hex_string)
            return bytes_obj.decode('latin-1')  # Use latin-1 to preserve all byte values
        except:
            return hex_string
    
    def scan_content(self, content, algorithms_to_use=None):
        """
        Scan content using specified algorithms (or all if none specified).
        Returns detection results with algorithm-specific matches.
        """
        if algorithms_to_use is None:
            algorithms_to_use = list(self.algorithms.keys())
        
        results = {
            "threats_found": [],
            "algorithm_detections": {},
            "scan_summary": {
                "total_signatures_checked": len(self.signatures),
                "algorithms_used": algorithms_to_use,
                "content_size": len(content)
            }
        }
        
        # Convert signatures to searchable patterns
        patterns = {}
        for pattern, sig_info in self.signatures.items():
            search_pattern = self.hex_to_string(pattern)
            patterns[search_pattern] = sig_info
        
        pattern_list = list(patterns.keys())
        detected_patterns = set()
        
        # Run each algorithm
        for algo_name in algorithms_to_use:
            if algo_name not in self.algorithms:
                continue
                
            algo = self.algorithms[algo_name]
            
            # For Aho-Corasick, use multi-pattern search directly
            if algo_name == "Aho-Corasick":
                matches = algo.search(content, pattern_list)
            else:
                matches = algo.search_multiple_patterns(content, pattern_list)
            
            results["algorithm_detections"][algo_name] = len(matches) if matches else 0
            
            # Collect detected patterns
            for pattern, positions in matches.items():
                if positions:
                    detected_patterns.add(pattern)
        
        # Build threat report
        for pattern in detected_patterns:
            if pattern in patterns:
                sig_info = patterns[pattern]
                threat = {
                    "signature_id": sig_info["id"],
                    "signature_name": sig_info["name"],
                    "threat_level": sig_info["threat_level"],
                    "pattern": sig_info["pattern"]
                }
                results["threats_found"].append(threat)
        
        # Sort threats by severity
        severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
        results["threats_found"].sort(
            key=lambda x: severity_order.get(x["threat_level"], 4)
        )
        
        return results
    
    def scan_file(self, file_path, algorithms_to_use=None):
        """
        Scan a file for virus signatures.
        """
        if not os.path.exists(file_path):
            return {
                "error": "File not found",
                "file": file_path
            }
        
        try:
            # Read file content
            with open(file_path, 'rb') as f:
                content = f.read().decode('latin-1')  # Use latin-1 for binary files
            
            # Scan content
            results = self.scan_content(content, algorithms_to_use)
            results["file"] = os.path.basename(file_path)
            results["file_size"] = len(content)
            
            # Add risk assessment
            threat_count = len(results["threats_found"])
            if threat_count == 0:
                results["risk_level"] = "SAFE"
            elif any(t["threat_level"] == "CRITICAL" for t in results["threats_found"]):
                results["risk_level"] = "CRITICAL"
            elif any(t["threat_level"] == "HIGH" for t in results["threats_found"]):
                results["risk_level"] = "HIGH"
            elif any(t["threat_level"] == "MEDIUM" for t in results["threats_found"]):
                results["risk_level"] = "MEDIUM"
            else:
                results["risk_level"] = "LOW"
            
            return results
            
        except Exception as e:
            return {
                "error": str(e),
                "file": file_path
            }
    
    def get_signature_info(self, signature_id=None):
        """
        Get information about signatures in the database.
        """
        if signature_id:
            for pattern, sig_info in self.signatures.items():
                if sig_info["id"] == signature_id:
                    return sig_info
            return None
        else:
            return list(self.signatures.values())
