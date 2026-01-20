# Contributing to Quran Semantic Search API

First off, thanks for taking the time to contribute! 🎉

This project is a **learning experiment** and a **Work in Progress**. We welcome contributions that help improve the semantic accuracy, code quality, or documentation.

---

## Getting Started

1. **Fork the repository** on GitHub.
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/your-username/quran-semantic-search.git
   cd quran-semantic-search
   ```
3. **Set up the environment**:
   We use a helper script to manage setup.
   ```bash
   python setup.py
   ```
   This will create a virtual environment, install dependencies, and generate necessary indices.

---

## Development Workflow

1. **Create a branch** for your feature or fix:
   ```bash
   git checkout -b feat/amazing-feature
   ```
2. **Make your changes**. Keep them focused and atomic.
3. **Test your changes**. Ensure the API runs and returns expected results.
   ```bash
   uvicorn api.main:app --reload
   ```

---

## Coding Standards

- **Python**: Follow PEP 8 style guide.
- **Type Hinting**: Use Python type hints heavily, especially for function arguments and return values.
- **FastAPI**: Use Pydantic models for all request/response schemas.
- **Simplicity**: Prefer readable, simple code over complex "clever" solutions.

---

## Commit Messages

We strictly follow the **Conventional Commits** specification.

**Format**: `<type>(<scope>): <description>`

**Types**:
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Changes that do not affect the meaning of the code (white-space, formatting, etc)
- `refactor`: A code change that neither fixes a bug nor adds a feature
- `chore`: Changes to the build process or auxiliary tools

**Example**:
```text
feat(search): implement context window for related ayahs
```

---

## Pull Requests

1. Push your branch to GitHub.
2. Open a Pull Request against the `main` branch.
3. Provide a clear title and description of what you changed and why.
4. Link to any relevant issues (e.g., `Closes #1`).

---

## Disclaimer

Please remember this is an educational project. Be kind and patient in your communications.
