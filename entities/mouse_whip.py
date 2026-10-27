"""Mouse preso ao cabo: preparação, estalo e recolhimento do chicote.

O desenho e o dano usam a mesma curva, interrompida ao tocar uma parede.
"""
import math
import pygame


class MouseWhip:
    DURATION = 26
    WINDUP = 6
    STRIKE_END = 16
    REACH = 76

    def __init__(self):
        self.facing = 1
        self.hit_targets = set()

    def start(self, facing):
        self.facing = facing
        self.hit_targets.clear()

    def age(self, player):
        return self.DURATION - player.attacking_timer

    def pose(self, player):
        age = self.age(player)
        return 0 if age < self.WINDUP else 1 if age < self.STRIKE_END else 2

    def is_striking(self, player):
        return player.attacking_timer > 0 and self.WINDUP <= self.age(player) < self.STRIKE_END

    @staticmethod
    def _smooth(t):
        return t * t * (3 - 2 * t)

    def points(self, player, solids=()):
        if player.attacking_timer <= 0:
            return []
        age = self.age(player)
        # Pontos de fixação nas mãos das três poses, relativos ao corpo.
        hands = [(-9, -9), (15, -3), (2, 0)]
        hx, hy = hands[self.pose(player)]
        logical_hand = pygame.Vector2(player.rect.centerx + hx * self.facing,
                                      player.rect.centery + hy)
        scale = player.VISUAL_SCALE
        hand = pygame.Vector2(player.rect.centerx + hx*scale*self.facing,
                              player.rect.bottom + (hy-player.height/2)*scale)
        # O desenho ampliado da mão não permite iniciar o fio além de uma parede.
        entries = [solid.clipline(logical_hand, hand) for solid in solids]
        entries = [pygame.Vector2(line[0]) for line in entries if line]
        if entries:
            hand = min(entries, key=lambda p: p.distance_squared_to(logical_hand))
        if age < self.WINDUP:
            t = self._smooth(age / self.WINDUP)
            end = pygame.Vector2(-18 - 12 * t, 12 - 42 * t)
            bend = -16
        elif age < self.STRIKE_END:
            t = self._smooth((age - self.WINDUP) / (self.STRIKE_END - self.WINDUP - 1))
            end = pygame.Vector2(-8 + (self.REACH + 8) * t, -34 + 37 * t)
            bend = -25 * (1 - t)
        else:
            t = self._smooth((age - self.STRIKE_END) / (self.DURATION - self.STRIKE_END))
            end = pygame.Vector2(self.REACH * (1 - t) + 7 * t, 6 + 12 * t)
            bend = 18 * math.sin(t * math.pi)
        end.x *= self.facing
        # A mão acompanha o sprite maior, mas a trajetória da ponta mantém o alcance.
        tip = logical_hand + end
        control = (hand + tip) / 2 + pygame.Vector2(0, bend)
        points = [hand]
        for i in range(1, 25):
            t = i / 24
            point = hand * (1 - t) ** 2 + control * (2 * (1 - t) * t) + tip * t * t
            # Segue o fio a partir da mão e para na primeira superfície.
            intersections = [s.clipline(points[-1], point) for s in solids]
            entries = [pygame.Vector2(line[0]) for line in intersections if line]
            if entries:
                point = min(entries, key=lambda p: p.distance_squared_to(points[-1]))
                points.append(point)
                break
            points.append(point)
        return points

    def hit_bounds(self, player, solids=()):
        if not self.is_striking(player):
            return None
        points = self.points(player, solids)
        xs, ys = [p.x for p in points], [p.y for p in points]
        return pygame.Rect(min(xs) - 5, min(ys) - 5,
                           max(xs) - min(xs) + 11, max(ys) - min(ys) + 11)

    def try_hit(self, player, target, solids):
        if not self.is_striking(player) or target in self.hit_targets or not target.alive:
            return False
        points = self.points(player, solids)
        area = target.rect.inflate(6, 6)
        if any(area.clipline(a, b) for a, b in zip(points, points[1:])):
            health = target.health
            target.take_damage(1)
            if target.health < health:
                self.hit_targets.add(target)
                return True
        return False

    def draw(self, surface, camera, player, solids):
        points = self.points(player, solids)
        if not points:
            return
        points = [p - camera.offset for p in points]
        coords = [(round(p.x), round(p.y)) for p in points]
        # Cabo escuro com realce para permanecer visível no cenário.
        pygame.draw.lines(surface, (12, 17, 24), False, coords, 4)
        pygame.draw.lines(surface, (160, 183, 192), False, coords, 2)
        pygame.draw.circle(surface, (191, 118, 65), coords[0], 2)
        # Mouse visto por cima: carcaça, divisão dos botões e rodinha.
        mouse = pygame.Surface((14, 10), pygame.SRCALPHA)
        pygame.draw.ellipse(mouse, (10, 15, 24), (0, 0, 14, 10))
        pygame.draw.ellipse(mouse, (223, 233, 237), (1, 1, 12, 8))
        pygame.draw.line(mouse, (50, 66, 78), (7, 1), (7, 5), 1)
        pygame.draw.line(mouse, (50, 66, 78), (3, 5), (11, 5), 1)
        pygame.draw.rect(mouse, (55, 166, 165), (6, 2, 2, 3))
        tangent = points[-1] - points[-2]
        angle = -math.degrees(math.atan2(tangent.y, tangent.x)) - 90
        mouse = pygame.transform.rotate(mouse, angle)
        surface.blit(mouse, mouse.get_rect(center=coords[-1]))
