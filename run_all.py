"""
Runs every step in the project, in order, the same way the README
does, and prints each result. Also saves everything into
check_results.json, which network_demo.html can show directly.

This is the one-command way to run the whole project.
"""

import json
import subprocess
import sys

STEPS = [
    ("Baseline network", ["python3", "networks/baseline.py"]),
    ("Benes network", ["python3", "-m", "networks.benes"]),
    ("Clos network", ["python3", "-m", "networks.clos"]),
    ("XGFT network", ["python3", "-m", "networks.xgft"]),
    ("Baseline routing check", ["python3", "-m", "tests.check_baseline_routing"]),
    ("Benes routing check", ["python3", "-m", "tests.check_benes_routing"]),
    ("Clos routing check", ["python3", "-m", "tests.check_clos_routing"]),
    ("XGFT routing check", ["python3", "-m", "tests.check_xgft_routing"]),
    ("Clos blocking check", ["python3", "-m", "tests.check_clos_blocking"]),
    ("Traffic demo", ["python3", "run_demo.py"]),
    ("Pictures", ["python3", "draw_networks.py"]),
    ("Scaling analysis", ["python3", "scaling_analysis.py"]),
    ("Blocking analysis", ["python3", "blocking_analysis.py"]),
    ("Demo page data", ["python3", "export_demo_data.py"]),
    ("Blocking demo data", ["python3", "export_blocking_demo.py"]),
]


def main():
    results = []
    ok = True
    for label, command in STEPS:
        print(f"\n=== {label} ===")
        result = subprocess.run(command, capture_output=True, text=True)
        print(result.stdout, end="")
        if result.returncode != 0:
            print(result.stderr, end="")
            ok = False
        results.append({"label": label, "output": result.stdout, "passed": result.returncode == 0})

    with open("check_results.json", "w") as f:
        json.dump(results, f, indent=2)

    print("\n=== Done ===")
    print("All steps passed." if ok else "Some steps failed, see above.")
    print("Saved check_results.json")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
