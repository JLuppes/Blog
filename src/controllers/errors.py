class ApiException(Exception):
    def __init__(self, msg, status_code):
        super().__init__(msg, status_code)
        if isinstance(msg, list):
            self.msg = msg
        else:
            self.msg = [msg]
        self.status_code = status_code

    def get_msgs(self):
        return ", ".join(self.msg)


def check_error(resp):
    # look for errors from Flask-Security API and throw exception with info
    jresp = resp.json()
    rdata = jresp.get("response")
    if not rdata:
        raise ApiException("Bad Api Response", resp.status_code)
    if "error" in rdata:
        raise ApiException(rdata["error"], resp.status_code)
    if "errors" in rdata:
        # these are form errors a dict of form label: [list of errors]
        msgs = []
        for label, emsgs in rdata["errors"].items():
            msgs.extend([f"{label}-{msg}" for msg in emsgs])
        raise ApiException(msgs, resp.status_code)
    if resp.status_code >= 400:
        raise ApiException("Error status w/o response", resp.status_code)
    return None