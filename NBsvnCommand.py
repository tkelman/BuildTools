#! /usr/bin/env python

#------------------------------------------------------------------------
# This file is distributed under the Common Public License.
# It is part of the BuildTools project in COIN-OR (www.coin-or.org)
#------------------------------------------------------------------------

import os
import urllib2
import re
import sys

import NBlogMessages
import NBemail
import NBosCommand

#------------------------------------------------------------------------
# Function for executing svn commands
#  svnCmd: String representing svn command
#  dir: Directory where command is to be run from
#  project: Coin project running the command (this is used to provide
#           a better message if an error is detected
#------------------------------------------------------------------------
def run(svnCmd,dir,project) :
  retVal='OK'
  os.chdir(dir)
  NBlogMessages.writeMessage('  Current directory: '+dir)
  NBlogMessages.writeMessage('  '+svnCmd)
  result = NBosCommand.run(svnCmd)
  if result['returnCode'] != 0 :
    NBemail.sendCmdMsgs(project,result,svnCmd)
    retVal='Error'
  return retVal


#------------------------------------------------------------------------
# Function which returns the latest stable version of a project
#------------------------------------------------------------------------
def latestStableVersion(project) :
  url='https://projects.coin-or.org/svn/'+project+'/stable'
  handle=urllib2.urlopen(url)
  html=handle.read()
  handle.close()

  # In html code find the latest version number
  #   <li><a href="3.2/">3.2/</a></li>
  #   <li><a href="3.3/">3.3/</a></li>
  r=r'<li><a href="(\d*\.\d*)/">(\d*\.\d*)/</a></li>'
  findResult=re.findall(r,html)
  if len(findResult)==0: return False
  latestStableVersionRepeated2Times = findResult[-1:][0]
  latestStableVersion=latestStableVersionRepeated2Times[0]
  return latestStableVersion

#------------------------------------------------------------------------
# Function which returns the latest release version of a project
# If there isn't a release version then False is returned
#------------------------------------------------------------------------
def latestReleaseVersion(project) :
  url='https://projects.coin-or.org/svn/'+project+'/releases'
  handle=urllib2.urlopen(url)
  html=handle.read()
  handle.close()

  # In html code find the latest version number
  #   <li><a href="1.6.0/">1.6.0/</a></li>
  r=r'<li><a href="(\d*\.\d*.\d*)/">(\d*\.\d*.\d*)/</a></li>'
  findResult=re.findall(r,html)
  if len(findResult)==0: return False
  latestReleaseVersionRepeated2Times = findResult[-1:][0]
  latestReleaseVersion=latestReleaseVersionRepeated2Times[0]
  return latestReleaseVersion


#------------------------------------------------------------------------
# Return svn revision number or url
# If not found the return -1
#------------------------------------------------------------------------
def svnRevision(url) :
  retVal=-1
  result = NBosCommand.run('svn info '+url)
  if result['returnCode']==0 :
    #reg=r'Revision: (\d+)'
    reg=r'Last Changed Rev: (\d+)'
    found=re.findall(reg,result['stdout'])
    if len(found)!=0 :
      retVal=int(found[0])
  return retVal
  

#------------------------------------------------------------------------
# newer(source, target)
# Return true if source and is more recently modified than target,
# (ie return true if source is newer than target and target needs
# to be rebuilt).
#
# If either sourrce or target don't exist then true is returned.
#
#------------------------------------------------------------------------
def newer(source,target) :

  #print '------------------------'
  #print source
  #print target
  #print '------------------------'
  #print ' '
  
  tarRev=svnRevision(target)
  if tarRev==-1 :
    # Target probably does not exist. It does not have an svn revision
    # nubmer, so return that it is out of date.
    return "Does not exist: "+target

  srcRev=svnRevision(source)
  if srcRev==-1 :
    # Source should exist. Something is wrong that will be caught
    # when an 'svn checkout' is done.
    return "Does not exist: "+source

  if srcRev>tarRev :
    return "New revision of: "+source

  # if there is an externals file then process it
  extFileName=os.path.join(target,"Externals")
  if os.path.isfile(extFileName) :
    extFilePtr = open(extFileName, "r")
    line = extFilePtr.readline()

    while line:
      line=line.strip()
      if line!='' :
        if line[0]!='#':
          reg=r'(\S+)(\s+)(\S+)'
          found=re.findall(reg,line)
          if len(found)!=1:
            # something is wrong. Do a rebuild
            return "Assumed out of date when reading: "+extFileName
          found=found[0]
          if len(found)!=3 :
            # something is wrong. Do a rebuild
            return "Assumed out of date when reading: "+extFileName
          extTarget=os.path.join(target,found[0])
          extSource=found[2]
          # Recursive call to see if external indicates rebuild
          msg=newer(extSource,extTarget) 
          if msg :
            extFilePtr.close()
            return msg
      line = extFilePtr.readline()

    extFilePtr.close()

  return False

