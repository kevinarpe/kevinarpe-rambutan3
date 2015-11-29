from rambutan3.check_args.annotation.BINARY_INPUT_STREAM import BINARY_INPUT_STREAM
from tests.check_args.annotation import RStreamTestUtil


def test():
    stream_test_tuple = RStreamTestUtil.create_stream_test_tuple()
    assert not BINARY_INPUT_STREAM.matches(stream_test_tuple.buffered_writer)
    assert BINARY_INPUT_STREAM.matches(stream_test_tuple.buffered_reader)
    assert not BINARY_INPUT_STREAM.matches(stream_test_tuple.writable_text_io_wrapper)
    assert not BINARY_INPUT_STREAM.matches(stream_test_tuple.readable_text_io_wrapper)
