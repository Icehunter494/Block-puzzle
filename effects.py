# effects.py

import random
import math
import pygame


# ==================================================
# PARTICLE
# ==================================================

class Particle:

    def __init__(
        self,
        x,
        y,
        color,
        size=6
    ):

        self.x = float(x)
        self.y = float(y)

        angle = random.uniform(
            0,
            math.pi * 2
        )

        speed = random.uniform(
            2,
            8
        )

        self.vx = (
            math.cos(angle)
            * speed
        )

        self.vy = (
            math.sin(angle)
            * speed
        )

        self.life = random.randint(
            25,
            50
        )

        self.max_life = self.life

        self.size = size

        self.color = color

        self.gravity = 0.15

    def update(self):

        self.vy += self.gravity

        self.x += self.vx
        self.y += self.vy

        self.life -= 1

    def alive(self):

        return self.life > 0

    def draw(
        self,
        surface
    ):

        alpha = (
            self.life /
            self.max_life
        )

        radius = max(
            1,
            int(
                self.size
                * alpha
            )
        )

        pygame.draw.circle(
            surface,
            self.color,
            (
                int(self.x),
                int(self.y)
            ),
            radius
        )


# ==================================================
# FLOATING TEXT
# ==================================================

class FloatingText:

    def __init__(
        self,
        text,
        x,
        y,
        color=(255,255,255),
        lifetime=60
    ):

        self.text = text

        self.x = x
        self.y = y

        self.color = color

        self.life = lifetime
        self.max_life = lifetime

    def update(self):

        self.y -= 1

        self.life -= 1

    def alive(self):

        return self.life > 0

    def draw(
        self,
        surface,
        font
    ):

        alpha = (
            self.life /
            self.max_life
        )

        text_surface = font.render(
            self.text,
            True,
            self.color
        )

        text_surface.set_alpha(
            int(alpha * 255)
        )

        surface.blit(
            text_surface,
            (
                self.x,
                self.y
            )
        )


# ==================================================
# COMBO POPUP
# ==================================================

class ComboPopup:

    def __init__(
        self,
        combo
    ):

        self.combo = combo

        self.scale = 1.0

        self.life = 90

    def update(self):

        self.life -= 1

        self.scale += 0.015

    def alive(self):

        return self.life > 0

    def draw(
        self,
        surface,
        font,
        screen_w
    ):

        alpha = min(
            255,
            self.life * 3
        )

        text = f"COMBO x{self.combo}"

        text_surface = font.render(
            text,
            True,
            (255,220,50)
        )

        text_surface.set_alpha(
            alpha
        )

        w = text_surface.get_width()

        surface.blit(
            text_surface,
            (
                screen_w // 2 - w // 2,
                20
            )
        )


# ==================================================
# GLOW PULSE
# ==================================================

class GlowPulse:

    def __init__(
        self,
        x,
        y,
        radius,
        color
    ):

        self.x = x
        self.y = y

        self.radius = radius

        self.color = color

        self.life = 30

    def update(self):

        self.radius += 2

        self.life -= 1

    def alive(self):

        return self.life > 0

    def draw(
        self,
        surface
    ):

        if self.life <= 0:
            return

        pygame.draw.circle(
            surface,
            self.color,
            (
                int(self.x),
                int(self.y)
            ),
            int(self.radius),
            2
        )


# ==================================================
# SCREEN SHAKE
# ==================================================

class ScreenShake:

    def __init__(self):

        self.strength = 0

        self.duration = 0

    def start(
        self,
        strength,
        duration
    ):

        self.strength = strength
        self.duration = duration

    def update(self):

        if self.duration > 0:
            self.duration -= 1

    def get_offset(self):

        if self.duration <= 0:
            return (0,0)

        return (
            random.randint(
                -self.strength,
                self.strength
            ),
            random.randint(
                -self.strength,
                self.strength
            )
        )


# ==================================================
# EFFECT MANAGER
# ==================================================

class EffectManager:

    def __init__(self):

        self.particles = []

        self.texts = []

        self.combos = []

        self.glows = []

        self.shake = ScreenShake()

    # ------------------------------

    def spawn_particles(
        self,
        x,
        y,
        color,
        amount=25
    ):

        for _ in range(amount):

            self.particles.append(

                Particle(
                    x,
                    y,
                    color
                )
            )

    # ------------------------------

    def spawn_score_text(
        self,
        text,
        x,
        y,
        color=(255,255,255)
    ):

        self.texts.append(

            FloatingText(
                text,
                x,
                y,
                color
            )
        )

    # ------------------------------

    def spawn_combo(
        self,
        combo
    ):

        self.combos.append(

            ComboPopup(
                combo
            )
        )

    # ------------------------------

    def spawn_glow(
        self,
        x,
        y,
        radius,
        color
    ):

        self.glows.append(

            GlowPulse(
                x,
                y,
                radius,
                color
            )
        )

    # ------------------------------

    def shake_screen(
        self,
        strength=8,
        duration=15
    ):

        self.shake.start(
            strength,
            duration
        )

    # ------------------------------

    def update(self):

        self.shake.update()

        for p in self.particles:
            p.update()

        for t in self.texts:
            t.update()

        for c in self.combos:
            c.update()

        for g in self.glows:
            g.update()

        self.particles = [
            p for p in self.particles
            if p.alive()
        ]

        self.texts = [
            t for t in self.texts
            if t.alive()
        ]

        self.combos = [
            c for c in self.combos
            if c.alive()
        ]

        self.glows = [
            g for g in self.glows
            if g.alive()
        ]

    # ------------------------------

    def draw(
        self,
        surface,
        font,
        screen_width
    ):

        for p in self.particles:
            p.draw(surface)

        for t in self.texts:
            t.draw(
                surface,
                font
            )

        for c in self.combos:
            c.draw(
                surface,
                font,
                screen_width
            )

        for g in self.glows:
            g.draw(surface)

    # ------------------------------

    def get_shake_offset(
        self
    ):

        return self.shake.get_offset()
        