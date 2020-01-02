from MyVideoCapture.MyVideoCaptureBase import MyVideoCaptureBase


def test_MyVideoCapture():

    vb = MyVideoCaptureBase("source")

    # Test: register uncallable
    assert not vb.unregister("ff")

    # Test: test normal flow
    def callback1(msg):
        print("This is callback1:", msg)

    vb.register(callback1)

    vb.notify("hello")

    assert vb.unregister(callback1)

    # Test: unregister didn't register
    def callback2(msg):
        print("This is callback2:", msg)

    assert not vb.unregister(callback2)

    # Test: unregister uncallable
    assert not vb.register("a")
