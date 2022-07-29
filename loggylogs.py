#!/usr/bin/env python3
import argparse
import lib
import sys

LOGS_PATH = './data/samples.log'


def create_argsparser():
    """Create the argument parser.

    :return argparse argsparser: an argument parser.
    """
    argsparser = argparse.ArgumentParser(allow_abbrev=False)
    argsparser.add_argument('--all', action='store_true', help='Perform all the available tests')
    argsparser.add_argument('--bodysize', action='store_true', help='Check the body size is not too important')
    argsparser.add_argument('--host', action='store_true', help='Check the host is valid')
    argsparser.add_argument('--ip', action='store_true', help='Check the IP address is valid')
    argsparser.add_argument('--httpmethod', action='store_true', help='Check which HTTP method is being used')
    argsparser.add_argument('--httpprotocol', action='store_true', help='Check if HTTP connections (i.e. without '\
                                                                        'encryption) are made to the server')
    argsparser.add_argument('--statuscode', action='store_true', help='Check the HTTP status code')
    argsparser.add_argument('--url', action='store_true', help='Check the URL is an endpoint available within the '\
                                                                'API documentation')
    argsparser.add_argument('--useragent', action='store_true', help='Check the user agent is a recognized web browser')
    return argsparser


def open_logs_file():
    """Open the file containing the logs.

    :return str logs_file: all the logs in one string.
    """
    display = lib.display.Display()
    try:
        with open(LOGS_PATH, 'r') as data:
            logs_file = data.readlines()
            return logs_file
    except FileNotFoundError:
        display.show_loading_error('The logs could not be found. Ensure the logs are located under the root of the \
                                    project and try again.')


def launch_scan(parser, scanner, scanner_func):
    """Load the logs in one string, parse it and call a Scanner method.

    :param Parser parser: a Parser object from the internal library.
    :param Scanner scanner: a Scanner object from the internal library.
    :param scanner_func: a Scanner method.
    """
    logs_file = open_logs_file()
    for line_number, log_entry in enumerate(logs_file):
        line_number += 1
        log_entry_details = parser.parse_log_entry(log_entry)
        scanner.load_log_entry(log_entry, log_entry_details, line_number)
        scanner_func()
    scanner.show_internal_counter()


def main():
    """Main entry point. Handle an argument parser and the different options."""
    display = lib.display.Display()
    parser = lib.parser.Parser()
    scanner = lib.scanner.Scanner(display)
    argsparser = create_argsparser()
    args = argsparser.parse_args()

    # Action: perform all the available tests
    if args.all:
        display.show_warning_question('Running all tests at once might create lots of duplicates.'\
                                      'Do you want to continue (y/n): ')
        launch_scan(parser, scanner, scanner.check_all)

    # Action: check the body size is not too important
    elif args.bodysize:
        launch_scan(parser, scanner, scanner.check_body_size)

    # Action: check the host is valid
    elif args.host:
        launch_scan(parser, scanner, scanner.check_host)

    # Action: check which HTTP method is being used
    elif args.httpmethod:
        launch_scan(parser, scanner, scanner.check_http_method)

    # Action: check if HTTP connections (i.e. without encryption) are made to the server
    elif args.httpprotocol:
        launch_scan(parser, scanner, scanner.check_http_protocol)

    # Action: check the IP address is valid
    elif args.ip:
        launch_scan(parser, scanner, scanner.check_ip_address_is_valid)

    # Action: check the HTTP status code
    elif args.statuscode:
        launch_scan(parser, scanner, scanner.check_status_code)

    # Action: check the URL is an endpoint available within the API documentation
    elif args.url:
        launch_scan(parser, scanner, scanner.check_url)

    # Action: check the user agent is a recognized web browser
    elif args.useragent:
        launch_scan(parser, scanner, scanner.check_user_agent)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nOperation interrupted')
        sys.exit(1)
