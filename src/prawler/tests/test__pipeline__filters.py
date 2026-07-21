from prawler.pipeline.filters import make_filter_stage

def test_filtro_ia_ignora_verbo_ir():
    stage = make_filter_stage(
        r'body ~= \b(?-i:IA)\b|\bChatGPT\b|\bClaude\s*Code\b|\bintelig[êe]ncia\s+artificial\b'
    )

    registros = [
        {"id": "1", "body": "eu ia sair mas usei o ChatGPT"},   # deve passar
        {"id": "2", "body": "ele ia embora de casa"},               # NÃO deve passar
        {"id": "3", "body": "a IA está avançando muito"},        # deve passar
        {"id": "4", "body": "testei o Claude Code ontem"},       # deve passar
        {"id": "5", "body": "inteligência artificial no dia a dia"}, # deve passar
        {"id": "6", "body": "ele INTELIGENCIA ARTIFICIAL embora de casa"},
        {"id": "7", "body": "EU AMO A INTEligencia artificial"},
        {"id": "8", "body": "Ele comentou que viria aqui em casa, mas não veio o inteligência."},  # NÃO deve passar
    ]

    resultado = list(stage(iter(registros)))
    ids_aprovados = {r["id"] for r in resultado}

    assert ids_aprovados == {"1", "3", "4", "5", "6", "7"}  # O registro 2 não deve passar, mas o registro 6 e 7 devem passar