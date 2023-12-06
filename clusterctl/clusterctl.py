from argparse import ArgumentParser
import sys
from getpass import getpass
from clusterctl.ssh import Client
import json

import logging as log
import paramiko

# wrapper for paramiko ssh client


def get_pas():  # for shading password
    passwd = getpass(prompt="Enter sudo  password: ", stream=None)
    return passwd


class Client:
    def __init__(self, hostname, user, key_file):
        self.sshclient = paramiko.SSHClient()
        self.user = user
        self.hostname = hostname
        self.keyfile = key_file  # file path for known hosts eg: .ssh/known_hosts
        self.allow_agent = False
        self.sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.sshclient.connect(
            hostname=self.hostname, username=self.user, key_filename=self.keyfile
        )

    def Execute(self, command, isSudo=False):
        try:
            stdin, stdout, stderr = self.sshclient.exec_command(
                command=command, timeout=2.5
            )
            if isSudo:
                # paswrd = str(input("please enter the sudo password :  "))
                paswrd = get_pas()
                stdin.write(paswrd + "\n")
        except TimeoutError as e:
            log.info("connection timed out")

        stdin.flush()
        out_stdout = stdout.read().decode("utf-8")
        out_stderr = stderr.read().decode("utf-8")
        stdin.close()
        # self.sshclient.close()
        if len(out_stderr) != 0:
            log.error(out_stderr)
        else:
            log.info(out_stdout)
            return out_stdout


class ConfigLoader:
    # takes the json file and loads all the config data
    def __init__(self, credential_file):
        self.file = credential_file

        with open(self.file) as file:
            self.nuc_data = json.load(file)

    def loadConfig(self, origin, key):
        for i in self.nuc_data[origin]:
            return i[key]


JsonConfig = ConfigLoader("/home/shiva/clusterctl/start_commands.json")  # data object


class CLIError(Exception):
    """Generic exception to raise and log different fatal errors."""

    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg

    def __str__(self):
        return self.msg

    def __unicode__(self):
        return self.msg


