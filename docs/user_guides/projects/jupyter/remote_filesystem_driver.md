# Configuring remote filesystem driver

### Introduction

We provide two ways to access and persist files in HopsFs from a jupyter notebook:

* `hdfscontentsmanager`: With `hdfscontentsmanager` you interact with the project datasets using the dataset api. When you
  start a notebook using the `hdfscontentsmanager` you will only see the files in the configured root path.
* `hopsfsmount`: With `hopsfsmount` all the project datasets are available in the jupyter notebook as a local filesystem.
  This means you can use native Python file I/O operations (copy, move, create, open, etc.) to interact with the project datasets.
  When you open the jupyter notebook you will see all the project datasets.

## Configuring the driver
To configure the driver you need to have admin role and set the `jupyter_remote_fs_driver` to either `hdfscontentsmanager` or `hopsfsmount`. The default driver is `hdfscontentsmanager`.

## Conclusion

In this guide you learned about the filesystem drivers for jupyter notebooks and how to configure them.
