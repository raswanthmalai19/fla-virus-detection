"""Evaluation of Virus Signature Detection System."""
import os
from backend.detector import VirusDetector

def evaluate(test_dir):
    detector = VirusDetector()
    files = os.listdir(test_dir)
    TP, FP, FN, TN = 0, 0, 0, 0
    
    for fname in files:
        fpath = os.path.join(test_dir, fname)
        # Determine ground truth from filename
        is_infected = fname.startswith('infected_')
        result = detector.scan_file(fpath)
        detected = result.get('risk_level', 'SAFE') != 'SAFE'
        if is_infected and detected:
            TP += 1
        elif not is_infected and detected:
            FP += 1
        elif is_infected and not detected:
            FN += 1
        elif not is_infected and not detected:
            TN += 1
    
    precision = TP / (TP + FP) if (TP + FP) > 0 else 0
    recall = TP / (TP + FN) if (TP + FN) > 0 else 0
    accuracy = (TP + TN) / (TP + FP + FN + TN) if (TP + FP + FN + TN) > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    
    print(f"True Positives: {TP}")
    print(f"False Positives: {FP}")
    print(f"False Negatives: {FN}")
    print(f"True Negatives: {TN}")
    print(f"Accuracy: {accuracy * 100:.2f}%")
    print(f"Precision: {precision * 100:.2f}%")
    print(f"Recall: {recall * 100:.2f}%")
    print(f"F1 Score: {f1 * 100:.2f}%")
    return accuracy * 100

if __name__ == "__main__":
    test_dir = "data/test_files"
    acc = evaluate(test_dir)
    if acc >= 94:
        print("Project meets accuracy requirement (>=94%)")
    else:
        print("Project does NOT meet accuracy requirement (<94%)")
