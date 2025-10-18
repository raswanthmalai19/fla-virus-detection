// API Configuration
const API_BASE_URL = 'http://localhost:5000/api';

// State
let selectedFile = null;

// DOM Elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const fileInfo = document.getElementById('fileInfo');
const fileName = document.getElementById('fileName');
const fileSize = document.getElementById('fileSize');
const removeFileBtn = document.getElementById('removeFile');
const scanButton = document.getElementById('scanButton');
const resultsSection = document.getElementById('resultsSection');
const loadingOverlay = document.getElementById('loadingOverlay');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    loadStatistics();
    loadSignatureCount();
});

// Setup Event Listeners
function setupEventListeners() {
    // Upload area click
    uploadArea.addEventListener('click', () => fileInput.click());
    
    // File input change
    fileInput.addEventListener('change', handleFileSelect);
    
    // Drag and drop
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleDrop);
    
    // Remove file button
    removeFileBtn.addEventListener('click', removeFile);
    
    // Scan button
    scanButton.addEventListener('click', scanFile);
}

// Handle file selection
function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) {
        setSelectedFile(file);
    }
}

// Handle drag over
function handleDragOver(event) {
    event.preventDefault();
    uploadArea.classList.add('drag-over');
}

// Handle drag leave
function handleDragLeave(event) {
    event.preventDefault();
    uploadArea.classList.remove('drag-over');
}

// Handle drop
function handleDrop(event) {
    event.preventDefault();
    uploadArea.classList.remove('drag-over');
    
    const file = event.dataTransfer.files[0];
    if (file) {
        setSelectedFile(file);
    }
}

// Set selected file
function setSelectedFile(file) {
    selectedFile = file;
    
    // Show file info
    fileName.textContent = file.name;
    fileSize.textContent = formatFileSize(file.size);
    
    uploadArea.style.display = 'none';
    fileInfo.style.display = 'flex';
    scanButton.disabled = false;
}

// Remove file
function removeFile(event) {
    event.stopPropagation();
    selectedFile = null;
    fileInput.value = '';
    
    uploadArea.style.display = 'block';
    fileInfo.style.display = 'none';
    scanButton.disabled = true;
}

// Scan file
async function scanFile() {
    if (!selectedFile) return;
    
    showLoading(true);
    
    try {
        const formData = new FormData();
        formData.append('file', selectedFile);
        
        const response = await fetch(`${API_BASE_URL}/scan`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error('Scan failed');
        }
        
        const data = await response.json();
        
        if (data.success) {
            displayResults(data);
            loadStatistics(); // Refresh statistics
        } else {
            alert('Error: ' + data.error);
        }
        
    } catch (error) {
        console.error('Scan error:', error);
        alert('Failed to scan file. Please ensure the backend server is running.');
    } finally {
        showLoading(false);
    }
}

// Display scan results
function displayResults(data) {
    // Show results section
    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth' });
    
    // Status badge
    const statusBadge = document.getElementById('statusBadge');
    const statusText = document.getElementById('statusText');
    const statusIcon = document.getElementById('statusIcon');
    
    statusBadge.className = 'status-badge ' + data.risk_level.toLowerCase();
    statusText.textContent = data.risk_level;
    
    // Update status icon based on risk level
    if (data.risk_level === 'SAFE') {
        statusIcon.innerHTML = '<polyline points="20 6 9 17 4 12"/>';
    } else {
        statusIcon.innerHTML = '<line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>';
    }
    
    // Threat count
    document.getElementById('threatCount').textContent = data.threat_count;
    
    // Scan info
    document.getElementById('scannedFile').textContent = data.filename;
    document.getElementById('scanTime').textContent = data.timestamp;
    document.getElementById('scannedSize').textContent = formatFileSize(data.file_size);
    
    // Algorithm detections
    displayAlgorithmResults(data.algorithm_detections);
    
    // Threats
    if (data.threats_found && data.threats_found.length > 0) {
        displayThreats(data.threats_found);
    } else {
        document.getElementById('threatsSection').style.display = 'none';
    }
}

// Display algorithm results
function displayAlgorithmResults(detections) {
    const algorithmGrid = document.getElementById('algorithmGrid');
    algorithmGrid.innerHTML = '';
    
    const algorithms = [
        { key: 'KMP', name: 'KMP (Knuth-Morris-Pratt)' },
        { key: 'Aho-Corasick', name: 'Aho-Corasick (Multi-Pattern)' },
        { key: 'DFA', name: 'DFA (Finite State Automaton)' }
    ];
    
    algorithms.forEach(algo => {
        const matches = detections[algo.key] || 0;
        
        const card = document.createElement('div');
        card.className = 'algorithm-card';
        card.innerHTML = `
            <div class="algorithm-name">${algo.name}</div>
            <div class="algorithm-matches">${matches}</div>
            <div class="algorithm-label">Matches</div>
        `;
        
        algorithmGrid.appendChild(card);
    });
}

// Display threats
function displayThreats(threats) {
    const threatsSection = document.getElementById('threatsSection');
    const threatsList = document.getElementById('threatsList');
    
    threatsSection.style.display = 'block';
    threatsList.innerHTML = '';
    
    threats.forEach(threat => {
        const item = document.createElement('div');
        item.className = `threat-item ${threat.threat_level.toLowerCase()}`;
        item.innerHTML = `
            <div class="threat-info">
                <div class="threat-name">${threat.signature_name}</div>
                <div class="threat-id">${threat.signature_id}</div>
            </div>
            <div class="threat-level ${threat.threat_level.toLowerCase()}">
                ${threat.threat_level}
            </div>
        `;
        
        threatsList.appendChild(item);
    });
}

// Load statistics
async function loadStatistics() {
    try {
        const response = await fetch(`${API_BASE_URL}/stats`);
        
        if (!response.ok) return;
        
        const data = await response.json();
        
        if (data.success) {
            const stats = data.statistics;
            
            document.getElementById('totalScans').textContent = stats.total_scans;
            document.getElementById('totalThreats').textContent = stats.total_threats_detected;
            document.getElementById('criticalThreats').textContent = stats.threat_levels.CRITICAL || 0;
            
            // Calculate clean files
            const cleanFiles = stats.total_scans - stats.total_threats_detected;
            document.getElementById('cleanFiles').textContent = Math.max(0, cleanFiles);
        }
    } catch (error) {
        console.error('Failed to load statistics:', error);
    }
}

// Load signature count
async function loadSignatureCount() {
    try {
        const response = await fetch(`${API_BASE_URL}/signatures`);
        
        if (!response.ok) return;
        
        const data = await response.json();
        
        if (data.success) {
            document.getElementById('signatureCount').textContent = data.count;
        }
    } catch (error) {
        console.error('Failed to load signature count:', error);
    }
}

// Show/hide loading overlay
function showLoading(show) {
    if (show) {
        loadingOverlay.classList.add('active');
    } else {
        loadingOverlay.classList.remove('active');
    }
}

// Format file size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
}

// Auto-refresh statistics every 30 seconds
setInterval(loadStatistics, 30000);
