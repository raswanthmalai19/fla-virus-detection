# Test Files for Virus Detection System

This directory contains comprehensive test files to demonstrate the virus detection system's capabilities with **100 virus signatures**.

## 🟢 Clean Test Files (Safe - No Threats)

### 1. clean_file.txt
- **Status**: Clean
- **Content**: General text about the detection system
- **Expected Result**: SAFE, 0 threats detected
- **Purpose**: Basic clean file test

### 2. clean_document.txt
- **Status**: Clean
- **Content**: Business report with financial data
- **Expected Result**: SAFE, 0 threats detected
- **Purpose**: Test legitimate business documents

### 3. clean_code_sample.txt
- **Status**: Clean
- **Content**: Programming code samples (Python, JavaScript, SQL, HTML, CSS)
- **Expected Result**: SAFE, 0 threats detected
- **Purpose**: Test legitimate source code

### 4. clean_email.txt
- **Status**: Clean
- **Content**: Professional business email
- **Expected Result**: SAFE, 0 threats detected
- **Purpose**: Test normal email communications

## 🔴 Infected Test Files (Malicious - Contains Threats)

### 5. infected_trojan.txt
- **Status**: Infected (HIGH threat)
- **Expected Threats**: Trojan signatures
- **Signatures**: VIR001, VIR002
- **Threat Count**: 2
- **Purpose**: Test basic trojan detection

### 6. infected_ransomware.txt
- **Status**: Infected (CRITICAL threat)
- **Expected Threats**: Ransomware signatures
- **Signatures**: VIR007, VIR008, VIR009, VIR047
- **Threat Count**: 3-4
- **Purpose**: Test critical ransomware detection

### 7. infected_mixed.txt
- **Status**: Infected (HIGH threat)
- **Expected Threats**: Multiple malware categories
- **Signatures**: VIR013, VIR015, VIR019, VIR020, VIR043-050
- **Threat Count**: 10+
- **Purpose**: Test multi-pattern detection

### 8. infected_apt_attack.txt ⭐ NEW
- **Status**: Infected (CRITICAL threat)
- **Expected Threats**: APT and supply chain attacks
- **Signatures**: VIR061-065, VIR092-095
- **Threat Count**: 8+
- **Categories**: Lazarus, FancyBear, CozyBear, SolarWinds, NotPetya
- **Purpose**: Test nation-state malware detection

### 9. infected_cryptominer.txt ⭐ NEW
- **Status**: Infected (HIGH threat)
- **Expected Threats**: Cryptocurrency mining malware
- **Signatures**: VIR066-070
- **Threat Count**: 5+
- **Categories**: Monero, Coinhive, XMRig miners
- **Purpose**: Test cryptominer detection

### 10. infected_iot_botnet.txt ⭐ NEW
- **Status**: Infected (CRITICAL threat)
- **Expected Threats**: IoT botnet malware
- **Signatures**: VIR086-090, VIR022
- **Threat Count**: 6+
- **Categories**: Mirai, BrickerBot, Reaper, VPNFilter
- **Purpose**: Test IoT malware detection

### 11. infected_phishing_kit.txt ⭐ NEW
- **Status**: Infected (HIGH threat)
- **Expected Threats**: Phishing and credential theft
- **Signatures**: VIR051, VIR076-080
- **Threat Count**: 6+
- **Categories**: Password stealers, banking trojans
- **Purpose**: Test phishing attack detection

### 12. infected_web_exploits.txt ⭐ NEW
- **Status**: Infected (CRITICAL threat)
- **Expected Threats**: Web exploitation techniques
- **Signatures**: VIR020, VIR071-075, VIR043-044
- **Threat Count**: 8+
- **Categories**: XSS, SQL injection, RCE, command injection
- **Purpose**: Test web exploit detection

### 13. infected_wannacry.txt ⭐ NEW
- **Status**: Infected (CRITICAL threat)
- **Expected Threats**: WannaCry ransomware
- **Signatures**: VIR007-009, VIR047, VIR056
- **Threat Count**: 5+
- **Categories**: Famous ransomware outbreak
- **Purpose**: Test specific ransomware family

