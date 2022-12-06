from hashlib import blake2b
import logging
import os
import sys

libpath = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(libpath, os.pardir, 'lib')]
import pan.xapi


class _MixinShared:
    @staticmethod
    def name(x, length):
        h = blake2b(x.encode(),
                    digest_size=length)
        return h.hexdigest()

    def xapi(self):
        tag = os.getenv('XAPI_TAG')
        if tag is None:
            raise RuntimeError('no XAPI_TAG in environment')
        kwargs = {'tag': tag}

        x = os.getenv('XAPI_DEBUG')
        if x is not None:
            debug = int(x)
            logger = logging.getLogger()
            if debug == 3:
                logger.setLevel(pan.xapi.DEBUG3)
            elif debug == 2:
                logger.setLevel(pan.xapi.DEBUG2)
            elif debug == 1:
                logger.setLevel(pan.xapi.DEBUG1)
            elif debug == 0:
                pass
            else:
                raise RuntimeError('XAPI_DEBUG level must be 0-3')

            log_format = '%(message)s'
            handler = logging.StreamHandler()
            formatter = logging.Formatter(log_format)
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return pan.xapi.PanXapi(**kwargs)


class Mixin(_MixinShared):
    def setUp(self):
        self.api = self.xapi()

    def tearDown(self):
        pass
