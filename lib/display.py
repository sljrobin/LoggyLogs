#!/usr/bin/env python3
import colorama
import sys


class Display(object):
    def __show_error_header(self, log_entry_line_number):
        """Display the line of a suspicious log.

        :param int log_entry_line_number: line where the log can be found.
        """
        message = 'Potential error on line {}. The following details thrown an error:'.format(log_entry_line_number)
        style = colorama.Style.NORMAL + colorama.Fore.RED + message + colorama.Style.RESET_ALL
        print(style)

    def __show_error_message(self, message):
        """Display the reason why an error has been thrown.

        :param str message: message to display.
        """
        style = colorama.Style.NORMAL + colorama.Fore.YELLOW + message + colorama.Style.RESET_ALL
        print(style)

    def __show_log_entry(self, log_entry):
        """Display the suspicious log to help manual inspection.

        :param str log_entry: one line from the file containing all the logs.
        """
        message = '{}'.format(log_entry)
        style = colorama.Style.NORMAL + colorama.Fore.BLUE + message + colorama.Style.RESET_ALL
        print(style)

    def show_error(self, log_entry_line_number, message, log_entry):
        """Concatenate the header, the reason, as well as the log entry.

        :param int log_entry_line_number: line where the log can be found.
        :param str message: message to display.
        :param str log_entry: one line from the file containing all the logs.
        """
        self.__show_error_header(log_entry_line_number)
        self.__show_error_message(message)
        self.__show_log_entry(log_entry)

    def show_scanner_counter(self, scanner_counter):
        """Show the counter of the scanner.

        :param int scanner_counter: scanner counter.
        """
        if scanner_counter == 0:
            message = 'No entries were found to be suspcious.'
            style = colorama.Style.NORMAL + colorama.Fore.GREEN + message + colorama.Style.RESET_ALL
            print(style)
        else:
            message = 'A total of {} suspicious entries have been found. Note that some entries might have been '\
                      'counted more than once in case they raised errors on multiple checks.'.format(scanner_counter)
            style = colorama.Style.NORMAL + colorama.Fore.CYAN + message + colorama.Style.RESET_ALL
            print(style)

    def show_loading_error(self, message):
        """"Display an error when a file fails to be loaded. Exit the program with an error.

        :param str message: message to display.
        """
        style = colorama.Style.NORMAL + colorama.Fore.RED + message + colorama.Style.RESET_ALL
        print(style)
        sys.exit(1)

    def show_warning_question(self, message):
        """Display a warning question.

        :param str message: message to display.
        """
        style = colorama.Style.NORMAL + colorama.Fore.YELLOW + message + colorama.Style.RESET_ALL
        while True:
            answer = input(style).lower().strip()
            if answer in ('y', 'yes'):
                return answer in ('y', 'yes')
            elif answer in ('n', 'no'):
                style = colorama.Style.NORMAL + colorama.Fore.RED + 'Quitting...' + colorama.Style.RESET_ALL
                print(style)
                sys.exit(0)
            else:
                message = 'You must answer \'yes\'/\'y\' or \'no\'/\'n\').'
                style_else = colorama.Style.NORMAL + colorama.Fore.RED + message + colorama.Style.RESET_ALL
                print(style_else)
