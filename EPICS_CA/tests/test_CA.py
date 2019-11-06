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

def test_connect():
    """Check that casput and caget work together"""
    PV_name = "TEST:TEST.VAL"
    casput(PV_name, 1)
    assert caget(PV_name) == 1


def test_disconnect():
    """Check that 'casdel' disconnects a PV"""
    PV_name = "TEST:TEST.VAL"
    casput(PV_name, 1)
    assert casget(PV_name) == 1
    assert caget(PV_name) == 1
    casdel(PV_name)
    assert casget(PV_name) is None
    from time import sleep
    sleep(1)
    assert caget(PV_name) is None
