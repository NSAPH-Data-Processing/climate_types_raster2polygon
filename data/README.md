# data/

This folder contains data placeholders. 

* To link entrypoints to the data placeholders decide which `datapaths` configuration file is adequate for your pipeline and run:

```bash
python src/create_datapaths.py datapaths=<filename>
```

Where `<filename>` refers to the file basename for a yaml file
for `datapaths` (i.e. without the path specification). This must
be one of the files in the `conf/datapaths` directory.