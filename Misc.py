from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout


class DropDownMenu(DropDown):
    pass


class CustomizedLabel(Label):
    pass


class DropDownButton(Button):
    pass


class MenuButton(Button):
    pass


class CustomizedButton(Button):
    pass


class CustomizedPopup(Popup):
    pass


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    ''' Adds selection and focus behaviour to the view. '''