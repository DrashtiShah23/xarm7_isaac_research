from pathlib import Path
import platform
import sys

def main():
    root = Path(__file__).resolve().parents[2]
    required_paths = [
        "assets/usd",
        "assets/urdf",
        "assets/meshes",
        "scenes",
        "screenshots",
        "notes",
        "docs",
        "scripts/python",
        "scripts/windows",
        "scripts/ubuntu",
        "github_repos",
        "experiments/logs",
        "experiments/results",
    ]

    print("xArm7 Isaac Sim workspace check")
    print("Root:", root)
    print("Operating system:", platform.platform())
    print("Python:", sys.version)

    missing = []
    for item in required_paths:
        path = root / item
        if path.exists():
            print("OK:", item)
        else:
            print("Missing:", item)
            missing.append(item)

    if missing:
        print("Workspace check failed.")
        print("Create the missing folders listed above.")
    else:
        print("Workspace check passed.")

if __name__ == "__main__":
    main()
