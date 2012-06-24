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
# @AUTHOR Oliver Merkel <merkel.oliver@web.de>
#
# Feel free to send contributions, pull requests, suggestions or
# any other feedback to the project. You are welcome!
#
import unittest
from svnstartcommithelper import SvnStartCommitHelperConstants
from svnstartcommithelper import SvnStartCommitHelperValidator

class TestSvnStartCommitHelperValidator(unittest.TestCase):

    def getOptionSelected(self):
        return 'Option1'
    
    def getOptionNotSelected(self):
        return SvnStartCommitHelperConstants.NOSELECTION

    def setUp(self):
        self.instance = SvnStartCommitHelperValidator()

    def tearDown(self):
        pass

    def testConstructor(self):
        self.assertIsInstance(self.instance, SvnStartCommitHelperValidator)

    def testAreOptionsSelected(self):
        self.instance.registerGetOptionCallback(self.getOptionSelected, 'the first choice')
        self.assertTrue(self.instance.areOptionsSelected())
        self.instance.registerGetOptionCallback(self.getOptionSelected, 'the second choice')
        self.assertTrue(self.instance.areOptionsSelected())
        self.instance.registerGetOptionCallback(self.getOptionNotSelected, 'the third choice')
        self.assertFalse(self.instance.areOptionsSelected())

if __name__=='__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSvnStartCommitHelperValidator)
    unittest.TextTestRunner(verbosity=2).run(suite)
