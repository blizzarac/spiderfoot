#-------------------------------------------------------------------------------
# Name:         sfp_stor_db
# Purpose:      SpiderFoot plug-in for storing events to the local SpiderFoot
#               SQLite database.
#
# Author:      Steve Micallef <steve@binarypool.com>
#
# Created:     14/05/2012
# Copyright:   (c) Steve Micallef 2012
# Licence:     GPL
#-------------------------------------------------------------------------------

import sys
import re
from sflib import SpiderFoot, SpiderFootPlugin

# SpiderFoot standard lib (must be initialized in setup)
sf = None
sfdb = None

class sfp__stor_db(SpiderFootPlugin):
    """Storage:Stores scan results into the back-end SpiderFoot database. You will need this."""

    # Default options
    opts = {
        'maxstorage':   1024 # max bytes for any piece of info stored (0 = unlimited)
    }

    # Option descriptions
    optdescs = {
        'maxstorage':   "Maximum bytes to store for any piece of information retreived (0 = unlimited.)"
    }

    def setup(self, sfc, target, userOpts=dict()):
        global sf
        global sfdb

        sf = sfc

        for opt in userOpts.keys():
            self.opts[opt] = userOpts[opt]

        # Use the database handle passed to us
        # Should change to get the DBH out of sfc
        sfdb = userOpts['__sfdb__']

    # What events is this module interested in for input
    # Because this is a storage plugin, we are interested in everything so we
    # can store all events for later analysis.
    def watchedEvents(self):
        return ["*"]

    # Handle events sent to this module
    def handleEvent(self, sfEvent):
        if self.opts['maxstorage'] != 0:
            if len(sfEvent.data) > self.opts['maxstorage']:
                sf.debug("Storing an event: " + sfEvent.eventType)
                sfdb.scanEventStore(self.opts['__guid__'], sfEvent, self.opts['maxstorage'])
                return None
        
        sf.debug("Storing an event: " + sfEvent.eventType)
        sfdb.scanEventStore(self.opts['__guid__'], sfEvent)


# End of sfp__stor_db class
