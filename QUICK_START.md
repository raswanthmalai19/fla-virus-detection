# Quick Start Guide

This guide will help you get the Virus Signature Detection System up and running quickly.

## Prerequisites

- Python 3.7 or higher
- Modern web browser (Chrome, Firefox, Safari, or Edge)
- Terminal/Command Prompt access

## Installation Steps

### 1. Navigate to Project Directory

```bash
cd /Users/raswanthmalaisamy/Desktop/vsd
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

or if you're using pip3:

```bash
pip3 install -r requirements.txt
```

### 3. Start the Backend Server

```bash
python backend/app.py
```

or:

```bash
python3 backend/app.py
```

You should see output like:
```
============================================================
🛡️  Virus Signature Detection System
============================================================
✓ Loaded 50 virus signatures
✓ 3 detection algorithms ready

📊 Algorithms:
   • KMP (Knuth-Morris-Pratt)
   • Aho-Corasick (Multi-Pattern)
   • DFA (Finite State Automaton)

🌐 Server starting at http://localhost:5000
============================================================
```

### 4. Open the Dashboard

Open your web browser and navigate to:
```
http://localhost:5000
```

## Testing the System

### Test with Sample Files

The project includes pre-made test files in `data/test_files/`:

1. **clean_file.txt** - Should show no threats
2. **infected_trojan.txt** - Should detect trojan signatures
3. **infected_ransomware.txt** - Should detect critical ransomware threats
4. **infected_mixed.txt** - Should detect multiple threats

### How to Scan

1. Click on the upload area or drag and drop a file
2. Select a test file from `data/test_files/`
3. Click "Scan File"
4. View the results showing:
   - Risk level (SAFE, LOW, MEDIUM, HIGH, CRITICAL)
   - Number of threats detected
   - Algorithm detection results
   - Detailed threat information

## Understanding the Results

### Risk Levels

- **SAFE**: No threats detected
- **LOW**: Minor threats detected
- **MEDIUM**: Moderate threats detected
- **HIGH**: Dangerous threats detected
- **CRITICAL**: Severe threats requiring immediate attention

### Algorithm Results

Each algorithm reports the number of pattern matches found:
- **KMP**: Linear time pattern matching with failure function
- **Aho-Corasick**: Multi-pattern matching using trie structure
- **DFA**: Deterministic finite automaton for pattern recognition

## Troubleshooting

### Port Already in Use

If port 5000 is already in use, edit `backend/app.py` and change the port:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Change to 5001 or any available port
```

### CORS Errors

If you see CORS errors, make sure the backend server is running and you're accessing the dashboard through `http://localhost:5000` not by opening the HTML file directly.

### Module Not Found

If you get "Module not found" errors:
```bash
pip install Flask Flask-CORS
```

## Next Steps

- Check out the full README.md for detailed documentation
- Explore the algorithm implementations in `backend/algorithms/`
- Review the virus signature database in `data/virus_signatures.txt`
- Check scan logs in the `logs/` directory

## Stopping the Server

Press `Ctrl+C` in the terminal where the server is running.
