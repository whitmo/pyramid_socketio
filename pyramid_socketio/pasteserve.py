from functools import partial
from gevent import reinit
from gevent.monkey import patch_all
from socketio import SocketIOServer


class ServerFactory(object):
    reinit = staticmethod(reinit)
    patch_all = staticmethod(partial(patch_all, dns=False))
    server_factory = SocketIOServer

    def __init__(self, global_conf, host, port, resource="socket.io", namespace='pyramid_socketio', patch=False):
        self.global_conf = global_conf
        self.host = host
        self.port = int(port)
        self.resource = resource
        self.namespace = namespace
        self.patch = patch

    def serve(self, app):
        self.reinit()
        if self.patch is True:
            self.patch_all()
        print "Serving on %s:%d (http://127.0.0.1:%d) ..." % (self.host, self.port, self.port)
        server = self.server_factory((self.host, self.port), app, resource=self.resource, namespace=self.namespace)
        server.serve_forever()

    __call__ = serve

server_factory_patched = partial(ServerFactory, patch=True)
