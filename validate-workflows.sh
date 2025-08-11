#!/bin/bash

# Simple YAML syntax checker for GitHub workflows
echo "🔍 Checking workflow syntax..."

WORKFLOW_DIR="c:/Users/swij5678/OneDrive - Sysco Corporation/Documents/test/python-service/.github/workflows"

# Check if Python is available for basic validation
if ! command -v python3 &> /dev/null; then
    echo "⚠️  Python3 not found, skipping validation"
    exit 0
fi

# Basic Python YAML validation
python3 << 'EOF'
import yaml
import os
import glob

workflow_dir = r"c:\Users\swij5678\OneDrive - Sysco Corporation\Documents\test\python-service\.github\workflows"
errors = []

for yaml_file in glob.glob(os.path.join(workflow_dir, "*.yml")):
    try:
        with open(yaml_file, 'r', encoding='utf-8') as f:
            yaml.safe_load(f)
        print(f"✅ {os.path.basename(yaml_file)} - Valid YAML syntax")
    except yaml.YAMLError as e:
        errors.append(f"❌ {os.path.basename(yaml_file)} - {str(e)}")
        print(f"❌ {os.path.basename(yaml_file)} - {str(e)}")
    except Exception as e:
        errors.append(f"❌ {os.path.basename(yaml_file)} - {str(e)}")
        print(f"❌ {os.path.basename(yaml_file)} - {str(e)}")

if errors:
    print(f"\n🚨 Found {len(errors)} YAML syntax errors")
    exit(1)
else:
    print(f"\n✅ All workflow files have valid YAML syntax")
    exit(0)
EOF
