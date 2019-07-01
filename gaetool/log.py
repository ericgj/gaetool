import sys
from logging import DEBUG, INFO, ERROR
from datetime import datetime

class FakeTerminal():
    does_styling = False

try:
    from blessings import Terminal
    T = Terminal(stream=sys.stderr)
except:
    T = FakeTerminal()


class Log():

    def __init__(self, level=INFO):
        self.level = level

    def __call__(self, msg, **kw):
        return LogContext(self.level, msg, kw)


class LogContext():

    def __init__(self, level, msg, args={}):
        self.level = level
        self._msg = msg
        self._args = args

    def __enter__(self):
        if self.level <= DEBUG:
            fmt = (
                "{t.yellow}•{t.normal} {msg} ({args})" if T.does_styling else
                "{timestamp:%Y-%m-%dT%H:%M:%S}   {msg} ({args})"
            )
            print( fmt.format(
                msg=self._msg, 
                args=", ".join([ "%s=%s" % (k,v) for k,v in self._args.items() ]),
                t=T,
                timestamp=datetime.now()
            ), file=sys.stderr)

        if self.level <= INFO:
            fmt = (
                "{t.yellow}•{t.normal} {msg}{t.move_up}" if T.does_styling else
                "{timestamp:%Y-%m-%dT%H:%M:%S}   {msg}"
            )
            print( fmt.format(
                msg=self._msg, 
                t=T,
                timestamp=datetime.now()
            ), file=sys.stderr)
            

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            if self.level <= INFO:
                fmt = (
                    "{t.green}✓ {msg}{t.normal}" if T.does_styling else
                    "{timestamp:%Y-%m-%dT%H:%M:%S} = {msg}"
                )
                print( fmt.format(
                    msg=self._msg,
                    t=T,
                    timestamp=datetime.now()
                ), file=sys.stderr)

            return True

        else:
            if self.level <= ERROR:
                fmt = (
                    "{t.red}✕ {msg}{t.normal}" if T.does_styling else
                    "{timestamp:%Y-%m-%dT%H:%M:%S} X {msg}"
                )
                print( fmt.format(
                    msg=self._msg,
                    t=T,
                    timestamp=datetime.now()
                ), file=sys.stderr)

            return False


if __name__ == '__main__':
    from time import sleep
    log = Log( INFO )

    with log("testing success"):
        sleep(3)

    with log("testing failure"):
        sleep(3)
        assert (1 == 0)



