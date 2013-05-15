import sublime, sublime_plugin
import subprocess
import os, os.path, re, sys

def strip_ansi_codes(s):
	return re.sub(r'\x1b\[([0-9,A-Z]{1,2}(;[0-9]{1,2})?(;[0-9]{3})?)?[m|K]?', '', s)

def call_gtm(view, cmd):
	filename = view.file_name()
	if filename:
		dir = os.path.dirname(filename)
		env = os.environ
		gtm_p = subprocess.Popen('gtm ' + cmd
			, cwd=dir
			, env=env
			, shell=True
			, stdout=subprocess.PIPE )
		exit_code = gtm_p.wait()
		# print(exit_code)
		if exit_code == 0: 
			return strip_ansi_codes(gtm_p.communicate()[0].decode("utf-8"))
		else: 
			if exit_code == 127: 
				raise Exception("gtm is not found in Sublime's PATH: " + env["PATH"])
			return None

def status(view):
	stat = None
	try:
		stat = call_gtm(view, 'status --short')
	except Exception as err:
		print('gtm error: ', err)
	if stat == None: view.erase_status('gtm')
	else: 
		status = stat.replace('[on]','  [ON]').replace('[off]','  [OFF]')
		view.set_status('gtm', 'gtm: ' + status)

class GtmListener(sublime_plugin.EventListener):
	def on_post_save_async(self, view):
		status(view)
	def on_modified_async(self, view):
		status(view)
	def on_selection_modified_async(self, view):
		status(view)
	def on_activated_async(self, view):
		status(view)

class GtmCommand(sublime_plugin.WindowCommand):
	def run(self, cmd):
		print('gtm ' + cmd + ':')
		try:
			print(call_gtm(self.window.active_view(), cmd))
		except Exception as err:
			sublime.error_message(str(err))

# class GtmListCommand(sublime_plugin.WindowCommand):
# 	def run(self):
# 		v = self.window.active_view()
# 		tasks = call_gtm(v, 'list --no-header')
# 		print(tasks)
# 		def switch_task(i):
# 			if i == -1: status(v)
# 			return
# 		# for t in tasks.splitlines(): 
# 			# t.split(' ')
# 		ts = [re.sub(r'\s+', ' ', t) for t in tasks.splitlines()]
# 		print(ts)
# 		self.window.show_quick_panel(ts, switch_task, sublime.MONOSPACE_FONT)
