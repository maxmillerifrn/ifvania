"""Classes dos encontros antigos, mantidos durante a migração da campanha.

A base executa as primitivas de ataque; cada professor decide sua estratégia.
A inclusão na campanha IFVania ainda depende de revisão narrativa.
"""
from entidades.chefe import Chefe
from entidades.romer_bug import RomerBug


class ChefePython(Chefe):
    def choose_attack(self, jogador):
        # Mantém distância com disparos; investe se o aluno se aproxima.
        return "lunge" if abs(jogador.rect.centerx - self.rect.centerx) < 90 else "spread"


class ChefeJava(Chefe):
    def choose_attack(self, jogador):
        # Alterna duas etapas de ataque, sem sorteio de comportamento genérico.
        self.passo_sequencia = getattr(self, 'passo_sequencia', 0) + 1
        return "slam" if self.passo_sequencia % 2 else "lunge"


class ChefeC(Chefe):
    def choose_attack(self, jogador):
        # Pressiona o corpo a corpo; usa tiros ao entrar nas fases de baixa vida.
        return "lunge" if self.etapa == 1 else "spread"


class ChefeSQL(Chefe):
    def choose_attack(self, jogador):
        # Disparos laterais quando o aluno está abaixo; leque no mesmo patamar.
        return "slam" if jogador.rect.centery > self.rect.centery else "spread"


class ChefeAssembly(Chefe):
    def choose_attack(self, jogador):
        # Combina as três primitivas em um ciclo próprio.
        ataques = ("spread", "lunge", "slam")
        passo = getattr(self, 'passo_sequencia', 0)
        self.passo_sequencia = passo + 1
        return ataques[passo % len(ataques)]


CLASSES_CHEFES = {
    "romerbug": RomerBug,
    "python": ChefePython,
    "java": ChefeJava,
    "c": ChefeC,
    "sql": ChefeSQL,
    "assembly": ChefeAssembly,
}
