# tiny-chess — entrypoint.
#
# The engine ships as an lzma-compressed payload in engine.lzma
# (3,927 bytes): its minified source is 10,614 bytes, far over the
# 4,096-byte per-file limit, and the rules expressly allow an lzma
# payload plus its unpacker. This loader is the unpacker: it
# decompresses the payload and executes it in this module's own
# namespace, exactly as if the engine source were written here.
import lzma
import os

_HERE = os.path.dirname(os.path.abspath(__file__))

def _load_engine() -> bytes:
    """Read and decompress the engine payload shipped beside this file."""
    with open(os.path.join(_HERE, "engine.lzma"), "rb") as f:
        return lzma.decompress(f.read())


# Execute the engine in this module's namespace: names it defines
# (the board, the search, the protocol client) become this module's
# own, and __name__ is "__main__" exactly when run as the entrypoint.
exec(compile(_load_engine(), "engine.py", "exec"), globals())
