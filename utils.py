import json
import datetime
def json_log(d: dict):
    x = {"timestamp": datetime.datetime.utcnow().isoformat()+"Z"}
    x.update(d)
    return json.dumps(x)
