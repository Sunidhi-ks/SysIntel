# ass4.py
import argparse
from ass1 import run_system_monitor
from ass2 import run_log_inspector
from ass3 import run_network_intel
from logger import logger

def generate_full_report():
    logger.info("Generating full system report")
    print("\n--- Full System Report ---\n")
    run_system_monitor()
    run_log_inspector()
    run_network_intel()
    print("\n--- End of Report ---\n")

def main():
    parser = argparse.ArgumentParser(description="SysIntel CLI Dashboard")
    parser.add_argument(
        '--option',
        type=int,
        choices=[1, 2, 3, 4, 5],
        required=True,
        help='''
        Options:
        1: System Monitor
        2: Log Inspector
        3: Network Intel
        4: Generate Full Report
        5: Exit
        '''
    )

    args = parser.parse_args()

    if args.option == 1:
        run_system_monitor()
    elif args.option == 2:
        run_log_inspector()
    elif args.option == 3:
        run_network_intel()
    elif args.option == 4:
        generate_full_report()
    elif args.option == 5:
        print("Exiting SysIntel CLI. Goodbye!")
        logger.info("User exited the CLI dashboard")

if __name__ == "__main__":
    main()
