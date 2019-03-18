import hashlib
import subprocess as sbp
import os
import pymzml
import time
import tempfile
import shutil

from pathlib import Path
from datetime import datetime

MARGIN = 0.1

tmp_dir = Path('./chem_spectra/tmp') # TBD

"""
docker run --name msconvert_docker \
    --rm -it \
    -e WINEDEBUG=-all \
    -v /Users/jason/workspace/python-project/chem-spectra-app/chem_spectra/tmp:/data \
    chambm/pwiz-skyline-i-agree-to-the-vendor-licenses bash
"""

class RawConverter():
    def __init__(self, file, params=False):
        self.fname = file.filename.split('.')[0]
        self.scan = params.get('scan', 0) if params else 0
        self.exact_mz = params.get('mass', 0) if params else 0
        self.bound_high = self.exact_mz + MARGIN
        self.bound_low = self.exact_mz - MARGIN
        self.target_dir, self.hash_str = self.__mk_dir(file)
        self.tf = self.__store_in_tmp(file)
        self.cmd_msconvert = self.__build_cmd_msconvert()
        self.__run_cmd()
        self.runs, self.spectrum = self.__read_mz_ml()
        self.xs, self.ys = self.__extract_xs_ys()
        self.datatable = self.__set_datatable()
        self.__clean()


    def __store_in_tmp(self, file):
        byteContent = file.stream.read()
        tf = tempfile.NamedTemporaryFile(
            prefix=self.fname,
            suffix='.RAW',
            dir=self.target_dir.absolute().as_posix()
        )
        with open(tf.name, 'w') as f:
            tf.write(byteContent)
        return tf


    def __mk_dir(self, file):
        hash_str = '{}{}'.format(datetime.now(), self.fname)
        hash_str = str.encode(hash_str)
        hash_str = hashlib.md5(hash_str).hexdigest()
        target_dir = tmp_dir / hash_str
        target_dir.mkdir(parents=True, exist_ok=True)
        return target_dir, hash_str


    def __build_cmd_msconvert(self):
        dk_img = 'chambm/pwiz-skyline-i-agree-to-the-vendor-licenses'
        cmd_msconvert = [
            'docker',
            'exec',
            '-d',
            'msconvert_docker',
            'wine',
            'msconvert',
            '/data/{}/{}'.format(self.hash_str, self.tf.name.split('/')[-1]),
            '-o',
            '/data/{}'.format(self.hash_str),
            '--ignoreUnknownInstrumentError'
        ]
        return cmd_msconvert


    def __run_cmd(self):
        sbp.run(self.cmd_msconvert)


    def __get_mzml_path(self):
        fname = ''.join(self.tf.name.split('/')[-1])
        fname = '.'.join(fname.split('.')[:-1])
        fname = '{}.mzML'.format(fname)
        mzml_path = self.target_dir / fname
        return mzml_path


    def __get_ratio(self, spc):
        match_xs, match_ys, all_ys, ratio = [], [], [], 0
        for pk in spc:
            all_ys.append(pk[1])
            if self.bound_low < pk[0] < self.bound_high:
                match_xs.append(pk[0])
                match_ys.append(pk[1])

        if len(match_xs) > 0:
            ratio = 100 * max(match_ys) / max(all_ys)

        return ratio


    def __decode(self, runs):
        spectrum, best_ratio = None, 0
        for idx, data in enumerate(runs):
            if self.scan:
                if idx + 1 == self.scan:
                    return data.peaks('raw')
                else:
                    continue

            spc = data.peaks('raw')
            if spectrum is None:
                spectrum = spc

            ratio = self.__get_ratio(spc)
            if best_ratio < ratio:
                best_ratio, spectrum = ratio, spc

        return spectrum


    def __read_mz_ml(self):
        mzml_path = self.__get_mzml_path()
        mzml_file = mzml_path.absolute().as_posix()

        runs, spectrum = None, None
        while True:
            if mzml_path.exists():
                try:
                    time.sleep(0.2)
                    runs = pymzml.run.Reader(mzml_file)
                    spectrum = self.__decode(runs)
                    break
                # except Exception as e: print(e)
                except:
                    pass
            else:
                time.sleep(0.1)

        return runs, spectrum


    def __extract_xs_ys(self):
        spc = self.spectrum
        return spc[:, 0], spc[:, 1]


    def __set_datatable(self):
        pts = self.xs.shape[0]
        datatable = []
        for idx in range(pts):
            datatable.append(
                '{}, {}\n'.format(
                    self.xs[idx],
                    self.ys[idx]
                )
            )
        return datatable


    def __clean(self):
        self.tf.close()
        shutil.rmtree(self.target_dir.absolute().as_posix())
