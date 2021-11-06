import sys
from server.client.client import Client
from game.engine import Engine
from game.utils.generate_game import generate
import game.config
import argparse
import subprocess
import updater

if __name__ == '__main__':

    plat = sys.platform
    # Setup Primary Parser
    par = argparse.ArgumentParser()

    # Create Subparsers
    spar = par.add_subparsers(title="Commands", dest="command")

    # Generate Subparser
    gen_subpar = spar.add_parser('generate', aliases=['g'], help='Generates a new random game map')
    
    # Run Subparser and optionals
    run_subpar = spar.add_parser('run', aliases=['r'],
                                 help='Runs your bot against the last generated map! "r -h" shows more options')

    run_subpar.add_argument('-debug', '-d', action='store', type=int, nargs='?', const=-1, 
                            default=None, dest='debug', help='Allows for debugging when running your code')
    
    run_subpar.add_argument('-quiet', '-q', action='store_true', default=False,
                            dest='q_bool', help='Runs your AI... quietly :)')

    # Visualizer Subparser
    vis_subpar = spar.add_parser('visualizer', aliases=['v'], help='Visualizes last run game')

    # Updating Subparser
    upd_subpar = spar.add_parser('update', aliases=['u'], help='Updates your game to match the newest version if possible')

    # Client parser
    client_parser = spar.add_parser("scrimmage", aliases= ['s'], help='run the client for the byte-le royale server')
    client_parser.add_argument("register", help='Create a new team and return a vID', default=False, action='store_true')
    client_parser.add_argument("submit", help='Submit a client for grading', default=False, action='store_true')
    client_parser.add_argument("stats", help='View stats relating to your team',default=False,  action='store_true')
    
    # Leaderboard subparser group
    leaderboard_group = client_parser.add_subparsers(title="leaderboard", dest='leaderboard')
    leaderboard = leaderboard_group.add_parser("leaderboard", aliases= ['l'],help='Commands relating to the leaderboard')
    leaderboard.add_argument("-include_alumni",  help='Include alumni in the leaderboard',default=False,  action='store_true')
    leaderboard.add_argument("-over_time",  help='See how you have scored over time', default=False,  action='store_true')

    # Parse Command Line
    par_args = par.parse_args()
    
    # Main Action variable
    action = par_args.command

    # Generate game options
    if action in ['generate', 'g']:
        generate()
    
    # Run game options
    elif action in ['run', 'r']:
        # Additional args
        quiet = False

        if par_args.debug is not None:
            if par_args.debug >= 0:
                game.config.Debug.level = par_args.debug
            else:
                print('Valid debug input not found, using default value')
        
        if par_args.q_bool:
            quiet = True
        engine = Engine(quiet)
        engine.loop()

     # Boot up the scrimmage server client
    elif action in ['server', 's', 'scrimmage']:
        cl = Client(par_args)


    elif action in ['visualizer', 'v']:
        # Check operating system and run corresponding visualizer
        if plat == "win32":
            print("You're running Windows")
            subprocess.call(["./visualizer.exe"])
        elif plat == "linux":
            print("You're a linux man I see.")
            subprocess.call(["./visualizer.x86_64"])
        elif plat == "darwin":
            print("We don't currently have visualizer support for Mac, we apologize. Give us a poke and we'll see what can do.")

    # Attempt to update the game
    elif action in ['update', 'u']:
        updater.update()
    
    # Print help if no arguments are passed
    if len(sys.argv) == 1:
        print("\nLooks like you didn't tell the launcher what to do!"
              + "\nHere's the basic commands in case you've forgotten.\n")
        par.print_help()
