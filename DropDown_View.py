import webbrowser
from kivy.core.window import Window
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.dropdown import DropDown
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.uix.listview import ListItemButton

from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition


Builder.load_string("""
#:import NoTransition kivy.uix.screenmanager.NoTransition
#:import ListAdapter kivy.adapters.listadapter.ListAdapter
#:import ListItemButton kivy.uix.listview.ListItemButton
<WrappedLabel@Label>:
    # don't automatically allocate y size
    # size_hint_y: None
    # height: self.texture_size[1] + (self.texture_size[1]/2)
    markup: True
    

<MyAppRoot>:
    orientation: "vertical"

    ActionBar:
        ActionView:
            ActionPrevious:
                title: "HELLO WORLD"
                with_previous: True
            ActionOverflow:
                ActionButton:
                    text: "Settings"
                    on_press: app.open_settings()
                ActionButton:
                    text: "Settings2"
                    on_press: app.open_settings()
    
    ScreenManager:
        id: screen_manager
        transition: NoTransition()
        StartScreen:
            # name if for kv reference
            name: "start_screen"
        VinnyScreen:
            # id is for python code to reference
            name: "vinny_screen"
            id: vinny_screen
        StartSessionScreen:
            name: "start_session_screen"
            id: start_session_screen
            
# @Screen == extend Screen
<StartScreen@Screen>:
    dropdown: dropdown.__self__
    AnchorLayout:
        anchor_x: 'left'
        anchor_y: 'top'
        Button:
            id: btn
            text: 'Press'
            on_release: dropdown.open(self)
            on_parent: dropdown.dismiss()
            size_hint_y: None
            height: '48dp'
    
        DropDown:
            id: dropdown
            # on_parent: self.dismiss()
            on_select: btn.text = '{}'.format(args[1])
    
            Button:
                text: 'Vinny'
                size_hint_y: None
                height: '48dp'
                on_press: dropdown.select(btn.text)
                on_release: 
                    app.root.changeScreen(self.text.lower())
    
            Button:
                text: 'Start Session'
                size_hint_y: None
                height: '48dp'
                on_press: dropdown.select(btn.text)
                on_release: 
                    app.root.changeScreen(self.text.lower())
                
    BoxLayout:
        # Settings
        orientation: "vertical"
        padding: root.width * .02, root.height * .02
        spacing: min(root.width, root.height) * .02
        
        WrappedLabel:
            # markup to change text formating
            text: "[b] MYOVATE [/b]"
            font_size: min(root.height, root.width) / 10
            
        Button: 
            text: "Annie"
        Button: 
            text: "Nick"
        Button: 
            text: "Janae"
        Button: 
            text: "Vinny"
            on_release: app.root.changeScreen(self.text.lower())

<VinnyScreen@Screen>:
    BoxLayout:
        padding: root.width * .02, root.height * .02
        Label: 
            # calls python file
            text: app.getText()
            halign: "center"
            markup: True
            font_size: root.height / 20
            #wrapped at width, but y is not constant (y adapts)
            text_size: self.width, None
            center_y: .5
            
            # links in text
            on_ref_press: app.on_ref_press(*args)
            
<StartSessionScreen>:
    first_name_text_input: first_name
    last_name_text_input: last_name
    session_list: session_list_view
    
    BoxLayout:
        padding: root.width * .02, root.height * .02
        orientation: "vertical"
        
        BoxLayout:
            size_hint_y: None
            height: "40dp"
            Label:
                text: "First name"
            TextInput:
                id: first_name
            Label:
                text: "Last name"
            TextInput:
                id: last_name
                
        BoxLayout:
            size_hint_y: None
            height: "40dp"
            Button:
                text: "Add Sensor"
                on_press: app.root.open_popup()
                size_hint_x: 15
        ListView:
            id: session_list_view
        #     adapter:
        #         ListAdapter(data=["Session 1"], cls=app.root.show_session_screen())
        Label: 
            # calls python file
            text: "Start a New Session"
            halign: "center"
            markup: True
            font_size: root.height / 20
            #wrapped at width, but y is not constant (y adapts)
            text_size: self.width, None
            center_y: .5
            
            # links in text
            on_ref_press: app.on_ref_press(*args)
        Button: 
            text: "Add Sensor"
            on_press: app.root.open_popup()

<CalibrationPopUp>:
    size_hint: .8, .8
    title: "Calibrate Sensor"
    title_size: root.height * .05
    auto_dissmmiss: False
    message: message
    wrapped_button: wrapped_button
    BoxLayout:
        orientation: "vertical"
        padding: root.width * .02, root.height * .02
        spacing: min(root.width, root.height) * .02
        Label: 
            id: message
            text: "Step 1 Step 2"
            halign: "center"
            font_size: root.height / 10
            text_size: self.width, None
            center_y: 0.5
        Button: 
            id: wrapped_button
            text: "Next"
            size_hint: 1, None
            height: root.height / 8
            on_release: root.dismiss()
        
""")


