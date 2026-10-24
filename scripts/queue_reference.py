"""Separate directed calibration only; never supplied to model prompts."""


def actions():
    def a(reset_n=1, clear=0, enable=1, write=0, read=0, data=0):
        return dict(reset_n=reset_n, clear=clear, enable=enable,
                    write=write, read=read, data=data)
    return [
        a(write=1, data=0x00000001), a(write=1, data=0x80000000),
        a(write=1, data=0xaaaaaaaa), a(write=1, read=1, data=0x55555555),
        a(read=1), a(read=1), a(read=1),
        a(write=1, read=1, data=0xf0f0f0f0),
        a(enable=0, write=1, read=1, data=0xffffffff),
        a(write=1, data=0x12345678), a(write=1, data=0x87654321),
        a(clear=1, enable=1), a(write=1, data=0xffffffff),
        a(reset_n=0, enable=0), a(enable=0), a(),
    ]