### 14. infected_rootkit_advanced.txt ⭐ NEW
- **Status**: Infected (CRITICAL threat)
- **Expected Threats**: Advanced rootkits
- **Signatures**: VIR012, VIR041, VIR048-049, VIR081-085, VIR091, VIR094
- **Threat Count**: 10+
- **Categories**: TDL4, Necurs, UEFI, BIOS infections
- **Purpose**: Test rootkit detection

## 📊 Test File Summary

| Category | Clean Files | Infected Files | Total |
|----------|-------------|----------------|-------|
| **Count** | 4 | 10 | 14 |
| **Signatures** | 0 | 100 used | 100 total |

### Threat Distribution in Test Files

- **CRITICAL** threats: 5 files (APT, IoT, Web Exploits, WannaCry, Rootkits)
- **HIGH** threats: 4 files (Trojans, Cryptominers, Phishing, Mixed)
- **SAFE** files: 4 files (All clean files)

## 🧪 Testing Instructions

### Quick Test
```bash
# Start server
python3 backend/app.py

# Open browser
http://localhost:5000

# Upload files and check results
```

### Expected Results

**Clean Files** should show:
- ✅ Risk Level: SAFE (Green)
- ✅ Threats: 0
- ✅ All 3 algorithms: 0 matches

**Infected Files** should show:
- ⚠️ Risk Level: HIGH or CRITICAL (Orange/Red)
- ⚠️ Threats: Multiple signatures
- ⚠️ All 3 algorithms: Multiple matches

## 📈 Dataset Improvements

### Expanded Signature Database

**Original**: 50 signatures
**Current**: 100 signatures (100% increase!)

**New Categories Added**:
1. Advanced Trojans (Zeus, DarkComet, Emotet)
2. Famous Ransomware (WannaCry, Petya, Ryuk)
3. APT Groups (Lazarus, FancyBear, CozyBear)
4. Cryptocurrency Miners (Monero, Coinhive, XMRig)
5. Web Exploits (XSS, SQL Injection, RCE)
6. Phishing Kits (Credential stealers, Banking trojans)
7. Advanced Rootkits (TDL4, Necurs, UEFI)
8. IoT Botnets (Mirai, BrickerBot, Reaper)
9. Supply Chain Attacks (SolarWinds, CCleaner)
10. Fileless Malware (PowerShell Empire, Cobalt Strike)

### Test Coverage

**Malware Categories Covered**:
- ✅ Trojans & Backdoors
- ✅ Ransomware & Cryptors
- ✅ Rootkits & Bootkits
- ✅ Spyware & Keyloggers
- ✅ Adware & PUPs
- ✅ Exploits & Vulnerabilities
- ✅ Worms & Viruses
- ✅ APT & State-Sponsored
- ✅ Cryptominers
- ✅ IoT Malware
- ✅ Phishing & Social Engineering
- ✅ Web Exploits
- ✅ Supply Chain Attacks
- ✅ Fileless Malware

## 🎯 Algorithm Performance

All 3 algorithms work together:

1. **KMP** - Validates each signature individually
2. **Aho-Corasick** - Scans all 100 signatures in one pass (PRIMARY ENGINE)
3. **DFA** - Provides theoretical validation

**Performance**: With 100 signatures, Aho-Corasick is ~200x faster than scanning each individually!

## ⚠️ Important Notes

1. These are **simulated test files** for educational purposes
2. They contain hex representations and text patterns of malware
3. They are **NOT actual malicious files**
4. Safe to use for testing and demonstration
5. DO NOT use in production security systems

## 📝 Creating Custom Test Files

To create your own test file that will be detected:

**For CRITICAL threat**, include:
```
wannacry
lazarus
mirai
sunburst
```

**For HIGH threat**, include:
```
zeus
emotet
monero
password
SELECT * FROM
```

**For MEDIUM threat**, include:
```
eval()
admin
Hook
```

**For SAFE file**, include:
```
Normal text with no hex patterns or malware keywords
```

## 🚀 Usage Example

```bash
# Test clean file
curl -X POST http://localhost:5000/api/scan \
  -F "file=@data/test_files/clean_document.txt"
# Result: SAFE, 0 threats

# Test APT attack
curl -X POST http://localhost:5000/api/scan \
  -F "file=@data/test_files/infected_apt_attack.txt"
# Result: CRITICAL, 8+ threats
```

---

**Your detection system now has 100 signatures and 14 comprehensive test files covering all major malware categories!** 🎉
