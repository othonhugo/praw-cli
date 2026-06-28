.PHONY: help lint format typecheck test bump-patch bump-minor bump-major

help:
	@echo "Comandos disponíveis:"
	@echo "  make lint           - Executa a verificação de código com ruff"
	@echo "  make format         - Formata o código com ruff"
	@echo "  make typecheck      - Executa a checagem de tipos estática com mypy"
	@echo "  make test           - Executa os testes unitários com pytest"
	@echo "  make bump-patch     - Aumenta a versão (patch, ex: 0.2.0 -> 0.2.1)"
	@echo "  make bump-minor     - Aumenta a versão (minor, ex: 0.2.0 -> 0.3.0)"
	@echo "  make bump-major     - Aumenta a versão (major, ex: 0.2.0 -> 1.0.0)"

lint:
	uv run ruff check src/
	uv run ruff format --check src/

format:
	uv run ruff format src/

typecheck:
	uv run mypy src/

test:
	uv run pytest

bump-patch:
	uv version --bump patch

bump-minor:
	uv version --bump minor

bump-major:
	uv version --bump major
