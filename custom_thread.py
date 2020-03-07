import threading

class BaseThread(threading.Thread):
    def __init__(self, target_args=None, callback=None, callback_args=None, *args, **kwargs):
        target = kwargs.pop('target')
        super(BaseThread, self).__init__(target=self.target_with_callback, *args, **kwargs)
        self.target_args = target_args
        self.callback = callback
        self.method = target
        self.callback_args = callback_args

    def target_with_callback(self):
        result = self.method(*self.target_args)
        if self.callback is not None:
            self.callback(*self.callback_args, result)