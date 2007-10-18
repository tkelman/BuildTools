#! /usr/bin/env python

import os
import sys
from socket import gethostname 
import smtplib

import NBuserConfig
import NBprojectConfig
import NBlogMessages

#------------------------------------------------------------------------
#
# This file contains the functions that deal with email
#
#------------------------------------------------------------------------

#------------------------------------------------------------------------
# Send email typically about an error.
#  project: coin project name
#  cmd: command being exucuted. perhaps: "svn update", "./configure", 
#       "make".
#  cmdMsgs: the messages generated by cmd.  This will typically contain
#       errors issued by cmd.
#------------------------------------------------------------------------
def sendCmdMsgs(project,cmdMsgs,cmd):
  curDir = os.getcwd()
  
  toAddrs = [unscrambleAddress(NBuserConfig.MY_EMAIL_ADDR)]
  if NBprojectConfig.PROJECT_EMAIL_ADDRS.has_key(project) \
     and \
     NBuserConfig.SEND_MAIL_TO_PROJECT_MANAGER:
    scrambledEmailAddress=NBprojectConfig.PROJECT_EMAIL_ADDRS[project]
    unscrambledEmailAddress=unscrambleAddress(scrambledEmailAddress)
    toAddrs.append(unscrambledEmailAddress)

  subject = project + " problem when running '" + cmd +"'"

  emailMsg  = "'" + cmd + "' from directory " + curDir + " failed.\n\n"

  emailMsg += "Operating System: "+sys.platform+" "+os.name+"\n"
  emailMsg += "Host name: "+gethostname()+"\n"

  if os.environ.has_key("PROCESSOR_IDENTIFIER") :
    emailMsg += "Processor: "+os.environ["PROCESSOR_IDENTIFIER"]+"\n"
                                         
  if os.environ.has_key("NUMBER_OF_PROCESSORS") :
    emailMsg += "Number of processors: "+os.environ["NUMBER_OF_PROCESSORS"]+"\n"
    
  if os.environ.has_key("PATH") :
    emailMsg += "PATH: "+os.environ["PATH"]+"\n"

  emailMsg +="\n"

  emailMsg += "stderr messages are:\n" 
  emailMsg += cmdMsgs['stderr']
  emailMsg += "\n\nstdout messages are:\n"
  emailMsg += cmdMsgs['stdout']
  if cmdMsgs.has_key('config.log') :
    emailMsg += "\n\nconfig.log messages are:\n"
    emailMsg += cmdMsgs['config.log']
  send(toAddrs,subject,emailMsg)
  NBlogMessages.writeMessage( "  email sent regarding "+project+" running '"+cmd+"'" )

#------------------------------------------------------------------------
# Send email 
#------------------------------------------------------------------------
def send(toAddrs,subject,message):

  sender = unscrambleAddress(NBuserConfig.SENDER_EMAIL_ADDR)  
  msgWHeader = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n"
       % (sender, ", ".join(toAddrs), subject))
  msgWHeader += message
  
  # Get smpt server password
  if os.path.isfile(NBuserConfig.SMTP_PASSWORD_FILENAME) :
    pwFilePtr = open(NBuserConfig.SMTP_PASSWORD_FILENAME,'r')
    smtppass  = pwFilePtr.read().strip()
    #print smtppass
    pwFilePtr.close()
  else :
    NBlogMessages.writeMessage( "Failure reading pwFileName=" + NBuserConfig.SMTP_PASSWORD_FILENAME )
    sys.exit(1)
    
  session = smtplib.SMTP(NBuserConfig.SMTP_SERVER_NAME,NBuserConfig.SMTP_SERVER_PORT)
  #session.set_debuglevel(1)
  if NBuserConfig.SMTP_SSL_SERVER==1 :
    session.ehlo('x')
    session.starttls()
    session.ehlo('x')  
  session.login(unscrambleAddress(NBuserConfig.SMTP_USER_NAME),smtppass)

  rc = session.sendmail(sender,toAddrs,msgWHeader)
  if rc!={} :
    NBlogMessages.writeMessage( 'session.sendmail rc='  )
    NBlogMessages.writeMessage( rc )
  session.quit()

#------------------------------------------------------------------------
# Decrypt email address 
#------------------------------------------------------------------------
def unscrambleAddress( scrambledEmailAddress ) :
  retVal = scrambledEmailAddress
  retVal = retVal.replace(' _AT_ ','@')
  retVal = retVal.replace(' _DOT_ ','.')
  return retVal

