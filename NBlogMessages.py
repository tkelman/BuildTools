#! /usr/bin/env python

#------------------------------------------------------------------------
# This file is distributed under the Common Public License.
# It is part of the BuildTools project in COIN-OR (www.coin-or.org)
#------------------------------------------------------------------------

import time

execfile('NBuserParametersDefault.py')
execfile('NBuserParameters.py')

#TODO: one could open the logfile once in the beginning, set it to sys.stdout, flush after each message, and close it finally

LOG_MESSAGES=''
FULL_LOG_MESSAGES=''

def clearMessages():
  global LOG_MESSAGES
  global FULL_LOG_MESSAGES
  FULL_LOG_MESSAGES+=LOG_MESSAGES
  LOG_MESSAGES=''

def getMessages():
  global LOG_MESSAGES
  return LOG_MESSAGES


def getAllMessages():
  global LOG_MESSAGES
  global FULL_LOG_MESSAGES
  retVal = FULL_LOG_MESSAGES+LOG_MESSAGES
  return retVal


#------------------------------------------------------------------------
# Function to write log messages
#------------------------------------------------------------------------
def writeMessage( msg ) :
  global LOG_MESSAGES
  logMsg = time.ctime(time.time())+': '
  logMsg += msg
  LOG_MESSAGES+=logMsg+'\n'
  if LOGPRINT :
    print logMsg
  if len(LOGFILE) > 0 and not LOGFILE.isspace() :
    logfile=open(NIGHTLY_BUILD_ROOT_DIR+'/'+LOGFILE, 'a')
    logfile.write(logMsg+'\n')
#    logfile.flush()
    logfile.close()
