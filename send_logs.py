import logging
from splunk_hec_handler import SplunkHecHandler

# Configure logger
logger = logging.getLogger("pytest_demo")
logger.setLevel(logging.INFO)

# Splunk HEC handler with sourcetype
handler = SplunkHecHandler(
    host="localhost",
    port=8088,
    token="4ce43004-99c0-4339-8af2-9e657cecfb99",
    index="main",              # Must exist in Splunk
    proto="http",              # HTTP for local dev
    verify=False,              # Disable SSL check for local dev
    sourcetype="pytests_demo"  # <-- Added this
)
logger.addHandler(handler)

# Send logs as plain strings
logger.info("Test log event from send_logs.py")

for i in range(1, 6):
    logger.info(f"Test log #{i} from Python")

print("Logs sent to Splunk HEC successfully!")
