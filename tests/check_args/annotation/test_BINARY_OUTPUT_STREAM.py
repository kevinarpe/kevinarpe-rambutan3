from rambutan3.check_args.annotation.BINARY_OUTPUT_STREAM import BINARY_OUTPUT_STREAM
from tests.check_args.annotation import RStreamTestUtil


def test():
    stream_test_tuple = RStreamTestUtil.create_stream_test_tuple()
    assert BINARY_OUTPUT_STREAM.matches(stream_test_tuple.buffered_writer)
    assert not BINARY_OUTPUT_STREAM.matches(stream_test_tuple.buffered_reader)
    assert not BINARY_OUTPUT_STREAM.matches(stream_test_tuple.writable_text_io_wrapper)
    assert not BINARY_OUTPUT_STREAM.matches(stream_test_tuple.readable_text_io_wrapper)
