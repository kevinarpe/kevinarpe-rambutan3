from rambutan3.check_args.annotation.INPUT_STREAM import INPUT_STREAM
from tests.check_args.annotation import RStreamTestUtil


def test():
    stream_test_tuple = RStreamTestUtil.create_stream_test_tuple()
    assert not INPUT_STREAM.matches(stream_test_tuple.buffered_writer)
    assert INPUT_STREAM.matches(stream_test_tuple.buffered_reader)
    assert not INPUT_STREAM.matches(stream_test_tuple.writable_text_io_wrapper)
    assert INPUT_STREAM.matches(stream_test_tuple.readable_text_io_wrapper)
