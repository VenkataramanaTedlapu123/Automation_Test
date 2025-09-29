import xml.etree.ElementTree as ET
import logging
from splunk_hec_handler import SplunkHecHandler

logger = logging.getLogger("pytests_demo")
logger.setLevel(logging.INFO)

handler = SplunkHecHandler(
    host="localhost",
    port=8088,
    token="YOUR_HEC_TOKEN",
    index="main",
    proto="http",
    verify=False,
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

    log_event = {
        "event": {
            "test_name": name,
            "class_name": classname,
            "status": status,
            "message": message
        }
    }
    logger.info(log_event)

print("Pytest results sent to Splunk successfully!")
