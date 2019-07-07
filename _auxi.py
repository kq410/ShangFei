import pandas as pd

class SetInput():
    """
    This is an object that initialise the input sets
    """
    def __init__(self, i, k, t):
        self.i = i
        self.k = k
        self.t = t

class ParaInput():
    """
    This is an object that initialise the parameters
    """
    def __init__(self, p, B, Bi, precedence):
        self.p = p
        self.B = B
        self.Bi = Bi
        self.precedence = precedence




def read_precedence(file):
    """
    This function is used to extract data from excel CSV
    """
    # precedence sets
    precedence_df = pd.read_excel(file)
    # get the list of all AOs
    precedence_element_list = precedence_df.AO_NUMBER.values.tolist()
    # convert it to dictionary using split
    # note here the comma is chinese comma
    precedence_dict = dict(zip(precedence_df.AO_NUMBER,
    precedence_df.PRE_AOS.apply(lambda x : x.split('，'))))

    # fitler the dictionary based on existence
    precedence_dict_filtered = {
    keys : list(filter(lambda x: (x in precedence_element_list), values))
    for keys, values in precedence_dict.items()
    }

    return precedence_element_list, precedence_dict_filtered


def convert_precedence(file):
    """
    This converts the precedence dictionary into a model readable dictionary
    """
    precedence_dict = read_precedence(file)[1]

    readable_dict = {}
    for key, value_list in precedence_dict.items():
        if key != 'initial':
            for each_precedence in value_list:
                readable_dict[key, each_precedence] = 1

    return readable_dict

def read_process_time(file):
    """
    This function is used to extract data from excel CSV
    """
    # precedence sets
    precedence_df = pd.read_excel(file)

    # convert it to dictionary using zip
    process_time_dict = dict(zip(precedence_df.AO_NUMBER,
    precedence_df.CYCLE))

    return process_time_dict

def get_resouce_set(file):
    """
    This function gets the resource set
    """
    # precedence df
    precedence_df = pd.read_excel(file)
    # get the set of resources
    resource_set = set(precedence_df.position.values.tolist())
    return resource_set

def get_resource_consumption(file):
    """
    This function gets the resource conspumtion matrix
    """
    precedence_df = pd.read_excel(file)

    resource_task_dict = {
    (AO, resource) : amount
    for AO, resource, amount in zip(precedence_df['AO_NUMBER'],
    precedence_df['position'], precedence_df['worker'])
    }


    return resource_task_dict
