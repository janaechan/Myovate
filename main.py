from kivy.app import App
from kivy.core.window import Window
import view
import CalibrationModuleApp


class Myovate(App):

    def build(self):
        return view.build()


if __name__ == '__main__':
    Window.fullscreen = 'auto'
    Myovate().run()