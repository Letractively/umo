#!/usr/bin/python

#
# This file is part of umo application.
#
# Copyright(c) 2011-2012 JoseMi(jholgui (at) gmail.com).
# http://umo.googlecode.com
# Twitter: @JoseMiHolguin
#
# This file may be licensed under the terms of of the
# GNU General Public License Version 2 (the ``GPL'').
#
# Software distributed under the License is distributed
# on an ``AS IS'' basis, WITHOUT WARRANTY OF ANY KIND, either
# express or implied. See the GPL for the specific language
# governing rights and limitations.
#
# You should have received a copy of the GPL along with this
# program. If not, go to http://www.gnu.org/licenses/gpl.html
# or write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#

## Requeriments:
## Lib xgoogle: http://www.catonmat.net/blog/python-library-for-google-search/
## Lib safebrowsing python: http://code.google.com/p/safebrowsing-python/
## Lib pybing: http://code.google.com/p/safebrowsing-python/

## Acknowledgements:
## Fimap project is thanked for being an inspiration and have made 
## possible the emergence of umo with some of your files and code.

#from safebrowsing.query_lookup import Lookup
from crawler import crawler
from googleScan import googleScan
from malwareScan import malwareScan
from bingScan import bingScan
import sys
import getopt
import umoconfig
import logging


__author__="JoseMi(jholgui (at) gmail.com)"
__date__ ="$21.06.2011 20:57:21$"
__version__ = "Beta 0.1"
config = {}

def show_help(AndQuit=False):
    print "Url Malware Owned (UMO): " + __version__
    print "Author: " + __author__
    print "Usage: ./umo.py [options]"
    print "## Operating Modes:"
    print "   -H , --harvest                Mode to harvest a URL recursivly for new URLs."
    print "   -g , --google                 Mode to use Google to aquire URLs."
    print "   -b , --bing                   Mode to use Bing to aquire URLs."
    print "   -s , --single                 Mode to use one single URL"
    print "## Variables:"
    print "   -u , --url=URL                The URL you want to test."
    print "                                 Needed in single mode (-s)."
    print "   -q , --query=QUERY            The Google Search QUERY."
    print "                                 Example: 'inurl:include.php'"
    print "        --skip-pages=X           Skip the first X pages from the Googlescanner."
    print "   -p , --pages=COUNT            Define the COUNT of pages to search (-g)."
    print "                                 Default is 10."
    print "        --results=COUNT          The count of results the Googlescanner should get per page."
    print "                                 Possible values Google: 10, 25, 50 or 100(default)."
    print "        --googlesleep=TIME       The time in seconds the Googlescanner should wait befor each"
    print "        --bingresults=COUNT      The count of results the bing scanner"
    print "        --bingkey=KEY      	    Key of API App Bing"
    print "                                 request to google. umo will count the time between two requests"
    print "   -d , --depth=CRAWLDEPTH       The CRAWLDEPTH (recurse level) you want to crawl your target site"
    print "                                 in harvest mode (-H). Default is 1."
    print "   -A , --user-agent=UA          The User-Agent which should be sent."
    print "   -h , --help                   Shows this cruft."
    print "## URL malware Analysis:"
    print "    --safebrowsing               Analysis URL with safebrowsing database."
    print "## Output modes"
    print "   -w , --write=RESULT           The RESULT URL's  with malware  will be written to file"
    print "## Update modules:" 
    print "   --update-safebrowsing         Update database malware and blacklist"
    print "## Version:" 
    print "   --version         	    Version of Url Malware Owned"
    print "## Examples:"
    print "  1. Scan a single URL with safebrowsing database:"
    print "        ./umo.py --safebrowsing -u -s 'http://localhost/test.htm' -w /tmp/malware_urls"
    print "  2. Scan Bing search results for detect malware with safebrowsing:"
    print "        ./umo.py --safebrowsing -b -q 'site:example.com' --bingresults=500 -w /tmp/malware_urls"
    print "  3. Scan Google search results for detect malware url with safebrowsing:"
    print "        ./umo.py --safebrowsing -g -q 'inurl:include.php' -w /tmp/malware_urls"
    print "  4. Crawling mode"
    print "        ./umo.py --safebrowsing -H -u 'http://localhost' -d 3 -w /tmp/malware_urls"
    print "  5. Update local safebrowsing database:"
    print "        ./umo.py --update-safebrowsing"
    if (AndQuit):
        sys.exit(0)


if __name__ == "__main__":
    config["p_url"] = None
    config["p_mode"] = None # 0=single ; 1=bing ;2=google ; 3=crawl
    config["p_useragent"] = getattr(umoconfig, 'user_agent')
    config["p_pages"] = getattr(umoconfig, 'pages')
    config["p_maxtries"] = getattr(umoconfig, 'maxtries')
    config["p_query"] = None
    config["p_write"] = getattr(umoconfig, 'malware')
    config["p_depth"] = getattr(umoconfig, 'depth')
    config["p_skippages"] = getattr(umoconfig, 'skippages') 
    config["p_results_per_query"] = getattr(umoconfig, 'results')
    config["p_googlesleep"] = getattr(umoconfig, 'googlesleep')
    config["p_bingresults"] = getattr(umoconfig, 'bingresults')
    config["p_bingkey"] = getattr(umoconfig, 'bingkey')
    config["p_safebrowsing"] = getattr(umoconfig, 'safebrowsing')
    config["p_updatesafebrowsing"] = getattr(umoconfig, 'updatesafebrowsing')
    config["p_enlaces"] = None
    config["p_umourls"] = getattr(umoconfig,'umourls')
    config["p_umolog"] = getattr(umoconfig,'umolog')
    
    # UMO logging
    
    logger = logging.getLogger('umo')
    hdlr = logging.FileHandler(getattr(umoconfig, 'umolog'))
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr) 
    logger.setLevel(logging.WARNING)
    config["p_logger"] = logger

