# -*- coding: utf-8 -*-

import json
import math
import sys

from json import JSONEncoder

import calfem.core as cfc
import calfem.geometry as cfg
import calfem.mesh as cfm
import calfem.vis_mpl as cfv
import calfem.utils as cfu

import numpy as np
import tabulate as tbl

import pyvtk as vtk

class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)

def try_convert(value, def_value):
    try:
        v = float(value)
    except ValueError:
        v = def_value

    return v


class InputData:
    """Klass för att definiera indata för vår modell."""

    def __init__(self):
        """InputData class constructor."""

        self.__version = 2

        self.__w = 0.1
        self.__h = 0.1
        self.__t = 1.0
        self.__a = 0.01
        self.__b = 0.01
        self.__x = 0.01
        self.__y = 0.01

        self.__lx = 1.7
        self.__ly = 1.7

        self.__ep = [1.0, 1]

        # --- Laster

        self.__loads = []

        # --- Randvillkor

        self.__bcs = [
            [80, 20],
            [85, 20],
            [90, 120.0],
            [95, 120.0]
        ]

        self.__el_size_factor = 0.01

        self.__a_end = self.__a + 0.01
        self.__b_end = self.__b + 0.01
        self.__param_filename = "param"
        self.__param_steps = 10
        self.__param_a = False
        self.__param_b = True

    def geometry(self):
        """Skapa en geometri instans baserat på definierade parametrar"""

        g = cfg.Geometry()

        w = self.__w
        h = self.__h
        a = self.__a
        b = self.__b
        x = self.__x
        y = self.__y

        g.point([0, 0])              # 0
        g.point([w, 0])              # 1
        g.point([w, h])              # 2
        g.point([0, h])              # 3
        g.point([x, h-y-b])          # 4
        g.point([x+a, h-y-b])        # 5
        g.point([x+a, h-y])          # 6
        g.point([x, h-y])            # 7

        g.spline([0, 1], marker=80)  # 0
        g.spline([1, 2], marker=80)  # 1
        g.spline([2, 3], marker=85)  # 2
        g.spline([3, 0], marker=85)  # 3
        g.spline([4, 5], marker=90)  # 4
        g.spline([5, 6], marker=90)  # 5
        g.spline([6, 7], marker=95)  # 6
        g.spline([7, 4], marker=95)  # 7

        g.surface([0, 1, 2, 3], holes=[[4, 5, 6, 7]])

        return g

    def save(self, filename):
        """Spara indata till fil."""

        input_data_dict = self.to_dict()

        ofile = open(filename, "w")
        json.dump(input_data_dict, ofile, sort_keys=True, indent=4)
        ofile.close()

    def to_dict(self):

        input_data = {}
        input_data["version"] = self.__version
        input_data["w"] = self.__w
        input_data["t"] = self.__t
        input_data["a"] = self.__a
        input_data["b"] = self.__b
        input_data["x"] = self.__x
        input_data["y"] = self.__y
        input_data["ep"] = self.__ep
        input_data["lx"] = self.__lx
        input_data["ly"] = self.__ly
        input_data["loads"] = self.__loads
        input_data["bcs"] = self.__bcs
        input_data["el_size_factor"] = self.__el_size_factor
        input_data["a_end"] = self.__a_end
        input_data["b_end"] = self.__b_end
        input_data["param_filename"] = self.__param_filename
        input_data["param_steps"] = self.__param_steps
        input_data["param_a"] = self.__param_a
        input_data["param_b"] = self.__param_b

        return input_data

    def from_dict(self, input_data):

        self.version = input_data["version"] = self.__version
        self.__w = input_data["w"]
        self.__t = input_data["t"]
        self.__a = input_data["a"]
        self.__b = input_data["b"]
        self.__x = input_data["x"]
        self.__y = input_data["y"]
        self.__ep = input_data["ep"]
        self.__lx = input_data["lx"]
        self.__ly = input_data["ly"]
        self.__loads = input_data["loads"]
        self.__bcs = input_data["bcs"]
        self.__el_size_factor = input_data["el_size_factor"]
        self.__a_end = input_data["a_end"]
        self.__b_end = input_data["b_end"]
        self.__param_filename = input_data["param_filename"]
        self.__param_steps = input_data["param_steps"]
        self.__param_a = input_data["param_a"]
        self.__param_b = input_data["param_b"]

    def load(self, filename):
        """Läs indata från fil."""

        ifile = open(filename, "r")
        input_data_dict = json.load(ifile)
        ifile.close()

        self.from_dict(input_data_dict)

    @property
    def w(self):
        return self.__w

    @w.setter
    def w(self, w):
        self.__w = try_convert(w, self.__w)

    @property
    def h(self):
        return self.__h

    @h.setter
    def h(self, h):
        self.__h = try_convert(h, self.__h)

    @property
    def a(self):
        return self.__a

    @a.setter
    def a(self, a):
        self.__a = try_convert(a, self.__a)

    @property
    def b(self):
        return self.__b

    @b.setter
    def b(self, b):
        self.__b = try_convert(b, self.__b)

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, x):
        self.__x = try_convert(x, self.__x)

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, y):
        self.__y = try_convert(y, self.__y)

    @property
    def lx(self):
        return self.__lx

    @lx.setter
    def lx(self, lx):
        self.__lx = try_convert(lx, self.__lx)

    @property
    def ly(self):
        return self.__ly

    @ly.setter
    def ly(self, ly):
        self.__ly = try_convert(ly, self.__ly)

    @property
    def el_size_factor(self):
        return self.__el_size_factor

    @el_size_factor.setter
    def el_size_factor(self, factor):
        self.__el_size_factor = try_convert(factor, self.__el_size_factor)

    @property
    def a_end(self):
        return self.__a_end

    @a_end.setter
    def a_end(self, a_end):
        self.__a_end = try_convert(a_end, self.__a_end)

    @property
    def b_end(self):
        return self.__b_end

    @b_end.setter
    def b_end(self, b_end):
        self.__b_end = try_convert(b_end, self.__b_end)

    @property
    def param_filename(self):
        return self.__param_filename

    @param_filename.setter
    def param_filename(self, filename):
        self.__param_filename = filename


    @property
    def param_steps(self):
        return self.__param_steps

    @param_steps.setter
    def param_steps(self, steps):
        self.__param_steps = steps

    @property
    def param_a(self):
        return self.__param_a

    @param_a.setter
    def param_a(self, flag):
        self.__param_a = flag
        self.__param_b = not flag

    @property
    def param_b(self):
        return self.__param_b

    @param_b.setter
    def param_b(self, flag):
        self.__param_b = flag
        self.__param_a = not flag

    @property
    def bcs(self):
        return self.__bcs

    @property
    def loads(self):
        return self.__loads

    @property
    def ep(self):
        return self.__ep

