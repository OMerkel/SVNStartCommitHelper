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
import tkinter.ttk as ttk
import os
import xml.dom.minidom as dom

class CommitHelperConstants(object):
    ERROR = 'Error'
    MSGOPTIONS = 'Please select an option for %s!'
    NOSELECTION = '<noselection>'
    TITLE = 'SVN Start Commit Helper'
    DEFAULTCONFIG = '''\
<config>
<messagebody>Brief: %s

%s: %s

Findings: %s

Reviewer(s): %s

Risk: %s

Jira key is %s

Lint (%s): %s</messagebody>
<templates>
<template>
<brief>Weekly update of list of open questions.</brief>
<comment>Updated the LOQ with information from weekly status telephone conference.</comment>
<findings>Spread sheet is outdated.</findings>
<reviewers>Matt</reviewers>
<risk option="1" />
<jirakey>PAN-176</jirakey>
<lint option="4">Not applicable.</lint>
</template>
<template>
<brief>master.xml update.</brief>
<comment>Added new IDs in master.xml.</comment>
<findings>Message IDs missing since interface changed.</findings>
<reviewers>Hank</reviewers>
<risk option="2" />
<jirakey>PAN-177</jirakey>
<lint option="4">Not applicable.</lint>
</template>
</templates>
<history/>
</config>
'''

class SvnStartCommitHelperValidator(object):
    optionCallbacks = []

    def registerGetOptionCallback(self, callback, name):
        self.optionCallbacks.append((callback, name))

    def areOptionsSelected(self):
        result = True
        for callback, name in self.optionCallbacks:
            result = result and not (callback() == CommitHelperConstants.NOSELECTION)
            if not result:
                tk.messagebox.showerror(CommitHelperConstants.ERROR, CommitHelperConstants.MSGOPTIONS % name)
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
        'Increase',
        'NA'
    ]

    def __init__(self, templateCallback, historyCallback, okCallback):
        tk.Tk.__init__(self)
        self.okCallback = okCallback
        self.templateCallback = templateCallback
        self.historyCallback = historyCallback
        self.title(CommitHelperConstants.TITLE)
        self.minsize(300,50)

        descriptionFrame = tk.Frame(self, bd=1, relief=tk.SUNKEN)
        descriptionFrame.grid(row=0, column=0, columnspan=3, rowspan=10,
            padx=2, pady=2, sticky=tk.N+tk.E+tk.S+tk.W)
        tk.Label(descriptionFrame, text='Brief').grid(row=0, sticky=tk.E)
        tk.Label(descriptionFrame, text='Comment').grid(row=5, sticky=tk.E)
        tk.Label(descriptionFrame, text='Findings').grid(row=10, sticky=tk.E)
        tk.Label(self, text='Reviewer(s)').grid(row=15, sticky=tk.E)
        tk.Label(self, text='Risk').grid(row=20, sticky=tk.E)
        tk.Label(self, text='Jira key is').grid(row=25, sticky=tk.E)
        tk.Label(self, text='Lint').grid(row=30, sticky=tk.E)

        self.briefVar = tk.StringVar(self)
        self.briefText = tk.Entry(descriptionFrame, width=69, textvariable=self.briefVar)
        self.briefText.grid(row=0, column=1, columnspan=2, sticky=tk.W+tk.E)

        self.commentText = tk.Text(descriptionFrame,
            width=69, height=5, wrap=tk.WORD)
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

        self.reviewersVar = tk.StringVar(self)
        self.reviewersText = tk.Entry(self, width=69, textvariable=self.reviewersVar)
        self.reviewersText.grid(row=15, column=1, columnspan=3, sticky=tk.W+tk.E)
        self.riskVar = tk.StringVar(self)
        self.riskVar.set(CommitHelperConstants.NOSELECTION)
        tk.OptionMenu(self, self.riskVar, *self.OPTIONSRISK).grid(row=20, column=1)
        self.jiraVar = tk.StringVar(self)
        self.jiraText = tk.Entry(self, width=16, textvariable=self.jiraVar)
        self.jiraText.grid(row=25, column=1)
        self.lintVar = tk.StringVar(self)
        self.lintVar.set(CommitHelperConstants.NOSELECTION)
        tk.OptionMenu(self, self.lintVar, *self.OPTIONSLINT).grid(row=30, column=1)
        self.lintTextVar = tk.StringVar(self)
        self.lintText = tk.Entry(self, width=50, textvariable=self.lintTextVar)
        self.lintText.grid(row=30, column=2, sticky=tk.W+tk.E)

        tk.Button(self, text="Template...", command=self.templateCallback).grid(row=0, column=90, rowspan=5, sticky=tk.W+tk.E+tk.N+tk.S, padx=5, pady=5)
        tk.Button(self, text="History...", command=self.historyCallback).grid(row=5, column=90, rowspan=5, sticky=tk.W+tk.E+tk.N+tk.S, padx=5, pady=5)
        tk.Button(self, text="OK", command=self.okCallback).grid(row=10, column=90, rowspan=25, sticky=tk.W+tk.E+tk.N+tk.S, padx=5, pady=5)
        self.protocol('WM_DELETE_WINDOW', self.okCallback)

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

    def selectFrom(self, entries, callback):
        treeColumns = ("Brief", "Comment", "Findings")
        self.selectEntries = entries
        self.listCallback = callback
        if [] != entries:
            listboxDialog = tk.Toplevel()
            listboxDialog.minsize(640,50)
            listboxDialog.title('Selection')
            self.tree = ttk.Treeview(listboxDialog, columns=treeColumns, show="headings",
                selectmode="browse")
            self.tree.column(treeColumns[0], width=150, anchor="center")
            self.tree.column(treeColumns[1], width=250)
            self.tree.column(treeColumns[2], width=200)
            self.tree.heading(treeColumns[0], text=treeColumns[0])
            self.tree.heading(treeColumns[1], text=treeColumns[1])
            self.tree.heading(treeColumns[2], text=treeColumns[2])
            self.tree.grid(column=0, row=0, sticky=tk.N+tk.E+tk.S+tk.W)
            treeScrollbar = tk.Scrollbar(listboxDialog)
            treeScrollbar.grid(row=0, column=1, sticky=tk.N+tk.S)
            treeScrollbar.config(command=self.tree.yview)
            self.tree.config(yscrollcommand=treeScrollbar.set)

            tk.Button(listboxDialog, text="OK", command=self.listSelected).grid(row=0, column=90, sticky=tk.W+tk.E+tk.N+tk.S, padx=5, pady=5)

            for entry in entries:
                self.tree.insert('', tk.END, values=entry[0:3])
            self.tree.selection_set(self.tree.identify_row(0))

    def listSelected(self):
        index = self.tree.index(self.tree.selection())
        self.listCallback(self.selectEntries[index])

    def updateFields(self, entry):
        self.briefVar.set(entry[0])
        self.commentText.delete('1.0', tk.END)
        self.commentText.insert(tk.END, entry[1])
        self.findingsText.delete('1.0', tk.END)
        self.findingsText.insert(tk.END, entry[2])
        self.reviewersVar.set(entry[3])
        self.riskVar.set(self.OPTIONSRISK[int(entry[4])])
        self.jiraVar.set(entry[5])
        self.lintVar.set(self.OPTIONSLINT[int(entry[6])])
        self.lintTextVar.set(entry[7])

