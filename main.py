#!/usr/bin/python3
import os, sys, re, glob, json, zipfile, subprocess, base64, random
from ast import literal_eval

uuid = "c81119fa-8a42-46ba-8efc-677f555a57f9"
vlpath = f"/{uuid}-vl"
vmpath = f"/{uuid}-vm"
trpath = f"/{uuid}-tr"

core_name = "util.py"

zip_pwd = "123456".encode('utf8')
port, vlport, vmport, trport = \
    8080, random.randint(10000, 20000), \
    random.randint(20001, 30000), random.randint(30001, 40000)
_ = "eydsb2cnOiB7J2xvZ2xldmVsJzogJ25vbmUnfSwgJ291dGJvdW5kcyc6IFt7J3Byb3Rv" \
    "Y29sJzogJ2ZyZWVkb20nfV0sICdpbmJvdW5kcyc6IFt7J3BvcnQnOiBOb25lLCAncHJvd" \
    "G9jb2wnOiAndmxlc3MnLCAnc2V0dGluZ3MnOiB7J2NsaWVudHMnOiBbeydpZCc6IE5vbm" \
    "UsICdmbG93JzogJ3h0bHMtcnByeC1kaXJlY3QnfV0sICdkZWNyeXB0aW9uJzogJ25vbmU" \
    "nLCAnZmFsbGJhY2tzJzogW3sncGF0aCc6IE5vbmUsICdkZXN0JzogTm9uZX0sIHsncGF0" \
    "aCc6IE5vbmUsICdkZXN0JzogTm9uZX0sIHsncGF0aCc6IE5vbmUsICdkZXN0JzogTm9uZ" \
    "X1dfSwgJ3N0cmVhbVNldHRpbmdzJzogeyduZXR3b3JrJzogJ3RjcCd9fSwgeydwb3J0Jz" \
    "ogTm9uZSwgJ2xpc3Rlbic6ICcxMjcuMC4wLjEnLCAncHJvdG9jb2wnOiAndmxlc3MnLCA" \
    "nc2V0dGluZ3MnOiB7J2NsaWVudHMnOiBbeydpZCc6IE5vbmV9XSwgJ2RlY3J5cHRpb24n" \
    "OiAnbm9uZSd9LCAnc3RyZWFtU2V0dGluZ3MnOiB7J25ldHdvcmsnOiAnd3MnLCAnd3NTZ" \
    "XR0aW5ncyc6IHsncGF0aCc6IE5vbmV9fX0sIHsncG9ydCc6IE5vbmUsICdsaXN0ZW4nOi" \
    "AnMTI3LjAuMC4xJywgJ3Byb3RvY29sJzogJ3ZtZXNzJywgJ3NldHRpbmdzJzogeydjbGl" \
    "lbnRzJzogW3snaWQnOiBOb25lfV19LCAnc3RyZWFtU2V0dGluZ3MnOiB7J25ldHdvcmsn" \
    "OiAnd3MnLCAnc2VjdXJpdHknOiAnbm9uZScsICd3c1NldHRpbmdzJzogeydwYXRoJzogT" \
    "m9uZX19fSwgeydwb3J0JzogTm9uZSwgJ2xpc3Rlbic6ICcxMjcuMC4wLjEnLCAncHJvdG" \
    "9jb2wnOiAndHJvamFuJywgJ3NldHRpbmdzJzogeydjbGllbnRzJzogW3sncGFzc3dvcmQ" \
    "nOiBOb25lfV19LCAnc3RyZWFtU2V0dGluZ3MnOiB7J25ldHdvcmsnOiAnd3MnLCAnc2Vj" \
    "dXJpdHknOiAnbm9uZScsICd3c1NldHRpbmdzJzogeydwYXRoJzogTm9uZX19fV19"
if __name__ == '__main__':
    dic = literal_eval(base64.b64decode(_.encode('utf8')).decode('utf8'))
    dic["inbounds"][0]["port"] = port
    dic["inbounds"][0]["settings"]["clients"][0]["id"] = uuid
    dic["inbounds"][0]["settings"]["fallbacks"][0]["path"] = vlpath
    dic["inbounds"][0]["settings"]["fallbacks"][0]["dest"] = vlport
    dic["inbounds"][0]["settings"]["fallbacks"][1]["path"] = vmpath
    dic["inbounds"][0]["settings"]["fallbacks"][1]["dest"] = vmport
    dic["inbounds"][0]["settings"]["fallbacks"][2]["path"] = trpath
    dic["inbounds"][0]["settings"]["fallbacks"][2]["dest"] = trport
    dic["inbounds"][1]["port"] = vlport
    dic["inbounds"][1]["settings"]["clients"][0]["id"] = uuid
    dic["inbounds"][1]["streamSettings"]["wsSettings"]["path"] = vlpath
    dic["inbounds"][2]["port"] = vmport
    dic["inbounds"][2]["settings"]["clients"][0]["id"] = uuid
    dic["inbounds"][2]["streamSettings"]["wsSettings"]["path"] = vmpath
    dic["inbounds"][3]["port"] = trport
    dic["inbounds"][3]["settings"]["clients"][0]["password"] = uuid
    dic["inbounds"][3]["streamSettings"]["wsSettings"]["path"] = trpath
    zfile = glob.glob(os.path.join(os.getcwd(), "*.zip"))
    if len(zfile) > 0:
        zfile = zfile[0]
        with zipfile.ZipFile(zfile) as z:
            for i in z.namelist():
                if not re.search(r"[xX]{1,}[rR]{1,}[aA]{1,}[yY]{1,}$", i): continue
                with open(os.path.join(os.getcwd(), core_name), 'wb') as c:
                    c.write(z.read(i, pwd=zip_pwd))
        os.remove(zfile)
    os.chmod(os.path.join(os.getcwd(), core_name), 0o777, )
    subprocess.run([os.path.join(os.getcwd(), core_name), base64.b64decode(b"cnVu").decode('utf8')],
                   stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                   input=json.dumps(dic, separators=(',', ':'), indent=2).encode('utf8'))
    print("bye~")
    sys.exit(0)
