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
   yum install python-setuptools python-imaging python-imaging-devel python-twitter python-feedparser cronolog mod_wsgi django-tagging python-simplejson mysql-devel
else
   yum install python-setuptools python-imaging python-imaging-devel python-twitter python-feedparser cronolog mod_wsgi django-tagging python-simplejson
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
echo "What would you like your site to be called (i.e. what would you like in the title bar)?"
read SITE_NAME

if [[ $MYSQL == "TRUE" ]]; then
   echo "Please enter your database name"
   read MYSQL_DB_NAME
   echo "Please enter your database user"
   read MYSQL_DB_USER
   echo "Please enter your database password"
   read MYSQL_DB_PASSWORD
   echo "Please enter your MySQL host (leave blank if local)"
   read MYSQL_DB_HOST
   echo "Please enter your MySQL port (leave blank if default, unchanged, which is 3306)"
   read MYSQL_DB_PORT
fi

echo "I'll now start the install (from source) of the python MySQL module that is required"
tar zxvf MySQL-python-1.2.2.tar.gz
cd MySQL-python-1.2.2; python setup.py build; python setup.py install
cd ..

echo "I'll now actually install django itself.."
easy_install django

echo "I'll now configure django_yaba"

# BEGIN THE SEDATHON!
cd ..
sed -i "s/GITHUB_USER_HOLDER/$GITHUB_USER/g" settings.py
sed -i "s/TWITTER_USER_HOLDER/$TWITTER_USER/g" settings.py
sed -i "s/TWITTER_PASS_HOLDER/$TWITTER_PASS/g" settings.py
sed -i "s/SITE_NAME_HOLDER/$SITE_NAME/g" settings.py
sed -i "s/URL_HOLDER/$HOST_NAME.$DOMAIN_NAME/g" settings.py
sed -i "s/PUBLIC_KEY_HOLDER/$RECAPTCHA_PUBLIC/g" settings.py
sed -i "s/PRIVATE_KEY_HOLDER/$RECAPTCHA_PRIVATE/g" settings.py
sed -i "s/DB_ENGINE_HOLDER/mysql/g" settings.py
sed -i "s/DB_NAME_HOLDER/$MYSQL_DB_NAME/g" settings.py
sed -i "s/DB_USER_HOLDER/$MYSQL_DB_USER/g" settings.py
sed -i "s/DB_PASS_HOLDER/$MYSQL_DB_PASSWORD/g" settings.py
sed -i "s/DB_HOST_HOLDER/$MYSQL_DB_HOST/g" settings.py
sed -i "s/DB_PORT_HOLDER/$MYSQL_DB_PORT/g" settings.py

# Now to setup Apache
echo "Starting the Apache setup"
mkdir -p /var/www/domains/$DOMAIN_NAME/$HOST_NAME/{logs,cgi-bin,ssl}
echo "Include vhosts.d/*.conf" >> /etc/httpd/conf.d/vhosts.conf
mkdir -p /etc/httpd/vhosts.d
cd ..
mv django-yaba django_yaba
mv django_yaba /var/www/domains/$DOMAIN_NAME/$HOST_NAME/
ln -s /var/www/domains/$DOMAIN_NAME/$HOST_NAME/django_yaba /var/www/domains/$DOMAIN_NAME/$HOST_NAME/htdocs
rsync -av /usr/lib/python*/site-packages/Django*/django/contrib/admin/media/ /var/www/domains/$DOMAIN_NAME/$HOST_NAME/django_yaba /var/www/domains/$DOMAIN_NAME/$HOST_NAME/htdocs/adminmedia
cp /var/www/domains/$DOMAIN_NAME/$HOST_NAME/django_yaba /var/www/domains/$DOMAIN_NAME/$HOST_NAME/htdocs/install/vhost_template /etc/httpd/vhosts.d/$HOST_NAME.$DOMAIN_NAME.conf
sed -i "s/HOST_NAME/$HOST_NAME/g" /etc/httpd/vhosts.d/$HOST_NAME.$DOMAIN_NAME.conf
sed -i "s/DOMAIN_NAME/$DOMAIN_NAME/g" /etc/httpd/vhosts.d/$HOST_NAME.$DOMAIN_NAME.conf
IP_ADDR=`ip addr | egrep "([0-9](.*)\.(.*)\.(.*)\.(.?)(.?)[0-9])" -o | egrep -v "(127|0.0.0.0)" | awk '{print $1}' | cut -d/ -f1`
apachectl -t

echo "Everything is now setup. You'll want to restart Apache at this time to pick up all of the changes"
echo "You should be able to hit your site via $IP_ADDR afterwards, or via http://$HOST_NAME.$DOMAIN_NAME assuming DNS is setup. The $IP_ADDR is an educated guess though, and depending on your setup may not work."
echo "Please enjoy django-yaba! You can email f4nt AT f4ntasmic DOT com with any issues, follow http://twitter.com/f4nt or visit www.f4ntasmic.com for updates as well. Also there's always the GitHub repo at http://github.com/f4nt/django-yaba/tree/master"
