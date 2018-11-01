import imp
import os
from argparse import ArgumentParser, ArgumentTypeError

from pacman_module.pacman import runGame
from pacman_module.ghostAgents import GreedyGhost, SmartyGhost, DumbyGhost
from pacman_module.wallAgents import MDPWaller, SlightlyPerturbedMDPWaller, HighlyPerturbedMDPWaller

def restricted_float(x):
    x = float(x)
    if x < 0.1 or x > 1.0:
        raise ArgumentTypeError("%r not in range [0.1, 1.0]" % (x,))
    return x


def positive_integer(x):
    x = int(x)
    if x < 0:
        raise ArgumentTypeError("%r is not >= 0" % (x,))
    return x


def load_agent_from_file(filepath):
    class_mod = None
    expected_class = 'PacmanAgent'
    mod_name, file_ext = os.path.splitext(os.path.split(filepath)[-1])

    if file_ext.lower() == '.py':
        py_mod = imp.load_source(mod_name, filepath)

    elif file_ext.lower() == '.pyc':
        py_mod = imp.load_compiled(mod_name, filepath)

    if hasattr(py_mod, expected_class):
        class_mod = getattr(py_mod, expected_class)

    return class_mod


ghosts = {}
ghosts["greedy"] = GreedyGhost
ghosts["smarty"] = SmartyGhost
ghosts["dumby"] = DumbyGhost

wallers = {}
wallers["exact"] = MDPWaller
wallers["perturbed"] = SlightlyPerturbedMDPWaller
wallers["hperturbed"] = HighlyPerturbedMDPWaller

if __name__ == '__main__':
    usage = """
    USAGE:      python run.py <game_options> <agent_options>
    EXAMPLES:   (1) python run.py
                    - plays a game with the human agent
                      in small maze
    """

    parser = ArgumentParser(usage)
    parser.add_argument(
        '--agentfile',
        help='Python file containing a `PacmanAgent` class.',
        default="humanagent.py")
    parser.add_argument(
        '--ghostagent',
        help='Ghost agent available in the `ghostAgents` module.',
        choices=["dumby", "greedy", "smarty"], default="greedy")
    parser.add_argument(
        '--layout',
        help='Maze layout (from layout folder).',
        default="small")
    parser.add_argument(
        '--silentdisplay',
        help="Disable the graphical display of the game.",
        action="store_true")
    parser.add_argument(
        '--wallagent',
        help="Wall agent available in the 'wallAgents' module.",
        choices=["exact","perturbed","hperturbed"], default="exact")
    parser.add_argument(
        '--seed',
        help="Seed for random number generator. Relevant if game tree is not deterministic. -1 means no fixed random seed.",
        type=int, default=-1)

    args = parser.parse_args()

    if (args.agentfile == "humanagent.py" and args.silentdisplay):
        print("Human agent cannot play without graphical display")
        exit()
    agent = load_agent_from_file(args.agentfile)(args)

    gagt = ghosts[args.ghostagent]
    nghosts = 1
    if (nghosts > 0):
        gagts = [gagt(i + 1) for i in range(nghosts)]
    else:
        gagts = []
    wagt = [wallers[args.wallagent](nghosts,args.seed)]
    total_score, total_computation_time, total_expanded_nodes = runGame(
        args.layout, agent, gagts, wagt, not args.silentdisplay, expout=0)

    print("Total score : " + str(total_score))
    print("Total computation time (seconds) : " + str(total_computation_time))
    print("Total expanded nodes : " + str(total_expanded_nodes))
