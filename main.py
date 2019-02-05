from kivy.app import App
from kivy.core.window import Window
import view

class Myovate(App):

    def build(self):
        return view.MainScreen().build()


if __name__ == '__main__':
    Window.fullscreen = 'auto'
    Myovate().run()