from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from collections import namedtuple
from collections import defaultdict
from ortools.sat.python import cp_model
import pandas as pd
import time
import _auxi

# task_list is the namedtuple for all tasks specifying the task
# index, duration, resource requirement(dictionary) and list
# of precedent tasks

class SolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self, variables):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__solution_count = 0
        self.__variables = variables
        self.__solution_limit = limit
        self.__start_time = time.time()

    def on_solution_callback(self):
        current_time = time.time()
        objective = self.ObjectiveValue()
        self.__solution_count += 1
        print('Solution %i, time = %f s, objective = %i' %
              (self.__solution_count, current_time - self.__start_time,
               objective))
        print()
        if self.__solution_count >= self.__solution_limit:
            print('Stop search after %i solutions' % self.__solution_limit)
            self.StopSearch()

    def solution_count(self):
        return self.__solution_count


class VarArrayAndObjectiveSolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self, variables, limit):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solution_count = 0
        self.__solution_limit = limit
        self.__start_time = time.time()

    def on_solution_callback(self):
        self.__solution_count += 1
        print('Solution %i' % self.__solution_count)
        print('  objective value = %i' % self.ObjectiveValue())
        # for v in self.__variables:
        #     print('  %s = %i' % (v, self.Value(v)), end=' ')
        print()
        if self.__solution_count >= self.__solution_limit:
            print('Stop search after %i solutions' % self.__solution_limit)
            self.StopSearch()


    def solution_count(self):
        return self.__solution_count


def data_input(data_type):

    Task = namedtuple("task",
    ['index', 'duration', 'resource', 'successor'])

    Resource = namedtuple("resource", ['index', 'max_capacity'])

    data = {}

    if data_type == 'real':

        print('Reading task/resource data.......')
        res_df = pd.read_excel('large_case_res.xlsx')
        res_list = res_df['res_no'].tolist()

        data['resource_list'] = [
        Resource(
        index = res_idx,
        max_capacity = res_df.loc[res_df['res_no'] == res_idx, 'num'].iloc[0])
        for res_idx in res_list]


        df_first = pd.read_csv('data3.csv')
        df = pd.read_excel('large_case_tasks.xlsx')

        task_no = df['no'].tolist()


        task_ID = df['AO_NUMBER'].tolist()

        successor_list = [str(
        df_first.loc[df_first['no'] == tidx, 'NEXT_AOS'].iloc[0]).split(',')
        for tidx in task_no]
        #print(successor_list)

        filtered_suc_list = []
        for each_list in successor_list:
            if each_list == ['nan']:
                filtered_suc_list.append([])
            else:
                filtered_suc_list.append(
                [int(x) for x in each_list if int(x) in task_no]
                )


        data['task_list'] = [
        Task(
        index = tidx,
        duration = int(df.loc[df['no'] == tidx, 'deal_time'].iloc[0]),
        resource = [int(x)
        for x in df.loc[df['no'] == tidx, 'con'].iloc[0].split(',')],
        successor = filtered_suc_list[tidx]
        ) for tidx in task_no
        ]



    else:
        data['task_list'] = [
                    Task(index = 1, duration = 3,
                    resource = {'A' : 2}, predecessor = None),
                    Task(index = 2, duration = 4,
                    resource = {'A' : 3}, predecessor = None),
                    Task(index = 3, duration = 2,
                    resource = {'A' : 4}, predecessor = [1]),
                    Task(index = 4, duration = 2,
                    resource = {'A' : 4}, predecessor = [2]),
                    Task(index = 5, duration = 1,
                    resource = {'A' : 3}, predecessor = [3]),
                    Task(index = 6, duration = 4,
                    resource = {'A' : 2}, predecessor = [4]),
                    Task(index = 7, duration = 0,
                    resource = {'A' : 0}, predecessor = [5, 6])
                    ]



        data['resource_list'] = [
        Resource(name = 'A', max_capacity = 4)]


    return data


