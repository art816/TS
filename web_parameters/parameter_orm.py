#!/usr/bin/env python3

# This is proprietary software.
# Part of cluster monitoring project.
# PEP8 codestyle used, python version 3.
#
# authors: artem pilkevich, dmitriy khodakov

# pylint: disable=too-few-public-methods

""" This module contain Parameters which are pure database objects.
"""

import sqlalchemy as alch
# from sqlalchemy.ext.declarative import declarative_base
from collections import OrderedDict


BASE = declarative_base()


class AbstractParameter(object):
    """ Abstract parameter class. """
    id = alch.Column(alch.Integer, primary_key=True)
    # Level can be err_min, warn_min, warn_max, err_max
    name = alch.Column(alch.TEXT, nullable=False)
    full_name = alch.Column(alch.TEXT, nullable=False)
    desc = alch.Column(alch.TEXT, nullable=False)
    identifier = alch.Column(alch.TEXT, nullable=False)
    units = alch.Column(alch.TEXT, nullable=True)
    value = alch.Column(alch.TEXT, nullable=False)


class Parameter(AbstractParameter, BASE):
    """ Constructor table. """
    __tablename__ = 'param'

    def __init__(self, name, full_name, desc, identifier, units, value):
        self.name = name
        self.full_name = full_name
        self.desc = desc
        self.identifier = identifier
        self.units = units
        self.value = value


def create_orm_parameters_dict(parameter_dict):
    """ Return dict param_name : orm parameters  """
    orm_parameters = OrderedDict()
    name_list = [name for name in parameter_dict]
    name_list.sort()
    for name in name_list:
        orm_parameters[name] = create_orm_parameter(parameter_dict[name])
    return orm_parameters


def create_orm_parameter(parameter):
    """ """
    name = parameter.name
    full_name = parameter.full_name
    desc = parameter.desc
    identifier = parameter.identifier
    units = parameter.units
    if parameter.value is None:
        value = "None"
    else:
        value = parameter.value

    return Parameter(name, full_name, desc, identifier, units, value)
