import json
import subprocess

from lib.cmd import Parser
from hookers.hunter_io_hook import HunterIoHook
from hookers.hibp_hook import BeenPwnedHook
from hookers.dehashed_hook import DehashedHook
from hookers.databasestoday_hook import DatabasesTodayHook
from lib.settings import (
    BANNER,
    display_found_databases,
    grab_api_tokens,
    check_ten_minute_email,
    TEN_MINUTE_EMAIL_EXTENSION_LIST
)
from lib.formatter import (
    info,
    error,
    warn,
    prompt
)


def main():
    try:
        opt = Parser().optparse()
        print(BANNER)
        res = Parser().check_opts(opt)
        if res is not None:
            to_search = res
        else:
            to_search = []
        do_not_search = []

        if len(to_search) == 0:
            if opt.singleEmail is None and opt.emailFile is None:
                warn("you have not provided an email to scan, redirecting to the help menu")
                subprocess.call(["python", "whatbreach.py", "--help"])
                exit(1)
            if opt.searchHunterIo and opt.singleEmail is not None:
                info("starting search on hunter.io using {}".format(opt.singleEmail))
                api_tokens = grab_api_tokens()
                file_results = HunterIoHook(
                    opt.singleEmail, api_tokens["hunter.io"], verify_emails=opt.verifyEmailsThroughHunterIo
                ).hooker()
                with open(file_results) as data:
                    emails = json.loads(data.read())["discovered_emails"]
                for email in emails:
                    to_search.append(email)
            elif opt.singleEmail is not None:
                info("starting search on single email address: {}".format(opt.singleEmail))
                to_search = [opt.singleEmail]
            elif opt.emailFile is not None:
                try:
                    open(opt.emailFile).close()
                except IOError:
                    error("unable to open file, does it exist?")
                    exit(1)
                with open(opt.emailFile) as emails:
                    info("parsing email file: {}".format(opt.emailFile))
                    to_search = emails.readlines()
                info("starting search on a total of {} email(s)".format(len(to_search)))

        for email in to_search:
            email = email.strip()

            if opt.checkTenMinuteEmail:
                if check_ten_minute_email(email, TEN_MINUTE_EMAIL_EXTENSION_LIST):
                    warn("email: {} appears to be a ten minute email".format(email))
                    answer = prompt("would you like to process the email[y/N]")
                    if answer.startswith("n"):
                        do_not_search.append(email)

            if email not in do_not_search:
                info("searching breached accounts on HIBP related to: {}".format(email))
                account_dumps = BeenPwnedHook(email).account_hooker()
                info("searching for paste dumps on HIBP related to: {}".format(email))

                if opt.searchPastebin:
                    paste_dumps = BeenPwnedHook(email).paste_hooker()
                else:
                    warn("suppressing discovered pastes")
                    paste_dumps = []

                if account_dumps is not None and paste_dumps is not None:
                    info(
                        "found a total of {} database breach(es) and a total of {} paste(s) pertaining to: {}".format(
                            len(account_dumps), len(paste_dumps), email
                        )
                    )
                    if opt.searchDehashed:
                        found_databases = DehashedHook(account_dumps).hooker()
                    else:
                        warn("suppressing discovered databases")
                        found_databases = {}
                    for i, dump in enumerate(paste_dumps, start=1):
                        found_databases["Paste#{}".format(i)] = str(dump)
                    display_found_databases(found_databases)
                    if opt.downloadDatabase:
                        for item in found_databases.keys():
                            if "Paste" not in item:
                                info("searching for downloadable databases using query: {}".format(item.lower()))
                                downloaded = DatabasesTodayHook(
                                    str(item), downloads_directory=opt.saveDirectory
                                ).hooker()
                                if len(downloaded) != 0:
                                    info(
                                        "downloaded a total of {} database(s) pertaining to query: {}".format(
                                            len(downloaded), item
                                        )
                                    )
                                    display_found_databases(downloaded, is_downloaded=True)
                                else:
                                    warn(
                                        "no databases appeared to be preset and downloadable related to query: {}".format(
                                            str(item)
                                        )
                                    )

                elif account_dumps is not None and paste_dumps is None:
                    info("found a total of {} database breach(es) pertaining to: {}".format(len(account_dumps), email))
                    if opt.searchDehashed:
                        found_databases = DehashedHook(account_dumps).hooker()
                    else:
                        warn("suppressing discovered databases")
                        found_databases = {}
                    if len(found_databases) != 0:
                        display_found_databases(found_databases)
                        if opt.downloadDatabase:
                            for item in found_databases.keys():
                                if "Paste" not in item:
                                    info("searching for downloadable databases using query: {}".format(item.lower()))
                                    downloaded = DatabasesTodayHook(
                                        str(item), downloads_directory=opt.saveDirectory
                                    ).hooker()
                                    if len(downloaded) != 0:
                                        info(
                                            "downloaded a total of {} database(s) pertaining to query: {}".format(
                                                len(downloaded), item
                                            )
                                        )
                                        display_found_databases(downloaded, is_downloaded=True)
                                    else:
                                        warn(
                                            "no databases appeared to be preset and downloadable related to query: {}".format(
                                                str(item)
                                            )
                                        )
                    else:
                        warn("no output to show, most likely due to output suppression or dehashed")
                elif account_dumps is None and paste_dumps is not None:
                    # this should never happen
                    error("no database dumps found nor any pastes found for: {}".format(email))
                else:
                    error("email {} was not found in any breach".format(email))

        if opt.staySalty:
            # i know that you think that you know shit
            # all the shade that's coming at me I wonder who throws it
            # you can't see the vision boy, you must be outta focus
            # that's a real hot program homie, I wonder who wrote it? oh shit
            # (lyrics ripped from iSpy by Kyle, all I do is steal bruh)
            warn("all this code was stolen with <3 by Eku")
    except KeyboardInterrupt:
        error("user quit the session")