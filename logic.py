import sys
from operator import itemgetter

this = sys.modules[__name__]

this.fuel_map = {"gas(euro/MWh)": ["gasfired"],
                 "kerosine(euro/MWh)": ["turbojet"],
                 "wind(%)": ["windturbine"],
                 "co2(euro/ton)": ["gasfired", "turbojet"]
                 }

# Due to the multiplication by 10 to avoid floating points calculation issues,
# We have a great number of levels of recursion. This should be OK (just playing, would
# never do it for real - or use recursion for that matter)
sys.setrecursionlimit(10000)


class PayLoad:
    """ Represents a payload problem
        with target payload, fuel prices
        and powerstations with all the
        necessary logic """

    def __init__(self, payload):
        # Verify proper format for the payload...
        self.load = 0
        self.fuels = payload["fuels"]
        self.payload = payload
        self.powerplants = []
        self.feasible = True
        self.unfeasible_reason = ""

        if self.verify_payload():
            # Get the load
            self.load = payload["load"]

            for powerplant in payload["powerplants"]:
                powerplant["price_per_Mw"] = 0.0
                powerplant["p"] = 0
                for fuel in payload["fuels"]:
                    if powerplant["type"] in this.fuel_map[fuel]:
                        if fuel == "co2(euro/ton)":
                            powerplant["price_per_Mw"] += payload["fuels"][fuel] * 0.3
                        elif fuel == "wind(%)":
                            # Wind Turbines are ON/OFF
                            # This should not be done, it is done ONLY to have a simplified visual representation and
                            # have no problems with FP arithmetics
                            powerplant["pmax"] = int(powerplant["pmax"] * payload["fuels"][fuel] / 10)
                            powerplant["pmin"] = powerplant["pmax"]
                        else:
                            powerplant["price_per_Mw"] += payload["fuels"][fuel] * (1 / powerplant["efficiency"])
                            # Notice that this may not be correct because we are assigning co2 costs for MW generated
                            # It should be related to amount of fuel burnt in my opinion

            sorted_pp = sorted(payload["powerplants"], key=itemgetter("price_per_Mw"))

            self.powerplants.extend(sorted_pp)
            self.scale_up()

            self.verify_load_feasibility()
            if self.feasible:
                self.calculate_vals()
                self.allocate_powerplants(0, 0)

            self.scale_down_and_clean()

    def sol_val(self):
        """ Calculate the value of a solution """

        val = 0
        for pp in self.powerplants:
            if "index" in pp:
                val += pp["vals"][pp["index"]]
        return val

    @staticmethod
    def possible_vals(pp):
        """ Allocates a list of all possible values admitted for a Powerplant
            it's very inefficient... """

        if pp["type"] == "w":
            vals = [0, pp["pmax"]]

        elif pp["type"] == "windturbine":
            vals = [0, pp["pmin"]]
            for i in range(pp["pmin"], pp["pmax"] - pp["pmin"] + 1):
                vals.append(pp["pmin"] + i)

        else:  # Turbojet
            vals = [0]
            for i in range(pp["pmin"], pp["pmax"] - pp["pmin"]):
                vals.append(pp["pmin"] + i)
        return vals

    def calculate_vals(self):
        """ Adding the possible values to the powerplants,
            shall be removed afterwards """
        for pp in self.powerplants:
            pp["vals"] = self.possible_vals(pp)
            pp["index"] = 0

    def allocate_powerplants(self, pp_number, pp_move_index):
        """ This is the allocation of the load to the powerplants
            simple backtracking, not complete but works on the examples
             and a number of other tests"""

        self.powerplants[pp_number]["index"] = pp_move_index

        if self.sol_val() == self.load:
            return True
        else:
            if self.sol_val() < self.load:
                if pp_move_index < len(self.powerplants[pp_number]["vals"]) - 1:

                    if self.allocate_powerplants(pp_number, pp_move_index + 1):
                        return True
                else:
                    if pp_number < len(self.powerplants) - 1:
                        if self.allocate_powerplants(pp_number + 1, 0):
                            return True
            else:  # Backtrack py putting previous to smaller satisfying...
                while self.sol_val() > self.load:
                    if pp_number > 0:
                        if self.powerplants[pp_number - 1]["index"] > 0:
                            self.powerplants[pp_number - 1]["index"] = self.powerplants[pp_number - 1]["index"] - 1
                        else:
                            self.powerplants[pp_number]["index"] = 0
                    else:
                        self.powerplants[pp_number]["index"] = 0
                if pp_number < len(self.powerplants) - 1:
                    if self.allocate_powerplants(pp_number + 1, 0):
                        return True

    def verify_load_feasibility(self):
        """ Checks if we can achieve it
            """
        max_load = 0
        for pp in self.powerplants:
            max_load += pp["pmax"]

        min_load = max_load
        for pp in self.powerplants:
            min_load = min(pp["pmin"], min_load)

        if self.load > max_load:
            self.feasible = False
            self.unfeasible_reason = f"Requested load {self.load/10} too high for our powerstations "
            return False

        if self.load < min_load:
            self.feasible = False
            self.unfeasible_reason = f"Requested load {self.load/10} too low for our powerstations "
            return False

        return True

    @staticmethod
    def verify_payload():
        """ Should verify that payload contains all required fields
            nothing done, just to remember that it should be there... """
        return True

    def scale_up(self):
        """ Multiply by 10 so to avoid floating point arithmetics tricks """
        self.load *= 10
        for pp in self.powerplants:
            if pp["type"] != "windturbine":
                pp["pmin"] *= 10
                pp["pmax"] *= 10

    def scale_down_and_clean(self):
        """ Divide by 10 to present the results with 1 decimal """
        self.load /= 10.0
        for pp in self.powerplants:
            pp["pmin"] /= 10.0
            pp["pmax"] /= 10.0
            if "index" in pp and "vals" in pp:
                pp["p"] = pp["vals"][pp["index"]] / 10
                del (pp["vals"])
                del (pp["index"])
            else:
                pp["p"] = 0
