class Pair:

    def  __init__(self, leak, privacy_details):
        self.__leak = leak
        self.__privacy_details = privacy_details

    def get_leak(self):
        return self.__leak

    def get_privacy_details(self):
        return self.__privacy_details