class OutputData:
    """Klass för att lagra resultaten från körningen."""

    def __init__(self):
        self.geometry = None
        self.a = None
        self.r = None
        self.ed = None
        self.qs = None
        self.qt = None
        self.max_flow = None
        self.flow = None
        self.coords = None
        self.edof = None
        self.dofs_per_node = None
        self.el_type = None

    def to_dict(self):
        return {
            "a": self.a,
            "r": self.r,
            "ed": self.ed,
            "qs": self.qs,
            "qt": self.qt,
            "max_flow": self.max_flow,
            "flow": self.flow,
            "coords": self.coords,
            "edof": self.edof,
            "dofs_per_node": self.dofs_per_node,
            "el_type": self.el_type
        }

    def from_dict(self, json_dict):
        self.a = np.asarray(json_dict["a"])
        self.r = np.asarray(json_dict["r"])
        self.ed = np.asarray(json_dict["ed"])
        self.qs = np.asarray(json_dict["qs"])
        self.qt = np.asarray(json_dict["qt"])
        self.max_flow = np.asarray(json_dict["max_flow"])
        self.flow = np.asarray(json_dict["flow"])
        self.coords = np.asarray(json_dict["coords"])
        self.edof = np.asarray(json_dict["edof"])
        self.dofs_per_node = np.asarray(json_dict["dofs_per_node"])
        self.el_type = np.asarray(json_dict["el_type"])


class TempModel:
    def __init__(self):
        self.__input_data = InputData()
        self.__output_data = OutputData()

    def from_json(self, json_str):
        model_data = json.loads(json_str)

        input_data_dict = model_data["input_data"]

    def from_dict(self, json_dict):

        self.input_data.from_dict(json_dict["input_data"])
        self.output_data.from_dict(json_dict["output_data"])

    def to_json(self):

        input_data_dict = self.input_data.to_dict()
        output_data_dict = self.output_data.to_dict()

        self.model = {
            "input_data": input_data_dict,
            "output_data": output_data_dict
        }

        return json.dumps(self.model, cls=NumpyArrayEncoder, sort_keys=True, indent=4)

    def save(self, filename):
        with open(filename, "w") as f:
            f.write(self.to_json())

    def load(self, filename):
        json_dict = {}
        with open(filename, "r") as f:
            json_dict = json.load(f)
        
        self.from_dict(json_dict)

    @property
    def input_data(self):
        return self.__input_data

    @input_data.setter
    def input_data(self, input_data):
        self.__input_data = input_data

    @property
    def output_data(self):
        return self.__output_data

    @output_data.setter
    def output_data(self, output_data):
        self.__output_data = output_data



