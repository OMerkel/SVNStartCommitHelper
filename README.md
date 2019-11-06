SVNStartCommitHelper
====================

http://sf.net/projects/svnstartcommith
https://github.com/OMerkel/SVNStartCommitHelper

Professional environments focus on high development standards in Source Code
Management. E.g. by usage of server side commit hooks to check for minimum
acceptance levels on code and documentation quality including commit message
structure and content.

*TortoiseSVN* offers only a free form text field to edit inside the Commit
Dialog. Developers might recall situations when struggling with commit message
structure and fighting the server side commit hooks instead focusing on
message content! Thus being annoyed instead of feeling an incentive to deliver
high quality descriptions here.

In such situations a helpful structured form instead of a free form multi-line
edit field is missing.

The **SVNStartCommitHelper** is a client side start commit hook script (as a
first version written in *Python* / Tkinter) exactly offering a
well-structured form to fill in. The edited content is transformed and
forwarded to the SVN commit dialog then. You still have full control on the
commit message then. While using the helper you focus on message quality now
instead struggling with message structure.

Since it is Python script...
----------------------------

* the edit form can easily be adapted to your needs.
* the resulting text structure as forwarded to the *TortoiseSVN* commit
dialog can easily be adapted.

So you will experience...
-------------------------

* Thus you get much higher acceptance rates on controlling and filtering
server side SVN commit hooks.
* Easier creation of well-structured commit messages will be experienced
on your side while matching higher QA and SCM standards.

Installation
------------

[[img src=svnstartcommithelper-howto-install.png alt=TortoiseSVN_Installation_Settings]]

The image shows a sample install of the start commit hook
script 'svnstartcommithelper.py'. In the *TortoiseSVN* settings dialog
select 'Hook Scripts', then 'Add...' the script using the settings shown.
In the command line text field adapt the values according to your
valid locations.

Migrating from previous version
-------------------------------

If migrating from previous versions then please be aware that the format of
the messagebody template in .svnsch/svnsch.conf might have changed.
In this case please backup your configuration file first.
Then you might need to remove or manually modify the configuration file. 

External links
--------------

* http://tortoisesvn.net/ - TortoiseSVN is an easy-to-use SCM / source control
software for Microsoft Windows implemented as a Windows shell extension.
* http://code.google.com/p/tortoisesvn/source/browse/ - TortoiseSVN source code.
* http://flavio.castelli.name/2006/02/16/svn-commit-helper/ - Svn-commit is a
command line utility for making rapid commit with subversion.
* http://python.org/ - Python Programming Language – Official Website.
