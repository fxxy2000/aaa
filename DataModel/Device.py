
class Device:

    def __init__(self, gsf_id, display_name, brand, model, carrier, icon):
        self.__web_id = None
        self.__gsf_id = gsf_id
        self.__display_name = display_name
        self.__brand = brand
        self.__model = model
        self.__carrier = carrier
        self.__icon_url = icon[:icon.index('=')]

    def get_display_name(self):
        return self.__display_name

    def get_carrier_name(self):
        return self.__carrier

    def get_brand_name(self):
        return self.__brand

    def get_model_name(self):
        return self.__model

    def get_web_id(self):
        return self.__web_id

    def set_web_id(self, web_id):
        self.__web_id = web_id

    def get_gsf_id(self):
        return self.__gsf_id

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
