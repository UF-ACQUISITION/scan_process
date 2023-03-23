cd  E:\0_en_cours\2020_classification\test\bruts
find -type f -name '*.laz' | D:\applications\rush.exe --jobs 20 "pdal pipeline E:\0_en_cours\2020_classification\pdal_outlier_csf.json --readers.las.filename={} --writers.las.filename=E:\0_en_cours\2020_classification\test\output\{.}_class.laz"
