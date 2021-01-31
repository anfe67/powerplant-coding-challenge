from unittest import TestCase
import json

import logic


class TestLogic(TestCase):
    """ Not a real unit test, just verifying that I am obtaining
        the minimum requirements, not looking for more except detecting
        unfeasible loads (too high) """

    def test_payload_init(self):
        print("\n--------> PAYLOAD 1\n")
        with open('../example_payloads/payload1.json', 'r') as f:
            json_payload = json.load(f)

            payload = logic.PayLoad(json_payload)
            if payload.feasible:
                print(f"Load {payload.load} achievable ")
            else:
                print(payload.unfeasible_reason)
            for powerplant in payload.powerplants:
                print(f"Powerplant: {powerplant['name']} generates:  {powerplant['p']}")

        print("--------> PAYLOAD 2\n")
        with open('../example_payloads/payload2.json', 'r') as f:
            json_payload = json.load(f)

            payload = logic.PayLoad(json_payload)
            if payload.feasible:
                print(f"Load {payload.load} achievable ")
            else:
                print(payload.unfeasible_reason)
            for powerplant in payload.powerplants:
                print(f"Powerplant: {powerplant['name']} generates:  {powerplant['p']}")

        print("--------> PAYLOAD 3\n")
        with open('../example_payloads/payload3.json', 'r') as f:
            json_payload = json.load(f)

            payload = logic.PayLoad(json_payload)
            if payload.feasible:
                print(f"Load {payload.load} achievable ")
            else:
                print(payload.unfeasible_reason)
            for powerplant in payload.powerplants:
                print(f"Powerplant: {powerplant['name']} generates:  {powerplant['p']}")

        print("--------> PAYLOAD 4 - HIGH\n")
        with open('../example_payloads/payload4high.json', 'r') as f:
            json_payload = json.load(f)

            payload = logic.PayLoad(json_payload)
            if payload.feasible:
                print(f"Load {payload.load} achievable ")
            else:
                print(payload.unfeasible_reason)
            for powerplant in payload.powerplants:
                print(f"Powerplant: {powerplant['name']} generates:  NOT CALCULATED")
