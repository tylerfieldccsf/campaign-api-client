import uuid
from datetime import datetime
from models import *

id_arg = uuid.uuid4()
version = 0
creation_date = datetime.now()
last_update = datetime.now()
filing_activity_type = FilingActivityType.New
filing_specification_key = "filing:specification:key"
origin = "I come from the land down under"
origin_filing_id = "filing_101"
agency_id = "AHW"
apply_to_filing_id = None
publish_sequence = 25

address = "4E3FF207CBE1820E09BF8D061ACECF76C368D009FFEE929DCFECDA7FEF8348A8124586AC1148D9C0F99C9E91C09CC905E58AE01A5C23E6186914F07718ABF404"
filing_content_link = ContentLink(".Fppc460-PacInitial.cal", "text/vnd+netfile.cal+csv", ContentLinkType.Cafs, address)

flare_activity = FlareActivity(id_arg, version, creation_date, last_update, filing_activity_type, filing_specification_key,
                               origin, origin_filing_id, agency_id, apply_to_filing_id, publish_sequence)
