import matlab.engine


class Matlab():
    def __init__(self):
        self.eng = matlab.engine.start_matlab()

    def getPositions(self, velocidad_x, velocidad_y, resistencia_aire, altura_volcan):
        try:
            v0x = velocidad_x
            v0y = velocidad_y
            x0 = 0  # Posición inicial en x
            y0 = altura_volcan
            b = resistencia_aire

            # Pasar las variables a MATLAB
            self.eng.workspace['v0x'] = v0x
            self.eng.workspace['v0y'] = v0y
            self.eng.workspace['x0'] = x0
            self.eng.workspace['y0'] = y0
            self.eng.workspace['b'] = b

            # Definir la ecuación diferencial para x(t) en MATLAB
            self.eng.eval("syms t x(t) y(t);", nargout=0)
            self.eng.eval("eqn_x = diff(x, t, 2) + b * diff(x, t) == 0;", nargout=0)
            self.eng.eval("cond1_x = x(0) == x0;", nargout=0)
            self.eng.eval(f"cond2_x = subs(diff(x, t), t, 0) == v0x;", nargout=0)
            self.eng.eval("sol_x = dsolve(eqn_x, [cond1_x, cond2_x]);", nargout=0)
            self.eng.eval("x_t = simplify(sol_x);", nargout=0)

            # Definir la ecuación diferencial para y(t) en MATLAB
            self.eng.eval("eqn_y = diff(y, t, 2) + b * diff(y, t) + 9.81 == 0;", nargout=0)
            self.eng.eval("cond1_y = y(0) == y0;", nargout=0)
            self.eng.eval(f"cond2_y = subs(diff(y, t), t, 0) == v0y;", nargout=0)
            self.eng.eval("sol_y = dsolve(eqn_y, [cond1_y, cond2_y]);", nargout=0)
            self.eng.eval("y_t = simplify(sol_y);", nargout=0)

            # Definir r como una función en términos de t en MATLAB
            self.eng.eval("r = [x_t; y_t];", nargout=0)

            # Aproximación numérica de T en MATLAB
            self.eng.eval("T = solve(y_t, t);", nargout=0)
            self.eng.eval("t_values = linspace(0, double(T), 50);", nargout=0)

            # Preparar los datos para la animación en MATLAB
            self.eng.workspace['t_values'] = self.eng.eval("t_values;")
            self.eng.workspace['x_values'] = self.eng.eval("subs(r(1), t, t_values);")
            self.eng.workspace['y_values'] = self.eng.eval("subs(r(2), t, t_values);")

            xValues = []

            # Crear funcion para eliminar el x10
            self.eng.eval("format short g", nargout=0)
            self.eng.eval("dcp = inline('round(input.*10.^number)./10.^number');", nargout=0)
            
            self.eng.eval("xValues_Short = dcp(x_values, 4);", nargout=0)
            self.eng.eval("xValues_vector = cast(xValues_Short, \"single\");", nargout=0)

            self.eng.eval("yValues_Short = dcp(y_values, 4);", nargout=0)
            self.eng.eval("yValues_vector = cast(yValues_Short, \"single\");", nargout=0)

            xValuesObject = self.eng.eval("xValues_vector()", nargout=1)
            yValuesObject = self.eng.eval("yValues_vector()", nargout=1)

            xValues = matlab.single(xValuesObject)[0]
            yValues = matlab.single(yValuesObject)[0]

            #self.eng.quit()

            return xValues, yValues
        except Exception as e:
            print("Error:", str(e))