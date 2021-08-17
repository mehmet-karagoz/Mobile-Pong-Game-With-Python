from random import randint

from kivy.app import App
from kivy.clock import Clock
from kivy.properties import NumericProperty, ReferenceListProperty, \
    ObjectProperty
from kivy.uix.widget import Widget
from kivy.vector import Vector


class PongGame(Widget):
    ball = ObjectProperty(None)

    def update(self, dt):
        self.ball.move()

        # set the limits to which the ball can go
        # for y coordinate
        if self.ball.y < 0 or self.ball.top > self.height:
            self.ball.velocity_y *= -1
        # for x coordinate
        if self.ball.x < 0 or self.ball.right > self.width:
            self.ball.velocity_x *= -1

    def serve_ball(self):
        self.ball.center = self.center
        self.ball.velocity = Vector(3, 0).rotate(randint(0, 90))


class Ball(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)

    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == "__main__":
    PongApp().run()
