from __future__ import print_function

from cloudmesh.shell.command import PluginCommand
from cloudmesh.shell.command import command


class SshCommand(PluginCommand):

    # see https://github.com/cloudmesh/client/blob/master/cloudmesh_client/shell/plugins/SecureShellCommand.py
    # noinspection PyUnusedLocal
    @command
    def do_ssh(self, args, arguments):
        """
        ::

            Usage:
                ssh table
                ssh list [--format=FORMAT]
                ssh cat
                ssh register NAME PARAMETERS
                ssh ARGUMENTS
                    conducts a ssh login on a machine while using a set of
                    registered machines specified in ~/.ssh/config

            Arguments:
              NAME        Name or ip of the machine to log in
              list        Lists the machines that are registered and
                          the commands to login to them
              PARAMETERS  Register te resource and add the given
                          parameters to the ssh config file.  if the
                          resource exists, it will be overwritten. The
                          information will be written in /.ssh/config

            Options:
               -v       verbose mode
               --format=FORMAT   the format in which this list is given
                                 formats includes table, json, yaml, dict
                                 [default: table]
               --user=USER       overwrites the username that is
                                 specified in ~/.ssh/config
               --key=KEY         The keyname as defined in the key list
                                 or a location that contains a public key

            Description:
                ssh list
                    lists the hostsnames  that are present in the
                    ~/.ssh/config file
                ssh cat
                    prints the ~/.ssh/config file
                ssh table
                    prints contents of the ~/.ssh/config file in table format
                ssh register NAME PARAMETERS
                    registers a host i ~/.ssh/config file
                    Parameters are attribute=value pairs
                    Note: Note yet implemented
                ssh ARGUMENTS
                    executes the ssh command with the given arguments
                    Example:
                        ssh myhost
                            conducts an ssh login to myhost if it is defined in
                            ~/.ssh/config file
        """

        print(arguments)

        # m = Manager()

        # if arguments.FILE:
        #    print("option a")
        #    m.list(arguments.FILE)

        # elif arguments.list:
        #    print("option b")
        #    m.list("just calling list without parameter")
