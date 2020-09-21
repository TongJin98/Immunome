# [Immunome](https://sites.google.com/ucsd.edu/immunome/)
The project tries to incorporate data analysis tools used by immunologists and update them to the latest Python packages. The repo currently contains a Django-based website that could perform local generation of VDJ anchors.

## Project Mentor
### [Robert Sinkovits, Ph.D.](https://github.com/sinkovit)

## Project Team - Elevation Peach
#### [Tong Jin](https://github.com/TongJin98) (Team Lead)
#### [Haoyin Xu](https://github.com/PSSF23)
#### [Mingyao Xu](https://github.com/MingyaoXu)
#### [Andy Duong](https://github.com/axpecial)

## Website Details
The project uses [Django](https://www.djangoproject.com/) to implement the website frameworks and html files for the webpages.

## VDJ Anchor Generator
Based on [previous works](https://github.com/TongJin98/HVP_anchors_generator), the VDJ Anchor Generator takes genetic sequences of V, D, or J genes from the CDR3 regions in immunoglobulins and generates the associated protein (amino acids) sequences. The results are based on the genes' unique conserved positions after VDJ recombination.

### Input
The VDJ Anchor Generator takes [IMGT](http://www.imgt.org/) `.fasta` files as input.

### Output
The VDJ Anchor Generator outputs Excel sheets.
