import urwid
import quotes

choices = "Новые Случайные".split()


def menu(title, choices):
    body = [urwid.Text(title), urwid.Divider()]
    for c in choices:
        button = urwid.Button(c)
        urwid.connect_signal(button, 'click', item_chosen, c)
        body.append(urwid.AttrMap(button, None, focus_map='reversed'))
    return urwid.ListBox(urwid.SimpleFocusListWalker(body))


def show_new():
    bash = quotes.BashQuotes()
    body = []
    text = ''
    for quote in bash.get_new_quotes():
        text += quote + '\n'
        text += bash.get_new_quotes()[quote] + '\n'
        body.append(urwid.Text(text))
        body.append(urwid.Divider())
    return body


def item_chosen(button, choice):
    if choice == 'Новые':
        response = show_new()
    # response = urwid.Text([u'You chose ', choice, u'\n'])
    done = urwid.Button(u'Ok')
    response.append(urwid.AttrMap(done, None, focus_map='reversed'))
    urwid.connect_signal(done, 'click', exit_program)
    main.original_widget = urwid.ListBox(urwid.SimpleFocusListWalker(response))
    # main.original_widget = urwid.Filler(urwid.Pile(response))


def exit_program(button):
    raise urwid.ExitMainLoop()


main = urwid.Padding(menu(u'Bash.im', choices), left=2, right=2)
top = urwid.Overlay(main, urwid.SolidFill(u'\N{MEDIUM SHADE}'),
                    align='center', width=('relative', 500),
                    valign='middle', height=('relative', 500),
                    min_width=40, min_height=20)
urwid.MainLoop(top, palette=[('reversed', 'standout', '')]).run()