if (len(sys.argv) == 1):
        print "Use -h for some help."
        print "./umo.py -h"
        sys.exit(0)

try:

        longSwitches = ["url="          , "help"       , "safebrowsing", "update-safebrowsing",
                        "user-agent="   , "query="      , "google"      , "bing"       , "pages=", 
                        "harvest"       , "write="     , "depth="      , "skip-pages=", "version",
                        "results="	, "googlesleep=", "bingkey="	, "bingresults",
                        ]
        optlist, args = getopt.getopt(sys.argv[1:], "u:msl:v:hA:gq:p:sxHw:d:bP:CIDTM:4R:", longSwitches)

        for k,v in optlist:
            if (k in ("-u", "--url")):
                config["p_url"] = v
            if (k in ("-s", "--single")):
                config["p_mode"] = 0
            if (k in ("-b", "--bing")):
                config["p_mode"] = 1
            if (k in ("-g", "--google")):
                config["p_mode"] = 2
            if (k in ("-H", "--harvest")):
                config["p_mode"] = 3
            if (k in ("-q", "--query")):
                config["p_query"] = v
            if (k in ("-p", "--pages")):
                config["p_pages"] = int(v)
            if (k in ("--results",)):
                config["p_results_per_query"] = int(v)
            if (k in ("--googlesleep",)):
                config["p_googlesleep"] = int(v)
            if (k in ("-A", "--user-agent")):
                config["p_useragent"] = v
            if (k in ("-w", "--write")):
                config["p_write"] = v
            if (k in ("-d", "--depth")):
                config["p_depth"] = int(v)
            if (k in ("-h", "--help")):
                show_help(True)
            if (k in ("--skip-pages",)):
                config["p_skippages"] = int(v)
            if (k in ("--bingresults",)):
                if int(v) > 999:
                    config["p_bingresults"] = 999
                else:
                    config["p_bingresults"] = int(v)
            if (k in ("--bingkey"),):
                config["p_bingkey"] = v
            if (k in ("--safebrowsing"),):
                config["p_safebrowsing"] = True
            if (k in ("--update-safebrowsing",)):
                config["p_updatesafebrowsing"] = True
            if (k in ("--version",)):
                print "Url Malware Owned (UMO): " + __version__
                print "Author: " + __author__
                sys.exit(0)

except getopt.GetoptError, err:
    config["logger"].error(err)
    sys.exit(1)

if (config["p_url"] == None and config["p_mode"] == 0):
    print "Target URL required. (-u)"
    sys.exit(1)
if (config["p_query"] == None and config["p_mode"] == 1):
    print "Bing Query required. (-q)"
    sys.exit(1)
if (config["p_query"] == None and config["p_mode"] == 2):
    print "Google Query required. (-q)"
    sys.exit(1)
if (config["p_url"] == None and config["p_mode"] == 3):
    print "Start URL required for harvesting. (-u)"
    sys.exit(1)
if (config["p_write"] == None and config["p_updatesafebrowsing"] == False):
    print "File output for results is required. (-w)"
    sys.exit(1)
if (config["p_bingkey"] == None and config["p_mode" == 1]):
    print "Bing key is required for Bing query mode (-bingkey=X)"
    sys.exit(1)
if (config["p_safebrowsing"] == None):
    print "Safebrowsing post analysis of URLs is necessary for UMO, not is only a crawler (--safebrowsing)"
    sys.exit(1)

try:
    
    if (config["p_updatesafebrowsing"] == True):
            m = malwareScan(config)
            m.update_sbg()
    elif (config["p_mode"] == 0):
        enlaces = []
        enlaces.append(config["p_url"])
        config["p_enlaces"] = enlaces
        m = malwareScan(config)
        m.scan_sbg()
    elif(config["p_mode"] == 1):
        g = bingScan(config)
        g.startBingScan()
        m = malwareScan(config)
        m.scan_sbg()
    elif(config["p_mode"] == 2):
        g = googleScan(config)
        #config = g.startGoogleScan()
        g.startGoogleScan()
        #m = malwareScan(config)
        #m.scan_sbg()
    elif(config["p_mode"] == 3):
        c = crawler(config)
        config["p_enlaces"] = c.crawl() 
        m = malwareScan(config)
        m.scan_sbg()
            

except KeyboardInterrupt:
        print "\n\n[ERROR] You have terminated UMO!"
        config["p_logger"].error('User finish umo application')

except Exception, err:
        print "[ERROR] Sorry, you have just found a bug!"
        print "[ERROR] If you are cool, send the following stacktrace to the bugtracker on http://umo.googlecode.com/"
        print "[ERROR]Please also provide the URL where umo crashed."
        raw_input("Push enter to see the error:")
        print "Exception: %s" %err
        config["p_logger"].error(err)
        raise
