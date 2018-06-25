"""Login view."""
import view

class LoginView(view.Base):
    """Widget in charge of handling Pleroline login activities."""

    def __init__(self, main_view):
        super(LoginView, self).__init__(main_view)
