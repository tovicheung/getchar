"""Library to read characters (non-blocking)"""

from sys import platform

if platform.startswith(("linux", "darwin", "freebsd")):
    import sys
    import select
    import tty
    import termios
    def getchar():
        def isData():
            return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])
        old_settings = termios.tcgetattr(sys.stdin)
        c = None
        try:
            tty.setcbreak(sys.stdin.fileno())
            if isData():
                c = sys.stdin.read(1)
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
        return c
    
    
    def getkey() -> str:
        """Get a keypress. If an escaped key is pressed, the full sequence is
        read and returned as noted in `_posix_key.py`."""

        c1 = getchar()

        if c1 != "\x1B":
            return c1

        c2 = getchar()
        if c2 not in "\x4F\x5B":
            return c1 + c2

        c3 = getchar()
        if c3 not in "\x31\x32\x33\x35\x36":
            return c1 + c2 + c3

        c4 = getchar()
        if c4 not in "\x30\x31\x33\x34\x35\x37\x38\x39":
            return c1 + c2 + c3 + c4

        c5 = getchar()
        return c1 + c2 + c3 + c4 + c5


elif platform in ("win32", "cygwin"):
    import msvcrt
    def getchar():
        if msvcrt.kbhit():
            return chr(int.from_bytes(msvcrt.getch(), "big"))
        
    
    def getkey() -> str:
        """Reads the next keypress. If an escaped key is pressed, the full
        sequence is read and returned as noted in `_win_key.py`."""

        ch = getchar()

        if ch is None:
            return ch

        # if it is a normal character:
        if ch not in "\x00\xe0":
            return ch

        # if it is a scpeal key, read second half:
        ch2 = getchar()

        if ch2 is None:
            return ch

        return "\x00" + ch2


else:
    raise NotImplementedError(f"The platform {platform} is not supported yet")
