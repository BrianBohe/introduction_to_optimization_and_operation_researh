from ortools.linear_solver import pywraplp

def crear_solver():
    instancia_solver = pywraplp.Solver('OptimizacionDeFabricacionDeArena', pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)
    return instancia_solver

def crear_variables(instancia_solver):
    """
    Agregamos las variables X, e Y al modelo. Donde:
    - X es la cantidad en kg de arena azul (la llamaremos cantidad_kg_producidos_de_arena_azul)
    - Y es la cantidad en kg de arena amarilla (la llamaremos cantidad_kg_producidos_de_arena_amarilla)
    """
    # los primeros dos argumentos definen el intervalo de valores que puede tomar la variable, el último es un nombre para el solver que nos permitirá buscar a variable 
    cantidad_kg_producidos_de_arena_azul = instancia_solver.NumVar(-instancia_solver.infinity(), instancia_solver.infinity(), 'cantidad_kg_producidos_de_arena_azul')
    
    cantidad_kg_producidos_de_arena_amarilla = instancia_solver.NumVar(-instancia_solver.infinity(), instancia_solver.infinity(), 'cantidad_kg_producidos_de_arena_amarilla')

    return instancia_solver # devolvemos la misma instancia modificada por referencia


def agregar_funcion_objetivo(instancia_solver, cantidad_kg_producidos_de_arena_azul, cantidad_kg_producidos_de_arena_amarilla):
    """
    Queremos 
        Maximizar 10 * X + 5 * Y
    """
    objective = instancia_solver.Objective()
    objective.SetCoefficient(cantidad_kg_producidos_de_arena_azul, 10)
    objective.SetCoefficient(cantidad_kg_producidos_de_arena_amarilla, 5)
    objective.SetMaximization()
    return instancia_solver

def agregar_restricciones(instancia_solver, cantidad_kg_producidos_de_arena_azul, cantidad_kg_producidos_de_arena_amarilla):
    # Constraint 1: 0 <= cantidad_kg_producidos_de_arena_azul.
    restriccion_inferior_sobre_kg_arena_azul = instancia_solver.Constraint(0, instancia_solver.infinity(), 'kg_producidos_de_arena_azul_no_puede_ser_menos_que_cero')
    restriccion_inferior_sobre_kg_arena_azul.SetCoefficient(cantidad_kg_producidos_de_arena_azul, 1)

    # Constraint 1: 0 <= cantidad_kg_producidos_de_arena_amarilla.
    restriccion_inferior_sobre_kg_arena_amarilla = instancia_solver.Constraint(0, instancia_solver.infinity(), 'kg_producidos_de_arena_amarilla_no_puede_ser_menos_que_cero')
    restriccion_inferior_sobre_kg_arena_amarilla.SetCoefficient(cantidad_kg_producidos_de_arena_amarilla, 1)

    # Constraint 3: 8 X + 3 Y <= 100 (capacidad de horas hombre)
    restriccion_capacidad_horas_hombre = instancia_solver.Constraint(-instancia_solver.infinity(), 100)
    restriccion_capacidad_horas_hombre.SetCoefficient(cantidad_kg_producidos_de_arena_azul, 8)
    restriccion_capacidad_horas_hombre.SetCoefficient(cantidad_kg_producidos_de_arena_amarilla, 3)

    return instancia_solver

def escribir_solucion_por_standard_output(funcion_objetivo, cantidad_kg_producidos_de_arena_azul, cantidad_kg_producidos_de_arena_amarilla):
    print('Máxima ganancia: {:.2f}'.format(funcion_objetivo.Value()))
    
    print('Produciendo {:.2f} Kg de arena azul'.format(cantidad_kg_producidos_de_arena_azul.solution_value()))
    print('Produciendo {:.2f} Kg de arena azul'.format(cantidad_kg_producidos_de_arena_amarilla.solution_value()))
    return

def main():
    
    # Creamos una instancia de la clase Solver ( quien contiene nuestro modelo y lo resuelve )
    instancia_solver = crear_solver()

    # Definimos nuestras variables de decisión
    instancia_solver = crear_variables(instancia_solver)

    # Ahora podemos acceder a cada una de las variables definidas a través del método look up
    cantidad_kg_producidos_de_arena_azul = instancia_solver.LookupVariable('cantidad_kg_producidos_de_arena_azul')
    cantidad_kg_producidos_de_arena_amarilla = instancia_solver.LookupVariable('cantidad_kg_producidos_de_arena_amarilla')

    # Definimos la función objetivo del modelo 
    instancia_solver = agregar_funcion_objetivo(instancia_solver, cantidad_kg_producidos_de_arena_azul, cantidad_kg_producidos_de_arena_amarilla)

    # Definimos las restricciones sobre nuestras variables
    instancia_solver = agregar_restricciones(instancia_solver, cantidad_kg_producidos_de_arena_azul, cantidad_kg_producidos_de_arena_amarilla)
    
    # Le pedimos a solver que resuelva el modelo
    instancia_solver.Solve()

    # Escribimos los valores obtenidos de las variables y la función objetivo
    escribir_solucion_por_standard_output(instancia_solver.Objective(), cantidad_kg_producidos_de_arena_azul, cantidad_kg_producidos_de_arena_amarilla)


if __name__ == '__main__':
    main()