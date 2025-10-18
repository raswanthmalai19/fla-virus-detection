# Virus Signature Detection System

A comprehensive malware detection system combining classical string matching algorithms with formal automata theory for efficient virus signature detection.

## Features

### Core Algorithms Implemented
1. **Knuth-Morris-Pratt (KMP)** - Linear time pattern matching with failure function
2. **Aho-Corasick** - Multi-pattern matching using trie and failure links
3. **DFA (Finite State Automaton)** - Deterministic finite automaton for pattern recognition

### System Capabilities
- Real-time file scanning for malware signatures
- Multi-algorithm detection for accuracy
- Detailed logging with timestamps
- Statistical analysis of scan results
- Pattern-based threat identification
- RESTful API for integration

## Project Structure

```
vsd/
├── backend/
│   ├── algorithms/
│   │   ├── kmp.py              # KMP Algorithm
│   │   ├── aho_corasick.py     # Aho-Corasick Algorithm
│   │   └── finite_automaton.py # DFA (Finite State Automaton)
│   ├── detector.py             # Main detection engine
│   ├── logger.py               # Logging system
│   └── app.py                  # Flask API server
├── frontend/
│   ├── index.html              # Main dashboard
│   ├── styles.css              # Styling
│   └── script.js               # Frontend logic
├── data/
│   ├── virus_signatures.txt    # Malware signature database
│   └── test_files/             # Sample test files
├── logs/                       # Detection logs
└── requirements.txt            # Python dependencies
```

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. Start the backend server:
   ```bash
   python backend/app.py
   ```

2. Open the dashboard:
   - Navigate to `frontend/index.html` in your browser
   - Or open via local server: `http://localhost:5000`

## How It Works

### 1. Signature Database
The system maintains a database of known malware signatures (hexadecimal patterns and string signatures).

### 2. Detection Process
When a file is uploaded:
- File content is read and analyzed
- All three algorithms scan for signature matches
- Each algorithm reports matches independently
- Results are aggregated and analyzed
- Threat level is determined based on matches

### 3. Algorithms Explained

**KMP Algorithm**: Uses failure function to avoid redundant comparisons. Time complexity: O(n+m)

**Aho-Corasick**: Builds a trie with failure links for simultaneous multi-pattern matching. Time complexity: O(n+m+z)

**DFA (Finite Automaton)**: Constructs deterministic finite automaton for pattern recognition with state transitions. Time complexity: O(n)

## Usage

1. **Upload File**: Click "Choose File" and select file to scan
2. **Scan**: Click "Scan File" to start detection
3. **View Results**: See detected threats, algorithms used, and statistics
4. **Check Logs**: View detailed scan logs with timestamps

## Technical Details

- **Backend**: Python 3.x with Flask
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Pattern Matching**: 3 powerful algorithms (KMP, Aho-Corasick, DFA)
- **API**: RESTful endpoints for file scanning
- **Logging**: Timestamped logs with full scan details

## API Endpoints

- `POST /api/scan` - Upload and scan file
- `GET /api/logs` - Retrieve scan logs
- `GET /api/stats` - Get detection statistics

## Author

Semester Project - Virus Detection System
