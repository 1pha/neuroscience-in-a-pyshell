# Preliminary

- [Preliminary](#preliminary)
  - [Bash](#bash)
    - [`find`](#find)
    - [GNU `parallel`](#gnu-parallel)
      - [Example](#example)
    - [`tmux`](#tmux)
  - [Freesurfer](#freesurfer)

## Bash
In neuroscience, many software tools and analyses are performed via command-line interfaces, making proficiency in Bash essential. Tools like FreeSurfer and FSL, which are widely used for neuroimaging data analysis, rely heavily on command-line operations. Bash scripting allows researchers to automate repetitive tasks, efficiently manage large datasets, and streamline complex workflows. Mastery of Bash can significantly enhance productivity and ensure reproducibility in research by enabling precise control over data processing pipelines.


### `find`
The `find` command literally finds all the files matched with conditions. These conditions not only include regex file name matching but also allow to search via file permission, file types or file sizes, making `find` unrivaled command for searching files. This is invaluable method for managing the numerous side-files generated from neuroscience software commands or feeding target files to `parallel` command.

```bash
find /path/to/directory -name "*.tmp" -type f -delete
```

- [Ultimate guide to Linux find command](https://snapshooter.com/learn/linux/find)

### GNU `parallel`
The gnu parallel command is a powerful tool that facilitates parallel execution of tasks. For instance, commands like FreeSurfer `mri_convert` typically process one file at a time. With gnu parallel, researchers can concurrently run multiple instances of same command across a directory of files, dramatically boosting productivity.

#### Example
Let's say we have to apply `mri_convert` on `.mgz` extension file, to convert them to `.nii`. Code for single file as follows
```bash
mri_convert sample.mgz sample.nii
```

What if we have to loop over ALL `.mgz` files in current directory? One may come up with `for` loop.
```bash
for file in $(ls *.mgz)
do
  mri_convert $file ${file%.mgz}.nii
done
```
However, this for loop is not able to run all files in parallel. Also if we have enough idle resources, it is smart to parallelize this job. Here we can use `parallel`.
```bash
# Takes arguments via `{}`
ls *.mgz | parallel mri_convert {} {.}.nii
```

What if we need a long script to be ran in parallel? We can move our `parallel` command into bash script and
Following code is an actual bash script that I used to apply `dcm2niix`.
```bash
#!/bin/bash
# SRC and TGT are source and target directory and DCM_DIR is directory containing all dcm files.
find $DCM_DIR -mindepth 2 -maxdepth 2 -type d | sort | parallel -j 4 --eta '
    echo Processing {}
    OUT="$(echo {} | sed "s|$SRC|$TGT|")"
    mkdir -p $OUT
    dcm2niix -o $OUT {}
'
```
There are numerous useful arguments to boost productivity. GNU provides well assorted [tutorial](https://www.gnu.org/software/parallel/parallel_tutorial.html).


### `tmux`
Most neuroscience commands take long time to finish its execution. One may want to put this job in the background. `nohup` or `&` command maybe a good option but my best preference is `tmux`. This capability is crucial for maintaining productivity and managing computational resources effectively. Users are allowed to create multiple windows and panes to work in the background.

One of the inconvenience is the default behavior of disabled mouse scroll, but you can resolve this via configuring with creating following `tmux.conf` file.
```
# tmux.conf file
set -g mouse on
```
and then run `tmux source tmux.conf` on the command line. 
 
- [A Quick and Easy Guide to tmux](https://hamvocke.com/blog/a-quick-and-easy-guide-to-tmux/)


## Freesurfer
Various tools exist to pre-process brains. One of widely used software tools is freesurfer, a powerful and widely used software package designed for the analysis and visualization of structural and functional neuroimaging data from magnetic resonance imaging (MRI) scans. It provides tools for the reconstruction of the brain’s cortical surface, segmentation of subcortical brain structures, and various other analyses related to brain anatomy and morphology. FreeSurfer is extensively utilized in neuroscience research for tasks such as measuring cortical thickness, generating 3D brain models, and performing longitudinal studies to track changes in brain structure over time. Its robust set of tools and comprehensive documentation make it an essential resource for researchers working with neuroimaging data. Recently, **freesurfer integrates other open-source commands into its software**, making it easier for users to keep the environment consistent removing necessities to install multiple packages.

I would recommend using docker image to run use freesurfer.
- [Download and Install Freesurfer](https://surfer.nmr.mgh.harvard.edu/fswiki/DownloadAndInstall)
- [Freesurfer Dockerhub](https://hub.docker.com/r/freesurfer/freesurfer)
