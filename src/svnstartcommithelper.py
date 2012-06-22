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

class SvnStartCommitHelperView(tk.Tk):
    TITLE = 'SVN Start Commit Helper'
    NOSELECTION = '<noselection>'
    OPTIONSRISK = [
        NOSELECTION,
        'Low',
        'Medium',
        'High'
    ]
    OPTIONSLINT = [
        NOSELECTION,
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
        self.title(self.TITLE)
        self.minsize(300,50)

        tk.Label(self, text='Comment').grid(row=5, sticky=tk.E)
        tk.Label(self, text='Findings').grid(row=10, sticky=tk.E)
        tk.Label(self, text='Reviewer(s)').grid(row=15, sticky=tk.E)
        tk.Label(self, text='Risk').grid(row=20, sticky=tk.E)
        tk.Label(self, text='Jira key is').grid(row=25, sticky=tk.E)
        tk.Label(self, text='Lint').grid(row=30, sticky=tk.E)

        self.commentText = tk.Entry(self, width=69)
        self.commentText.grid(row=5, column=1, columnspan=2)
        self.findingsText = tk.Entry(self, width=69)
        self.findingsText.grid(row=10, column=1, columnspan=2)
        self.reviewersText = tk.Entry(self, width=69)
        self.reviewersText.grid(row=15, column=1, columnspan=2)
        self.riskVar = tk.StringVar(self)
        self.riskVar.set(self.NOSELECTION)
        tk.OptionMenu(self, self.riskVar, *self.OPTIONSRISK).grid(row=20, column=1)
        self.jiraText = tk.Entry(self, width=16)
        self.jiraText.grid(row=25, column=1)
        self.lintVar = tk.StringVar(self)
        self.lintVar.set(self.NOSELECTION)
        tk.OptionMenu(self, self.lintVar, *self.OPTIONSLINT).grid(row=30, column=1)
        self.lintText = tk.Entry(self, width=50)
        self.lintText.grid(row=30, column=2)

        tk.Button(self, text="OK", command=self.callback).grid(row=5, column=90, rowspan=30, sticky=tk.W+tk.E+tk.N+tk.S, padx=5, pady=5)
        self.protocol('WM_DELETE_WINDOW', self.callback)

    def getNoSelection(self):
        return self.NOSELECTION

    def getCommentText(self):
        return self.commentText.get().strip()

    def getFindingsText(self):
        return self.findingsText.get().strip()

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
    ERROR = 'Error'
    MSGRISK = 'Please select an option for the risk level correlated to the commit!'
    MSGLINT = 'Please select an option for Lint first!'
    view = None

    def __init__(self):
        self.view = SvnStartCommitHelperView(self.checkExit)
        self.view.mainloop()
    
    def checkExit(self):
        if self.view.getRiskOption() == self.view.getNoSelection():
            tkinter.messagebox.showerror(self.ERROR, self.MSGRISK)
        else:
            if self.view.getLintOption() == self.view.getNoSelection():
                tkinter.messagebox.showerror(self.ERROR, self.MSGLINT)
            else:
                self.writeSvnCommitMessage()
                self.tearDown()

    def writeSvnCommitMessage(self):
        f=open(tk.sys.argv[2], mode='w')
        f.write('%s: %s\n\n' % (os.environ.get('USERNAME'), self.view.getCommentText()))
        f.write('Findings: %s\n\n' % self.view.getFindingsText())
        f.write('Reviewer(s): %s\n\n' % self.view.getReviewersText())
        f.write('Risk: %s\n\n' % self.view.getRiskOption())
        f.write('Jira key is %s\n\n' % self.view.getJiraText())
        f.write('Lint (%s): %s\n' % (self.view.getLintOption(), self.view.getLintText()))
    
    def tearDown(self):
        self.view.quit()
        self.view.destroy()

if __name__=='__main__':
    if 4==len(tk.sys.argv):
        controller = SvnStartCommitHelperController()