def data_frame_to_excel(df, file_path):
    """
    This function converts the solution_df to excel
    """
    writer_reference = pd.ExcelWriter(file_path)
    df.to_excel(writer_reference, startcol = 4, startrow = 1)
    worksheet = writer_reference.sheets['Sheet1']

    writer_reference.save()


def main():

    data = data_input('real')

    # create the model
    print('Creating CP scheduling model......')
    model = cp_model.CpModel()

    # This would contain whether particular resource is active in
    # a particular interval
    intervals_per_resource = defaultdict(list)
    # This would contain the demand of the resource at each interval
    demands_per_resource = defaultdict(list)

    task_starts = {}

    task_ends = {}

    #interval_var = {}

    horizon = 200

    # task_starts: Variable for the start time of the task.
    # duration: Length of the time interval for the task.
    # task_ends: Variable for the end time of the task.
    # 'interval_%i' % (task.index)): Name for the interval variable.
    print('Genrating the interval and the makespan variables......')

    for task in data['task_list']:
        suffix = '_t%i' % (task.index)
        task_starts[task.index] = model.NewIntVar(
        0, horizon, 'start of task' + suffix
        )
        task_ends[task.index] = model.NewIntVar(
        0, horizon, 'end of task' + suffix
        )
        interval_var = model.NewIntervalVar(
        task_starts[task.index], task.duration,
        task_ends[task.index], 'interval' + suffix
        )

        for res in range(len(task.resource)):
            demand = task.resource[res]

            demands_per_resource[res].append(demand)

            intervals_per_resource[res].append(interval_var)


    # create makespan variable:
    makespan = model.NewIntVar(0, horizon, 'makespan')

    # add precedence constraints
    print('Adding precedence constraints......')
    for task in data['task_list']:
        if task.successor != [] and task.successor != None:
            for suc in task.successor:
                model.Add(task_ends[task.index] <= task_starts[suc])
                model.Add(task_ends[task.index] <= makespan)

        elif task.successor == [] and task.index == data['task_list'][-1].index:
            #print('==============================true')
            model.Add(task_ends[task.index] <= makespan)
            #model.Add(task_ends[task.index] <= task_starts[suc])
        else:
            model.Add(task_ends[task.index] <= makespan)

    # add resource constraints
    print('Adding resource constraints......')
    for r in data['resource_list']:
        # get the maximum capacity
        c = r.max_capacity
        print(c)
        model.AddCumulative(
        intervals_per_resource[r.index], demands_per_resource[r.index], c
        )


    # add objective
    objective = makespan
    model.Minimize(objective)

    # solve the model
    print('Solving using CpSolver......')
    solver = cp_model.CpSolver()
    time_limit = 2000
    solver.parameters.max_time_in_seconds = time_limit
    status = solver.Solve(model)


    # if solution is feasible or optimal after 50s then print it
    if status == cp_model.FEASIBLE or status == cp_model.OPTIMAL:
        # out put as dataframe structure
        df_list = []
        for each_task in data['task_list']:
            start_time = solver.Value(task_starts[each_task.index])
            finish_time = solver.Value(task_ends[each_task.index])
            size = each_task.duration


            int_med_list = [start_time, finish_time, size]
            int_med_list.extend(each_task.resource)


            df_list.append(int_med_list)

            results_df = pd.DataFrame(df_list)
            results_df.columns = ['start_time', 'finish time', 'size',
            'res0', 'res1', 'res2', 'res3', 'res4', 'res5', 'res6', 'res7',
            'res8', 'res9', 'res10', 'res11', 'res12', 'res13', 'res14',
            'res15', 'res16', 'res17', 'res18', 'res19'
            ]


    else:
        print('Model still not feasible after %is'%(time_limit))


    solution_printer = VarArrayAndObjectiveSolutionPrinter(
    [makespan, task_starts, task_ends], 1
    )

    solver.SolveWithSolutionCallback(model, solution_printer)

    print(solver.ResponseStats())

    print('Number of solutions found: %i' % solution_printer.solution_count())

    #print(results_df)
    data_frame_to_excel(results_df,
    'C:\\Users\\kq410\\github\\ShangFei/test_results_new.xlsx'
    )


if __name__ == '__main__':
    main()
