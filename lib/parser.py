#!/usr/bin/env python3
import datetime
import re


class Parser(object):
    def __get_ip_address(self, log_entry):
        """Get the IP address of a log.

        :param str log_entry: one line from the file containing all the logs.
        :return str log_ip_address: the IP address of a log.
        """
        log_ip_address = log_entry.split('-', 1)[0]
        log_ip_address = log_ip_address.split(" ")[0]
        return log_ip_address

    def __get_date(self, log_entry):
        """Get the date of a log.

        :param str log_entry: one line from the file containing all the logs.
        :return datetime log_date_converted: the date of a log.
        """
        pattern = "\[(.*?)\]"
        log_date = re.search(pattern, log_entry).group(0)
        log_date = log_date.replace('[', '')
        log_date = log_date.replace(']', '')
        log_date_converted = datetime.datetime.strptime(log_date, '%d/%b/%Y:%H:%M:%S %z')
        return log_date_converted

    def __get_request(self, log_entry):
        """Get the HTTP request, including the HTTP method.

        :param str log_entry: one line from the file containing all the logs.
        :return str log_request: HTTP request.
        """
        pattern = "\"(.+?)\""
        matches = re.findall(pattern, log_entry)
        log_request = matches[0]
        return log_request

    def __get_request_method(self, log_entry):
        """Get the HTTP method (e.g. GET, POST, etc.).

        :param str log_entry: one line from the file containing all the logs.
        :return str log_request_method: the HTTP method.
        """
        log_request = self.__get_request(log_entry)
        log_request_method = log_request.split(" ", 1)[0]
        log_request_method = log_request_method.replace('\"', '')
        return log_request_method

    def __get_request_url(self, log_entry):
        """Get the URL (i.e. specifically, the reached endpoint).

        :param str log_entry: one line from the file containing all the logs.
        :return str log_request_url: the URL.
        """
        log_request = self.__get_request(log_entry)
        log_request_url = log_request.split(" ", 1)
        log_request_url = log_request_url[1]
        return log_request_url

    def __get_status_code(self, log_entry):
        """Get the HTTP status code (e.g. HTTP 2xx, HTTP 3xx, etc.).

        :param str log_entry: one line from the file containing all the logs.
        :return str log_status_code: the HTTP status code.
        """
        log_status_code = log_entry.split(" ")
        log_status_code = log_status_code[8]
        return log_status_code

    def __get_body_size(self, log_entry):
        """Get the size of the HTTP request body.

        :param str log_entry: one line from the file containing all the logs.
        :return str log_body_size: the body of the HTTP request.
        """
        log_body_size = log_entry.split(" ")
        log_body_size = log_body_size[9]
        return log_body_size

    def __get_host(self, log_entry):
        """Get the host that is reached.

        :param str log_entry: one line from the file containing all the logs.
        :return str log_host: the reached host.
        """
        log_host = log_entry.split(" ")
        log_host = log_host[10]
        return log_host

    def __get_user_agent(self, log_entry):
        """Get the user agent.

        :param str log_entry: one line from the file containing all the logs.
        :return str log_user_agent: the recorded user agent of a log.
        """
        pattern = "\"(.+?)\""
        matches = re.findall(pattern, log_entry)
        log_user_agent = matches[2]
        return log_user_agent

    def parse_log_entry(self, log_entry):
        """Main method that is parsing a single log entry. All the data is then recorded in a dictionary for a further
        use.

        :param str log_entry: one line from the file containing all the logs.
        :return dict log_entry_details: dictionary containing all the pieces of information of a log entry.
        """
        log_entry = log_entry.strip()

        # Creating and appending a dictionary for each log entry
        log_entry_details = {}
        log_entry_details['ip'] = self.__get_ip_address(log_entry)
        log_entry_details['date'] = self.__get_date(log_entry)
        log_entry_details['method'] = self.__get_request_method(log_entry)
        log_entry_details['url'] = self.__get_request_url(log_entry)
        log_entry_details['statuscode'] = self.__get_status_code(log_entry)
        log_entry_details['bodysize'] = self.__get_body_size(log_entry)
        log_entry_details['host'] = self.__get_host(log_entry)
        log_entry_details['useragent'] = self.__get_user_agent(log_entry)

        return log_entry_details
