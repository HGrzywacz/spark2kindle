import urlparse
import urllib
import re
import os

import prototypes


class SparkIndex(prototypes.Index):

    def __init__(self, url):

        page = urllib.urlopen(url)
        page_source = page.readlines()

        self.title = "Invisible Man"
        self.author = self.get_author(page_source)
        self.sections = self.get_sections(page_source)
        [self.dirname, self.dirname_no_slash] = self.make_dirnames(url)

        os.mkdir(self.dirname)

        print "Author: " + self.author
        print "Title: " + self.title
        print self.dirname

    def make_dirnames(self, url):
        m = re.search('.+\/(.+)$', url) # + matches one on more repetition
        if m.group(1)[-1] == "/":
            dirname = m.group(1)
            dirname_no_slash = dirname.rstrip("/")
        else:
            dirname_no_slash = m.group(1)
            dirname = dirname_no_slash + "/"

        return [dirname, dirname_no_slash]


    def get_author(self, page_source):
        regAuthor = re.compile('<div.*?\"authorRight\">(.*?)<\/')
        for line in page_source:
            m = regAuthor.search(line)
            if m:
                # print(m.group(1))
                author = m.group(1)
                return author

    def get_title(self, page_source):
        regTitle = re.compile('<div.*?\"titleLeft\"><h2>(.*?)<\/')
        for line in page_source:
            m = regTitle.search(line)
            if m:
                # print(m.group(1))
                title = m.group(1)
                return title

    def get_sections(self, page_source):
        regSections = re.compile('<div.*?entry.*?(http:.*?)\">(.*?)<')
        sections = list()
        for line in page_source:
            m = regSections.search(line)
            if m:
                sections.append([m.group(2),m.group(1)])
        return sections


class SparkSection(prototypes.Section):
    """ docstring
    """

    def __init__(self, section, index):
        # section to tuple: para [tytul , adres]
        self.title = section[0]
        self.url = section[1]
        self.dirname = index.dirname
        page = urllib.urlopen(self.url)
        page_source = page.readlines()
        self.content = self.get_content(page_source)
        self.content = self.clean_content(self.content)

        filename = urlparse.urlparse(self.url)[2]
        m = re.search('.*\/(.*)', filename)
        self.filename = m.group(1)

        print "\t" + self.title + " " + self.filename

        self.make_file()

    def get_content(self, page_source):
        regContentStart = re.compile('class=\"studyGuideText\"')
        regContentStop = re.compile('<div class=\"previous\">')
        i = 0
        for line in page_source:
            mstart = regContentStart.search(line)
            if mstart:
                start = i + 1
            mstop = regContentStop.search(line)
            if mstop:
                stop = i - 1
            i = i + 1
        return page_source[start:stop]

    def clean_content(self, content):
        cleaned_content = list()
        for line in content:
            line = re.sub('<input.*?>',' ',line)
            cleaned_content.append(line)
        return cleaned_content

    def make_file(self):
        f = file(self.dirname + self.filename,'w')
        self.write_top(f)
        self.write_content(f)
        self.write_bottom(f)
        f.close()

    def write_top(self, f):
        f.write('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">' + "\n")
        f.write('<html xmlns="http://www.w3.org/1999/xhtml">' + "\n")
        f.write('<head>' + "\n")
        f.write('<title>' + self.title + '</title>' + "\n")
        f.write('<link rel="stylesheet" href="styles.css" type="text/css">' + "\n")
        f.write('</head>' + "\n")

    def write_content(self, f):
        f.write("\n" + '<body>' + "\n")

        for line in self.content:
            f.write(line)

        f.write("\n" + '</body>' + "\n")

    def write_bottom(self, f):
        f.write('</html>' + "\n")
