# Complete Usage Guide

This comprehensive guide covers everything you need to know to use the Virus Signature Detection System.

## Table of Contents

1. [Installation](#installation)
2. [Starting the System](#starting-the-system)
3. [Using the Dashboard](#using-the-dashboard)
4. [Understanding Results](#understanding-results)
5. [API Usage](#api-usage)
6. [Troubleshooting](#troubleshooting)

---

## Installation

### Prerequisites

- **Python**: 3.7 or higher
- **pip**: Python package manager
- **Web Browser**: Modern browser (Chrome, Firefox, Safari, Edge)

### Step 1: Install Dependencies

Open a terminal in the project directory and run:

```bash
pip install -r requirements.txt
```

Or for Python 3 specifically:

```bash
pip3 install -r requirements.txt
```

This installs:
- Flask (web framework)
- Flask-CORS (cross-origin resource sharing)
- Werkzeug (WSGI utilities)

### Step 2: Verify Installation

Test the algorithms:

```bash
python test_algorithms.py
```

Expected output:
```
✓ All 3 algorithms working correctly!
  • KMP (Knuth-Morris-Pratt)
  • Aho-Corasick (Multi-Pattern)
  • DFA (Finite State Automaton)
```

---

## Starting the System

### Method 1: Using Startup Scripts (Easiest)

**On macOS/Linux:**
```bash
chmod +x run_server.sh
./run_server.sh
```

**On Windows:**
```cmd
run_server.bat
```

### Method 2: Manual Start

```bash
python backend/app.py
```

Or:

```bash
python3 backend/app.py
```

### Expected Output

You should see:

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

 * Running on http://0.0.0.0:5000
 * Press CTRL+C to quit
```

---

## Using the Dashboard

### Step 1: Open Dashboard

Open your web browser and navigate to:

```
http://localhost:5000
```

### Step 2: Upload a File

**Option A: Click to Upload**
1. Click on the upload area
2. Select a file from your computer
3. File information will be displayed

**Option B: Drag and Drop**
1. Drag a file from your file explorer
2. Drop it onto the upload area
3. File information will be displayed

### Step 3: Scan the File

1. Click the **"Scan File"** button
2. Wait for the scan to complete (usually < 1 second)
3. Results will appear below

### Step 4: Review Results

The results section shows:

- **Status Badge**: Color-coded risk level
- **Threat Count**: Number of threats detected
- **File Information**: Name, scan time, file size
- **Algorithm Results**: How many matches each algorithm found
- **Threat Details**: List of specific threats (if any)

---

## Understanding Results

### Risk Levels

| Level | Color | Meaning |
|-------|-------|---------|
| **SAFE** | Green | No threats detected |
| **LOW** | Blue | Minor threats, low risk |
| **MEDIUM** | Yellow | Moderate threats detected |
| **HIGH** | Orange | Dangerous threats found |
| **CRITICAL** | Red | Severe threats, immediate action needed |

### Algorithm Results Grid

Shows how many pattern matches each algorithm found:

```
┌────────────────────────────────┬──────────┐
│ KMP (Knuth-Morris-Pratt)       │ 3 Matches│
│ Aho-Corasick (Multi-Pattern)   │ 3 Matches│
│ DFA (Finite State Automaton)   │ 3 Matches│
└────────────────────────────────┴──────────┘
```

**What it means:**
- All algorithms finding the same threats = High confidence
- Discrepancies = Worth investigating (rare in this system)

### Threat Details

Each detected threat shows:

- **Signature Name**: Type of malware
- **Signature ID**: Unique identifier (e.g., VIR001)
- **Threat Level**: Severity (CRITICAL/HIGH/MEDIUM/LOW)

Example:
```
┌────────────────────────────────────────┐
│ Ransomware.Cryptor.AES      [CRITICAL] │
│ VIR007                                 │
└────────────────────────────────────────┘
```

### Statistics Dashboard

At the bottom, you'll see overall statistics:

- **Total Scans**: Number of files scanned
- **Threats Found**: Total threats detected across all scans
- **Critical Threats**: Count of critical-level threats
- **Clean Scans**: Number of files with no threats

---

## Testing with Sample Files

The project includes test files in `data/test_files/`:

### 1. Clean File Test

**File**: `clean_file.txt`

**Expected Result**:
- Risk Level: **SAFE** (Green)
- Threats: **0**
- All algorithms: **0 matches**

**Purpose**: Verify no false positives

### 2. Trojan Detection Test

**File**: `infected_trojan.txt`

**Expected Result**:
- Risk Level: **HIGH** (Orange)
- Threats: **2**
- Signatures: VIR001, VIR002
- All 3 algorithms: **2 matches**

**Purpose**: Test trojan signature detection

### 3. Critical Threat Test

**File**: `infected_ransomware.txt`

**Expected Result**:
- Risk Level: **CRITICAL** (Red)
- Threats: **3**
- Signatures: VIR007, VIR008, VIR009
- All 3 algorithms: **3 matches**

**Purpose**: Test critical ransomware detection

### 4. Multi-Threat Test

**File**: `infected_mixed.txt`

**Expected Result**:
- Risk Level: **HIGH/CRITICAL**
- Threats: **10+**
- Multiple signature types
- All 3 algorithms: **10+ matches**

**Purpose**: Test multi-pattern detection

---

## API Usage

You can also use the system programmatically via the REST API.

### Scan a File

**Endpoint**: `POST /api/scan`

**Using curl**:
```bash
curl -X POST http://localhost:5000/api/scan \
  -F "file=@/path/to/file.txt"
```

**Using Python requests**:
```python
import requests

url = "http://localhost:5000/api/scan"
files = {"file": open("test_file.txt", "rb")}
response = requests.post(url, files=files)
print(response.json())
```

**Response**:
```json
{
  "success": true,
  "filename": "test_file.txt",
  "risk_level": "HIGH",
  "threat_count": 3,
  "threats_found": [
    {
      "signature_id": "VIR007",
      "signature_name": "Ransomware.Cryptor.AES",
      "threat_level": "CRITICAL"
    }
  ],
  "algorithm_detections": {
    "KMP": 3,
    "Aho-Corasick": 3,
    "DFA": 3
  }
}
```

### Get Statistics

**Endpoint**: `GET /api/stats`

```bash
curl http://localhost:5000/api/stats
```

### Get Recent Logs

**Endpoint**: `GET /api/logs?limit=10`

```bash
curl http://localhost:5000/api/logs?limit=10
```

### Get Signatures

**Endpoint**: `GET /api/signatures`

```bash
curl http://localhost:5000/api/signatures
```

### Health Check

**Endpoint**: `GET /api/health`

```bash
curl http://localhost:5000/api/health
```

---

## Advanced Usage

### Scanning Specific Algorithms Only

You can specify which algorithms to use:

```bash
curl -X POST http://localhost:5000/api/scan \
  -F "file=@test.txt" \
  -F "algorithms=KMP,DFA"
```

### Viewing Logs

Scan logs are stored in the `logs/` directory as JSON files:

```bash
cat logs/scan_log_20241013.json
```

### Adding Custom Signatures

Edit `data/virus_signatures.txt`:

```
VIR051|Custom.Malware.Test|CUSTOMPATTERNHEX|HIGH
```

Format: `SIGNATURE_ID|NAME|HEX_PATTERN|THREAT_LEVEL`

Restart the server to load new signatures.

---

## Troubleshooting

### Problem: Port 5000 Already in Use

**Solution 1**: Stop the process using port 5000
```bash
# On macOS/Linux
lsof -ti:5000 | xargs kill -9

# On Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

**Solution 2**: Change the port in `backend/app.py`
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

Then access: `http://localhost:5001`

### Problem: "Module not found" Error

**Solution**: Install required packages
```bash
pip install Flask Flask-CORS Werkzeug
```

### Problem: CORS Error in Browser

**Cause**: Opening HTML file directly instead of through the server

**Solution**: Always access via `http://localhost:5000`, not `file:///`

### Problem: Dashboard Shows "Failed to scan file"

**Checks**:
1. Is the backend server running?
2. Check the terminal for error messages
3. Try a different file
4. Check file size (max 10MB)

### Problem: No Threats Detected When Expected

**Checks**:
1. Verify the file contains the expected patterns
2. Check that signatures are loaded (see server startup)
3. Look at algorithm detection counts (should be > 0)
4. Verify pattern format in signature database

### Problem: Server Won't Start

**Checks**:
1. Python version: `python3 --version` (need 3.7+)
2. Dependencies installed: `pip list | grep -i flask`
3. No syntax errors: `python3 -m py_compile backend/app.py`
4. Port not in use: `lsof -i :5000` (macOS/Linux)

---

## Performance Tips

### For Large Files (Near 10MB Limit)

- **Aho-Corasick** is the most efficient for multiple patterns
- Scanning takes O(file_size) time regardless of signature count
- Typical scan time: 0.1 - 1 second for 10MB file

### For Many Signatures

- Aho-Corasick scales linearly with file size
- Adding more signatures has minimal impact on scan time
- The system can handle 100+ signatures efficiently

---

## Security Notes

⚠️ **Important**: This is an educational project

- Designed for learning string matching algorithms
- Not a replacement for commercial antivirus software
- Signature-based detection only (no heuristics or ML)
- Test files are simulated, not real malware

---

## Getting Help

### Documentation Files

- **README.md**: Overview and installation
- **QUICK_START.md**: Get started quickly
- **ALGORITHMS_EXPLAINED.md**: Detailed algorithm explanations
- **PROJECT_OVERVIEW.md**: Complete project documentation
- **PROJECT_PRESENTATION_GUIDE.md**: Tips for presenting
- **USAGE_GUIDE.md**: This file

### Common Questions

**Q: Can I scan my actual system files?**  
A: Yes, but remember this is a learning tool, not production antivirus.

**Q: How accurate is the detection?**  
A: 100% for known signatures in the database, 0% for unknown threats.

**Q: Can I add regex patterns?**  
A: Not currently, but you can add hex patterns to the signature database.

**Q: Why these 3 algorithms?**  
A: KMP for reliability, Aho-Corasick for multi-pattern efficiency, DFA for theoretical foundation. They complement each other perfectly.

**Q: Which algorithm is most important?**  
A: Aho-Corasick is the primary engine as it handles all 50 signatures simultaneously.

---

## System Requirements

### Minimum

- Python 3.7+
- 512MB RAM
- Modern web browser
- ~20MB disk space

### Recommended

- Python 3.9+
- 1GB RAM
- Chrome/Firefox/Safari latest version
- 50MB disk space (for logs)

---

## File Limits

- **Maximum file size**: 10MB
- **Supported file types**: All (text, binary, executables, etc.)
- **Concurrent scans**: 1 at a time (sequential)

---

## Best Practices

1. **Test with sample files first** before scanning real files
2. **Review algorithm results** - all should agree
3. **Check logs** regularly for scan history
4. **Backup signature database** before modifications
5. **Restart server** after adding new signatures

---

## Next Steps

1. ✅ Run the test script: `python test_algorithms.py`
2. ✅ Start the server: `./run_server.sh` or `python backend/app.py`
3. ✅ Open dashboard: `http://localhost:5000`
4. ✅ Test with clean file: `data/test_files/clean_file.txt`
5. ✅ Test with infected file: `data/test_files/infected_ransomware.txt`
6. ✅ Review the algorithm explanations: `ALGORITHMS_EXPLAINED.md`
7. ✅ Prepare presentation: `PROJECT_PRESENTATION_GUIDE.md`

---

Enjoy exploring string matching algorithms and virus detection! 🛡️
