#!/bin/sh

####################################
# This script processes the reports as a professionnal reporter
# Author : S. Afanou
# Date : June 2017
# email : afanousergio@gmail.com
####################################

echo "Python location"
which python
echo "Starting script gary reporter"
scriptdirectory="$(dirname "$0")"
echo Moving to script directory $scriptdirectory
cd $(dirname "$0")
echo Current directory is $(pwd)

appname=garyreporter
lockfilename=$appname_lockfile.lock

echo Checking if we must update the current code from github

git remote update
LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse @{u})
BASE=$(git merge-base @ @{u})

if [ $LOCAL = $REMOTE ]; then
    echo "Up-to-date"
elif [ $LOCAL = $BASE ]; then
    echo "Need to pull. Pulling ..."
    git pull --rebase
    echo "Done."
    echo "Activate the virtual env"
    . venv/bin/activate 
    echo "Installing new requirements"
    pip install -r requirements.txt
elif [ $REMOTE = $BASE ]; then
    echo "Need to push"
else
    echo "Diverged"
fi

echo "Display ps -af command without awk"
ps -af | grep $appname

echo "Display ps -af command with awk"
echo `ps -af | grep $appname | awk '{print $2}'`

echo "Display ps -af command and store in a variable"
#currentpid=$(ps -af | grep $appname | awk '$8 == "/bin/sh ./eepm_videos_processor.sh" {print $2}')
currentpid=$$
echo "Current pid $currentpid"
echo $currentpid

#lockfile $lockfilename -l

echo Checking the lock file ...
if [ -a $lockfilename ]; then
	echo Lock file exist.
	echo Checking if the process is still running ...

	lockfilepid=`cat $lockfilename`
	echo "lockfilepid is $lockfilepid"

	#ps aux | grep `cat $lockfilename` > /dev/null
	#if [ $? -eq 0 ]; then
	if [ "$currentpid" -eq "$lockfilepid" ]; then
		echo "Current pid $currentpid equals lockfilepid $lockfilepid"
		echo "Process is running ... Exiting ..."
	else
		echo "Current pid $currentpid NOT equals lockfilepid $lockfilepid"
	  	echo "Process is not running. This is a dead lock. Removing the lock file"
	    rm -f $lockfilename
	fi

else
	echo "Lock file doesn't exist. Executing the script ..."

	echo "Writing the pid of the current process to the file $lockfilename"
	#echo $(date) > $lockfilename
	#`ps -af | grep $appname | grep -v grep | awk '{print $2}'` > $lockfilename
	echo $currentpid > $lockfilename

	echo Here is the content of the lockfile
	cat $lockfilename
	echo "-------------------------------------------------"
	echo "---------- STARTING GARY'S JOB ------------------"
    echo "-------------------------------------------------"
	echo ""
    echo "Loading virtual environment"
    . venv/bin/activate

    echo "Starting the reporter job"
    garys_result=$(python process_my_articles.py)
    echo "Gary's report results : $garys_result"

    ## Collect some disk statistics on the server
	echo "-------------------------------------------------"
	echo "-------------- STATS COLLECTION -----------------"
    echo "-------------------------------------------------"
	echo "Disc space status"
    #df -ah

	echo "Anyways, let's delete the lock file to be able to execute the script again ... on the next call"
	echo Removing the lock file
	rm -f $lockfilename

fi

