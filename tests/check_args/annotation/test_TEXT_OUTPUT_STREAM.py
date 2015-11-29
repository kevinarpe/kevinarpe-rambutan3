from rambutan3.check_args.annotation.TEXT_OUTPUT_STREAM import TEXT_OUTPUT_STREAM
from tests.check_args.annotation import RStreamTestUtil


def test():
    stream_test_tuple = RStreamTestUtil.create_stream_test_tuple()
    assert not TEXT_OUTPUT_STREAM.matches(stream_test_tuple.buffered_writer)
    assert not TEXT_OUTPUT_STREAM.matches(stream_test_tuple.buffered_reader)
    assert TEXT_OUTPUT_STREAM.matches(stream_test_tuple.writable_text_io_wrapper)
    assert not TEXT_OUTPUT_STREAM.matches(stream_test_tuple.readable_text_io_wrapper)
