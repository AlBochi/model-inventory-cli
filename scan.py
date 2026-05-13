#!/usr/bin/env python3
"""
Model Inventory CLI — Saillent
Scans enterprise directories for AI/ML model artifacts and generates
an OSFI E-23 / SR 11-7 compliant inventory report.
"""

import os
import json
import hashlib
import argparse
from datetime import datetime
from pathlib import Path

MODEL_EXTENSIONS = {".pkl", ".h5", ".onnx", ".pt", ".pth", ".pb", ".sav", ".joblib", ".mar", ".pmml"}

def scan_directory(root_path, approved_registry=None):
    inventory = []
    registry = set()
    
    if approved_registry and os.path.exists(approved_registry):
        with open(approved_registry) as f:
            registry = {line.strip() for line in f if line.strip()}
    
    for ext in MODEL_EXTENSIONS:
        for filepath in Path(root_path).rglob(f"*{ext}"):
            stat = filepath.stat()
            file_hash = hashlib.sha256(filepath.read_bytes()).hexdigest()[:16]
            
            entry = {
                "model_name": filepath.name,
                "type": ext.replace(".", ""),
                "path": str(filepath),
                "size_kb": round(stat.st_size / 1024, 2),
                "last_modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "sha256_prefix": file_hash,
                "in_registry": str(filepath) in registry,
                "risk_flag": "OK" if str(filepath) in registry else "SHADOW_AI"
            }
            inventory.append(entry)
    
    return inventory

def generate_report(inventory):
    total = len(inventory)
    registered = sum(1 for m in inventory if m["in_registry"])
    shadow = total - registered
    
    report = {
        "generated_at": datetime.now().isoformat(),
        "framework": "OSFI E-23 / SR 11-7",
        "inventory": inventory,
        "summary": {
            "total_models": total,
            "registered_models": registered,
            "shadow_ai_models": shadow,
            "compliance_gap": f"{(shadow/total*100):.1f}%" if total > 0 else "0%"
        },
        "recommendations": []
    }
    
    if shadow > 0:
        report["recommendations"].append(f"IMMEDIATE ACTION: {shadow} unregistered models detected. Initiate Shadow AI governance review.")
    if total == 0:
        report["recommendations"].append("No models found. Verify scan directory or model storage patterns.")
    if registered == total and total > 0:
        report["recommendations"].append("All models registered. Maintain current governance cadence.")
    
    return report

def main():
    parser = argparse.ArgumentParser(description="Saillent Model Inventory CLI")
    parser.add_argument("path", help="Root directory to scan")
    parser.add_argument("--registry", help="Path to approved model registry file", default=None)
    parser.add_argument("--output", help="Output JSON file", default="model_inventory_report.json")
    args = parser.parse_args()
    
    print(f"\n🔍 Saillent Model Inventory CLI")
    print(f"   Scanning: {args.path}")
    print(f"   Framework: OSFI E-23 / SR 11-7\n")
    
    inventory = scan_directory(args.path, args.registry)
    report = generate_report(inventory)
    
    with open(args.output, "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"✅ Scan complete.")
    print(f"   Total models found: {report['summary']['total_models']}")
    print(f"   Registered: {report['summary']['registered_models']}")
    print(f"   ⚠️  Shadow AI: {report['summary']['shadow_ai_models']}")
    print(f"   Compliance gap: {report['summary']['compliance_gap']}")
    print(f"   Report saved: {args.output}\n")
    
    for rec in report["recommendations"]:
        print(f"   📋 {rec}")

if __name__ == "__main__":
    main()
