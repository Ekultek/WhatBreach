import argparse

import lib.settings
import lib.formatter


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
        search_opts.add_argument(
            "-sH", "--search-hunter", action="store_true", default=False, dest="searchHunterIo",
            help="Search hunter.io with a provided email address and query for all information, this "
                 "will process all emails found as normal"
        )
        search_opts.add_argument(
            "-wL", "--search-weleakinfo", action="store_true", default=False, dest="searchWeLeakInfo",
            help="Search weleakinfo.com as well as HIBP for results"
        )
        search_opts.add_argument(
            "-cA", "--check-accounts", action="store_true", default=False, dest="checkEmailAccounts",
            help="Check the profiles associated with an email address"
        )
        search_opts.add_argument(
            "-sB", "--snusbase", action="store_true", default=False, dest="searchSnusBase",
            help="Search snusbase.com for more leaks with a provided email address"
        )
        search_opts.add_argument(
            "-c", "--cookie", metavar="DEHASHED-COOKIE", dest="dehashedCookie",
            help=argparse.SUPPRESS
        )

        misc_opts = parser.add_argument_group("misc opts")
        misc_opts.add_argument(
            "--do-retry", action="store_true", default=False, dest="retryOnFail",
            help="Retry requests to HIBP if they the first one fails"
        )
        misc_opts.add_argument(
            "-dP", "--download-pastes", action="store_true", default=False, dest="downloadPastes",
            help="Download pastes associated with the email address found (if any)"
        )
        misc_opts.add_argument(
            "-vH", "--verify-hunter", action="store_true", default=False, dest="verifyEmailsThroughHunterIo",
            help="Verify the emails found on hunter.io for deliverable status"
        )
        misc_opts.add_argument(
            "-cT", "--check-ten-minute", action="store_true", default=False, dest="checkTenMinuteEmail",
            help="Check if the provided email address is a ten minute email or not"
        )
        misc_opts.add_argument(
            "-d", "--download", action="store_true", default=False, dest="downloadDatabase",
            help="Attempt to download the database if there is one available"
        )
        misc_opts.add_argument(
            "-s", "--save-dir", metavar="DIRECTORY-PATH", default=lib.settings.DOWNLOADS_PATH, dest="saveDirectory",
            help="Pass a directory to save the downloaded databases into instead of the `HOME` path"
        )
        misc_opts.add_argument(
            "--throttle", metavar="TIME", type=int, dest="throttleRequests", default=0,
            help="Throttle the HIBP requests to help prevent yourself from being blocked"
        )
        # easter egg, because we gotta keep it salty ya know
        misc_opts.add_argument(
            "-sS", "--stay-salty", action="store_true", default=False, dest="staySalty",
            help=argparse.SUPPRESS
        )
        return parser.parse_args()

    @staticmethod
    def check_opts(opt):
        need_emails = False
        if opt.singleEmail is not None and opt.emailFile is not None:
            lib.formatter.warn(
                "you have provided a list of emails and a singular email at the same time, we're going to put them all "
                "together and go with it"
            )
            need_emails = True
        if not opt.searchDehashed and not opt.searchPastebin:
            lib.formatter.warn(
                "you have chosen to not output any of the discovered data, literally nothing will be shown, whats the "
                "point of WhatBreach if it doesn't find anything? Drop one of the suppressive flags"
            )
            exit(1)
        if opt.downloadPastes and not opt.searchPastebin:
            lib.formatter.warn(
                "you have provided that you don't want to see any pastebin output, WhatBreach isn't going to "
                "search for pastes if it doesn't need to. So we're not gonna download the pastes, genius.."
            )
            opt.downloadPastes = False
        if opt.saveDirectory != lib.settings.DOWNLOADS_PATH and not opt.downloadDatabase:
            lib.formatter.warn(
                "you've chosen a save directory, but nothing is being downloaded? I mean this isn't going to have any "
                "problems but it's kinda weird right?"
            )
        if opt.staySalty:
            lib.formatter.info("#staysalty")

        if need_emails:
            return lib.settings.smoosh_multi(opt.singleEmail, opt.emailFile)
