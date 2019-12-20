#!/bin/python3
# -*- coding: utf-8 -*-
import sys
import smtplib
import tarfile
from email.mime.text import MIMEText

ARCHIVE_MODE = 'w:gz'
SMTP_PORT=25

class MailUtil(object):

    def __init__(self,
                 smtp_server: str,
                 from_addr: str,
                 to_addr: str,
                 cc_addr: str,
                 ses_accesskey=None,
                 ses_secretkey=None,
                 port=SMTP_PORT,
                 is_sesauth=False
    ):
        """Mail class for util
        
        Args:
            smtp_server (str): SMTP server host/ip
            from_addr (str): From address
            to_addr (str): To address
            cc_addr (str): Cc address
            ses_accesskey ([type], optional): Defaults to None. IAM AccessKey
            ses_secretkey ([type], optional): Defaults to None. IAM SecretKey
            is_sesauth ([type], optional): Defaults to False. send a mail via ses if it sets TRUE.
                ses_accesskey and ses_secretkey arguments must be specified.
        """
        self.smtp_server = smtp_server
        self.from_addr = from_addr
        self.to_addr = to_addr
        self.cc_addr = cc_addr
        self.__ses_accesskey = ses_accesskey
        self.__ses_secretkey = ses_secretkey
        self.__ses_auth = (self.__ses_accesskey, self.__ses_secretkey)
        self.port = port
        self.is_sesauth = is_sesauth

    def send_mail(self, subject: str, body: str):
        """send mail vis smtp or amazon ses
        
        Args:
            subject (str): [description]
            body (str): [description]

        Raises:
            smtplib.SMTPException: you can describe error message from "strerror" attr.
        """
        mail = MIMEText(body)
        mail['To'] = self.to_addr
        mail['Cc'] = self.cc_addr
        mail['From'] = self.from_addr
        mail['Subject'] = subject

        try:
            with smtplib.SMTP(self.smtp_server, self.port) as server:
                server.ehlo()
                if self.is_sesauth:
                    server.starttls()
                    server.login(*self.__ses_auth)
                server.sendmail(self.from_addr,
                                [[self.to_addr], [self.cc_addr]],
                                mail.as_string())
        except smtplib.SMTPException:
            raise
    
    def set_fromaddress(self, from_addr: str):
        self.from_addr = from_addr
    
    def set_ccaddress(self, cc_addr: str):
        self.cc_addr = cc_addr

    def set_toaddress(self, to_addr: str):
        self.to_addr = to_addr

    def set_smtpserver(self, smtp_server: str):
        self.smtp_server = smtp_server


def compress_to_tar(self, src_path: str, archive_name=None, archive_mode=None):
    """Compress the specified file/dir to tar archive.
    
    Args:
        src_path (str): source file path
        archive_name ([type], optional): Defaults to None. archive file path created.
        archive_mode ([type], optional): Defaults to None. default is write mode.
    Raises:
        FileNotFoundError: raised when source file not found.
        PermissionError: raised when failed to read/write source file or archive.
        tarfile.TarError: raised when compressing to tar archive for any reason.
    """
    if archive_name is None:
        archive_name = r"{0}.tar.gz".format(src_path)
    if archive_mode is None:
        archive_mode = ARCHIVE_MODE
    try:
        with tarfile.open(archive_name, archive_mode) as tar:
            tar.add(src_path)
    except FileNotFoundError as notfound_e:
        sys.stderr.write("{0} not found.".format(src_path))
        raise notfound_e
    except PermissionError as perm_e:
        sys.stderr.write("Permission error to read/write source file or archive.")
        raise perm_e
    except tarfile.TarError as tar_e:
        sys.stderr.write("raised unexpected error when compressing to tar file")
        raise tar_e

def gen_ascii(string: str):
    """generate ascii-code from string
    
    Args:
        string (str): literal
    """
    for char in string:
        yield ord(char)

def binary_search(list: list, target: str):
    """binary search
    
    Args:
        list (list): sorted list
        target (str): search target
    """
    low = 0
    high = len(list) - 1
    while low <= high:
        mid = (low + high) // 2
        pick = list[mid]
        if pick == target:
            return mid
        if pick > target:
            high = mid -1
        else:
            low = mid + 1
    return None
