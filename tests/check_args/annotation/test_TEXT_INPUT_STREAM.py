from rambutan3.check_args.annotation.TEXT_INPUT_STREAM import TEXT_INPUT_STREAM
from tests.check_args.annotation import RStreamTestUtil


def test():
    stream_test_tuple = RStreamTestUtil.create_stream_test_tuple()
    assert not TEXT_INPUT_STREAM.matches(stream_test_tuple.buffered_writer)
    assert not TEXT_INPUT_STREAM.matches(stream_test_tuple.buffered_reader)
    assert not TEXT_INPUT_STREAM.matches(stream_test_tuple.writable_text_io_wrapper)
    assert TEXT_INPUT_STREAM.matches(stream_test_tuple.readable_text_io_wrapper)
