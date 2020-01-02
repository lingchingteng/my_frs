from collections import deque


class MyVideoCaptureBase:
    def __init__(self, source):
        self.source = source
        self.observers = deque()

    def read(self):
        raise NotImplementedError("method read not implemented")

    def register(self, callback):
        try:
            callback({"status": "ok", "msg": "register successed"})
            self.observers.append(callback)
            return True
        except Exception:
            return False

    def unregister(self, callback):
        try:
            self.observers.remove(callback)
            callback({"status": "ok", "msg": "unregister successed"})
            return True
        except ValueError:
            try:
                callback({"status": "fail", "msg": "you are not registered"})
                return False
            except Exception:
                return False

    def notify(self, msg):
        for o in self.observers:
            try:
                o(msg)
            except Exception as e:
                print(e)
