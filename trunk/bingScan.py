#
# This file is part of umo application.
#
# Copyright(c) 2011-2012 JoseMi(jholgui (at) gmail.com).
# http://umo.googlecode.com
# http://twitter.com/JoseMiHolguin
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

from pybing.query import WebQuery
import umoconfig
import sys

__author__="JoseMi(jholgui (at) gmail.com)"
__date__ ="$28.06.2011 06:55:16$"

class bingScan:

    def __init__(self, config):
        self.config = config
        self.config["p_bingkey"] = getattr(umoconfig, 'bingkey')
        if (self.config["p_bingresults"] > 0):
            print "Bing Scanner will skip the first %d results..."%(self.config["p_bingresults"])


    def startBingScan(self):
 
        print "Querying Bing Search: '%s' with max Bing results %d..."%(self.config["p_query"], self.config["p_bingresults"])
        query = WebQuery(self.config["p_bingkey"], query=self.config["p_query"])
        results = query.execute()
        enlaces = []
        resultsbing = self.config["p_bingresults"]
        for result in results[:resultsbing]:
          enlaces.append(result.url)

        self.config["p_enlaces"] = enlaces

        if (len(enlaces) == 0): 
        	sys.stderr.write("Not results by bing search\n")
          sys.exit(0)
        try:
        return self.config
        except KeyboardInterrupt:
                raise
        print "Bing Scan completed."
