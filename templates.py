#AES addition to corenlp. provides templates for simple wrappers around corenlp (hacked to exploit batch_parse). aimed at extracting sentiment data.
from corenlp import StanfordCoreNLP, batch_parse
import random
import string
import os
import numpy as np

rootSCNLP='/usr/local/Cellar/python/2.7.6/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/corenlp-python/'
global tempdir, corenlp_dir, sentmapping
corenlp_dir =rootSCNLP+ "stanford-corenlp-full-2013-11-12/"
tempdir='/usr/local/Cellar/python/2.7.6/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/corenlp/temp/'
sentmapping={0:'very negative', 1: 'negative', 2:'neutral', 3:'positive', 4:'very positive'}

class InteractiveParser():
    def __init__(self):
        self.tempdir=tempdir
    def writefile(self):
        randletters=''.join([random.choice(string.letters + string.digits) for i in range(10)])
        self.filename='%s%s/temptext%s.txt' %(self.tempdir, randletters,randletters)
        self.innerdir='%s%s/' % (self.tempdir, randletters)
        while os.path.exists(self.filename): #make sure that file doesn't already exist
            randletters=''.join([random.choice(string.letters + string.digits) for i in range(10)])
            self.innerdir='%s%s/' % (self.tempdir, randletters)
            self.filename='%stemptext%s.txt' %(self.innerdir, randletters)
        os.mkdir(self.innerdir)
        with open(self.filename, 'w') as f:
            f.write(self.text)
    def deletefile(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)
        if os.path.exists(self.innerdir):
            os.rmdir(self.innerdir)
    def parse(self, text):
        self.text=text
        self.writefile()
        parse=batch_parse(self.innerdir, corenlp_dir)
        parse=[el for el in parse if 'temptext' in el['file_name']]
        if len(parse)>1:
            print "warning: multiple files. using only first temptext file."
        parse=parse[0]
        self.deletefile()
        print "parse completed"
        summary=summarizeparse(parse)
        return parse, summary

class FileParser():
    def __init__(self):
        self.inputfile=None
        self.tempdir
    def copyfile(self, inputfile):
        randletters=''.join([random.choice(string.letters + string.digits) for i in range(10)])
        self.filename='%s%s/temptext%s.txt' %(self.tempdir, randletters,randletters)
        self.innerdir='%s%s/' % (self.tempdir, randletters)
        while os.path.exists(self.filename): #make sure that file doesn't already exist
            randletters=''.join([random.choice(string.letters + string.digits) for i in range(10)])
            self.innerdir='%s%s/' % (self.tempdir, randletters)
            self.filename='%stemptext%s.txt' %(self.innerdir, randletters)
        os.mkdir(self.innerdir)
        os.cp(inputfile, self.filename)
    def deletefile(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)
        if os.path.exists(self.innerdir):
            os.rmdir(self.innerdir)
    def parse(self, inputfile):
        self.copyfile(inputfile)
        parse=batch_parse(self.innerdir, corenlp_dir)
        parse=[el for el in parse if 'temptext' in el['file_name']]
        if len(parse)>1:
            print "warning: multiple files. using only first temptext file."
        parse=parse[0]
        self.deletefile()
        print "parse completed"
        summary=summarizeparse(parse)
        return parse, summary
        
class DirectoryParser():
    def __init__(self):
        self.stimtextdir=None
    def parse(self, stimtextdir):
        self.stimtextdir=stimtextdir
        parse=batch_parse(self.stimtextdir, corenlp_dir)
        parse=[el for el in parse if '.DS_Store' != el['file_name']]
        if len(parse)>1:
            print "warning: multiple files. using only first temptext file."
        parse=parse[0]
        print "parse completed"
        summary=summarizeparse(parse)
        return parse, summary

def summarizeparse(parse):
    summary={'numsentences':len(parse['sentences'])}
    summary['svals']=[sent['sentimentValue'] for sent in parse['sentences']]
    summary['sclasses']=[sent['sentiment'] for sent in parse['sentences']]
    summary['avgsentiment']=np.mean(summary['svals'])
    summary['sentiment']=sentmapping[round(summary['avgsentiment'])]
    print '***************************************'
    print "average sentiment = %s (%s)" % (summary['avgsentiment'], summary['sentiment'])
    print '***************************************'
    return summary
    
        

p=InteractiveParser()
output1, summary1=p.parse('the characters were very unrealistic')
output2, summary2=p.parse('the birthday present did not arrive in time for the party')
output3, summary3=p.parse('it rained on her wedding day')
output4, summary4=p.parse('I would only go to see it if it were free')