[logd://<name>]
* This is the macOS logd input component for the Splunk platform

* You can supply the following arguments, which are equivalent to the same arguments for the "log show" command on macOS:
logd-backtrace = <string>
logd-debug = <string>
logd-info = <string>
logd-loss = <string>
logd-signpost = <string>

* --predicate, Filters messages using the provided predicate based on NSPredicate. Only a single predicate is supported, but it can be a compound one.
logd-predicate = <string>

* The process on which to operate.  You can pass this option more than once to operate on multiple processes.
logd-process = <string>

* Include symbol names and source line numbers for messages, if available.
logd-source = <string>

* which fields to include
logd-include-fields = <string>

* which fields to exclude
logd-exclude-fields = <string>

* logd how often to query interval in secs
logd-interval = <string>

* logd starttime to query in fmt "YYYY-MM-DD HH:MM:SS"
logd-starttime = <string>

* reserved for future use
logd-freetext = <string>
