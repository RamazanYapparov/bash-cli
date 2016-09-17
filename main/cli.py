#!/usr/bin/python3.5
import urwid
import quotes

# import main.quotes as quotes

choices = "Новые Случайные".split()

bash = quotes.BashQuotes()

cur_page = bash.last_page


def menu(title='Bash.im', choices="Новые Случайные".split()):
    body = [urwid.Text(title), urwid.Divider()]
    for c in choices:
        button = urwid.Button(c)
        urwid.connect_signal(button, 'click', item_chosen, c)
        body.append(urwid.AttrMap(button, None, focus_map='reversed'))
    return urwid.ListBox(urwid.SimpleFocusListWalker(body))


def show_new():
    quotes_list = bash.get_new_quotes()
    return get_quotes_body(quotes_list)


def show_random():
    quotes_list = bash.get_random_quotes()
    return get_quotes_body(quotes_list, random=True)


def get_quotes_body(quotes_dict, random=False):
    body = []
    if not random:
        for quote in sorted(quotes_dict, reverse=True):
            text = ''
            text += quote + '\n'
            text += quotes_dict[quote] + '\n'
            body.append(urwid.Text(text))
            body.append(urwid.Divider())
    else:
        for quote in quotes_dict:
            text = ''
            text += quote + '\n'
            text += quotes_dict[quote] + '\n'
            body.append(urwid.Text(text))
            body.append(urwid.Divider())
    return body


def show_next():
    quotes_list = bash.get_next_page(cur_page)
    return get_quotes_body(quotes_list)


def show_prev():
    quotes_list = bash.get_prev_page(cur_page)
    return get_quotes_body(quotes_list)


def item_chosen(button, choice):
    if choice == 'Новые':
        response = show_new()
    else: # choice == 'Случайные':
        response = show_random()
    show_page(response)


def show_page(response, **kwargs):
    kwargs['page'] = ''
    done = urwid.Button(u'Ok')
    response.append(urwid.AttrMap(done, None, focus_map='reversed'))
    urwid.connect_signal(done, 'click', exit_program)
    main.original_widget = urwid.ListBox(urwid.SimpleFocusListWalker(response))


def exit_program():
    raise urwid.ExitMainLoop()


def show_menu():
    main.original_widget = menu('Bash.im', choices)


def process_input(key):
    if key in ['TAB', 'tab']:
        show_menu()
    elif key in ['q', 'Q']:
        exit_program()
    elif key in ['right', 'p']:
        show_page(show_next())
    elif key in ['left', 'o']:
        show_page(show_prev())


main = urwid.Padding(menu(u'Bash.im', choices), left=2, right=2)
top = urwid.Overlay(main, urwid.SolidFill(u'\N{MEDIUM SHADE}'),
                    align='center', width=('relative', 500),
                    valign='middle', height=('relative', 500),
                    min_width=40, min_height=20)
urwid.MainLoop(top, unhandled_input=process_input, palette=[('reversed', 'standout', '')]).run()
