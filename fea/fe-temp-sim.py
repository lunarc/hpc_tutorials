# -*- coding: utf-8 -*-

import os, sys

import tempmodel2 as tm

if __name__ == "__main__":

    if len(sys.argv)==3:
        input_filename = sys.argv[1]
        output_filename = sys.argv[2]
    else:
        print("Usage: "+sys.argv[0]+" input_filename output_filename")
        sys.exit(1)

    print("Creating empty model...")
    temp_model = tm.TempModel()
    temp_model.load(input_filename)
    temp_model.input_data.el_size_factor = 0.05

    print("Solving model...")
    temp_solver = tm.Solver(temp_model.input_data, temp_model.output_data)
    temp_solver.execute()

    temp_model.save(output_filename)




