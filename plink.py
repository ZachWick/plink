import curses
from parser import PlinkParser

def setup_color_pairs ():
    # color pair id, text color, background color
    curses.init_pair (1, curses.COLOR_WHITE, curses.COLOR_RED)
    curses.init_pair (2, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair (3, curses.COLOR_WHITE, curses.COLOR_GREEN)

def lineify (parser):
    lines = parser.content.splitlines()    
    return lines

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

def main ():
    screen = curses.initscr()
    curses.start_color()
    setup_color_pairs()
    curses.noecho()
    curses.cbreak()
    screen.keypad (True)
    curses.curs_set(0)

    parser = PlinkParser()
    parser.url      = "http://zachwick.com/posts/my_xxx_tld.html"
    parser.title    = ""
    parser.links    = []
    parser.images   = []
    parser.href     = ""
    parser.data     = ""
    parser.src      = ""
    parser.alt      = ""
    parser.content  = ""
    parser.isLink   = False
    parser.isImg    = False
    parser.isTitle  = False
    parser.inBody   = False
    parser.newline  = False
    parser.maxLines = curses.LINES - 2
    parser.lastLine = 0

    parser.parse_html_at_url (parser.url)

    parser.content_lines = lineify (parser)

    screen.clear()
    screen.refresh()

    half_fill = (curses.COLS - len(parser.url.expandtabs()) - len(parser.title.expandtabs()) - 3)//2
    title_line = ""
    for x in range (0, half_fill):
        title_line += " "
    title_line += parser.url + " - " + parser.title
    for x in range (0, half_fill):
        title_line += " "
    parser.title_line = title_line
    screen.addstr (0, 0, parser.title_line, curses.color_pair(2))
    screen.refresh()
    
    next_page (screen, parser)
    
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

if __name__ == "__main__":    
    main()
