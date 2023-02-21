import pytest
from chem_spectra.controller.helper.file_container import FileContainer

source_dir_molfile = './tests/fixtures/source/molfile/c60h57fn4.mol'
source_dir_molfile_benzene = './tests/fixtures/source/molfile/benzene.mol'

@pytest.fixture
def invalid_molfile():
    return 'Just a normal text'

@pytest.fixture
def molfile_text():
    molfile = open(source_dir_molfile, "r")
    molfile_data = molfile.read()
    molfile.close()
    return molfile_data

@pytest.fixture
def molfile():
    molfile = open(source_dir_molfile, "r")
    molfile_str = molfile.read()
    molfile.close()
    molfile_data = FileContainer().from_str(molfile_str)
    return molfile_data

@pytest.fixture
def molfile_benzene():
    molfile = open(source_dir_molfile_benzene, "r")
    molfile_data = molfile.read()
    molfile.close()
    return molfile_data
