import pytest

# Simulando um banco de dados em memória
banco_de_dados = []

def registrar_aluno(nome, email, idade):
    """Registra um aluno no banco de dados simulado"""
    for aluno in banco_de_dados:
        if aluno["email"] == email:
            return {"erro": "Aluno já cadastrado"}, 400
    novo_aluno = {"nome": nome, "email": email, "idade": idade}
    banco_de_dados.append(novo_aluno)
    return novo_aluno, 201

def consultar_alunos():
    """Retorna a lista de alunos cadastrados"""
    return banco_de_dados, 200

@pytest.fixture
def limpar_banco():
    """Esvazia o banco de dados antes de cada teste"""
    global banco_de_dados
    banco_de_dados = []

def test_registro_aluno(limpar_banco):
    """Testa o registro de um aluno no banco de dados"""
    aluno, status = registrar_aluno("João Silva", "joao.silva@email.com", 20)
    assert status == 201
    assert aluno["nome"] == "João Silva"
    assert aluno["email"] == "joao.silva@email.com"
    assert aluno["idade"] == 20

def test_consulta_aluno(limpar_banco):
    """Testa a consulta do aluno cadastrado"""
    registrar_aluno("João Silva", "joao.silva@email.com", 20)
    alunos, status = consultar_alunos()
    assert status == 200
    assert any(aluno["email"] == "joao.silva@email.com" for aluno in alunos)

def test_registro_duplicado(limpar_banco):
    """Testa a tentativa de registrar um aluno já existente"""
    registrar_aluno("João Silva", "joao.silva@email.com", 20)
    resposta, status = registrar_aluno("João Silva", "joao.silva@email.com", 20)
    assert status == 400
    assert "erro" in resposta

