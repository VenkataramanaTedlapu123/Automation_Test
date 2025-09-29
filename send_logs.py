import xml.etree.ElementTree as ET
import logging
from splunk_hec_handler import SplunkHecHandler

logger = logging.getLogger("pytests_demo")
logger.setLevel(logging.INFO)

# Splunk HEC handler (JSON over HTTPS)
handler = SplunkHecHandler(
    host="127.0.0.1",        # Use actual host
    port=8088,
    token="4ce43004-99c0-4339-8af2-9e657cecfb99",
    index="main",
    proto="https",            # HTTPS
    verify=False,             # Set True if you have cert
    sourcetype="pytests_demo"
)
logger.addHandler(handler)

# Parse pytest XML
tree = ET.parse("reports/junit-report.xml")
root = tree.getroot()

for testcase in root.iter("testcase"):
    name = testcase.attrib.get("name")
    classname = testcase.attrib.get("classname")
    status = "passed"
    message = ""

    if testcase.find("failure") is not None:
        status = "failed"
        message = testcase.find("failure").text
    elif testcase.find("error") is not None:
        status = "error"
        message = testcase.find("error").text

    # Send as JSON
    log_event = {
        "event": {
            "test_name": name,
            "class_name": classname,
            "status": status,
            "message": message
        }
    }

    try:
        logger.info(log_event)
    except Exception as e:
        print(f"Failed to send log to Splunk: {e}")

print("Pytest results sent to Splunk successfully!")
