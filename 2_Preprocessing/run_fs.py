import argparse
import subprocess
import multiprocessing as mp
from pathlib import Path


BASE_DIR: Path
NONREG_PATH: list
FS_DIR: Path

def run_fs(fname: str):
    stem = fname.stem

    # Run Fastsurfer
    try:
        subprocess.call(["./run_fastsurfer.sh",
                         "--t1", fname,
                         "--sd", BASE_DIR / "seg",
                         "--sid", stem,
                         "--seg_only", "--allow_root",
                         "--threads", "8", "--device", "cuda"], cwd=FS_DIR)
        subprocess.call(["rm", BASE_DIR / f"tmp_nii/{stem}.nii"])
        return True
    except:
        raise


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--num_proc", default=2, type=int, help="num_proc for multiprocess")
    args = parser.parse_args()
    return args


def main(args):
    fnames = [(fname,) for fname in NONREG_PATH]
    with mp.Pool(processes=args.num_proc) as p:
        p.starmap(func=run_fs, iterable=fnames)


if __name__=="__main__":
    args = parse_args()
    main(args)