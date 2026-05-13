# Model Inventory CLI

A command-line tool to scan and catalog AI models across an organization. Built for financial institutions preparing for OSFI E-23 and SR 11-7 compliance.

## What It Does

- Scans directories and codebases for model files (.pkl, .h5, .onnx, .pt, etc.)
- Generates a JSON inventory with model name, type, location, and last modified date
- Flags potential Shadow AI — models not in the approved registry
- Outputs a compliance-ready audit report

## Why It Matters

OSFI E-23 and SR 11-7 require institutions to maintain a complete AI model inventory. Most firms cannot answer the question: "How many AI models are running in this organization right now?" This tool provides the answer.

## Quick Start

git clone https://github.com/AlBochi/model-inventory-cli.git
cd model-inventory-cli
pip install -r requirements.txt
python scan.py /path/to/your/codebase

## Output


## Regulatory Alignment

- OSFI E-23 Model Inventory Requirements
- SR 11-7 Model Identification and Classification
- CFPB Fair Lending Model Documentation

## Status

Proof of concept. Built by Saillent to demonstrate what enterprise-grade model inventory should look like.

## License

MIT
