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
import os.path
import xml.dom.minidom as dom
from string import Template

class CommitHelperConstants(object):
    AVOIDCONFIGFILE = False
    ERROR = 'Error'
    INFO = 'Information'
    MSGOPTIONS = 'Please select an option for %s!'
    MSGFILESIZE = 'Could not determine file size of %s!'
    MSGPARSEERROR = 'XML file could not be parsed!'
    MSGFILEEMPTY = 'XML file has size 0.'
    MSGCANTWRITECONFIG = 'Could not open %s for writing default config.'
    MSGMAKECONFIGPATH = 'Creating directory %s now.'
    MSGCREATECONFIGFILE = 'Creating config file %s.'
    MSGEMPTYHISTORY = 'Commit message history is still empty.'
    MSGERRORWRITINGFILE = 'Could not open %s for writing config.'
    NOSELECTION = '<noselection>'
    TITLE = 'SVN Start Commit Helper'
    MAXHISTORYSIZE = 20
    CONFIGDIR = '.svnsch'
    CONFIGFILE = 'svnsch.conf'
    XMLTAGCONFIG = 'config'
    XMLTAGMESSAGEBODY = 'messagebody'
    XMLTAGTEMPLATES = 'templates'
    XMLTAGTEMPLATE = 'template'
    XMLTAGBRIEF = 'brief'
    XMLTAGCOMMENT = 'comment'
    XMLTAGFINDINGS = 'findings'
    XMLTAGREVIEWERS = 'reviewers'
    XMLTAGRISK = 'risk'
    XMLTAGJIRAKEY = 'jirakey'
    XMLTAGLINT = 'lint'
    XMLTAGHISTORY = 'history'
    XMLTAGITEM = 'item'
    XMLATTRIBUTEOPTION = 'option'
    DEFAULTCONFIGTEMPLATE = Template('''\
<$tagroot>
<$tagmessagebody>Brief: $brief

$user: $comment

Findings: $findings

Reviewer(s): $reviewers

Risk: $riskoption

Jira key is $jirakey

Lint ($lintoption): $lint</$tagmessagebody>
<$tagtemplates>
<$tagtemplate>
<$tagbrief>Weekly update of list of open questions.</$tagbrief>
<$tagcomment>Updated the LOQ with information from weekly status telephone conference.</$tagcomment>
<$tagfindings>Spread sheet is outdated.</$tagfindings>
<$tagreviewers>Matt</$tagreviewers>
<$tagrisk $attributeoption="Low" />
<$tagjirakey>PAN-176</$tagjirakey>
<$taglint $attributeoption="NA">Not applicable.</$taglint>
</$tagtemplate>
<$tagtemplate>
<$tagbrief>master.xml update.</$tagbrief>
<$tagcomment>Added new IDs in master.xml.</$tagcomment>
<$tagfindings>Message IDs missing since interface changed.</$tagfindings>
<$tagreviewers>Hank</$tagreviewers>
<$tagrisk $attributeoption="Medium" />
<$tagjirakey>PAN-177</$tagjirakey>
<$taglint $attributeoption="NA">Not applicable.</$taglint>
</$tagtemplate>
</$tagtemplates>
<$taghistory/>
</$tagroot>
''')
    DEFAULTCONFIG = DEFAULTCONFIGTEMPLATE.substitute(
        tagroot=XMLTAGCONFIG,
        tagmessagebody=XMLTAGMESSAGEBODY,
        tagtemplates=XMLTAGTEMPLATES,
        tagtemplate=XMLTAGTEMPLATE,
        tagbrief=XMLTAGBRIEF,
        tagcomment=XMLTAGCOMMENT,
        tagfindings=XMLTAGFINDINGS,
        tagreviewers=XMLTAGREVIEWERS,
        tagrisk=XMLTAGRISK,
        tagjirakey=XMLTAGJIRAKEY,
        taglint=XMLTAGLINT,
        taghistory=XMLTAGHISTORY,
        attributeoption=XMLATTRIBUTEOPTION,
        brief='$brief',
        user='$user',
        comment='$comment',
        findings='$findings',
        reviewers='$reviewers',
        riskoption='$riskoption',
        jirakey='$jirakey',
        lintoption='$lintoption',
        lint='$lint'
    )

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

        templateButton = tk.Button(self, text="Template...", command=self.templateCallback)
        templateButton.grid(row=0, column=90, rowspan=5, sticky=tk.W+tk.E+tk.N+tk.S,
            padx=5, pady=5)
        if not CommitHelperConstants.AVOIDCONFIGFILE:
            historyButton = tk.Button(self, text="History...", command=self.historyCallback)
            historyButton.grid(row=5, column=90, rowspan=5, sticky=tk.W+tk.E+tk.N+tk.S,
                padx=5, pady=5)
        okButton = tk.Button(self, text="OK", command=self.okCallback)
        okButton.grid(row=10, column=90, rowspan=25, sticky=tk.W+tk.E+tk.N+tk.S,
            padx=5, pady=5)
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

            okButton = tk.Button(listboxDialog, text="OK", command=self.listSelected)
            okButton.grid(row=0, column=90, sticky=tk.W+tk.E+tk.N+tk.S, padx=5, pady=5)

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
        self.riskVar.set(entry[4])
        self.jiraVar.set(entry[5])
        self.lintVar.set(entry[6])
        self.lintTextVar.set(entry[7])

