from dialog_logic import *

def choice_probabilities(ra, cb):
    z = ra + cb - ra * cb
    return (
        ra * (1 - cb) / z,
        (1 - ra) * cb / z,
        ra * cb / z
    )

def locate(from_state, to_state):
    # find a cell in the transition matrix that corresponds to the transition from from_state to to_state
    return (from_state[0] - 1) * 3 + from_state[1] - 1, (to_state[0] - 1) * 3 + to_state[1] - 1


def build_transition_matrix(alice: Actor, bob: Actor):
    transition = np.eye(9)

    def fill_disagreement(va, vb, valt = 3):
        pa1, pa2, pa3 = choice_probabilities(alice.resistance, bob.persuasion)
        pb1, pb2, pb3 = choice_probabilities(bob.resistance, alice.persuasion)
        transition[locate((va, vb), (va, vb))] = pa1 * pb1
        transition[locate((va, vb), (va, va))] = pa1 * pb2
        transition[locate((va, vb), (vb, vb))] = pa2 * pb1
        transition[locate((va, vb), (vb, va))] = pa2 * pb2
        transition[locate((va, vb), (va, valt))] = pa1 * pb3
        transition[locate((va, vb), (valt, vb))] = pa3 * pb1
        transition[locate((va, vb), (valt, valt))] = pa3 * pb3
        transition[locate((va, vb), (vb, valt))] = pa2 * pb3
        transition[locate((va, vb), (valt, va))] = pa3 * pb2

    fill_disagreement(1, 2)
    fill_disagreement(2, 1)
    return transition

def engage_in_dialog(alice: Actor, bob: Actor, iterations, name="dialog"):
    matrix = build_transition_matrix(alice, bob)
    communicate(
        alice.preference(),
        bob.preference(),
        matrix, iterations, name)