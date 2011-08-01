#
# This file is part of fimap and modified for umo application
#
# Author the original file:
# Copyright(c) 2009-2010 Iman Karim(ikarim2s@smail.inf.fh-brs.de).
# http://fimap.googlecode.com
#
# Modified by:
# Copyright(c) 2011-2012 JoseMi (jholgui@gmail.com) 
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

from xgoogle.search import GoogleSearch
from safebrowsing.query_lookup import Lookup
from malwareScan import malwareScan
import time,datetime,sys


__author__="JoseMi(jholgui (at) gmail.com)"
__date__ ="$28.07.2011 06:55:16$"

class googleScan:

    def __init__(self, config):
        self.config = config
        self.gs = GoogleSearch(self.config["p_query"], random_agent=True)
        self.gs.results_per_page = self.config["p_results_per_query"];
        self.cooldown = self.config["p_googlesleep"];
        if (self.config["p_skippages"] > 0):
            print "UMO Google Scanner will skip the first %d pages..."%(self.config["p_skippages"])


    def getNextPage(self):
        results = self.gs.get_results()
        return(results)

    def startGoogleScan(self):
        print "Querying Google Search: '%s' with max pages %d..."%(self.config["p_query"], self.config["p_pages"])

        pagecnt = 0
        curtry = 0
        enlaces = []
        last_request_time = datetime.datetime.now()

        while(pagecnt < self.config["p_pages"]):
            pagecnt = pagecnt +1
            redo = True
            while (redo):
              try:
                current_time = datetime.datetime.now()
                diff = current_time - last_request_time
                diff = int(diff.seconds)

                if (diff <= self.cooldown):
                    if (diff > 0): 
                        self.config["p_logger"].info("Commencing %ds google cooldown..." %(self.cooldown - diff))
                        time.sleep(self.cooldown - diff)
                    
                last_request_time = datetime.datetime.now()
                results = self.getNextPage()
                
                redo = False
              except KeyboardInterrupt:
                raise
              except Exception, err:
                print err
                redo = True
                self.config["p_logger"].error("[RETRYING PAGE %d]" %(pagecnt))
                curtry = curtry +1
                if (curtry > self.config["p_maxtries"]):
                    self.config["p_logger"].error("MAXIMAL COUNT OF (RE)TRIES REACHED!")
                    sys.exit(1)
                    
            curtry = 0
            if (len(results) == 0): break
            self.config["p_logger"].error("[PAGE %d]" %(pagecnt))
            try: 
                for r in results:
                    enlaces.append(r.url)
            except KeyboardInterrupt:
                raise
            time.sleep(1)
        
        enlaces_uniq = list(set(enlaces))
        self.config["p_enlaces"] = enlaces_uniq
        return self.config
        print "Google Scan completed, look at report: " + self.config["p_write"]