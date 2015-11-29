from rambutan3.check_args.annotation.OUTPUT_STREAM import OUTPUT_STREAM
from tests.check_args.annotation import RStreamTestUtil


def test():
    stream_test_tuple = RStreamTestUtil.create_stream_test_tuple()
    assert OUTPUT_STREAM.matches(stream_test_tuple.buffered_writer)
    assert not OUTPUT_STREAM.matches(stream_test_tuple.buffered_reader)
    assert OUTPUT_STREAM.matches(stream_test_tuple.writable_text_io_wrapper)
    assert not OUTPUT_STREAM.matches(stream_test_tuple.readable_text_io_wrapper)
