#! /usr/bin/env python

#----------------------------------------------------------------------
# This file contains variables that person running this scirpt
# might need to change. 
#----------------------------------------------------------------------


#----------------------------------------------------------------------
# NIGHTLY_BUILD_ROOT_DIR: 
#   directory where code will be checked out and builds
#   done. If the directory does not exist, it will be created.
#----------------------------------------------------------------------
NIGHTLY_BUILD_ROOT_DIR = '/home/jp/COIN'

#----------------------------------------------------------------------
# Values for sending mail:
#  SMTP_SERVER_NAME: name of smtp server. For gmail server 
#                 this is smtp.gmail.com
#  SMTP_SERVER_PORT: port number of the smtp server. This is typically 25,
#                 but for gmail server it is 587.
#  SMTP_SSL_SERVER: 0 or 1. If 1 then SMTP uses SSL (sometimes called startltls).
#                 For gmail this is 1.
#  SMTP_USER_NAME: name of authorized user on server. If using gmail server
#                 this is gmail_userid@gmail.com which is coded as
#                 'gmail_userid _AT_ gmail _DOT_ com.  
#  SMTP_PASSWORD_FILENAME: name of file containing smtp user's password
#  SENDER_EMAIL_ADDR: email sent by this script will be from this address
#  MY_EMAIL_ADDR: All problems detected by the script will be sent to
#                 this email address. The intention is for this to be
#                 the email address of the person running this script
#  SEND_MAIL_TO_PROJECT_MANAGER: 0 or 1. If 1 then any problems
#                 detected are sent to MY_EMAIL_ADDRESS and the
#                 project manager.
#----------------------------------------------------------------------
#SMTP_SERVER_NAME = 'outgoing.verizon.net'
#SMTP_SERVER_PORT = 25
#SMTP_SSL_SERVER = 0
#SMTP_USER_NAME = 'jpfasano'

SMTP_SERVER_NAME = 'smtp.gmail.com'
SMTP_SERVER_PORT = 587
SMTP_SSL_SERVER = 1
SMTP_USER_NAME = 'jpfasano _AT_ gmail _DOT_ com'
SMTP_PASSWORD_FILENAME = '/home/jp/bin/smtpPwFile'

SENDER_EMAIL_ADDR='jpfasano _AT_ verizon _DOT_ net'
MY_EMAIL_ADDR='jpfasano _AT_ us _DOT_ ibm _DOT_ com'
SEND_MAIL_TO_PROJECT_MANAGER=0
#SMTP_SERVER_NAME = 'gsbims.chicagogsb.edu'


#----------------------------------------------------------------------
# List of Projects to be processed by script
#----------------------------------------------------------------------
PROJECTS = ['CoinUtils','DyLP','Clp','SYMPHONY','Vol','Osi','Cgl','Cbc','Ipopt','OS','CppAD']
PROJECTS = ['Clp','CppAD']