class Solver:
    """Klass för att hantera lösningen av vår beräkningsmodell."""

    def __init__(self, input_data, output_data):
        self.input_data = input_data
        self.output_data = output_data

    def execute(self):
        """Metod för att utföra finita element beräkningen."""

        # --- Överför modell variabler till lokala referenser

        ep = self.input_data.ep
        lx = self.input_data.lx
        ly = self.input_data.ly
        loads = self.input_data.loads
        bcs = self.input_data.bcs
        el_size_factor = self.input_data.el_size_factor

        # --- Nätgenerering

        el_type = 3
        dofs_per_node = 1
        geometry = self.input_data.geometry()

        mesh = cfm.GmshMeshGenerator(geometry)

        # Factor that changes element sizes.

        mesh.el_size_factor = el_size_factor
        mesh.el_type = el_type
        mesh.dofs_per_node = dofs_per_node

        coords, edof, dofs, bdofs, _ = mesh.create()

        # --- Beräkna element koordinater

        ex, ey = cfc.coordxtr(edof, coords, dofs)

        self.input_data.ex = ex
        self.input_data.ey = ey

        # --- Beräkna D-matris

        D = np.array([[lx, 0.0],
                      [0.0, ly]], float)

        # --- Assemblera systemmatris

        n_dofs = edof.max()

        K = np.zeros([n_dofs, n_dofs])

        for etopo, eex, eey in zip(edof, ex, ey):
            Ke = cfc.flw2i4e(eex, eey, ep, D)
            cfc.assem(etopo, K, Ke)

        # --- Lösning av ekvationssystem

        f = np.zeros([n_dofs, 1])
        bc_prescr = np.array([], int)
        bc_val = np.array([], float)

        for bc in bcs:
            bc_prescr, bc_val = cfu.applybc(
                bdofs, bc_prescr, bc_val, bc[0], bc[1]
            )

        for load in loads:
            cfu.applyforcetotal(bdofs, f, load[0], load[1])

        a, r = cfc.solveq(K, f, bc_prescr, bc_val)

        # --- Beräkna elementkrafter

        ed = cfc.extractEldisp(edof, a)

        max_flow = []
        flow = []
        for eex, eey, eed in zip(ex, ey, ed):
            qs, qt, _ = cfc.flw2i4s(eex, eey, ep, D, eed)
            max_flow.append(
                math.sqrt(math.pow(qs[0, 0], 2) + math.pow(qs[0, 1], 2))
            )
            flow.append([qs[0, 0], qs[0, 1], 0.0])

        self.output_data.geometry = geometry
        self.output_data.a = a
        self.output_data.r = r
        self.output_data.ed = ed
        self.output_data.qs = qs
        self.output_data.qt = qt
        self.output_data.max_flow = max_flow
        self.output_data.flow = flow
        self.output_data.coords = coords
        self.output_data.edof = edof
        self.output_data.dofs_per_node = dofs_per_node
        self.output_data.el_type = el_type

    def execute_param_study(self):
        """Kör parameter studie"""

        old_a = self.input_data.a
        old_b = self.input_data.b

        i = 1

        if self.input_data.param_a:
            a_range = np.linspace(
                self.input_data.a,
                self.input_data.a_end,
                self.input_data.param_steps
            )
            for a in a_range:
                print("Executing for a = %g..." % a)
                self.input_data.a = a
                self.execute()
                self.export_vtk(
                    "%s_%02d.vtk" % (self.input_data.param_filename, i)
                )
                i += 1
        elif self.input_data.param_b:
            b_range = np.linspace(
                self.input_data.b,
                self.input_data.b_end,
                self.input_data.param_steps
            )

            for b in b_range:
                print("Executing for b = %g..." % b)
                self.input_data.b = b
                self.execute()
                self.export_vtk(
                    "%s_%02d.vtk" % (self.input_data.param_filename, i)
                )
                i += 1

        self.input_data.a = old_a
        self.input_data.b = old_b

    def export_vtk(self, filename):
        """Export results to VTK"""

        print("Exporting results to %s." % filename)

        points = self.output_data.coords.tolist()
        polygons = (self.output_data.edof-1).tolist()

        point_data = vtk.PointData(
            vtk.Scalars(self.output_data.a.tolist(), name="pressure")
        )
        cell_data = vtk.CellData(
            vtk.Scalars(self.output_data.max_flow, name="max_flow"),
            vtk.Vectors(self.output_data.flow, "flow")
        )
        structure = vtk.PolyData(points=points, polygons=polygons)

        vtk_data = vtk.VtkData(structure, point_data, cell_data)
        vtk_data.tofile(filename, "ascii")


