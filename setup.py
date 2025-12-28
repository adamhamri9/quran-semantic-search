import os
import subprocess
import sys
import platform

def run_command(command):
    return subprocess.run(command, shell=True, check=True)

def main():
    print("--- Quran Semantic Search Setup ---")

    # 1. Create Virtual Environment
    if not os.path.exists("venv"):
        print("Creating virtual environment...")
        run_command(f"{sys.executable} -m venv venv")

    # 2. Determine pip path based on OS
    if platform.system() == "Windows":
        pip_path = os.path.join("venv", "Scripts", "pip")
        python_executable = os.path.join("venv", "Scripts", "python")
    else:
        pip_path = os.path.join("venv", "bin", "pip")
        python_executable = os.path.join("venv", "bin", "python")

    # 3. Install Requirements
    print("Installing dependencies...")
    run_command(f"{pip_path} install --upgrade pip")
    run_command(f"{pip_path} install -r requirements.txt")

    # 4. Prepare Quran Data
    print("Preparing Quran data...")
    run_command(f"{python_executable} scripts/prepare_quran.py")

    # 5. Prepare Translations Data
    print("Preparing translations data...")
    run_command(f"{python_executable} scripts/prepare_translations.py")

    # 6. Embed Quran Data
    print("Embedding Quran data...")
    run_command(f"{python_executable} scripts/embed_quran.py")

    # 7. Embed Translations Data
    print("Embedding translations data...")
    target_langs = input("Enter target language codes separated by spaces (or press Enter for all): ").strip()
    run_command(f"{python_executable} scripts/embed_translations.py {target_langs}")

    print("Setup completed successfully!")

if __name__ == "__main__":
    main()