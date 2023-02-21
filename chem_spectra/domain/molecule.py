from rdkit import Chem
from rdkit.Chem import Descriptors, AllChem, Draw, rdDepictor   # noqa: F401

from chem_spectra.lib.shared.buffer import store_str_in_tmp
from chem_spectra.controller.helper.file_container import FileContainer
import chem_spectra.lib.chem.ifg as ifg

class MoleculeModel:
    def __init__(self, molfile, layout=False, decorate=False):
        self.layout = layout
        self.decorate = decorate
        if isinstance(molfile, str):
            self.moltxt = molfile
        elif isinstance(molfile, FileContainer):
            self.moltxt = molfile.core
        else:
            self.moltxt = False

        self.mol = self.__set_mol()
        self.smi = self.__set_smi()
        self.mass = self.__set_mass()
        self.svg = self.__set_svg()

    def __decorate(self, mol):
        if self.layout == '1H':
            m_hyd = Chem.AddHs(mol)
            AllChem.Compute2DCoords(m_hyd)
            self.moltxt = Chem.MolToMolBlock(m_hyd)
            return m_hyd
        else:
            return mol

    def __set_mol(self):
        if not self.moltxt:
            return False
        tf = store_str_in_tmp(self.moltxt, suffix='.mol')
        mol = Chem.MolFromMolFile(tf.name)
        tf.close

        if self.decorate:
            mol = self.__decorate(mol)
        return mol

    def __set_smi(self):
        if not self.mol:
            return ''
        smi = Chem.MolToSmiles(self.mol, canonical=True)
        return smi

    def __set_mass(self):
        if not self.mol:
            return ''
        mass = Descriptors.ExactMolWt(self.mol)
        return str(round(mass, 3))

    def __set_svg(self):
        if not self.mol:
            return ''
        drawer = Draw.MolDraw2DSVG(300, 150)
        drawer.DrawMolecule(self.mol)
        drawer.FinishDrawing()
        svg = drawer.GetDrawingText().replace('svg:', '')
        return svg

    def __clear_mapnum(self, mol):
        [
            atom.ClearProp('molAtomMapNumber')
            for atom in mol.GetAtoms()
            if atom.HasProp('molAtomMapNumber')
        ]

    def fgs(self):
        fg_smas = []
        fgs = ifg.identify_functional_groups(self.mol)

        for fg in fgs:
            target = fg.type
            mol = Chem.MolFromSmarts(target)
            self.__clear_mapnum(mol)
            sma = Chem.MolToSmarts(mol)
            fg_smas.append(sma)

        return list(set(fg_smas))