class SessionListButton(ListItemButton):
    pass


class StartSessionScreen(Screen):
    first_name_text_input = ObjectProperty()
    last_name_text_input = ObjectProperty()
    session_list = ObjectProperty()

    def add_sensor(self):
        pass


class CalibrationPopUp(Popup):
    """Popup to prompt user to calibrate sensor

    """
    GOOD = "{} :D"
    BAD = "{}, Correct answer is [b]{}[/b]"
    GOOD_LIST = "Awesome! Amazing! Excellent! Correct!".split()
    BAD_LIST = "Awesome! Amazing! Excellent! Correct!".split()

    # ObjectProperty goes to .kv file and gets id of variable
    message = ObjectProperty()
    wrapped_button = ObjectProperty()

    def __init__(self, *args, **kwargs):
        super(CalibrationPopUp, self).__init__(*args, **kwargs)

    def open(self, correct=True):
        # When complete close popup
        # If answer is correct take off button if it is visible
        if correct:
            if self.wrapped_button in self.content.children:
                self.content.remove_widget(self.wrapped_button)
        # if not complete display next button
        else:
            if self.wrapped_button not in self.content.children:
                self.content.add_widget(self.wrapped_button)

        # set up text message
        self.message.text = self._prep_text(correct)

        # display popup
        super(CalibrationPopUp, self).open()
        if correct:
            Clock.schedule_once(self.dismiss, 2)

    def _prep_text(self, correct):
        if correct:
            return "COMPLETE"
        else:
            return "NEXT STEP"


class MyAppRoot(BoxLayout):
    """Root of all widgets

    """
    def __init__(self, **kwargs):
        super(MyAppRoot, self).__init__(**kwargs)
        # List of previous screens
        self.screen_list = []
        self.calibration_popup = CalibrationPopUp()
        self.session_list_button = SessionListButton()
        # self.session_test = SessionTest()

    def changeScreen(self, next_screen):
        operations = "annie nick janae vinny".split()
        question = None

        if self.ids.screen_manager.current not in self.screen_list:
            self.screen_list.append(self.ids.screen_manager.current)

        if next_screen == "vinny":
            self.ids.screen_manager.current = "vinny_screen"
        elif next_screen == "start session":
            self.ids.screen_manager.current = "start_session_screen"

    def onBackButton(self):
        # check if there are any screens to go back to
        if self.screen_list:
            self.ids.screen_manager.current = self.screen_list.pop()
            # don't want to close
            return True
        return False

    def open_popup(self):
        self.calibration_popup.open()

    def show_session_screen(self):
        return self.session_list_button


class MyApp(App):
    """App objects

    """
    def __init__(self, **kwargs):
        super(MyApp, self).__init__(**kwargs)
        # runs onBackButton in MyApp
        Window.bind(on_keyboard=self.onBackButton)

    def onBackButton(self, window, key, *args):
        # user presses back button
        if key == 27:
            # runs onBackButton in MyAppRoot
            return self.root.onBackButton()

    def build(self):
        return MyAppRoot()

    def getText(self):
        return ("ABOUT MYOVATE AKA BUTT SMASH"
                "[b][ref=source]go to google[/ref][/b]")

    def on_ref_press(self, instance, ref):
        _dict = {
            "source": "https://google.com"
        }

        webbrowser.open(_dict[ref])


if __name__ == '__main__':
    MyApp().run()
