class HeaderComponent:
    def __init__(self, page):
        self.page = page
        self.logo = "#logo"
        self.user_menu = "#userMenu"

    def is_logo_visible(self):
        return self.page.is_visible(self.logo)