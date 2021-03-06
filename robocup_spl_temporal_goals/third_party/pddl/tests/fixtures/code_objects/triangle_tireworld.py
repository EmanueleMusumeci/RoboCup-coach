# -*- coding: utf-8 -*-
#
# Copyright 2021 WhiteMech
#
# ------------------------------
#
# This file is part of pddl.
#
# pddl is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pddl is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with pddl.  If not, see <https://www.gnu.org/licenses/>.
#

"""This test module contains the fixtures for 'triangle-tireworld' domain and problem."""
import pytest

from third_party.pddl.pddl.core import Action, Domain, Problem, Requirements
from third_party.pddl.pddl.logic.base import And, OneOf
from third_party.pddl.pddl.logic.helpers import constants, variables
from third_party.pddl.pddl.logic.predicates import Predicate


@pytest.fixture(scope="session")
def triangle_tireworld_domain():
    """The 'triangle-tireworld' domain."""
    # types
    location = "location"

    # terms
    to, from_, loc = variables("to from loc", types=[location])

    # constants:
    constants = None

    # predicates
    vehicleat = Predicate("vehicleat", loc)
    spare_in = Predicate("spare-in", loc)
    road = Predicate("road", from_, to)
    not_flattire = Predicate("not-flattire")
    predicates = {vehicleat, spare_in, road, not_flattire}

    # actions
    # move-car
    move_car_name = "move-car"
    move_car_parameters = [from_, to]
    move_car_precondition = vehicleat(from_) & road(from_, to) & not_flattire
    move_car_effect = And(
        OneOf(
            vehicleat(to) & ~vehicleat(from_),
            vehicleat(to) & ~vehicleat(from_) & ~not_flattire,
        )
    )
    move_car = Action(
        move_car_name, move_car_parameters, move_car_precondition, move_car_effect
    )

    # changetire
    changetire_name = "changetire"
    changetire_parameters = [loc]
    changetire_precondition = spare_in(loc) & vehicleat(loc)
    changetire_effect = ~spare_in(loc) & not_flattire
    changetire = Action(
        changetire_name,
        changetire_parameters,
        changetire_precondition,
        changetire_effect,
    )

    name = "triangle-tire"
    requirements = {
        Requirements.STRIPS,
        Requirements.NON_DETERMINISTIC,
        Requirements.TYPING,
    }
    types = {location}
    actions = {
        move_car,
        changetire,
    }
    domain = Domain(
        name=name,
        requirements=requirements,
        types=types,
        constants=constants,
        predicates=predicates,
        actions=actions,
    )
    return domain


@pytest.fixture(scope="session")
def triangle_tireworld_problem_01():
    """Triangle-tireworld problem 01."""
    # objects
    objects = [l1, l2, l3, l4, l5, l6, l7, l8, l9] = constants(
        "l1 l2 l3 l4 l5 l6 l7 l8 l9", types=["location"]
    )

    # predicates
    vehicleat = Predicate("vehicleat", l1)
    spare_in = Predicate("spare-in", l1)
    road = Predicate("road", l1, l2)
    not_flattire = Predicate("not-flattire")

    init = {
        vehicleat(l1),
        road(l1, l2),
        road(l2, l3),
        road(l1, l4),
        road(l2, l5),
        road(l4, l2),
        road(l5, l3),
        road(l4, l7),
        road(l7, l5),
        spare_in(l4),
        spare_in(l5),
        spare_in(l7),
        spare_in(l7),
    }

    goal = vehicleat(l3)

    problem_name = "triangle-tire-1"

    problem = Problem(
        problem_name,
        domain_name="triangle-tire",
        objects=objects,
        init=init,
        goal=goal,
    )
    return problem
