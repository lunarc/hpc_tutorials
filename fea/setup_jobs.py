# -*- coding: utf-8 -*-

import os, sys

import numpy as np
import tempmodel2 as tm

if __name__ == "__main__":

    print("Creating empty model...")
    temp_model = tm.TempModel()
    temp_model.input_data.el_size_factor = 0.05

    a_range = np.linspace(0.01, 0.06, 10)
    b_range = np.linspace(0.01, 0.06, 10)

    curr_dir = os.getcwd()
    job_number = 0

    for a in a_range:
        for b in b_range:
            temp_model.input_data.a = a
            temp_model.input_data.b = b

            job_dir = "job_%d" % job_number

            if not os.path.exists(job_dir):
                os.mkdir(job_dir)

            os.chdir(job_dir)
            temp_model.save("temp_model_%d.json" % (job_number))
            os.chdir(curr_dir)

            job_number += 1