def main(argv=None):
    """Command line options."""

    program_name = "clusterctl"
    program_descrption = "to controll supervisor instruction and execute commands"

    try:
        # Setup argument parser
        parser = ArgumentParser(prog=program_name, description=program_descrption)
        parser.add_argument(
            "-s",
            "--sudo",
            action="store_true",
            help="run supervisorctl actions with sudo (nopasswd))",
        )
        parser.add_argument("-V", "--version", action="version", version=0.1)
        parser.add_argument("origin", help="arm, base, vision.")
        # parser.add_argument("supervisorctl-action", help="A supervisorctl action (and optional argument). For more details, see Supervisor documentation about the available supervisorctl actions.")

        subparsers = parser.add_subparsers(
            help="One of the available supervisorctl actions.\n ",
            dest="supervisorctl-action",
        )
        subparsers.add_parser("status", help="Get status info of all processes.")
        subparsers.add_parser(
            "reread", help="Reread the configuration files of supervisord"
        )
        subparsers.add_parser("reload", help="Restart remote supervisord")
        subparsers.add_parser(
            "update",
            help="Reload the configuration files of supervisord and add/remove processes as necessary",
        )
        start_subparser = subparsers.add_parser("start", help="Start a process by name")
        start_subparser.add_argument("process-name", help="Name of the process")
        stop_subparser = subparsers.add_parser("stop", help="Stop a process by name")
        stop_subparser.add_argument("process-name", help="Name of the process")
        restart_subparser = subparsers.add_parser(
            "restart", help="Restart a process by name"
        )
        restart_subparser.add_argument("process-name", help="Name of the process")
        restart_subparser = subparsers.add_parser(
            "exec", help="execute a shell command"
        )
        restart_subparser.add_argument("process-name", help="Name of the process")

        restart_subparser = subparsers.add_parser("           ", help="           ")
        restart_subparser.add_argument("process-name", help="Name of the process")

        restart_subparser = subparsers.add_parser("origin", help="Process Name")
        restart_subparser.add_argument("process-name", help="Name of the process")

        restart_subparser = subparsers.add_parser("           ", help="           ")
        restart_subparser.add_argument("process-name", help="Name of the process")

        restart_subparser = subparsers.add_parser("arm", help="hardware_controller")
        restart_subparser.add_argument("process-name", help="Name of the process")
        restart_subparser = subparsers.add_parser("arm", help="task_manager")
        restart_subparser.add_argument("process-name", help="Name of the process")
        restart_subparser = subparsers.add_parser("arm", help="conveyor_bridge")
        restart_subparser.add_argument("process-name", help="Name of the process")
        restart_subparser = subparsers.add_parser("arm", help="canbus")
        restart_subparser.add_argument("process-name", help="Name of the process")

        restart_subparser = subparsers.add_parser("           ", help="           ")
        restart_subparser.add_argument("process-name", help="Name of the process")

        restart_subparser = subparsers.add_parser("vision", help="left_camera")
        restart_subparser.add_argument("process-name", help="Name of the process")
        restart_subparser = subparsers.add_parser("vision", help="right_camera")
        restart_subparser.add_argument("process-name", help="Name of the process")
        restart_subparser = subparsers.add_parser("vision", help="left_camera_filter")
        restart_subparser.add_argument("process-name", help="Name of the process")
        restart_subparser = subparsers.add_parser("vision", help="right_camera_filter")
        restart_subparser.add_argument("process-name", help="Name of the process")
        restart_subparser = subparsers.add_parser(
            "vision", help="left_camera_detection"
        )
        restart_subparser.add_argument("process-name", help="Name of the process")
        restart_subparser = subparsers.add_parser(
            "vision", help="right_camera_detection"
        )
        restart_subparser.add_argument("process-name", help="Name of the process")

        restart_subparser = subparsers.add_parser("           ", help="           ")
        restart_subparser.add_argument("process-name", help="Name of the process")

        restart_subparser = subparsers.add_parser("base", help="base_controller")
        restart_subparser.add_argument("process-name", help="Name of the process")
        restart_subparser = subparsers.add_parser("base", help="formant_vel")
        restart_subparser.add_argument("process-name", help="Name of the process")
        restart_subparser = subparsers.add_parser("base", help="base_tf")
        restart_subparser.add_argument("process-name", help="Name of the process")
        restart_subparser = subparsers.add_parser("base", help="canbus")
        restart_subparser.add_argument("process-name", help="Name of the process")

        # Process arguments
        args = parser.parse_args(argv)
        verbose = 0
        origin = getattr(args, "origin")

        # host_pattern = ''
        supervisorctl_action = getattr(args, "supervisorctl-action")

        sudo = args.sudo
        supervisorctl_executable = "supervisorctl"

        command = " "
        process = " "

        if supervisorctl_action not in ["status", "reread", "update", "reload"]:
            if supervisorctl_action not in ["start", "stop", "restart"]:
                sys.exit(main(["-h"]))
            else:
                process = getattr(args, "process-name")
                command = (
                    supervisorctl_executable
                    + " "
                    + supervisorctl_action
                    + " "
                    + process
                )
        else:
            command = supervisorctl_executable + " " + supervisorctl_action

        if origin == "arm":
            conn1 = Client(
                JsonConfig.loadConfig(origin, "ip"),
                JsonConfig.loadConfig(origin, "user"),
                JsonConfig.loadConfig(origin, "public_key"),
            )
            if process == "canbus":
                status = conn1.Execute("sudo -S ~/./enable_pcan.sh", True)
                print(status)
                conn1.sshclient.close()
            else:
                status = conn1.Execute(command, isSudo=False)
                print(status)
                conn1.sshclient.close()
        elif origin == "base":
            conn2 = Client(
                JsonConfig.loadConfig(origin, "ip"),
                JsonConfig.loadConfig(origin, "user"),
                JsonConfig.loadConfig(origin, "public_key"),
            )
            if process == "canbus":
                status = conn2.Execute("sudo -S ~/./enable_pcan.sh", True)
                print(status)
                conn2.sshclient.close()
            else:
                status = conn2.Execute(command=command, isSudo=False)
                print(status)
                # print(supervisorctl_executable + " " +command)
                conn2.sshclient.close()
        elif origin == "vision":
            conn3 = Client(
                JsonConfig.loadConfig(origin, "ip"),
                JsonConfig.loadConfig(origin, "user"),
                JsonConfig.loadConfig(origin, "public_key"),
            )
            status = conn3.Execute(command=command, isSudo=False)
            print(status)
            conn3.sshclient.close()

    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0


if __name__ == "__main__":
    # sys.exit(main(["-h"]))
    main()
