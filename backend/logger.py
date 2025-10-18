"""
Logging System for Virus Detection
Handles timestamped logs and scan statistics
"""

import os
import json
from datetime import datetime

class DetectionLogger:
    def __init__(self, log_dir="logs"):
        self.log_dir = log_dir
        self.ensure_log_directory()
        
    def ensure_log_directory(self):
        """Create log directory if it doesn't exist"""
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
    
    def log_scan(self, scan_data):
        """
        Log a scan operation with timestamp.
        scan_data should contain: filename, results, statistics, etc.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {
            "timestamp": timestamp,
            "scan_data": scan_data
        }
        
        # Create log filename with date
        log_filename = f"scan_log_{datetime.now().strftime('%Y%m%d')}.json"
        log_path = os.path.join(self.log_dir, log_filename)
        
        # Read existing logs
        logs = []
        if os.path.exists(log_path):
            try:
                with open(log_path, 'r') as f:
                    logs = json.load(f)
            except:
                logs = []
        
        # Append new log entry
        logs.append(log_entry)
        
        # Write back to file
        with open(log_path, 'w') as f:
            json.dump(logs, f, indent=2)
        
        return timestamp
    
    def get_recent_logs(self, limit=10):
        """
        Get recent log entries.
        """
        all_logs = []
        
        # Get all log files
        if os.path.exists(self.log_dir):
            log_files = sorted([f for f in os.listdir(self.log_dir) if f.endswith('.json')])
            
            # Read logs from most recent files
            for log_file in reversed(log_files):
                log_path = os.path.join(self.log_dir, log_file)
                try:
                    with open(log_path, 'r') as f:
                        logs = json.load(f)
                        all_logs.extend(logs)
                except:
                    continue
                
                if len(all_logs) >= limit:
                    break
        
        # Return most recent logs
        return all_logs[-limit:][::-1]
    
    def get_statistics(self):
        """
        Calculate overall statistics from logs.
        """
        total_scans = 0
        total_threats = 0
        threat_levels = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
        algorithm_usage = {}
        
        if os.path.exists(self.log_dir):
            log_files = [f for f in os.listdir(self.log_dir) if f.endswith('.json')]
            
            for log_file in log_files:
                log_path = os.path.join(self.log_dir, log_file)
                try:
                    with open(log_path, 'r') as f:
                        logs = json.load(f)
                        
                        for log_entry in logs:
                            total_scans += 1
                            scan_data = log_entry.get("scan_data", {})
                            
                            # Count threats
                            threats = scan_data.get("threats_found", [])
                            total_threats += len(threats)
                            
                            # Count threat levels
                            for threat in threats:
                                level = threat.get("threat_level", "MEDIUM")
                                if level in threat_levels:
                                    threat_levels[level] += 1
                            
                            # Count algorithm usage
                            detections = scan_data.get("algorithm_detections", {})
                            for algo, matches in detections.items():
                                if matches:
                                    algorithm_usage[algo] = algorithm_usage.get(algo, 0) + 1
                except:
                    continue
        
        return {
            "total_scans": total_scans,
            "total_threats_detected": total_threats,
            "threat_levels": threat_levels,
            "algorithm_usage": algorithm_usage
        }
    
    def export_log(self, output_file):
        """
        Export all logs to a single file.
        """
        all_logs = []
        
        if os.path.exists(self.log_dir):
            log_files = sorted([f for f in os.listdir(self.log_dir) if f.endswith('.json')])
            
            for log_file in log_files:
                log_path = os.path.join(self.log_dir, log_file)
                try:
                    with open(log_path, 'r') as f:
                        logs = json.load(f)
                        all_logs.extend(logs)
                except:
                    continue
        
        with open(output_file, 'w') as f:
            json.dump(all_logs, f, indent=2)
        
        return len(all_logs)
