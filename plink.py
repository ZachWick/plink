import curses
from parser import PlinkParser
from urllib.parse import urlparse, urlunparse

def setup_color_pairs ():
    # color pair id, text color, background color
    curses.init_pair (1, curses.COLOR_WHITE, curses.COLOR_RED)
    curses.init_pair (2, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair (3, curses.COLOR_WHITE, curses.COLOR_GREEN)

def lineify (parser):
    lines = parser.content.splitlines()    
    return lines

def get_url (screen, parser):
    parser.parse_html_at_url (parser.urls[-1])

    parser.content_lines = lineify (parser)

    screen.clear()

    half_fill = (curses.COLS - len(parser.urls[-1].expandtabs()) - len(parser.title.expandtabs()) - 3)//2
    title_line = ""
    for x in range (0, half_fill):
        title_line += " "
    title_line += parser.urls[-1] + " - " + parser.title
    for x in range (0, half_fill):
        title_line += " "
    parser.title_line = title_line
    screen.addstr (0, 0, parser.title_line, curses.color_pair(2))
    screen.refresh()

    parser.maxLines = curses.LINES - 2
    next_page (screen, parser)

def get_url_and_go (screen, parser):
    screen.addstr ( curses.LINES - 1, 0, "URL: ", curses.color_pair(3))
    screen.refresh()
    url = screen.getstr (curses.LINES - 1, 6, curses.COLS - 1 - 6)
    url = url.decode('utf-8')
    parser.set_url (url)
    get_url (screen, parser)
    
def next_page (screen, parser):
    screen.clear()
    screen.refresh()
    for line in range (parser.lastLine, parser.maxLines):
        if line < len(parser.content_lines) - 1:
            screen.addstr ((line % (curses.LINES - 2)) + 1, 0, parser.content_lines[line])
    screen.addstr (0, 0, parser.title_line, curses.color_pair(2))
    screen.refresh()
    parser.lastLine += curses.LINES - 2
    parser.maxLines += parser.maxLines

def prev_page (screen, parser):
    screen.clear()
    screen.refresh()
    for line in range (parser.lastLine - (2 * (curses.LINES - 2)), parser.lastLine - curses.LINES - 2):
        if line >= 0 and line < len(parser.content_lines) - 1:
            screen.addstr ((line % (curses.LINES - 2)) + 1, 0, parser.content_lines[line])
    screen.addstr (0, 0, parser.title_line, curses.color_pair(2))
    screen.refresh()
    parser.lastLine -= curses.LINES - 2
    parser.maxLines -= max(parser.maxLines, curses.LINES - 2)
        

def show_link_list (screen, parser):
    screen.clear()
    screen.addstr (2, 0, "Links:")
    link_count = 0
    for link in parser.links:
        (text, href) = link
        disp_str = "["+str(link_count)+"] "+href
        screen.addstr (link_count + 2, 0, disp_str)
        link_count += 1
    screen.refresh()

    screen.addstr ( curses.LINES - 1, 0, "Link: ", curses.color_pair(3))
    screen.refresh()
    char = screen.getstr (curses.LINES - 1, 7, curses.COLS - 1 - 7)    

    (name, url) = parser.links[int(char)]
    parsed_link = urlparse (url)

    link_to_parse = (parser.location.scheme if parsed_link.scheme == "" else parsed_link.scheme,
                     parser.location.netloc if parsed_link.netloc == "" else parsed_link.netloc,
                     parsed_link.path,
                     parsed_link.params,
                     parsed_link.query,
                     parsed_link.fragment)

    url = urlunparse (link_to_parse)
    parser.set_url (url)
    get_url (screen, parser)

def go_back (screen, parser):
    if len(parser.urls) >= 2:
        parser.urls.pop()
        parser.set_url (parser.urls[-1])
    elif len(parser.urls) == 1:
        parser.set_url (parser.urls[0])
    else:
        pass
    get_url (screen, parser)
    

def main ():
    screen = curses.initscr()
    curses.start_color()
    setup_color_pairs()
    curses.noecho()
    curses.cbreak()
    screen.keypad (True)
    curses.curs_set(0)

    parser = PlinkParser()
    parser.maxLines = curses.LINES - 2
    parser.set_url ("http://zachwick.com/")

    get_url (screen, parser)
        
    while True:
        key = screen.getkey()
        if key == "q":
            # Curses cleanup
            curses.nocbreak()
            screen.keypad (False)
            curses.echo()
            curses.endwin()
            exit()
        elif key == "n":
            next_page (screen, parser)
        elif key == "p":
            prev_page (screen, parser)
        elif key == "g":
            get_url_and_go (screen, parser)
        elif key == "l":
            show_link_list (screen, parser)
        elif key == "b":
            go_back (screen, parser)

if __name__ == "__main__":    
    main()
