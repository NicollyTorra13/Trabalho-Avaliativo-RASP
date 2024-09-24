class Autorizacoes:
    def __init__(self):
        # Dicionário de autorizações com tags como chaves e nomes como valores
        self._autorizados = {
            123456789: "João Silva",
            987654321: "Maria Souza",
            555666777: "Carlos Pereira"
        }

    def __contains__(self, tag):
        # Verifica se a tag está no dicionário de autorizados
        return tag in self._autorizados

    def __getitem__(self, tag):
        # Retorna o nome do colaborador a partir da tag, se ela estiver autorizada
        return self._autorizados.get(tag, None)

    def adicionar_autorizacao(self, tag, nome):
        # Adiciona uma nova tag e nome ao dicionário de autorizados
        self._autorizados[tag] = nome

    def remover_autorizacao(self, tag):
        # Remove uma tag do dicionário de autorizados
        if tag in self._autorizados:
            del self._autorizados[tag]
