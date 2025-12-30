from pathlib import Path
import subprocess
import sys
import platform


def run_command(command):
    return subprocess.run(command, check=True)


def main():
    print("--- Quran Semantic Search Setup ---")

    # 1. Create Virtual Environment
    venv_dir = Path("venv")
    if not venv_dir.exists():
        print("Creating virtual environment...")
        run_command([sys.executable, "-m", "venv", str(venv_dir)])

    # 2. Determine pip & python paths based on OS
    if platform.system() == "Windows":
        pip_path = venv_dir / "Scripts" / "pip"
        python_executable = venv_dir / "Scripts" / "python"
    else:
        pip_path = venv_dir / "bin" / "pip"
        python_executable = venv_dir / "bin" / "python"

    # 3. Install Requirements
    print("Installing dependencies...")
    run_command([str(pip_path), "install", "-r", "requirements.txt"])

    # 4. Prepare Quran Data
    print("Preparing Quran data...")
    run_command([str(python_executable), "-m", "scripts.prepare_quran"])

    # 5. Prepare Translations Data
    print("Preparing translations data...")
    run_command([str(python_executable), "-m", "scripts.prepare_translations"])

    # 6. Embed Quran Data
    print("Embedding Quran data...")
    run_command([str(python_executable), "-m", "scripts.embed_quran"])

    # 7. Embed Translations Data
    print("Embedding translations data...")
    target_langs = input(
        "Enter target language codes separated by spaces (or press Enter for all): "
    ).strip()
    run_command(
        [str(python_executable), "-m", "scripts.embed_translations", target_langs]
    )

    print("Setup completed successfully! you can now run the API using:")
    print(f"uvicorn api.main:app")


if __name__ == "__main__":
    main()
