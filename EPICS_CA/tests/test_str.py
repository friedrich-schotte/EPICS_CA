import sys; sys.path.append("..")
try: from .. import CA
except ValueError: import CA
try: from .. import CAServer
except ValueError: import CAServer

caget = CA.caget
caput = CA.caput
casget = CAServer.casget
casput = CAServer.casput
casdel = CAServer.casdel

PV_name = "TEST:TEST_STR.STRVAL"
strval = "test"

def test_str():
    """Check that casput and caget work together"""
    casput(PV_name,strval)
    assert caget(PV_name) == strval

