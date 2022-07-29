#!/usr/bin/env python3
import ipaddress
import re
import sys


class Scanner(object):
    def __init__(self, display):
        """Initialize the Scanner object.

        :param Display display: a Display object from the internal library.
        """

        self.__display = display
        self.__hosts = ['https://www.google.com/', 'https://status.google.com/']
        self.__limit_body_size = 1500
        self.__urls = ['/1/indexing', '/1/infrastructure', '/1/inventory', '/1/latency', '/1/reachability', '/1/status']
        self.__user_agents_path = './data/user-agents.txt'
        self.internal_counter = 0
        self.log_entry_line_number = None
        self.log_entry = None
        self.log_entry_details = None

    def __raise_error(self, error_message):
        """Raise an error by displaying an error message. Also
        increment the internal counter by 1.

        :param str error_message: error message to display.
        """
        self.__display.show_error(self.log_entry_line_number, error_message, self.log_entry)
        self.internal_counter += 1

    def __check_log_entry(self):
        """Ensure the logs are not empty."""
        if self.log_entry_details is None:
            sys.exit(1)

    def load_log_entry(self, log_entry, log_entry_details, line_number):
        """Get the required information of a single log to perform the scan. It includes:
        - The log data: to display the content in case of an error.
        - The log details: to access the pieces of information to be scanned (e.g. HTTP method, URL, etc.).
        - The line of the log: to be able to quickly retrieve the line number in the file containing all the logs.

        :param str log_entry: one line from the file containing all the logs.
        :param dict log_entry_details: dictionary containing all the pieces of information of a log entry.
        :param int line_number: line where the log can be found.
        """
        self.log_entry = log_entry
        self.log_entry_details = log_entry_details
        self.log_entry_line_number = line_number

    def check_ip_address_is_valid(self):
        """Check if an IP address has a valid format. If not, display an error."""
        self.__check_log_entry()
        log_ip_address = self.log_entry_details['ip']
        try:
            ip = ipaddress.ip_address(log_ip_address)
        except ValueError:
            error_message = 'IP address {} is not valid.'.format(log_ip_address)
            self.__raise_error(error_message)

    def check_http_method(self):
        """Check if all the genuine HTTP methods are valid, following a whitelist approach. Methods such as TRACE or
        DEBUG should be discarded, especially in a production environment. If unauthorised methods are logged, display
        an error.
        """
        self.__check_log_entry()
        log_http_method = self.log_entry_details['method']
        allowed_methods = ['GET', 'POST', 'HEAD', 'PUT', 'DELETE', 'OPTIONS']
        if log_http_method not in allowed_methods:
            error_message = 'The method of this request (i.e. \'{}\') looks suspicious.'.format(log_http_method)
            self.__raise_error(error_message)

    def check_url(self):
        """Check if the endpoint are listed within the public API documentation. If not, display an error."""
        self.__check_log_entry()
        log_url = self.log_entry_details['url']
        error_raise = True

        for url in self.__urls:
            if log_url.startswith(url):
                error_raise = False

        if error_raise:
            error_message = 'The requested endpoint (i.e. \'{}\') is not being used by the documentation.' \
                .format(log_url)
            self.__raise_error(error_message)

    def check_status_code(self):
        """Check the HTTP status code of a request. The 5xx HTTP error codes might be interesting during a log
        inspection, as they might have been caused by injection attacks (e.g. cross-site scripting, SQL injections,
        etc.). If a 5xx HTTP error is found, display an error.
        """
        self.__check_log_entry()
        log_status_code = self.log_entry_details['statuscode']
        pattern = "[5-9][0-9][0-9]+"
        matches = re.findall(pattern, log_status_code)
        if len(matches) != 0:
            error_message = 'The HTTP code contained in this request (i.e. \'{}\') is related to a server-side error.'\
                .format(log_status_code)
            self.__raise_error(error_message)

    def check_body_size(self):
        """Check the size (in bytes) of the HTTP request. Large requests might be used during denial of service (DoS)
        attacks to exhaust the server. If the request appears too large, display an error.
        """
        self.__check_log_entry()
        log_body_size = self.log_entry_details['bodysize']
        if int(log_body_size) >= self.__limit_body_size:
            error_message = 'The body size of this HTTP request (\'{}\') seems quite large.'.format(log_body_size)
            self.__raise_error(error_message)

    def check_host(self):
        """Check the host used to perform the request is related to the API, following a whitelist approach. If not,
        display an error."""
        self.__check_log_entry()
        log_host = self.log_entry_details['host']
        error_raise = True

        for host in self.__hosts:
            if host in log_host:
                error_raise = False
                break

        if error_raise:
            error_message = 'The host on this request (i.e. \'{}\') seems invalid.'.format(log_host)
            self.__raise_error(error_message)

    def check_http_protocol(self):
        """Check if the request has been performed over HTTP, and not HTTPS. If so, display an error."""
        self.__check_log_entry()
        log_host = self.log_entry_details['host']
        if 'http://' in log_host:
            error_message = 'The access to the host has been done without HTTPS on this request'.format(log_host)
            self.__raise_error(error_message)

    def check_user_agent(self):
        """Check the user agent, following a whitelist approach. Loads a list of valid user agents. If not listed,
        display an error.
        """
        self.__check_log_entry()
        log_user_agent = self.log_entry_details['useragent']
        try:
            with open(self.__user_agents_path, 'r') as patterns:
                if log_user_agent not in patterns.read():
                    error_message = 'The user agent of this HTTP request (\'{}\') seems suspicious.'.format(
                        log_user_agent)
                    self.__raise_error(error_message)
        except FileNotFoundError:
            self.__display.show_loading_error('The logs could not be found. Ensure the logs are located under the root'
                                              'of the project and try again.')

    def check_all(self):
        """Perform all the checks previously described."""
        self.check_ip_address_is_valid()
        self.check_http_method()
        self.check_url()
        self.check_status_code()
        self.check_body_size()
        self.check_host()
        self.check_http_protocol()
        self.check_user_agent()

    def show_internal_counter(self):
        """Show an internal counter related to the number of log entries that have been scanned. This counter helps to
        create statistics.
        """
        self.__display.show_scanner_counter(self.internal_counter)
