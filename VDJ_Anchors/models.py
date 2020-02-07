from django.db import models

'''
To do:

1. input file databases for thre genes: V, D, J.
2. total file database
3. output data
'''

import argparse
import sys
from Bio import SeqIO
import csv
import math
import re
import xlwt
import os

class VGene(models.Model):
    data = {}