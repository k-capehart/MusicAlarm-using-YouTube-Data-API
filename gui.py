import musicalarm

from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.properties import StringProperty
from time import localtime, strftime, sleep, strptime
from functools import partial

class GUI(App):
	time = StringProperty()

	def update_clock(self, *args):
		self.time = strftime("%I:%M %p", localtime())

	def build(self):
		self.load_kv('test.kv')
		f = F();
		Clock.schedule_interval(self.update_clock, .5)
		return (f)

	def alarm(self):
		musicalarm.alarm()

class F(FloatLayout):
	pass

if __name__ == '__main__': 
	GUI().run()