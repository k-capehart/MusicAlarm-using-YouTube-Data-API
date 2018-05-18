import musicalarm

from kivy.config import Config
Config.set('graphics', 'resizable', False)

from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.properties import StringProperty
from time import localtime, strftime, sleep, strptime
from functools import partial
from kivy.graphics import *

class GUI(App):
	time = StringProperty()
	f = None

	def update_clock(self, *args):
		self.time = strftime("%I:%M %p", localtime())

	def build(self):
		self.load_kv('layouts.kv')
		self.f = F()
		Clock.schedule_interval(self.update_clock, .5)
		return (self.f)

	def alarm(self):
		my_time = self.f.ids.my_time.text
		if(my_time == ""):
			print("Try again")
		else:
			musicalarm.set_alarm(strptime(my_time, "%I:%M %p"))
			self.f.ids.my_time.text = ""
			self.f.ids.info.text = "Get ready to praise the sun at %s" % my_time

class F(FloatLayout):
	pass

if __name__ == '__main__': 
	GUI().run()