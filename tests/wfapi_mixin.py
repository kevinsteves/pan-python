import logging
import os
import sys

libpath = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(libpath, os.pardir, 'lib')]
import pan.wfapi


class _MixinShared:
    def wfapi(self):
        tag = os.getenv('WFAPI_TAG')
        if tag is None:
            raise RuntimeError('no WFAPI_TAG in environment')
        kwargs = {'tag': tag}

        x = os.getenv('WFAPI_DEBUG')
        if x is not None:
            debug = int(x)
            logger = logging.getLogger()
            if debug == 3:
                logger.setLevel(pan.wfapi.DEBUG3)
            elif debug == 2:
                logger.setLevel(pan.wfapi.DEBUG2)
            elif debug == 1:
                logger.setLevel(pan.wfapi.DEBUG1)
            elif debug == 0:
                pass
            else:
                raise RuntimeError('WFAPI_DEBUG level must be 0-3')

            log_format = '%(message)s'
            handler = logging.StreamHandler()
            formatter = logging.Formatter(log_format)
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return pan.wfapi.PanWFapi(**kwargs)


class Mixin(_MixinShared):
    def setUp(self):
        self.api = self.wfapi()

    def tearDown(self):
        pass
