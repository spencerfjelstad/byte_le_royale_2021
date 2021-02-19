import sys
from scrimmage.client import Client
from game.engine import Engine
from game.utils.generate_game import generate
from wrapper.updater import update
import game.config
import argparse
import subprocess

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

<<<<<<< HEAD
     # Scrimmage Subparser
=======
    # Scrimmage Subparser
>>>>>>> 64e0112d1f24b83df3e2e279d4f8a07e4014d9ff
    scrim_subpar = spar.add_parser('scrimmage', aliases=['s'], help='Boot client for scrimmage server')
    
    # Visualizer Subparser
    vis_subpar = spar.add_parser('visualizer', aliases=['v'], help='Runs visualizer of your last run game')

    # Updater Subparser
    upd_subpar = spar.add_parser('update', aliases=['u'], help='Checks for updates and installs if updates are found')

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
    elif action in ['scrimmage', 's']:
        cl = Client()


    elif action in ['visualizer', 'v']:
        # Check operating system and run corresponding visualizer
        if plat == "win32":
            print("You're running Windows")
            subprocess.call(["../game/visualizer/visualizer.exe"])
        elif plat == "linux":
            print("You're a linux man I see.")
            subprocess.call(["./visualizer.x86_64"])
        elif plat == "darwin":
            print("Not currently supported. If you need a MacOS version of the visualizer," 
                + "please contact the dev team, we may be able to get you one.")

    elif action in ['update', 'u']:
        update()
    
    # Print help if no arguments are passed
    if len(sys.argv) == 1:
        print("\nLooks like you didn't tell the launcher what to do!"
              + "\nHere's the basic commands in case you've forgotten.\n")
        par.print_help()
