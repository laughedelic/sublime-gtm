import sublime, sublime_plugin
import subprocess
import os.path

def status(view):
	filename = view.file_name()
	if filename:
		dir = os.path.dirname(filename)
		# gtm_p = subprocess.Popen(['gtm', 'status', '--short', '--no-label']
		# gtm_p = subprocess.Popen('/usr/local/bin/gtm prompt-status'
		gtm_p = subprocess.Popen('/usr/local/bin/gtm status -s'
			, cwd=dir
			, shell=True
			, stdout=subprocess.PIPE )
		exit_code = gtm_p.wait()
		# print(exit_code)
		if exit_code == 0: 
			out = gtm_p.communicate()[0].decode("utf-8") 
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
	# def on_deactivated_async(self, view):
	# 	status(view)
