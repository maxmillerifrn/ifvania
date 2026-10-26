"""Classes dos encontros antigos, mantidos durante a migração da campanha.

A base executa as primitivas de ataque; cada professor decide sua estratégia.
A inclusão na campanha IFVania ainda depende de revisão narrativa.
"""
from entities.boss import Boss
from entities.romer_bug import RomerBug


class PythonBoss(Boss):
    def choose_attack(self, player):
        # Mantém distância com disparos; investe se o aluno se aproxima.
        return "lunge" if abs(player.rect.centerx - self.rect.centerx) < 90 else "spread"


class JavaBoss(Boss):
    def choose_attack(self, player):
        # Alterna duas etapas de ataque, sem sorteio de comportamento genérico.
        self.combo_step = getattr(self, "combo_step", 0) + 1
        return "slam" if self.combo_step % 2 else "lunge"


class CBoss(Boss):
    def choose_attack(self, player):
        # Pressiona o corpo a corpo; usa tiros ao entrar nas fases de baixa vida.
        return "lunge" if self.phase == 1 else "spread"


class SQLBoss(Boss):
    def choose_attack(self, player):
        # Disparos laterais quando o aluno está abaixo; leque no mesmo patamar.
        return "slam" if player.rect.centery > self.rect.centery else "spread"


class AssemblyBoss(Boss):
    def choose_attack(self, player):
        # Combina as três primitivas em um ciclo próprio.
        attacks = ("spread", "lunge", "slam")
        step = getattr(self, "combo_step", 0)
        self.combo_step = step + 1
        return attacks[step % len(attacks)]


BOSS_CLASSES = {
    "romerbug": RomerBug,
    "python": PythonBoss,
    "java": JavaBoss,
    "c": CBoss,
    "sql": SQLBoss,
    "assembly": AssemblyBoss,
}
