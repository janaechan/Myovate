import kivy
kivy.require('1.10.1')

from kivy.app import App
from kivy.core.window import Window
import view
import ScreenManager


class Myovate(App):

    def build(self):
        # return view.MainScreen().build()
        return ScreenManager.Screens().run()


if __name__ == '__main__':
    Window.fullscreen = 'auto'
    Myovate().run()
