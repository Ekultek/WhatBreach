import argparse


class Parser(argparse.ArgumentParser):

    def __init__(self):
        super(Parser, self).__init__()

    @staticmethod
    def optparse():
        parser = argparse.ArgumentParser()
        mandatory = parser.add_argument_group("mandatory opts")
        mandatory.add_argument(
            "-e", "--email", metavar="EMAIL", dest="singleEmail", default=None,
            help="Pass a single email to scan for"
        )
        mandatory.add_argument(
            "-l", "-f", "--list", "--file", metavar="PATH", dest="emailFile", default=None,
            help="Pass a file containing emails one per line to scan"
        )

        search_opts = parser.add_argument_group("search opts")
        search_opts.add_argument(
            "-nD", "--no-dehashed", action="store_false", default=True, dest="searchDehashed",
            help="Suppres dehashed output"
        )
        search_opts.add_argument(
            "-nP", "--no-pastebin", action="store_false", default=True, dest="searchPastebin",
            help="Suppress Pastebin output"
        )

        misc_opts = parser.add_argument_group("misc opts")
        misc_opts.add_argument(
            "-cT", "--check-ten-minute", action="store_true", default=False, dest="checkTenMinuteEmail",
            help="Check if the provided email address is a ten minute email or not"
        )
        misc_opts.add_argument(
            "-d", "--download", action="store_true", default=False, dest="downloadDatabase",
            help="Attempt to download the database if there is one available"
        )
        # easter egg, because we gotta keep it salty ya know
        misc_opts.add_argument(
            "-sS", "--stay-salty", action="store_true", default=False, dest="staySalty",
            help=argparse.SUPPRESS
        )
        return parser.parse_args()
