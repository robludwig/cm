from __future__ import print_function

from cloudmesh.shell.command import PluginCommand
from cloudmesh.shell.command import command


class SecgroupCommand(PluginCommand):

    # see https://github.com/cloudmesh/client/blob/master/cloudmesh_client/shell/plugins/SecgroupCommand.py
    # noinspection PyUnusedLocal
    @command
    def do_secgroup(self, args, arguments):
        """
        ::

            Usage:
                secgroup list [--format=FORMAT]
                secgroup list --cloud=CLOUD [--format=FORMAT]
                secgroup list GROUP [--format=FORMAT]
                secgroup add GROUP RULE FROMPORT TOPORT PROTOCOL CIDR
                secgroup delete GROUP [--cloud=CLOUD]
                secgroup delete GROUP RULE
                secgroup upload [GROUP] [--cloud=CLOUD]
            Options:
                --format=FORMAT Specify output format, in one of the following:
                                table, csv, json, yaml, dict. The default value
                                is 'table'.
                --cloud=CLOUD   Name of the IaaS cloud e.g. kilo,chameleon.
                                The clouds are defined in the yaml file.
                                If the name "all" is used for the cloud all
                                clouds will be selected.
            Arguments:
                RULE          The security group rule name
                GROUP         The label/name of the security group
                FROMPORT      Staring port of the rule, e.g. 22
                TOPORT        Ending port of the rule, e.g. 22
                PROTOCOL      Protocol applied, e.g. TCP,UDP,ICMP
                CIDR          IP address range in CIDR format, e.g.,
                              129.79.0.0/16

            Examples:
                secgroup list
                secgroup list --cloud=kilo
                secgroup add my_new_group webapp 8080 8080 tcp 0.0.0.0/0
                seggroup delete my_group my_rule
                secgroup delete my_unused_group --cloud=kilo
                secgroup upload --cloud=kilo

            Description:
                security_group command provides list/add/delete
                security_groups for a tenant of a cloud, as well as
                list/add/delete of rules for a security group from a
                specified cloud and tenant.
                Security groups are first assembled in a local database.
                Once they are defined they can be added to the clouds.
                secgroup list [--format=FORMAT]
                    lists all security groups and rules in the database
                secgroup list GROUP [--format=FORMAT]
                    lists a given security group and its rules defined
                    locally in the database
                secgroup list --cloud=CLOUD [--format=FORMAT]
                    lists the security groups and rules on the specified clouds.
                secgroup add GROUP RULE FROMPORT TOPORT PROTOCOL CIDR
                    adds a security rule with the given group and the details
                    of the security rules
                secgroup delete GROUP [--cloud=CLOUD]
                    Deletes a security group from the local database. To make
                    the change on the remote cloud, using the 'upload' command
                    afterwards.
                    If the --cloud parameter is specified, the change would be
                    made directly on the specified cloud
                secgroup delete GROUP RULE
                    deletes the given rule from the group. To make this change
                    on the remote cloud, using 'upload' command.
                secgroup upload [GROUP] [--cloud=CLOUD...]
                    uploads a given group to the given cloud. If the cloud is
                    not specified the default cloud is used.
                    If the parameter for cloud is "all" the rules and groups
                    will be uploaded to all active clouds.
                    This will synchronize the changes (add/delete on security
                    groups, rules) made locally to the remote cloud(s).
        """

        print(arguments)

        # m = Manager()

        # if arguments.FILE:
        #    print("option a")
        #    m.list(arguments.FILE)

        # elif arguments.list:
        #    print("option b")
        #    m.list("just calling list without parameter")
