"""Login view."""
import urwid

import view
import utils

class LoginView(view.Base):
    """Widget in charge of handling Pleroline login activities."""

    def __init__(self, main_view):
        email_edit = urwid.Edit(caption='> ')
        password_edit = urwid.Edit(caption='> ', mask='*')
        login_button = urwid.Button('Log In')
        widgets = [
            urwid.Text('Email', align='center'),
            email_edit,
            urwid.Text('Password', align='center'),
            password_edit,
            urwid.LineBox(login_button)]
        login_box = utils.create_pile_flow(widgets, 25, 'center')
        super(LoginView, self).__init__(main_view, optional_base=login_box)
        urwid.connect_signal(
            login_button, 'click', self.do_login,
            user_args=[email_edit, password_edit])

    def do_login(self, email_widget, password_widget, _):
        """Logs user in."""
        email = email_widget.get_edit_text()
        password = password_widget.get_edit_text()
        (success, err) = self.main.try_log_in(email, password)
        if not success:
            password_widget.set_edit_text('')
            print(err)
        else:
            self.main.replace_view('main')
