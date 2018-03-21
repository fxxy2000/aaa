import Norton.PartnerService_pb2 as PartnerService
import Pair
import RiskCategory
import operator

class AppInfo:
    ads_behaviors = [ PartnerService.GreywareBehavior.NOTIFICATION_BAR_ADS,\
                      PartnerService.GreywareBehavior.SHORTCUT_ADS,\
                      PartnerService.GreywareBehavior.BOOKMARK_ADS,\
                      PartnerService.GreywareBehavior.DIALTONE_ADS,\
                      PartnerService.GreywareBehavior.SMS_INBOX_ADS,\
                      PartnerService.GreywareBehavior.CLICK_SMS,\
                      PartnerService.GreywareBehavior.IN_CONTEXT_ADS ]
    privacy_behaviors = [ PartnerService.GreywareBehavior.ACCOUNT_INFO, \
                          PartnerService.GreywareBehavior.AUDIO_INFO, \
                          PartnerService.GreywareBehavior.BROWSER_HISTORY, \
                          PartnerService.GreywareBehavior.BROWSER_BOOKMARKS, \
                          PartnerService.GreywareBehavior.CALENDAR_INFO, \
                          PartnerService.GreywareBehavior.CALL_LOG, \
                          PartnerService.GreywareBehavior.CAMERA_INFO, \
                          PartnerService.GreywareBehavior.CONTACT_INFO, \
                          PartnerService.GreywareBehavior.DEVICE_INFO, \
                          PartnerService.GreywareBehavior.EMAIL_ADDRESS, \
                          PartnerService.GreywareBehavior.INSTALLED_APP_INFO, \
                          PartnerService.GreywareBehavior.LOCATION_INFO, \
                          PartnerService.GreywareBehavior.OPERATOR_INFO, \
                          PartnerService.GreywareBehavior.PHONE_NUMBER, \
                          PartnerService.GreywareBehavior.PHOTO_INFO_WITH_USER_INTERACTION, \
                          PartnerService.GreywareBehavior.PHOTO_INFO_WITHOUT_USER_INTERACTION, \
                          PartnerService.GreywareBehavior.RUNNING_APP_INFO, \
                          PartnerService.GreywareBehavior.SIM_CARD_INFO, \
                          PartnerService.GreywareBehavior.SMS_INFO, \
                          PartnerService.GreywareBehavior.SETTINGS_INFO, \
                          PartnerService.GreywareBehavior.SOCIAL_NETWORK_ACCOUNT, \
                          PartnerService.GreywareBehavior.VIDEO_INFO_WITH_USER_INTERACTION, \
                          PartnerService.GreywareBehavior.VIDEO_INFO_WITHOUT_USER_INTERACTION, \
                          PartnerService.GreywareBehavior.VOICE_MAIL_ACCOUNT ]

    unusual_behavior = [ PartnerService.GreywareBehavior.CHANGE_HOMEPAGE, \
                         PartnerService.GreywareBehavior.SELF_UPDATE, \
                         PartnerService.GreywareBehavior.INSTALL_APP ]



    high_severity_behaviors = [ PartnerService.GreywareBehavior.ACCOUNT_INFO, \
                                PartnerService.GreywareBehavior.AUDIO_INFO, \
                                PartnerService.GreywareBehavior.BOOKMARK_ADS, \
                                PartnerService.GreywareBehavior.BROWSER_BOOKMARKS, \
                                PartnerService.GreywareBehavior.BROWSER_HISTORY, \
                                PartnerService.GreywareBehavior.CALENDAR_INFO, \
                                PartnerService.GreywareBehavior.CALL_LOG, \
                                PartnerService.GreywareBehavior.CAMERA_INFO, \
                                PartnerService.GreywareBehavior.CHANGE_HOMEPAGE, \
                                PartnerService.GreywareBehavior.CLICK_SMS, \
                                PartnerService.GreywareBehavior.CONTACT_INFO, \
                                PartnerService.GreywareBehavior.DIALTONE_ADS, \
                                PartnerService.GreywareBehavior.EMAIL_ADDRESS, \
                                PartnerService.GreywareBehavior.INSTALL_APP, \
                                PartnerService.GreywareBehavior.NOTIFICATION_BAR_ADS, \
                                PartnerService.GreywareBehavior.PHONE_NUMBER, \
                                PartnerService.GreywareBehavior.PHOTO_INFO_WITH_USER_INTERACTION, \
                                PartnerService.GreywareBehavior.PHOTO_INFO_WITHOUT_USER_INTERACTION, \
                                PartnerService.GreywareBehavior.SELF_UPDATE, \
                                PartnerService.GreywareBehavior.SHORTCUT_ADS, \
                                PartnerService.GreywareBehavior.SMS_INBOX_ADS, \
                                PartnerService.GreywareBehavior.SMS_INFO, \
                                PartnerService.GreywareBehavior.SOCIAL_NETWORK_ACCOUNT, \
                                PartnerService.GreywareBehavior.VIDEO_INFO_WITHOUT_USER_INTERACTION, \
                                PartnerService.GreywareBehavior.VIDEO_INFO_WITH_USER_INTERACTION, \
                                PartnerService.GreywareBehavior.VOICE_MAIL_ACCOUNT ]
    medium_severity_behaviors = [ PartnerService.GreywareBehavior.INSTALLED_APP_INFO, \
                                  PartnerService.GreywareBehavior.LOCATION_INFO, \
                                  PartnerService.GreywareBehavior.RUNNING_APP_INFO ]
    low_severity_behaviors = [ PartnerService.GreywareBehavior.DEVICE_INFO, \
                               PartnerService.GreywareBehavior.IN_CONTEXT_ADS, \
                               PartnerService.GreywareBehavior.OPERATOR_INFO, \
                               PartnerService.GreywareBehavior.SETTINGS_INFO, \
                               PartnerService.GreywareBehavior.SIM_CARD_INFO ]
    def  __init__(self, reputation, app):
        self._reputation = reputation
        self._app = app
        self._risk_categories = []
        self._highest_rating = PartnerService.PerformanceRating.UNKNOWN
        self.categorizeApp()

    def get_reputation(self):
        return self._reputation

    def get_highest_rating(self):
        return self._highest_rating

    def is_highest_rating_high_or_greater(self):
        return self._highest_rating >= PartnerService.PerformanceRating.HIGH

    def is_highest_rating_medium_or_greater(self):
        return self._highest_rating >= PartnerService.PerformanceRating.MEDIUM

    def get_risk_categories(self):
        return self._risk_categories

    def get_risk_categories_count(self):
        if not self._risk_categories:
            return 0
        return len(self._risk_categories)

    def get_app(self):
        return self._app

    def get_localized_category_first(self):
        if not self._risk_categories:
            return "No Risk"
        return self.get_localized_category(self._risk_categories[0])

    def get_localized_category(self, risk_category):
        # print "the risk category = " + str(risk_category)
        if not self._risk_categories:
            return "No Risk"
        if risk_category == RiskCategory.RiskCategory.MALWARE:
            return "Malware"
        elif risk_category == RiskCategory.RiskCategory.PRIVACY_RISK:
            return "Privacy Risk"
        elif risk_category == RiskCategory.RiskCategory.UNUSUAL_BEHAVIOUR_RISK:
            return "Unusual Behavior"
        elif risk_category == RiskCategory.RiskCategory.INTRUSIVE_ADS_RISK:
            return "Intrusive Ads"
        elif risk_category == RiskCategory.RiskCategory.HIGH_BATTERY_USAGE_RISK:
            return "High Battery Usage"
        elif risk_category == RiskCategory.RiskCategory.HIGH_DATA_USAGE_RISK:
            return "High Data Usage"
        else:
            return ""

    def get_greyware_rating(self):
        if self._reputation is None:
            return PartnerService.GreywareRating()
        return self._reputation.greyware

    def get_security_rating(self):
        if self._reputation is None:
            return PartnerService.SecurityRating.NEUTRAL
        return self._reputation.security.score_rating

    def has_security_rating(self):
        return self.get_security_rating() != PartnerService.SecurityRating.NEUTRAL

    def is_malicious(self):
        return self.get_security_rating() <= PartnerService.SecurityRating.LOW_BAD

    def get_battery_background(self):
        if self._reputation is None:
            return PartnerService.PerformanceRating.UNKNOWN
        return self._reputation.performance.battery_background

    def get_network_mobile_background(self):
        if self._reputation is None:
            return PartnerService.PerformanceRating.UNKNOWN
        return self._reputation.performance.network_background_mobile

    def parse_greyware_behaviors(self):
        self.__behavior_privacy_details = dict()
        greyware_rating = self.get_greyware_rating();
        for greyware_risk in greyware_rating.library_list:
            for greyware_behavior in greyware_risk.behavior_list:
                behavior_name = greyware_behavior.behavior_name;
                leak = greyware_behavior.leak
                privacy_details = greyware_behavior.privacy_details
                pair = Pair.Pair(leak, privacy_details)
                self.__behavior_privacy_details[behavior_name] = pair

        return len(self.__behavior_privacy_details.keys());

    def get_behaviors(self):
        return self.__behavior_privacy_details.keys()

    def get_highest_severity(self, behaviors):
        overall_rating = PartnerService.PerformanceRating.NONE
        for behavior in behaviors:
            behavior_rating = self.get_behavior_severity(behavior)
            if behavior_rating > overall_rating:
                overall_rating = behavior_rating
        return overall_rating

    def get_behavior_severity(self, greyware_behavior):
        if greyware_behavior in AppInfo.high_severity_behaviors:
            return PartnerService.PerformanceRating.HIGH
        elif greyware_behavior in AppInfo.medium_severity_behaviors:
            return PartnerService.PerformanceRating.MEDIUM
        elif greyware_behavior in AppInfo.low_severity_behaviors:
            return PartnerService.PerformanceRating.LOW
        else:
            return PartnerService.PerformanceRating.UNKNOWN

    def rate_ads(self):
        ad_behavior = self.get_ads_behavior()
        return self.get_highest_severity(ad_behavior)

    def get_ads_behavior(self):
        behaviors = self.get_behaviors()
        ad_behavior = []
        for behavior in behaviors:
            if behavior in AppInfo.ads_behaviors:
                ad_behavior.append(behavior)
        return ad_behavior;

    def rate_privacy(self):
        privacy_behavior = self.get_privacy_behaviors()
        return self.get_highest_severity(privacy_behavior)

    def get_privacy_behaviors(self):
        behaviors = self.get_behaviors()
        privacy_behavior = []
        for behavior in behaviors:
            if behavior in AppInfo.privacy_behaviors:
                privacy_behavior.append(behavior)
        return privacy_behavior

    def rate_unusual(self):
        unusual_behavior = self.get_unusual_behaviors()
        return self.get_highest_severity(unusual_behavior)

    def get_unusual_behaviors(self):
        behaviors = self.get_behaviors()
        unusual_behavior = []
        for behavior in behaviors:
            if behavior in AppInfo.unusual_behavior:
                unusual_behavior.append(behavior)
        return unusual_behavior

    def categorizeApp(self):
        #print "App name: " + self._app.get_name().encode('utf8')
        self.parse_greyware_behaviors()
        ads_score_rating = self.rate_ads()
        #print "Ads score: " + str(ads_score_rating)
        #print self.get_ads_behavior()
        privacy_score_rating = self.rate_privacy()
        #print "privacy score: " + str(privacy_score_rating)
        #print self.get_privacy_label()
        unusual_behavior = self.rate_unusual()
        #print "unusual score: " + str(unusual_behavior)
        #print self.get_unusual_label()
        battery_score_rating = self.get_battery_background()
        #print "battery score: " + str(battery_score_rating)
        #print self.get_battery_usage_label()
        data_score_rating = self.get_network_mobile_background()
        #print "data score: " + str(data_score_rating)
        #print self.get_network_usage_label()

        if not self.has_security_rating():
            #print "security score: " + str(self.get_security_rating())
            self._highest_rating = PartnerService.PerformanceRating.UNKNOWN
        else:
            if self.is_malicious():
                self._highest_rating = PartnerService.PerformanceRating.HIGH
                self._risk_categories.append(RiskCategory.RiskCategory.MALWARE)
            else :
                category = dict()
                if privacy_score_rating >= PartnerService.PerformanceRating.MEDIUM:
                    #print "privacy score rating"
                    category[RiskCategory.RiskCategory.PRIVACY_RISK] = privacy_score_rating
                if unusual_behavior >= PartnerService.PerformanceRating.MEDIUM:
                    #print "unusual score rating"
                    category[RiskCategory.RiskCategory.UNUSUAL_BEHAVIOUR_RISK] = unusual_behavior
                if ads_score_rating >= PartnerService.PerformanceRating.HIGH:
                    #print "ads score rating"
                    category[RiskCategory.RiskCategory.INTRUSIVE_ADS_RISK] = ads_score_rating

                if len(category.keys()) > 0:
                    sorted_category = sorted(category.items(), key=operator.itemgetter(1), reverse=True)
                    highest_category = sorted_category[0];
                    self._highest_rating = highest_category[1];
                    for ind_category in sorted_category:
                        self._risk_categories.append(ind_category[0])
                if not self._risk_categories:
                    if battery_score_rating >= PartnerService.PerformanceRating.HIGH :
                        #print "battery score rating"
                        self._risk_categories.append(RiskCategory.RiskCategory.HIGH_BATTERY_USAGE_RISK)
                        self._highest_rating = PartnerService.PerformanceRating.LOW;
                    if data_score_rating >= PartnerService.PerformanceRating.HIGH :
                        #print "data score rating"
                        self._risk_categories.append(RiskCategory.RiskCategory.HIGH_DATA_USAGE_RISK)
                        self._highest_rating = PartnerService.PerformanceRating.LOW;

    def get_privacy_label(self):
        privacy_rating = self.rate_privacy();
        if privacy_rating == PartnerService.PerformanceRating.NONE:
            return "No Privacy Risks"
        else:
            privacy_string = "Privacy Risk: \033[1m" + str(PartnerService.PerformanceRating.ScoreRating.Name(privacy_rating)) + "\033[0m"
            privacy_behaviors = self.get_privacy_behaviors()
            privacy_string+="\n The following information is shared:"
            for privacy_behavior in privacy_behaviors:
                privacy_string+="\n   -" + str(PartnerService.GreywareBehavior.Behavior.Name(privacy_behavior))
            return privacy_string

    def get_privacy_label_html(self):
        return self.get_privacy_label().replace("\033[1m", "<b>").replace("\n", "<br />").replace("\033[0m", "</b>")

    def get_unusual_label(self):
        unusual_rating = self.rate_unusual();
        if unusual_rating == PartnerService.PerformanceRating.NONE:
            return "No Unusual Behaviors"
        else:
            unusual_string = "Unusual Behavior Risk: \033[1m" + str(PartnerService.PerformanceRating.ScoreRating.Name(unusual_rating)) + "\033[0m"
            unusual_behaviors = self.get_unusual_behaviors()
            unusual_string+="\n The app is exhibiting the following unusual behaviors"
            for privacy_behavior in unusual_behaviors:
                unusual_string+="\n   -" + str(PartnerService.GreywareBehavior.Behavior.Name(privacy_behavior))
            return unusual_string

    def get_unusual_label_html(self):
        return self.get_unusual_label().replace("\033[1m", "<b>").replace("\n", "<br />").replace("\033[0m", "</b>")

    def get_ads_label(self):
        ads_rating = self.rate_ads()
        if ads_rating == PartnerService.PerformanceRating.NONE:
            return "No Ads"
        else:
            ads_string = "Ads Behavior Risk: \033[1m" + str(PartnerService.PerformanceRating.ScoreRating.Name(ads_rating)) + "\033[0m"
            ads_behaviors = self.get_ads_behavior()
            ads_string+="\n The app is exhibiting the following ads behaviors"
            for privacy_behavior in ads_behaviors:
                ads_string+="\n   -" + str(PartnerService.GreywareBehavior.Behavior.Name(privacy_behavior))
            return ads_string

    def get_ads_label_html(self):
        return self.get_ads_label().replace("\033[1m", "<b>").replace("\n", "<br />").replace("\033[0m", "</b>")

    def get_battery_usage_label(self):
        battery_rating = self.get_battery_background()
        if battery_rating <= PartnerService.PerformanceRating.NONE:
            return None
        else:
            ads_string = "Background battery Usage: \033[1m" + str(PartnerService.PerformanceRating.ScoreRating.Name(battery_rating)) + "\033[0m"
            return ads_string

    def get_battery_usage_label_html(self):
            return self.get_battery_usage_label().replace("\033[1m", "<b>").replace("\n", "<br />").replace("\033[0m", "</b>")

    def get_network_usage_label(self):
        network_rating = self.get_network_mobile_background()
        if network_rating <= PartnerService.PerformanceRating.NONE:
            return None
        else:
            ads_string = "Network Mobile Usage: \033[1m" + str(PartnerService.PerformanceRating.ScoreRating.Name(network_rating)) + "\033[0m"
            return ads_string

    def get_network_usage_label_html(self):
        return self.get_network_usage_label().replace("\033[1m", "<b>").replace("\n", "<br />").replace("\033[0m", "</b>")
