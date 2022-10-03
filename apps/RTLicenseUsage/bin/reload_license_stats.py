# this module is required to setup an admin handler.
import os
import splunk.admin as admin
import splunk.entity as entity
import splunk.clilib.cli_common as comm

TARGET_LICENSE = "enterprise"
APPHOME = os.path.join(comm.splunk_home, "etc", "apps", "RTLicenseUsage")
OUTFILE = os.path.join(APPHOME, "default", "data", "ui", "views", "License_Usage.xml")
INFILE  = OUTFILE + ".template"

SEC = 86400

class TestHandler(admin.MConfigHandler):
  def setup(self):
     self.supportedArgs.addOptArg("license_quota")
#    pass

  def handleList(self, confInfo):
    x = entity.getEntity("/licenser/stacks", TARGET_LICENSE, sessionKey = self.getSessionKey())
    confInfo["quota"].append("license_quota", x["quota"])
    

  def handleEdit(self, confInfo):
    name = self.callerArgs.id
    args = self.callerArgs

    QUOTA = int(args["license_quota"][0])  

    QUOTA_KB = QUOTA    / 1024
    QUOTA_MB = QUOTA    / 1048576
    QUOTA_GB = QUOTA_MB / 1024

#	Change these as needed. If in the order of 100GB/day use quota_gb and quota_mb
#	If less, use quota_mb and quota_kb respectively

    QUOTA_STR     = "%d %d %d" % (0.45 * QUOTA_GB, 0.9 * QUOTA_GB, QUOTA_GB)
    CURR_THRU_STR = "%d %d %d %d" % (0.45 * QUOTA_KB / SEC, 0.9 * QUOTA_KB / SEC, QUOTA_KB / SEC, 1.5 * QUOTA_KB / SEC)
    PRED_QUOT_STR = "%d %d %d" % (0.45 * QUOTA_GB, 0.9 * QUOTA_GB, QUOTA_GB)
    TTL_QUOT_STR  = "%s %d" % (QUOTA_STR, 1.5 * QUOTA_GB)

    contents = open(INFILE, "r").read()
    
    contents = contents.replace("SUBST_LICENSE_QUOTA",       QUOTA_STR)
    contents = contents.replace("SUBST_CURRENT_THRUPUT",     CURR_THRU_STR)
    contents = contents.replace("SUBST_PRED_LICENSE_QUOTA",  PRED_QUOT_STR)
    contents = contents.replace("SUBST_TOTAL_LICENSE_QUOTA", TTL_QUOT_STR)
    
    open(OUTFILE, "w").write(contents)


admin.init(TestHandler, admin.CONTEXT_APP_ONLY)