class SvnStartCommitHelperModel(object):
    dom = None

    def __init__(self):
        self.dom = dom.parseString(CommitHelperConstants.DEFAULTCONFIG)

    def getText(self, nodelist):
        rc = []
        for node in nodelist:
            if node.TEXT_NODE == node.nodeType:
                rc.append(node.data)
        return ''.join(rc)

    def getMessageBody(self):
        messageElement = self.dom.getElementsByTagName('messagebody')[0]
        bodyText = self.getText(messageElement.childNodes)
        return bodyText

    def getTemplates(self):
        rc = []
        templates = self.dom.getElementsByTagName('template')
        for template in templates:
            brief = self.getText(template.getElementsByTagName('brief')[0].childNodes)
            comment = self.getText(template.getElementsByTagName('comment')[0].childNodes)
            findings = self.getText(template.getElementsByTagName('findings')[0].childNodes)
            reviewers = self.getText(template.getElementsByTagName('reviewers')[0].childNodes)
            risk = template.getElementsByTagName('risk')[0].getAttribute('option')
            jirakey = self.getText(template.getElementsByTagName('jirakey')[0].childNodes)
            element = template.getElementsByTagName('lint')[0]
            lintOption = element.getAttribute('option')
            lintText = self.getText(element.childNodes)
            rcElement = ( brief, comment, findings, reviewers,
                          risk, jirakey, lintOption, lintText )
            rc.append(rcElement)
        return rc

    def getHistory(self):
        rc = []
        return rc

class SvnStartCommitHelperController(object):

    def __init__(self, argv):
        self.argv = tk.sys.argv
        self.model = SvnStartCommitHelperModel()
        self.view = SvnStartCommitHelperView(self.getTemplate, self.getHistory,
            self.checkExit)
        self.validator = SvnStartCommitHelperValidator()
        self.validator.registerGetOptionCallback(self.view.getRiskOption, 'the risk level correlated to the commit')
        self.validator.registerGetOptionCallback(self.view.getLintOption, 'the Lint run')
        self.view.mainloop()

    def checkExit(self):
        if self.validator.areOptionsSelected():
            self.writeSvnCommitMessage()
            self.tearDown()

    def getTemplate(self):
        entries = self.model.getTemplates()
        self.view.selectFrom(entries, self.updateFields)

    def getHistory(self):
        entries = self.model.getHistory()
        self.view.selectFrom(entries, self.updateFields)

    def updateFields(self, entry):
        self.view.updateFields(entry)

    def getMessage(self):
        return ( self.view.getBriefText(), os.getlogin(), self.view.getCommentText(),
            self.view.getFindingsText(), self.view.getReviewersText(),
            self.view.getRiskOption(), self.view.getJiraText(),
            self.view.getLintOption(), self.view.getLintText() )

    def writeSvnCommitMessage(self):
        message = self.model.getMessageBody() % self.getMessage()
        if 4==len(self.argv):
            open(tk.sys.argv[2], mode='w').write(message)
        else:
            print(message)

    def tearDown(self):
        self.view.quit()
        self.view.destroy()

if __name__=='__main__':
    controller = SvnStartCommitHelperController(tk.sys.argv)
