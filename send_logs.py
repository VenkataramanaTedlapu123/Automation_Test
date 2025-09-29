import os
import xml.etree.ElementTree as ET
import logging
from splunk_hec_handler import SplunkHecHandler

# ------------------------------
# Configurable Settings
# ------------------------------
SPLUNK_HOST = os.getenv("SPLUNK_HOST", "localhost")
SPLUNK_PORT = int(os.getenv("SPLUNK_PORT", 8088))
SPLUNK_TOKEN = os.getenv("SPLUNK_TOKEN", "4ce43004-99c0-4339-8af2-9e657cecfb99")
SPLUNK_INDEX = os.getenv("SPLUNK_INDEX", "main")
SPLUNK_PROTO = os.getenv("SPLUNK_PROTO", "http")  # "http" or "https"
SPLUNK_VERIFY = os.getenv("SPLUNK_VERIFY", "False").lower() in ("true", "1")  # SSL cert verify
SOURCE_TYPE = os.getenv("SPLUNK_SOURCETYPE", "pytests_demo")

# Path to pytest XML report
REPORT_PATH = os.path.join(os.getcwd(), "reports", "junit-report.xml")
if not os.path.exists(REPORT_PATH):
    raise FileNotFoundError(f"Pytest report not found: {REPORT_PATH}")

# ------------------------------
# Setup Logger
# ------------------------------
logger = logging.getLogger("pytests_demo")
logger.setLevel(logging.INFO)

handler = SplunkHecHandler(
    host=SPLUNK_HOST,
    port=SPLUNK_PORT,
    token=SPLUNK_TOKEN,
    index=SPLUNK_INDEX,
    proto=SPLUNK_PROTO,
    verify=SPLUNK_VERIFY,
    sourcetype=SOURCE_TYPE
)
logger.addHandler(handler)

# ------------------------------
# Parse pytest XML & Send Logs
# ------------------------------
tree = ET.parse(REPORT_PATH)
root = tree.getroot()

for testcase in root.iter("testcase"):
    name = testcase.attrib.get("name")
    classname = testcase.attrib.get("classname")
    status = "passed"

    if testcase.find("failure") is not None:
        status = "failed"
    elif testcase.find("error") is not None:
        status = "error"

    log_msg = f"{classname}.{name} - {status}"
    try:
        logger.info(log_msg)
    except Exception as e:
        print(f"Failed to send log to Splunk: {e}")

print("Pytest results sent to Splunk successfully!")
