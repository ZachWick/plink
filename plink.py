from parser import PlinkParser

if __name__ == "__main__":
    parser = PlinkParser()
    parser.title   = ""
    parser.links   = []
    parser.images  = []
    parser.href    = ""
    parser.data    = ""
    parser.src     = ""
    parser.alt     = ""
    parser.content = ""
    parser.isLink  = False
    parser.isImg   = False
    parser.isTitle = False
    parser.inBody  = False
    parser.parse_html_at_url ("http://zachwick.com/posts/my_xxx_tld.html")
    print (parser.title)
    print (parser.links)
    print (parser.content)
