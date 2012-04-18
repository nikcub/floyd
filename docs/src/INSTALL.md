

# Usage

    $ cd /path/to/site
    $ floyd create
    [site created]
    $ floyd generate
    [site generated]
    $ floyd deploy appengine
    [site deployed] (in theory)

# Help

    $ floyd help

or for a command

    $ floyd help [command]


# Upgrading to the latest stable release

depends on your install method:

    $ pip install --upgrade floyd

    $ easy_install floyd

    $ git pull upstream
    $ python setup.py install

# Latest Development Branch

Using pip

    $ pip install -e git://github.com/nikcub/Floyd.git#egg=floyd

Or straight from the git repository:

    $ git clone git://github.com/nikcub/Floyd floyd
    $ cd floyd
    $ python setup.py install

# Google AppEngine Support

 * Download the [Google AppEngine SDK](http://code.google.com/appengine/downloads.html) for your platform and install it
 * Open the command line (Terminal in OS X, Command Prompt in Windows) and cd to the directory containing the generated site
 * Run: $ appcfg.py update .

# Safe Password Storage

If you have two-factor authentication activated with your Google ID, or you do not wish to store your Google password in configuration files (which is *strongly recommended*) then create a single-use password that is used in automatic deployments to Google App Engine from Floyd.

To do this:

1. Recommended: enable 2-step authentication by visiting the [Google Account](https://www.google.com/settings/) page and enabling the setting under 'Security' (switch '2-step verification' to on)
1. Generate an application specific password by going to the [Authorized Access Settings Page](https://accounts.google.com/b/0/IssuedAuthSubTokens)
1. Under the heading 'Application Specific Passwords' enter a name such as `floyd deploy` and generate a password
1. Store the generated password in your Floyd configuration file under `password` (spaces are not important, they are there for legibility)
