import sublime, sublime_plugin
import subprocess
import os.path
import os
import re

def strip_ansi_codes(s):
	return re.sub(r'\x1b\[([0-9,A-Z]{1,2}(;[0-9]{1,2})?(;[0-9]{3})?)?[m|K]?', '', s)

def status(view):
	filename = view.file_name()
	if filename:
		dir = os.path.dirname(filename)
		env = os.environ
		gtm_p = subprocess.Popen('gtm status -s'
			, cwd=dir
			, env=env
			, shell=True
			, stdout=subprocess.PIPE )
		exit_code = gtm_p.wait()
		# print(exit_code)
		if exit_code == 0: 
			out = strip_ansi_codes(gtm_p.communicate()[0].decode("utf-8"))
			status = out.replace('[on]','  [ON]').replace('[off]','  [OFF]')
			view.set_status('gtm', 'gtm: ' + status)
		else: view.erase_status('gtm')

class GtmListener(sublime_plugin.EventListener):
	def on_post_save_async(self, view):
		status(view)
	def on_modified_async(self, view):
		status(view)
	def on_selection_modified_async(self, view):
		status(view)
	def on_activated_async(self, view):
		status(view)
