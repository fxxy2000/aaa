import Norton.PartnerService_pb2 as PartnerService


class Reputation:

    def __init__(self, app, rating):
        self.__app = app
        self.__rating = rating

    def get_app(self):
        return self.__app

    def get_rating(self):
        return self.__rating

    def get_rating_name(self):
        return PartnerService.SecurityRating.ScoreRating.Name(self.__rating)

    def to_string(self):
        return "App: " + self.__app.get_name + "\nRating: " + self.get_rating_name()
