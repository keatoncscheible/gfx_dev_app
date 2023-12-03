import shutil
from pathlib import Path

import pytest

from pyfx.audio_processor import AudioProcessor
from pyfx.exceptions import InvalidRootPedalFolderError
from pyfx.pedal_builder.pedal_builder import PedalBuilder


@pytest.fixture
def pedal_builder_fixture(request):
    root_pedal_folder = request.param
    return lambda: PedalBuilder(
        root_pedal_folder=root_pedal_folder,
        audio_processor=AudioProcessor(),
    )


@pytest.fixture
def default_pedal_builder_fixture(request):
    root_pedal_folder = Path("./tests/pedals")

    def finalizer():
        shutil.rmtree(root_pedal_folder)

    # Register the finalizer to run after the test
    request.addfinalizer(finalizer)

    yield PedalBuilder(
        root_pedal_folder=root_pedal_folder,
        audio_processor=AudioProcessor(),
    )


@pytest.mark.parametrize("pedal_builder_fixture", [None], indirect=True)
def test_pedal_builder_invalid_root_folder(pedal_builder_fixture):
    with pytest.raises(InvalidRootPedalFolderError):
        _ = pedal_builder_fixture()


@pytest.mark.parametrize("pedal_builder_fixture", ["./test/pedals", Path("./test/pedals")], indirect=True)
def test_pedal_builder_valid_root_folder(pedal_builder_fixture):
    try:
        _ = pedal_builder_fixture()
    except InvalidRootPedalFolderError:
        pytest.fail("InvalidRootPedalFolderError raised unexpectedly")


def test_create_new_pedal(default_pedal_builder_fixture):
    pedal_builder: PedalBuilder = default_pedal_builder_fixture
    pedal_builder.create_new_pedal()
    assert pedal_builder.root_pedal_folder.exists()
