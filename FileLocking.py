# FileLocking v1.05
# Art Chaidarun
# 2012-07-16

import os, time, getpass
import sublime, sublime_plugin

class FileLockingCommand(sublime_plugin.EventListener):

  ############################## SETTINGS ##############################
  #
  # @me       Display name (must be unique for each collaborator).
  #           Should be seven ASCII characters or fewer.
  # @project  Only files whose paths contain this string will be locked.
  # @lockext  File extension for lock files - must begin with dot.
  #
  me = getpass.getuser() # Account username
  project = "myprojectname"
  lockext = ".sublimelock"
  #
  ######################################################################

  forceclose = ""

  def on_load(self, view):
    if view.file_name() is not None:
      print(view.file_name() + ": " + "on_load")
      view.run_command("check_lock")

  def on_close(self, view):
    if view.file_name() is not None:
      print(view.file_name() + ": " + "on_close")
      view.run_command("remove_lock")

class CheckLockCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    filepath = str(self.view.file_name())
    filename = filepath.split(os.sep)[-1]
    lockfile = filepath + FileLockingCommand.lockext
    if (FileLockingCommand.project in lockfile) and (FileLockingCommand.lockext not in filepath):
      try:
        with open(lockfile, 'rU') as f:
          lockinfo = f.read().splitlines()
          locker = lockinfo[0]
          locktime = os.path.getmtime(lockfile)
          if locker == FileLockingCommand.me:
            print("You opened a file that was locked by yourself.")
          else:
            # File is already locked, so don't let user open it.
            f.close()
            minutesago = (int(time.time()) - locktime) // 60
            fuzzymsg = (str(minutesago) + " minutes" if minutesago < 60 else str(minutesago // 60) + " hours") + " ago"
            FileLockingCommand.forceclose = "Sorry, " + locker + " locked " + filename + " at " + time.strftime("%I:%M %p", time.localtime(locktime)) + " (" + fuzzymsg + ")."
            sublime.error_message(FileLockingCommand.forceclose)
            self.view.window().run_command("close")
      except IOError as e:
        # File isn't locked already, so lock it. The lockfile contains the locker's name.
        f = open(lockfile, 'w')
        f.write(FileLockingCommand.me)
        f.close()
        msg = FileLockingCommand.me + " locked " + filename
        sublime.status_message(msg)
        print(msg)

class RemoveLockCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    if FileLockingCommand.forceclose.__len__():
      # Buffer was closed due to lock.
      FileLockingCommand.forceclose = ""
    else:
      # Buffer was closed by user.
      filepath = str(self.view.file_name())
      filename = filepath.split(os.sep)[-1]
      lockfile = filepath + FileLockingCommand.lockext
      if (FileLockingCommand.project in lockfile) and (FileLockingCommand.lockext not in filepath):
        try:
          with open(lockfile, 'rU') as f:
            if f.read().splitlines()[0] == FileLockingCommand.me:
              # Unlock the file.
              f.close()
              os.remove(lockfile)
              msg = FileLockingCommand.me + " removed the lock on " + filename
              sublime.status_message(msg)
              print(msg)
            else:
              print("You just closed a file (" + filename + ") that was supposed to have already been locked by someone else.")
        except IOError as e:
          print("You closed a file that should've been locked but whose lockfile is missing.")
