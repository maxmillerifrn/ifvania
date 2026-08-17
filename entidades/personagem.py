
class Personagem():

    def __init__(self,x,y):
        self.x= x
        self.y=y
        #estado físico
        self.jumps_used = 0
        self.on_wall=0
        self.facing = 1
        self.on_ground=False
        #Combate/Vida
        self.max_vidas = 6
        self.vidas = self.max_vidas
        self.invulnerabilidade = 0
        self.attack_cooldown = 0
        self.attacking_time = 0

        #Timers da Habilidade
        self.dash_timer = 0
        self.dash_cooldown_timer = 0
        self.shot_cooldown = 0
        self.shield_active = False
        self.shield_cooldown = 0
        #Habilidades
        self.habilidades = set()
        #Progresso
        self.chefes_derrotados = set()
        self.alive=True