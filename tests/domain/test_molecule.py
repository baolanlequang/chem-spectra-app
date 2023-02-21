import pytest
from rdkit.Chem import Mol
from chem_spectra.domain.molecule import MoleculeModel

def test_init_molecule_model_without_molfile():
    molecule = MoleculeModel(molfile=None)
    assert molecule.mol is False
    assert molecule.layout is False
    assert molecule.decorate  is False

def test_init_molecule_model_with_invalid_molfile(invalid_molfile):
    molecule = MoleculeModel(molfile=invalid_molfile)
    assert molecule.moltxt == invalid_molfile
    assert molecule.mol is None

def test_init_molecule_model_with_molfile_text(molfile_text):
    molecule = MoleculeModel(molfile=molfile_text)
    assert molecule.moltxt == molfile_text
    assert isinstance(molecule.mol, Mol)

def test_init_molecule_model_with_molfile(molfile_text, molfile):
    molecule = MoleculeModel(molfile=molfile)
    assert molecule.moltxt == molfile_text
    assert isinstance(molecule.mol, Mol)

def test_molecule_model_set_mol(molfile):
    molecule = MoleculeModel(molfile=molfile)
    mol = molecule._MoleculeModel__set_mol()
    assert mol is not None
    assert isinstance(mol, Mol)

def test_molecule_model_decorate_mol_non_1H(molfile):
    molecule = MoleculeModel(molfile=molfile)
    mol = molecule._MoleculeModel__set_mol()
    decorated_mol = molecule._MoleculeModel__decorate(mol)
    assert isinstance(mol, Mol)
    assert decorated_mol == mol

def test_molecule_model_decorate_mol_1H(molfile):
    molecule = MoleculeModel(molfile=molfile, layout='1H')
    mol = molecule._MoleculeModel__set_mol()
    decorated_mol = molecule._MoleculeModel__decorate(mol)
    assert isinstance(mol, Mol)
    assert decorated_mol != mol

def test_molecule_model_set_smile(molfile_benzene):
    molecule = MoleculeModel(molfile=molfile_benzene)
    smi = molecule._MoleculeModel__set_smi()
    assert smi == 'c1ccccc1'
    assert molecule.smi == smi

def test_molecule_model_set_mass(molfile_benzene):
    molecule = MoleculeModel(molfile=molfile_benzene)
    mass = molecule._MoleculeModel__set_mass()
    assert mass == '78.047'    # REF: https://www.genome.jp/entry/C01407
    assert molecule.mass == mass

def test_molecule_model_set_svg(molfile_benzene):
    molecule = MoleculeModel(molfile=molfile_benzene)
    svg = molecule._MoleculeModel__set_svg()
    assert '</svg>' in svg
    assert molecule.svg == svg

def test_molecule_model_clear_atom_map_number(molfile):
    molecule = MoleculeModel(molfile=molfile)
    molecule._MoleculeModel__clear_mapnum(molecule.mol)
    atoms = molecule.mol.GetAtoms()
    for atom in atoms:
        assert atom.HasProp('molAtomMapNumber') is 0

def test_molecule_model_fgs(molfile):
    molecule = MoleculeModel(molfile=molfile)
    fgs = molecule.fgs()
    assert isinstance(fgs, list)
