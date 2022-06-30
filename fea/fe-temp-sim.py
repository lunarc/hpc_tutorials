# -*- coding: utf-8 -*-

import os, sys

import tempmodel2 as tm

if __name__ == "__main__":

    print("Creating empty model...")
    temp_model1 = tm.TempModel()
    temp_model1.input_data.el_size_factor = 0.05
    temp_model1.save("temp_model_empty.json")

    print("Loading empty model...")
    temp_model2 = tm.TempModel()
    temp_model2.load("temp_model_empty.json")

    print("Solving model...")
    temp_solver = tm.Solver(temp_model2.input_data, temp_model2.output_data)
    temp_solver.execute()

    print("Saving with results...")
    temp_model2.save("temp_model_results.json")

    print("Loading with results...")
    temp_model3 = tm.TempModel()
    temp_model3.load("temp_model_results.json")

    print("Saving back with results...")
    temp_model3.save("temp_model_results_read.json")


    #temp_solver.execute()