class Report:
    """Klass för presentation av indata och utdata i rapportform."""

    def __init__(self, input_data, output_data):
        self.input_data = input_data
        self.output_data = output_data
        self.report = ""

    def clear(self):
        self.report = ""

    def add_text(self, text=""):
        self.report += str(text)+"\n"

    def __str__(self):

        np.set_printoptions(
            formatter={'float': '{: 10.3f}'.format}, threshold=sys.maxsize
        )

        self.clear()
        self.add_text()
        self.add_text("-------------------------------------------------------------")
        self.add_text("-------------- Model input ----------------------------------")
        self.add_text("-------------------------------------------------------------")
        self.add_text()
        self.add_text("Model parameters:")
        self.add_text()

        parameters = [
            ["w", self.input_data.w],
            ["h", self.input_data.h],
            ["a", self.input_data.a],
            ["b", self.input_data.b],
            ["x", self.input_data.x],
            ["y", self.input_data.y],
        ]

        self.add_text(
            tbl.tabulate(
                parameters,
                headers=["Parameter", "Value"],
                numalign="right",
                floatfmt=".4f",
                tablefmt="psql",
                )
            )

        # --- Randvillkor

        self.add_text()
        self.add_text("Model boundary conditions:")
        self.add_text()
        self.add_text(
            tbl.tabulate(
                self.input_data.bcs,
                headers=["Marker", "Pressure"],
                numalign="right",
                floatfmt=".4f",
                tablefmt="psql",
                )
            )
        self.add_text()
        self.add_text("Conductivty:")
        self.add_text()

        cond = [
            ["lx", self.input_data.lx],
            ["ly", self.input_data.ly]
        ]

        self.add_text(
            tbl.tabulate(
                cond,
                headers=["Parameter", "Value"],
                numalign="right",
                floatfmt=".4f",
                tablefmt="psql",
                )
            )
        self.add_text()
        self.add_text("-------------------------------------------------------------")
        self.add_text("-------------- Results --------------------------------------")
        self.add_text("-------------------------------------------------------------")
        self.add_text()
        self.add_text("Element coordinates:")
        self.add_text()

        self.add_text(
            tbl.tabulate(
                self.output_data.coords,
                headers=["Node", "x", "y"],
                numalign="right",
                floatfmt=".4f",
                tablefmt="psql",
                showindex=range(1, len(self.output_data.coords) + 1)
                )
            )
        self.add_text()
        self.add_text("Element topology:")
        self.add_text()
        self.add_text(
            tbl.tabulate(
                self.output_data.edof,
                headers=["Element", "i1", "i2", "i3", "i4", "i5"],
                numalign="right",
                tablefmt="psql",
                showindex=range(1, len(self.output_data.edof) + 1)
                )
            )
        self.add_text()
        self.add_text("Element displacements:")
        self.add_text()
        self.add_text(
            tbl.tabulate(
                self.output_data.ed,
                headers=["Element", "ed1", "ed2", "ed3", "ed4", "ed5"],
                numalign="right",
                tablefmt="psql",
                floatfmt=".4f",
                showindex=range(1, len(self.output_data.ed) + 1)
                )
            )
        self.add_text()
        self.add_text("Displacements:")
        self.add_text()
        self.add_text(
            tbl.tabulate(
                self.output_data.a,
                headers=["Node", "Pressure"],
                numalign="right",
                floatfmt=".4f",
                tablefmt="psql",
                showindex=range(1, len(self.output_data.a) + 1)
                )
            )
        self.add_text()
        self.add_text("Reactions:")
        self.add_text()
        self.add_text(
            tbl.tabulate(
                self.output_data.r,
                headers=["Node", "Flow"],
                numalign="right",
                floatfmt=".4f",
                tablefmt="psql",
                showindex=range(1, len(self.output_data.r) + 1)
                )
            )
        self.add_text()
        self.add_text("Element flows:")
        self.add_text()

        flow_arr = np.asarray(self.output_data.flow)

        self.add_text(
            tbl.tabulate(
                flow_arr[:, 0:2],
                headers=["Element", "qx", "qy"],
                numalign="right",
                tablefmt="psql",
                floatfmt=".4f",
                showindex=range(1, len(flow_arr) + 1)
                )
            )
        self.add_text()
        return self.report


