class User:
    def __init__(self):
        self.__devices = {}
        self.__first_name = None
        self.__last_name = None
        self.__email = None
        self.__avatar_url = None

    def set_name(self, first, last):
        self.__first_name = first
        self.__last_name = last

    def set_email(self, email):
        self.__email = email

    def get_email(self):
        return self.__email

    def get_display_name(self):
        return self.__first_name + ' ' + self.__last_name

    def set_avatar_url(self, avatar_url):
        self.__avatar_url = avatar_url

    def get_avatar_url(self):
        return self.__avatar_url