"""Professores da sequência escolar, sem comportamento de inimigo."""
import assets
import settings
from entities.character import Character


class Teacher(Character):
    NAMES = {'max': 'Professor Max', 'romerito': 'Professor Romerito'}

    def __init__(self, x, y, identity):
        super().__init__(x, y, *settings.CHARACTER_SIZE, health=1)
        self.name = self.NAMES[identity]
        self.frames = assets.load_character_frames(
            [f'npcs/{identity}_{i}.png' for i in range(2)])
        self.image = self.frames[0]
        self.contact_damage = 0
        self.animation_tick = 0

    def update(self):
        self.animation_tick += 1
        self.image = self.frames[(self.animation_tick // 30) % 2]
