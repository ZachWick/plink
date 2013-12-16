from html.parser import HTMLParser
from html.entities import name2codepoint
import urllib3

class PlinkParser (HTMLParser):
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

    def handle_data (self, data):
        #print ("Data    :", data)
        if self.isLink:
            self.data = data
            self.construct_link()
        elif self.isTitle:
            self.title = data        
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
            self.content += self.data

    def construct_image (self):
        self.images.append( (self.alt, self.src) )
        if self.getContent:
            self.content += alt

    def parse_html_at_url (parser, url):
        html = ''
        http_pool = urllib3.connection_from_url (url)
        r = http_pool.urlopen ('GET', url)
        parser.feed (r.data.decode('utf-8'))
