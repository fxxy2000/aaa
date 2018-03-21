import requests

import PartnerService_pb2 as PartnerService
from DataModel.Reputation import Reputation
from DataModel.AppInfo import AppInfo

partner_key = "b7319f9be46a40169819c42ef4b612e8e7bb976261414db3883f674c97a37c7a"
client_guid = b'\x97\x74\xd5\x6d\x68\x2e\x54\x9c'
market_name = "Google Marketplace"
cookie = 0
pqs_server = "https://shasta-mrs.symantec.com/partner"
pqs_headers = {"Content-Type": "application/application/octet-stream"}


class PQS:

    def __init__(self):
        print "PQS class initiated!"

    def single_scan(self, app):
        query = self._build_query([app.get_package_name()])
        result = self._do_scan(query)
        if result:
            reputation = Reputation(app, result[0].security.score_rating)
            return reputation
        else:
            return None

    def batch_scan(self, apps):
        query = self._build_query([package.get_package_name() for package in apps])
        result = self._do_scan(query)
        if result:
            reputations = []
            for i, app in enumerate(apps):
                reputations.append(Reputation(app, result[i].security.score_rating))
            return reputations
        else:
            return None

    def batch_scan_app_info(self, apps):
        if apps:
            query = self._build_query([package.get_package_name() for package in apps])
            result = self._do_scan(query)
            if result:
                reputations = []
                for i, app in enumerate(apps):
                    reputations.append(AppInfo(result[i], app))
                return reputations
            else:
                return None
        else:
            return None

    @staticmethod
    def _do_scan(query):
        print "Scanning..."
        session = requests.Session()
        response = session.post(pqs_server, data=query.SerializeToString(), headers=pqs_headers, verify=True)
        if response.ok:
            result = PartnerService.Response()
            result.ParseFromString(response.content)
            print "Scan succeeded!"
            return [data for data in result.reputations]
        else:
            print "Scan failed: " + response.status_code
            return None

    @staticmethod
    def _build_query(package_names):
        query = PartnerService.Query()
        query.partner_key = partner_key
        query.client_guid = client_guid

        for package_name in package_names:
            package_info = query.packages.add()
            package_info.package_name = package_name
            package_info.market_name = market_name
            package_info.cookie = cookie

        return query
