
class App:

    def __init__(self, package, name, icon):
        self.__package_name = package
        self.__name = name
        self.__icon_url = icon

    def get_name(self):
        return self.__name

    def get_package_name(self):
        return self.__package_name

    def get_small_icon_url(self):
        return self.__get_icon_url("128")

    def get_media_icon_url(self):
        return self.__get_icon_url("256")

    def get_large_icon_url(self):
        return self.__get_icon_url("512")

    def __get_icon_url(self, size):
        if not self.__icon_url or "" == self.__icon_url:
            return ""
        else:
            return self.__icon_url + "=w" + size
