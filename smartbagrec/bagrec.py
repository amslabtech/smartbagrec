#!/usr/bin/env python3


from argparse import ArgumentParser
from modules.contents import SmartBagRec


def main() -> None:
    parser = ArgumentParser("bagrec command usage")
    parser.add_argument("--profile", "-p", action="store_true",  help="Open profile selector directly")
    args = parser.parse_args()

    if args.profile:
        smart_bag_rec = SmartBagRec("SmartBagRec")
        smart_bag_rec.open_profile()
    else:
        SmartBagRec("SmartBagRec")()


if __name__ == "__main__":
    main()