class Visualisation:
    """Klass för visualisering av resulat"""

    def __init__(self, input_data, output_data):
        """Konstruktor"""

        self.input_data = input_data
        self.output_data = output_data

        self.geom_fig = None
        self.mesh_fig = None
        self.el_value_fig = None
        self.node_value_fig = None

        self.geom_widget = None
        self.mesh_widget = None
        self.el_value_widget = None
        self.node_value_widget = None

    def show(self):
        """Visa alla visualiseringsfönster"""
        geometry = self.output_data.geometry
        a = self.output_data.a
        max_flow = self.output_data.max_flow
        coords = self.output_data.coords
        edof = self.output_data.edof
        dofs_per_node = self.output_data.dofs_per_node
        el_type = self.output_data.el_type

        cfv.figure()
        cfv.draw_geometry(geometry, title="Geometry")

        cfv.figure()
        cfv.draw_element_values(max_flow, coords, edof, dofs_per_node, el_type,
                                None, draw_elements=False, title="Max flows")

        cfv.figure()
        cfv.draw_mesh(coords, edof, dofs_per_node, el_type, filled=True,
                      title="Mesh")

        cfv.figure()
        cfv.draw_nodal_values(a, coords, edof, el_type=el_type,
                              draw_elements=False, title="Nodal values")

        cfv.colorbar()

    def close_all(self):
        """Stäng alla visualiseringsfönster"""

        cfv.closeAll()

        self.geom_fig = None
        self.mesh_fig = None
        self.el_value_fig = None
        self.node_value_fig = None

        if self.geom_widget is not None:
            self.geom_widget.close()
        if self.mesh_widget is not None:
            self.mesh_widget.close()
        if self.el_value_widget is not None:
            self.el_value_widget.close()
        if self.node_value_widget is not None:
            self.node_value_widget.close()

    def show_geometry(self, no_show=False):
        """Visa geometri visualisering"""

        geometry = self.output_data.geometry

        self.geom_fig = cfv.figure(self.geom_fig)

        if self.geom_widget is None:
            self.geom_widget = cfv.figure_widget(self.geom_fig)

        cfv.clf()
        cfv.draw_geometry(geometry, title="Geometry")

        if no_show:
            return self.geom_widget

        self.geom_widget.show()

        return None

    def show_mesh(self, no_show=False):
        """Visa nät visualisering"""

        coords = self.output_data.coords
        edof = self.output_data.edof
        dofs_per_node = self.output_data.dofs_per_node
        el_type = self.output_data.el_type

        self.mesh_fig = cfv.figure(self.mesh_fig)

        if self.mesh_widget is None:
            self.mesh_widget = cfv.figure_widget(self.mesh_fig)

        cfv.clf()
        cfv.draw_mesh(coords, edof, dofs_per_node, el_type, filled=True,
                      title="Mesh")

        if no_show:
            return self.mesh_widget

        self.mesh_widget.show()

        return None

    def show_nodal_values(self, no_show=False):
        """Visa nodvärden"""

        a = self.output_data.a
        coords = self.output_data.coords
        edof = self.output_data.edof
        dofs_per_node = self.output_data.dofs_per_node
        el_type = self.output_data.el_type

        self.node_value_fig = cfv.figure(self.node_value_fig)

        if self.node_value_widget is None:
            self.node_value_widget = cfv.figure_widget(self.node_value_fig)

        cfv.clf()
        cfv.draw_nodal_values(a, coords, edof, dofs_per_node=dofs_per_node,
                              el_type=el_type, draw_elements=False,
                              title="Nodal values")

        if no_show:
            return self.node_value_widget

        self.node_value_widget.show()

        return None

    def show_element_values(self, no_show=False):
        """Visa elementvärden"""

        max_flow = self.output_data.max_flow
        coords = self.output_data.coords
        edof = self.output_data.edof
        dofs_per_node = self.output_data.dofs_per_node
        el_type = self.output_data.el_type

        self.el_value_fig = cfv.figure(self.el_value_fig)

        if self.el_value_widget is None:
            self.el_value_widget = cfv.figure_widget(self.el_value_fig)

        cfv.clf()
        cfv.draw_element_values(max_flow, coords, edof, dofs_per_node, el_type,
                                None, draw_elements=False, title="Max flows")

        if no_show:
            return self.el_value_widget

        self.el_value_widget.show()

        return None
