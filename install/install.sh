#!/bin/bash

PRESENT_WORKING=`pwd`
OS_VERSION=`cat /etc/issue | egrep [0-9] -o | head -1`
if [[ `uname -a | grep -o x86_64` == "x86_64" ]]; then
   ARCH="x86_64"
else
   ARCH="i386"
fi

echo "Checking to see if the EPEL repository is in place currently"
rpm -qa | grep epel
EPEL_INSTALLED=$?

if [[ $EPEL_INSTALLED != "0" ]]; then
   echo "EPEL not installed, installing now."
   rpm -Uvh http://download.fedora.redhat.com/pub/epel/$OS_VERSION/$ARCH/epel-release-5-3.noarch.rpm
fi

echo "Will you be using MySQL as a database backend? (the only option currently, this question is for future use. Waste of your time ftw"
MYSQL="TRUE"

if [[ $mysql == "yes" || $mysql == "y" || $mysql == "YES" || $mysql == "Y" || $mysql == "YeS" ]]; then
   MYSQL="TRUE"   
fi

echo "I will now proceed to install a selection of RPMs on your behalf. I will not force these out of kindness, so please press 'Y' to accept the downloads when yum prompts you."
if [[ $MYSQL == "TRUE" ]]; then
   yum install python-setuptools python-imaging python-imaging-devel python-twitter python-feedparser cronolog mod_wsgi django-tagging mysql-devel
else
   yum install python-setuptools python-imaging python-imaging-devel python-twitter python-feedparser cronolog mod_wsgi django-tagging
fi

echo "Now we'll need to collect some information from you to determine how to setup your blog for you. Please answer the following questions, and I'll complete the setup for you!"
echo "What is your GitHub username? (leave blank if you don't have one, and this feature will be disabled)"
read GITHUB_USER
echo "What is your Twitter username? (leave blank if you don't have one, and this feature will be disabled)"
read TWITTER_USER
if [ -z $TWITTER_USER ]; then
   TWITTER_PASS=""
else
   echo "What is your Twitter password? (This information is collected so you can auto-tweet new posts)"
   read TWITTER_PASS
fi
echo "Please enter your ReCaptcha (http://recaptcha.net/) PUBLIC key"
read RECAPTCHA_PUBLIC
echo "Please enter your ReCaptcha (http://recaptcha.net/) PRIVATE key"
read RECAPTCHA_PRIVATE
echo "Please enter your site's host name (i.e. 'www')"
read HOST_NAME
echo "Please enter your site's domain name (i.e. 'example.com')"
read DOMAIN_NAME

if [[ $MYSQL == "TRUE" ]]; then
   echo "Please enter your database name"
   read MYSQL_DB_NAME
   echo "Please enter your database password"
   read MYSQL_DB_PASSWORD
   echo "Please enter your MySQL host (leave blank if local)"
   read MYSQL_DB_HOST
   echo "Please enter your MySQL port (leave blank if default, unchanged, which is 3306)"
   read MYSQL_DB_PORT
fi


