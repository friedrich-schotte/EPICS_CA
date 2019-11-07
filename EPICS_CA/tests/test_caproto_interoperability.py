import sys; sys.path.append("..")
try: from .. import CA
except ValueError: import CA
caget = CA.caget
caput = CA.caput

def install(module_name):
    from logging import warning
    try: 
        try: from pip import main as pipmain
        except ImportError: from pip._internal.main import main as pipmain
        pipmain(['install',module_name])
    except Exception as x: warning("caproto: %s" % x)

caproto_installed = False
try:
    import caproto.server
    caproto_installed = True
except: pass

if not caproto_installed: install('caproto')

try:
    import caproto.server
    caproto_installed = True
except: pass

from threading import Thread
server = Thread()

if caproto_installed:        
    
    from caproto.server import PVGroup, pvproperty, run
    from caproto import ChannelType

    class IOC(PVGroup):
        INTVAL = pvproperty(value=1)
        STRVAL = pvproperty(value="test",dtype=ChannelType.STRING)
        ##STRVAL = pvproperty(value="test",dtype=str) # bad idea: str maps to CHAR array not STRING

    ioc = IOC(prefix='TEST:TEST.')
    
    def run_server():
        import asyncio
        asyncio.set_event_loop(asyncio.new_event_loop())
        run(ioc.pvdb,module_name='caproto.asyncio.server')

    def start_server():
        from threading import Thread
        global server
        server = Thread(target=run_server,daemon=True)
        server.start()

    start_server()

##CA.DEBUG = True
##import logging
##logging.getLogger().setLevel(level=logging.DEBUG)
##logging.getLogger('caproto').setLevel(logging.WARNING)

##CA.timeout = 5
from time import sleep

def test_str():
    if server.is_alive():
        assert caget('TEST:TEST.STRVAL',timeout=5) == 'test'
        caput('TEST:TEST.STRVAL','new_value',wait=True,timeout=5)
        sleep(0.5)
        assert caget('TEST:TEST.STRVAL',timeout=5) == 'new_value'

def test_int():
    if server.is_alive():
        assert caget('TEST:TEST.INTVAL',timeout=5) == 1
        caput('TEST:TEST.INTVAL',2,wait=True,timeout=5)
        sleep(0.5)
        assert caget('TEST:TEST.INTVAL',timeout=5) == 2

