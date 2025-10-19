from tests.documents.attributes import ATTRIBUTES_TEST


def test_attributes(snapshot) -> None:
    assert ATTRIBUTES_TEST == snapshot
