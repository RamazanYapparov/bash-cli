#!/usr/bin/python3.5
import urwid
import quotes

# import main.quotes as quotes

choices = "Новые Случайные".split()
bash = quotes.BashQuotes()
args = {}


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

    cur = []

    if not random:
        cur.append(quotes_dict[1])
        quotes_dict = sorted(dict(quotes_dict[0]).items(), reverse=True)

        body.append(urwid.Text('Страница ' + str(cur[0])))
        body.append(urwid.Divider(div_char='@'))
        body.append(urwid.Divider())
    else:
        quotes_dict = list(quotes_dict.items())

    for quote in quotes_dict:
        quote_id = quote[0]
        body.append(urwid.Text(quote_id))
        body.append(urwid.Divider(div_char='-'))
        quote_text = ''
        quote_text += quote[1] + '\n'
        quote_text = quote_text[0:-1]
        body.append(urwid.Text(quote_text))
        body.append(urwid.Divider(div_char='-'))
        body.append(urwid.Divider())
        body.append(urwid.Divider(div_char='@'))
        body.append(urwid.Divider())
    return body


def show_next():
    quotes_list = bash.get_next_page()
    return get_quotes_body(quotes_list)


def show_prev():
    quotes_list = bash.get_prev_page()
    return get_quotes_body(quotes_list)


def item_chosen(button, choice):
    if choice == 'Новые':
        args['is_random'] = False
        response = show_new()
    elif choice == 'Случайные':
        args['is_random'] = True
        response = show_random()
    show_page(response)


def show_page(response):
    response.append(urwid.AttrMap(done, None, focus_map='reversed'))
    main.original_widget = urwid.ListBox(urwid.SimpleFocusListWalker(response))


def exit_program():
    raise urwid.ExitMainLoop()


def show_menu():
    main.original_widget = menu('Bash.im', choices)


def process_input(key):
    if key in ['TAB', 'tab']:
        show_menu()
    elif key in ['q', 'Q', 'й', 'Й']:
        exit_program()
    elif key in ['right'] and not args['is_random']:
        show_page(show_next())
    elif key in ['left'] and not args['is_random']:
        show_page(show_prev())
    elif key in ['r', 'R', 'к', 'К'] and args['is_random']:
        show_page(show_random())


main = urwid.Padding(menu(u'Bash.im', choices), left=2, right=2)
top = urwid.Overlay(main, urwid.SolidFill(u'\N{MEDIUM SHADE}'),
                    align='center', width=('relative', 500),
                    valign='middle', height=('relative', 500),
                    min_width=40, min_height=20)
urwid.MainLoop(top, unhandled_input=process_input, palette=[('reversed', 'standout', '')]).run()
