"""
The MIT License

Copyright (c) 2012 Oliver Merkel <Merkel.Oliver@web.de>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
#
# This section contains a list of people who've made non-trivial
# contribution to the SVNStartCommitHelper project. Such contributors
# who commit code to the project are encouraged to add their names
# here. Please keep the list sorted by first names.
#
# @AUTHOR Oliver Merkel <merkel.oliver@web.de>
#
# Feel free to send contributions, pull requests, suggestions or
# any other feedback to the project. You are welcome!
#

import tkinter.messagebox
import tkinter as tk
import os

class CommitHelperConstants(object):
    ERROR = 'Error'
    MSGOPTIONS = 'Please select an option for %s!'
    NOSELECTION = '<noselection>'
    TITLE = 'SVN Start Commit Helper'
    MESSAGEBODY = '''Brief: %s\n
%s: %s\n
Findings: %s\n
Reviewer(s): %s\n
Risk: %s\n
Jira key is %s\n
Lint (%s): %s\n'''

class SvnStartCommitHelperValidator(object):
    optionCallbacks = []

    def registerGetOptionCallback(self, callback, name):
        self.optionCallbacks.append((callback, name))

    def areOptionsSelected(self):
        result = True
        for callback, name in self.optionCallbacks:
            result = result and not (callback() == CommitHelperConstants.NOSELECTION)
            if not result:
                tk.messagebox.showerror(CommitHelperConstants.ERROR,  CommitHelperConstants.MSGOPTIONS % name)
                break
        return result

class SvnStartCommitHelperView(tk.Tk):
    OPTIONSRISK = [
        CommitHelperConstants.NOSELECTION,
        'Low',
        'Medium',
        'High'
    ]
    OPTIONSLINT = [
        CommitHelperConstants.NOSELECTION,
        'Decrease',
        'Equal',
        'Increase'
    ]
    callback = None
    commentText = None
    findings = None
    reviewers = None
    riskVar = None
    jiraText = None    
    lintVar = None
    lintText = None

    def __init__(self, callback):
        tk.Tk.__init__(self)
        self.callback = callback
        self.title(CommitHelperConstants.TITLE)
        self.minsize(300,50)

        descriptionFrame = tk.Frame(self, bd=1, relief=tk.SUNKEN)
        descriptionFrame.grid(row=0, column=0, columnspan=3,
            padx=2, pady=2, sticky=tk.N+tk.E+tk.S+tk.W)
        tk.Label(descriptionFrame, text='Brief').grid(row=0, sticky=tk.E)
        tk.Label(descriptionFrame, text='Comment').grid(row=5, sticky=tk.E)
        tk.Label(descriptionFrame, text='Findings').grid(row=10, sticky=tk.E)
        tk.Label(self, text='Reviewer(s)').grid(row=15, sticky=tk.E)
        tk.Label(self, text='Risk').grid(row=20, sticky=tk.E)
        tk.Label(self, text='Jira key is').grid(row=25, sticky=tk.E)
        tk.Label(self, text='Lint').grid(row=30, sticky=tk.E)

        self.briefText = tk.Entry(descriptionFrame, width=69)
        self.briefText.grid(row=0, column=1, columnspan=2, sticky=tk.W+tk.E)
        self.commentText = tk.Text(descriptionFrame, width=69, height=5, wrap=tk.WORD)
        self.commentText.grid(row=5, column=1)
        self.commentScrollbar = tk.Scrollbar(descriptionFrame)
        self.commentScrollbar.grid(row=5, column=2, sticky=tk.N+tk.S)
        self.commentScrollbar.config(command=self.commentText.yview)
        self.commentText.config(yscrollcommand=self.commentScrollbar.set)
        self.findingsText = tk.Text(descriptionFrame, width=69, height=5, wrap=tk.WORD)
        self.findingsText.grid(row=10, column=1)
        self.findingsScrollbar = tk.Scrollbar(descriptionFrame)
        self.findingsScrollbar.grid(row=10, column=2, sticky=tk.N+tk.S)
        self.findingsScrollbar.config(command=self.findingsText.yview)
        self.findingsText.config(yscrollcommand=self.findingsScrollbar.set)

        self.reviewersText = tk.Entry(self, width=69)
        self.reviewersText.grid(row=15, column=1, columnspan=3, sticky=tk.W+tk.E)
        self.riskVar = tk.StringVar(self)
        self.riskVar.set(CommitHelperConstants.NOSELECTION)
        tk.OptionMenu(self, self.riskVar, *self.OPTIONSRISK).grid(row=20, column=1)
        self.jiraText = tk.Entry(self, width=16)
        self.jiraText.grid(row=25, column=1)
        self.lintVar = tk.StringVar(self)
        self.lintVar.set(CommitHelperConstants.NOSELECTION)
        tk.OptionMenu(self, self.lintVar, *self.OPTIONSLINT).grid(row=30, column=1)
        self.lintText = tk.Entry(self, width=50)
        self.lintText.grid(row=30, column=2, sticky=tk.W+tk.E)

        tk.Button(self, text="OK", command=self.callback).grid(row=0, column=90, rowspan=35, sticky=tk.W+tk.E+tk.N+tk.S, padx=5, pady=5)
        self.protocol('WM_DELETE_WINDOW', self.callback)

    def getBriefText(self):
        return self.briefText.get().strip()

    def getCommentText(self):
        return self.commentText.get('1.0', tk.END).strip()

    def getFindingsText(self):
        return self.findingsText.get('1.0', tk.END).strip()

    def getReviewersText(self):
        return self.reviewersText.get().strip()

    def getRiskOption(self):
        return self.riskVar.get()

    def getJiraText(self):
        return self.jiraText.get().strip()

    def getLintOption(self):
        return self.lintVar.get()

    def getLintText(self):
        return self.lintText.get().strip()

class SvnStartCommitHelperController(object):
    view = None
    validator = None
    argv = None

    def __init__(self, argv):
        self.argv = tk.sys.argv
        self.view = SvnStartCommitHelperView(self.checkExit)
        self.validator = SvnStartCommitHelperValidator()
        self.validator.registerGetOptionCallback(self.view.getRiskOption, 'the risk level correlated to the commit')
        self.validator.registerGetOptionCallback(self.view.getLintOption, 'the Lint run')
        self.view.mainloop()
    
    def checkExit(self):
        if self.validator.areOptionsSelected():
            self.writeSvnCommitMessage()
            self.tearDown()

    def getMessage(self):
        return ( self.view.getBriefText(), os.getlogin(), self.view.getCommentText(),
            self.view.getFindingsText(), self.view.getReviewersText(),
            self.view.getRiskOption(), self.view.getJiraText(),
            self.view.getLintOption(), self.view.getLintText() )

    def writeSvnCommitMessage(self):
        message = CommitHelperConstants.MESSAGEBODY % self.getMessage()
        if 4==len(self.argv):
            open(tk.sys.argv[2], mode='w').write(message)
        else:
            print(message)
    
    def tearDown(self):
        self.view.quit()
        self.view.destroy()

if __name__=='__main__':
    controller = SvnStartCommitHelperController(tk.sys.argv)