class SvnStartCommitHelperModel(object):

    def __init__(self):
        pass

    def getText(self, nodelist):
        rc = []
        for node in nodelist:
            if node.TEXT_NODE == node.nodeType:
                rc.append(node.data)
        return ''.join(rc)

    def getMessageBody(self):
        dom = self.getDom()
        messageElement = dom.getElementsByTagName(CommitHelperConstants.XMLTAGMESSAGEBODY)[0]
        bodyText = self.getText(messageElement.childNodes)
        return bodyText

    def getItem(self, node):
            brief = self.getText(node.getElementsByTagName(CommitHelperConstants.XMLTAGBRIEF)[0].childNodes)
            comment = self.getText(node.getElementsByTagName(CommitHelperConstants.XMLTAGCOMMENT)[0].childNodes)
            findings = self.getText(node.getElementsByTagName(CommitHelperConstants.XMLTAGFINDINGS)[0].childNodes)
            reviewers = self.getText(node.getElementsByTagName(CommitHelperConstants.XMLTAGREVIEWERS)[0].childNodes)
            risk = node.getElementsByTagName(CommitHelperConstants.XMLTAGRISK)[0].getAttribute(CommitHelperConstants.XMLATTRIBUTEOPTION)
            jirakey = self.getText(node.getElementsByTagName(CommitHelperConstants.XMLTAGJIRAKEY)[0].childNodes)
            element = node.getElementsByTagName(CommitHelperConstants.XMLTAGLINT)[0]
            lintOption = element.getAttribute(CommitHelperConstants.XMLATTRIBUTEOPTION)
            lintText = self.getText(element.childNodes)
            return ( brief, comment, findings, reviewers,
                risk, jirakey, lintOption, lintText )

    def getDomFromFile(self):
        rc = None
        homePath = os.path.expanduser('~')
        configPath = os.path.join(homePath, CommitHelperConstants.CONFIGDIR)
        configFile = os.path.join(configPath, CommitHelperConstants.CONFIGFILE)
        if not configPath is None:
            if not os.path.exists(configPath):
                tk.messagebox.showinfo(CommitHelperConstants.INFO,
                    CommitHelperConstants.MSGMAKECONFIGPATH % configPath)
                os.chdir(homePath)
                os.mkdir(CommitHelperConstants.CONFIGDIR)
            if os.path.exists(configPath) and os.path.isdir(configPath):
                if os.path.exists(configFile) and os.path.isfile(configFile):
                    try:
                        file = open(configFile, 'r')
                    except IOError:
                        tk.messagebox.showerror(CommitHelperConstants.ERROR,
                            CommitHelperConstants.MSGFILESIZE % configFile)
                    else:
                        size = os.fstat(file.fileno()).st_size
                        if 0 < size:
                            try:
                                rc = dom.parse(file)
                            except IOError:
                                tk.messagebox.showerror(CommitHelperConstants.ERROR,
                                    CommitHelperConstants.MSGPARSEERROR)
                        else:
                            tk.messagebox.showerror(CommitHelperConstants.ERROR,
                                CommitHelperConstants.MSGFILEEMPTY)
                        file.close()
                else:
                    tk.messagebox.showinfo(CommitHelperConstants.INFO,
                        CommitHelperConstants.MSGCREATECONFIGFILE % configFile)
                    try:
                        file = open(configFile, 'w')
                    except IOError:
                        tk.messagebox.showerror(CommitHelperConstants.ERROR,
                            CommitHelperConstants.MSGCANTWRITECONFIG  % configFile)
                    else:
                        file.write(CommitHelperConstants.DEFAULTCONFIG)
                        file.flush()
                        file.close()
        return rc

    def getDom(self):
        rc = None
        internalDom = dom.parseString(CommitHelperConstants.DEFAULTCONFIG)
        if CommitHelperConstants.AVOIDCONFIGFILE:
            rc = internalDom
        else:
            rc = self.getDomFromFile()
            if None == rc:
                rc = internalDom
        return rc

    def getTemplates(self):
        rc = []
        dom = self.getDom()
        templates = dom.getElementsByTagName(CommitHelperConstants.XMLTAGTEMPLATE)
        for template in templates:
            rc.append(self.getItem(template))
        return rc

    def getHistory(self):
        rc = []
        dom = self.getDom()
        historyElement = dom.getElementsByTagName(CommitHelperConstants.XMLTAGHISTORY)[0]
        items = historyElement.getElementsByTagName(CommitHelperConstants.XMLTAGITEM)
        if [] != items:
            for item in items:
                rc.append(self.getItem(item))
        else:
            tk.messagebox.showinfo(CommitHelperConstants.INFO,
                CommitHelperConstants.MSGEMPTYHISTORY)
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
            self.updateHistory()
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

    def sameInHistory(self, message, items):
        rc = False
        for item in items:
            historyMessage = list(self.model.getItem(item))
            rc = historyMessage == message
            if rc:
                break
        return rc

    def appendMessage(self, dom, message):
        historyElement = dom.getElementsByTagName(CommitHelperConstants.XMLTAGHISTORY)[0]
        item = dom.createElement(CommitHelperConstants.XMLTAGITEM)
        brief = dom.createElement(CommitHelperConstants.XMLTAGBRIEF)
        briefText = dom.createTextNode(message[0])
        comment = dom.createElement(CommitHelperConstants.XMLTAGCOMMENT)
        commentText = dom.createTextNode(message[1])
        findings = dom.createElement(CommitHelperConstants.XMLTAGFINDINGS)
        findingsText = dom.createTextNode(message[2])
        reviewers = dom.createElement(CommitHelperConstants.XMLTAGREVIEWERS)
        reviewersText = dom.createTextNode(message[3])
        risk = dom.createElement(CommitHelperConstants.XMLTAGRISK)
        risk.setAttribute(CommitHelperConstants.XMLATTRIBUTEOPTION, message[4])
        jirakey = dom.createElement(CommitHelperConstants.XMLTAGJIRAKEY)
        jirakeyText = dom.createTextNode(message[5])
        lint = dom.createElement(CommitHelperConstants.XMLTAGLINT)
        lint.setAttribute(CommitHelperConstants.XMLATTRIBUTEOPTION, message[6])
        lintText = dom.createTextNode(message[7])
        brief.appendChild(briefText)
        comment.appendChild(commentText)
        findings.appendChild(findingsText)
        reviewers.appendChild(reviewersText)
        jirakey.appendChild(jirakeyText)
        lint.appendChild(lintText)
        item.appendChild(brief)
        item.appendChild(comment)
        item.appendChild(findings)
        item.appendChild(reviewers)
        item.appendChild(risk)
        item.appendChild(jirakey)
        item.appendChild(lint)
        historyElement.appendChild(item)
        items = historyElement.getElementsByTagName(CommitHelperConstants.XMLTAGITEM)
        while len(items) > CommitHelperConstants.MAXHISTORYSIZE:
            historyElement.removeChild(items[0])
            items = historyElement.getElementsByTagName(CommitHelperConstants.XMLTAGITEM)
        homePath = os.path.expanduser('~')
        configPath = os.path.join(homePath, CommitHelperConstants.CONFIGDIR)
        configFile = os.path.join(configPath, CommitHelperConstants.CONFIGFILE)
        try:
            config = open(configFile, 'w')
            config.write(dom.toxml())
            config.flush()
            config.close()
        except IOError:
            tk.messagebox.showerror(CommitHelperConstants.ERROR,
                CommitHelperConstants.MSGERRORWRITINGFILE % configFile)

    def updateHistory(self):
        if not CommitHelperConstants.AVOIDCONFIGFILE:
            message = list(self.getMessage())
            del message[1:2]
            dom = self.model.getDom()
            historyElement = dom.getElementsByTagName(CommitHelperConstants.XMLTAGHISTORY)[0]
            items = historyElement.getElementsByTagName(CommitHelperConstants.XMLTAGITEM)
            if not self.sameInHistory(message, items):
                self.appendMessage(dom, message)

    def writeSvnCommitMessage(self):
        messageTemplate = Template(self.model.getMessageBody())
        message = self.getMessage()
        messageText = messageTemplate.substitute(
            brief=message[0],
            user=message[1],
            comment=message[2],
            findings=message[3],
            reviewers=message[4],
            riskoption=message[5],
            jirakey=message[6],
            lintoption=message[7],
            lint=message[8])
        if 4==len(self.argv):
            open(tk.sys.argv[2], mode='w').write(messageText)
        else:
            print(messageText)

    def tearDown(self):
        self.view.quit()
        self.view.destroy()

if '__main__'==__name__:
    SvnStartCommitHelperController(tk.sys.argv)
