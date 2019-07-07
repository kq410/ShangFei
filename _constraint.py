import pyomo.environ as pyo

def constraint_definition(model):
    """
    This function takes in the model object and initialise
    user-defined constraints
    """
    isetlist = list(model.i)
    def objective_rule(model):
        """
        This constraint defines the objective function
        """
        return sum(t * model.x[i, t] for t in model.t
        for i in model.i if i == isetlist[-1])

    def constraint_rule_1V1(model, i, j):
        """
        precedence constraint type 1
        """
        if model.precedence[j, i] == 1:
            return sum(t * model.x[j, t] for t in model.t) >= \
                   sum(t * model.x[i, t] for t in model.t) + model.p[i]
        else:
            return pyo.Constraint.Skip


    def constraint_rule_2(model, k, t):
        """
        resource constraint
        """
        # summation = 0
        # for i in model.i:
        #     print('i:', i)
        #     if t >=  model.p[i]:
        #         print('t: ', t)
        #         print('p[i]: ', model.p[i])
        #         tao = range(t - model.p[i], t + 1)
        #         summation += model.x[i, tao] * model.Bi[i, k]
        #         print('summation:', type(summation))
        #         print('tao: ', tao)
        #     else:
        #         summation += 0
        # return summation <= model.B[k]

        return sum(model.Bi[i, k] * model.x[i, tao] for i in model.i
        for tao in model.t if tao >= t - model.p[i] and tao <= t) \
        <= model.B[k]


    def constraint_rule_3(model, i):
        """
        Each task is executed once
        """
        return sum(model.x[i, t] for t in model.t) == 1


    model.objective_function = pyo.Objective(
                               rule = objective_rule,
                               sense = pyo.minimize, doc = 'minimize time'
                               )


    model.constraint1V1 = pyo.Constraint(
                        model.i, model.j, rule = constraint_rule_1V1,
                        doc = 'refer to constraint_rule_1V1'
                        )

    model.constraint2 = pyo.Constraint(
                        model.k, model.t, rule = constraint_rule_2,
                        doc = 'refer to constraint_rule_2'
                        )

    model.constraint3 = pyo.Constraint(
                        model.i, rule = constraint_rule_3,
                        doc = 'refer to constraint_rule_3'
                        )
