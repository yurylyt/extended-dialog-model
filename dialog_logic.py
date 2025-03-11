from helpers import *

class Actor:
    def __init__(self, resistance, persuasion, va, vb, valt=0):
        self.resistance = resistance
        self.persuasion = persuasion
        self.va = va
        self.vb = vb
        self.valt = valt

    def preference(self):
        return np.array([self.va, self.vb, self.valt])

# Replace the existing actor function with:
def actor(resistance, persuasion, va, vb, valt=0):
    return Actor(resistance, persuasion, va, vb, valt)

def make_joint_preference(alice, bob):
    dialog_matrix = np.zeros((3, 3))
    for i in range(3):
        for j in range(3):
            dialog_matrix[i, j] = alice[i] * bob[j]

    return dialog_matrix

def communicate(alice_preference, bob_preference, transition, iterations=1, name="dialog"):
    alice_results = []
    bob_results = []
    # convert to floats
    alice_preference = np.array(alice_preference).astype(float)
    bob_preference = np.array(bob_preference).astype(float)

    alice_results.append(alice_preference)
    bob_results.append(bob_preference)
    # print("Initial joint preference")
    # print(make_joint_preference(alice, bob))

    for i in range(iterations):
        dialog_matrix = make_joint_preference(alice_preference, bob_preference)

        result = np.dot(dialog_matrix.flatten(), transition).reshape(3,3)
        # print("\nResult")
        # print(result)

        # marginalize result to get Alice's opinion
        alice_preference = np.zeros(3)
        # Sum all rows in the result
        for i in range(3):
            alice_preference[i] = result[i].sum()

        # print("\nAlice's opinion")
        # print(alice, "->", alice_result)

        # marginalize result to get Bob's opinion
        bob_preference = np.zeros(3)
        # Sum all columns in the result
        for i in range(3):
            bob_preference[i] = result[:, i].sum()

        # print("\nBob's opinion")
        # print(bob, "->", bob_result)
        alice_results.append(alice_preference)
        bob_results.append(bob_preference)
        # return alice_result, bob_result
    plot_side_by_side(alice_results, bob_results, name)
    # print("\nAlice")
    # print('\n'.join(str(x) for x in alice_results))
    # plot_results(alice_results)

    # print("\nBob")
    # print('\n'.join(str(x) for x in bob_results))
    # plot_results(bob_results)

