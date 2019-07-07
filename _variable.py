import pyomo.environ as pyo

def variable_initialisation(model):
    """
    This function takes in the model as the input and initialise
    the variables, their characteristics and bounds
    """
    model.x = pyo.Var(
                      model.i, model.t, within = pyo.Binary,
                      doc = 'if task i starts at time interval t'
    )
