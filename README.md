Sublime Text 2 File Locking
====================

This is a quick plugin I wrote for a team project I'm working on that's contained entirely a shared Dropbox folder.

Due to the lack of a listener in the API for detecting operations that read files but don't actually open an editing buffer (e.g. file previews), this plugin works best when those features are avoided. Otherwise you'll run into issues with files that are locked even though nobody's editing them. I've included a command-line utility, viewlocks.py, that can manually delete locks if that happens.

Use at your own risk and hack as needed.

Getting started
---------------
1. Have all team members go to "Tools > New Plugin..." and paste in the contents of FileLocking.py.
2. In the "Settings" block, all members must set the 'project' and 'lockext' variables to the same string. The 'me' variable may optionally be given a custom value per member (the default value is the name of the currently logged in user).
3. Have everyone save the plugin file to the default Packages/User directory, ideally in unison.
4. Add viewlocks.py to the project's root directory.

Viewing locks
------------
Display all currently existing locks, their owners, and their creation times:

    python viewlocks.py

Display all locks set by the team member who has their 'me' variable set to 'john':

    python viewlocks.py john

Remove all locks set by john:

    python viewlocks.py john -r
