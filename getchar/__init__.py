import sys

if sys.platform == "win32":

    import msvcrt

    def _getchar() -> str | None:
        if msvcrt.kbhit():
            return chr(int.from_bytes(msvcrt.getch(), "big"))

    def _getkey() -> str | None:
        ch = _getchar()
        if ch is None:
            return ch
        # if it is a normal character, return it
        if ch not in "\x00\xe0":
            return ch
        # if it is a special key, read second half
        ch2 = _getchar()
        if ch2 is None:
            return ch
        return "\x00" + ch2

    def getkeys() -> list[str]:
        keys: list[str] = []
        key = _getkey()
        while key is not None:
            keys.append(key)
            key = _getkey()
        return keys

else:

    import os
    import select
    import termios
    import fcntl
    
    def getkeys() -> list[str]:
        fd = sys.stdin.fileno()
        old_term = termios.tcgetattr(fd)
        new_term = termios.tcgetattr(fd)
        new_term[3] = new_term[3] & ~(termios.ICANON | termios.ECHO)
        termios.tcsetattr(fd, termios.TCSANOW, new_term)
        old_flags = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, old_flags | os.O_NONBLOCK)
    
        try:
            chars: list[str] = []
            while True:
                r, w, x = select.select([sys.stdin], [], [], 0.0)
                if r:
                    key = os.read(fd, 1024).decode()
                    chars.append(key)
                else:
                    break
        finally:
            termios.tcsetattr(fd, termios.TCSAFLUSH, old_term)
            fcntl.fcntl(fd, fcntl.F_SETFL, old_flags)

        keys: list[str] = []

        while len(chars):
            c1 = chars.pop(0)

            if c1 != "\x1B" or len(chars) == 0:
                keys.append(c1)
                continue

            c2 = chars.pop(0)
            if c2 not in "\x4F\x5B":
                keys.append(c1 + c2)
                continue

            c3 = chars.pop(0)
            if c3 not in "\x31\x32\x33\x35\x36":
                keys.append(c1 + c2 + c3)
                continue

            c4 = chars.pop(0)
            if c4 not in "\x30\x31\x33\x34\x35\x37\x38\x39":
                keys.append(c1 + c2 + c3 + c4)
                continue

            c5 = chars.pop(0)
            keys.append(c1 + c2 + c3 + c4 + c5)

        return keys
