from html.parser import HTMLParser
from html.entities import name2codepoint
import urllib3
from urllib.parse import urlparse

class PlinkParser (HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.title    = ""
        self.links    = []
        self.images   = []
        self.urls     = []
        self.href     = ""
        self.data     = ""
        self.src      = ""
        self.alt      = ""
        self.content  = ""
        self.isLink   = False
        self.isImg    = False
        self.isTitle  = False
        self.inBody   = False
        self.newline  = False
        self.lastLine = 0

    def handle_starttag (self, tag, attrs):
        #print ("Start tag:", tag)
        #for attr in attrs:
        #    print ("    attr:", attr)
        if tag == "a":
            self.isLink = True
            self.getContent = True
            for attr in attrs:
                [name, data] = attr
                if name == "href":
                    self.href = data
        elif tag == "title":
            self.isTitle = True
            self.getContent = False
        elif tag == "img":
            self.isImg = True
            self.getContent = True
            for attr in attrs:
                [name, data] = attr
                if name == "src":
                    self.src = data
                elif name == "alt":
                    self.alt = data
            self.construct_image()
        elif tag == "body":
            self.inBody = True
            self.getContent = True
        elif tag == "br":
            self.getContent = True
            self.newline = True
        elif tag == "script" or tag == "style" or tag == "link" or tag == "meta":
            self.getContent = False
        else:
            self.getContent = True

    def handle_endtag (self, tag):
        # print ("End tag  :", tag)
        if tag == "a":
            self.isLink  = False
        elif tag == "img":
            self.isImg   = False
        elif tag == "title":
            self.isTitle = False
        elif tag == "body":
            self.inBody = False
        elif tag == "br":
            self.newline = False

    def handle_data (self, data):
        #print ("Data    :", data)
        if self.isLink:
            self.data = data
            self.construct_link()
        elif self.isTitle:
            self.title = data        
        elif self.newline:
            self.content += "\n"
        else:
            if self.getContent:
                self.content += data

    def handle_comment (self, comment):
        print ("Comment   :", comment)

    def handle_entityref (self, name):
        c = chr (name2codepoint[name])
        print ("Named entity: ", c)

    def handle_charref (self, name):
        if name.startswith ('x'):
            c = chr (int (name[1:], 16))
        else:
            c = chr (int (name))
        print ("Num entity: ", c)

    def handle_decl (self, data):
        print ("Decl   :", data)

    def construct_link (self):
        self.links.append( (self.data, self.href) )
        if self.getContent:
            self.content += self.data + " ["+str(len(self.links))+"] "+"("+self.href+")"

    def construct_image (self):
        self.images.append( (self.alt, self.src) )
        if self.getContent:
            self.content += alt

    def parse_html_at_url (self, url):
        http_pool = urllib3.connection_from_url (url)
        del self.links[:]
        del self.images[:]
        self.href     = ""
        self.data     = ""
        self.src      = ""
        self.alt      = ""
        self.content  = ""
        self.isLink   = False
        self.isImg    = False
        self.isTitle  = False
        self.inBody   = False
        self.newline  = False
        self.lastLine = 0
        r = http_pool.urlopen ('GET', url)
        self.feed (r.data.decode('utf-8'))

    def set_url (self, url):
        self.location = urlparse(url)
        self.urls.append (url)
