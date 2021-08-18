from kivy.app import App
from kivy.clock import Clock
from kivy.properties import NumericProperty, ReferenceListProperty, \
    ObjectProperty
from kivy.uix.widget import Widget
from kivy.vector import Vector


class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    def update(self, dt):
        self.ball.move()

        # bounce of paddles
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        # score
        if self.ball.y < self.y:
            self.player2.score += 1
            self.serve_ball(vel=(0, 4))
        if self.ball.y > self.height - 20:
            self.player1.score += 1
            self.serve_ball(vel=(0, -4))

        # set the limits to which the ball can go
        # for y coordinate
        if self.ball.y < 0 or self.ball.top > self.height:
            self.ball.velocity_y *= -1
        # for x coordinate
        if self.ball.x < 0 or self.ball.right > self.width:
            self.ball.velocity_x *= -1

    def serve_ball(self, vel=(0, 4)):
        self.ball.center = self.center
        self.ball.velocity = vel

    def on_touch_move(self, touch):
        if touch.y < self.height / 3:
            self.player1.center_x = touch.x
        if touch.y > self.height - self.height / 3:
            self.player2.center_x = touch.x


class Ball(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)

    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(self.velocity) + self.pos


class PongPaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_x - self.center_x) / (self.width / 2)
            vx *= 1.15
            vy *= -1.15
            ball.velocity = vx, vy + offset


class PongApp(App):
    def build(self):
        self.icon = "icon.png"
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == "__main__":
    PongApp().run()
