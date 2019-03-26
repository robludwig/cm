#################################################################
# nosetest -v --nopature
# nosetests -v --nocapture tests/test_compute_azure.py
#################################################################

import subprocess
import time
from pprint import pprint

from cloudmesh.common.Printer import Printer
from cloudmesh.common.util import HEADING
from cloudmesh.common.util import banner
from cloudmesh.compute.libcloud.Provider import Provider
from cloudmesh.management.configuration.SSHkey import SSHkey
from cloudmesh.management.configuration.config import Config
from cloudmesh.management.configuration.name import Name


class TestName:

    def setup(self):
        banner("setup", c="-")
        self.user = Config()["cloudmesh"]["profile"]["user"]
        self.clouduser = 'cc'
        self.name_generator = Name(
            experiment="exp",
            group="grp",
            user=self.user,
            kind="vm",
            counter=1)

        self.name = str(self.name_generator)
        self.name_generator.incr()

        self.new_name = str(self.name_generator)

        self.p = Provider(name="azure")

        self.secgroupname = "CM4TestSecGroup"
        self.secgrouprule = {"ip_protocol": "tcp",
                             "from_port": 8080,
                             "to_port": 8088,
                             "ip_range": "129.79.0.0/16"}
        self.testnode = None

    def test_001_list_keys(self):
        HEADING()
        pprint(self.p.user)
        pprint(self.p.cloudtype)
        pprint(self.p.spec)

    def test_01_list_keys(self):
        HEADING()
        self.keys = self.p.keys()
        # pprint(self.keys)

        print(Printer.flatwrite(self.keys,
                                sort_keys=("name"),
                                order=["name", "fingerprint"],
                                header=["Name", "Fingerprint"])
              )

    def test_02_key_upload(self):
        HEADING()

        key = SSHkey()
        print(key.__dict__)

        self.p.key_upload(key)

        self.test_01_list_keys()

    def test_03_list_flavors(self):
        HEADING()
        flavors = self.p.flavors()
        pprint(flavors)

        print(Printer.flatwrite(flavors,
                                sort_keys=(
                                    "name", "extra.cores",
                                    "extra.max_data_disks", "price"),
                                order=["name", "extra.cores",
                                       "extra.max_data_disks", "price"],
                                header=["Name", "VCPUS", "max_data_disks",
                                        "Price"])
              )

        """
        {'bandwidth': None,
          'cloud': 'azure',
          'created': '2019-02-22 21:15:09.897719',
          'disk': 127,
          'driver': 'azure_asm',
          'extra': {'cores': 16, 'max_data_disks': 32},
          'id': 'Standard_D14',
          'kind': 'flavor',
          'name': 'D14 Faster Compute Instance',
          'price': '1.6261',
          'ram': 114688,
          'updated': '2019-02-22 21:15:09.897719'}
        """

    def test_04_list_vm(self):
        HEADING()
        vms = self.p.list()
        pprint(vms)

        print(Printer.flatwrite(vms,
                                sort_keys=("name"),
                                order=["name",
                                       "state",
                                       "extra.task_state",
                                       "extra.vm_state",
                                       "extra.userId",
                                       "extra.key_name",
                                       "private_ips",
                                       "public_ips"],
                                header=["Name",
                                        "State",
                                        "Task state",
                                        "VM state",
                                        "User Id",
                                        "SSHKey",
                                        "Private ips",
                                        "Public ips"])
              )

    def test_17_list_images(self):
        HEADING()
        images = self.p.images()
        pprint(images[:10])

        print(Printer.flatwrite(images[:10],
                                sort_keys=("id", "name"),
                                order=["name", "id", 'extra.os'],
                                header=["Name", "id", 'extra.os'])
              )

        """
        {'cloud': 'azure',
          'driver': 'azure_asm',
          'extra': {'affinity_group': '',
                    'category': 'Public',
                    'description': '<p>Visual Studio Community 2015 Update 3 is our '
                                   'free, full featured and extensible IDE for '
                                   'non-enterprise application development. This image '
                                   'contains Windows Server 2012 R2 with Visual Studio '
                                   'Community 2015 Update 3. It allows you to easily '
                                   'and quickly set up a development environment in '
                                   'Azure to build and test applications using Visual '
                                   'Studio.</p><p>This image was created from the '
                                   'latest bits available on 8/20/2018.</p><p>The '
                                   'Visual Studio software is preinstalled in this VM, '
                                   'but you must acquire a Visual Studio subscription '
                                   'separately which allows you to sign in to and run '
                                   'Visual Studio on this VM.</p>',
                    'location': 'Southeast Asia;Australia East;Australia '
                                'Southeast;Brazil South;Canada Central;North '
                                'Europe;West Europe;Central India;South India;West '
                                'India;Japan East;Japan West;UK South;UK West;Central '
                                'US;South Central US;West US 2;West Central US',
                    'media_link': '',
                    'os': 'Windows',
                    'vm_image': False},
          'id': '03f55de797f546a1b29d1b8d66be687a__VS-2015-Comm-VSU3-AzureSDK-29-WS2012R2-2018-08-20',
          'kind': 'image',
          'name': 'Visual Studio Community 2015 Update 3 with Azure SDK 2.9 on Windows '
                  'Server 2012 R2'},
        
        """


class forstudentstocomplete:

    def test_05_list_secgroups(self):
        HEADING()
        secgroups = self.p.list_secgroups()
        for secgroup in secgroups:
            print(secgroup["name"])
            rules = self.p.list_secgroup_rules(secgroup["name"])

            print(Printer.write(rules,
                                sort_keys=(
                                "ip_protocol", "from_port", "to_port",
                                "ip_range"),
                                order=["ip_protocol", "from_port", "to_port",
                                       "ip_range"],
                                header=["ip_protocol", "from_port", "to_port",
                                        "ip_range"])
                  )

    def test_06_secgroups_add(self):
        self.p.add_secgroup(self.secgroupname)
        self.test_05_list_secgroups()

    def test_07_secgroup_rules_add(self):
        rules = [self.secgrouprule]
        self.p.add_rules_to_secgroup(self.secgroupname, rules)
        self.test_05_list_secgroups()

    def test_08_secgroup_rules_remove(self):
        rules = [self.secgrouprule]
        self.p.remove_rules_from_secgroup(self.secgroupname, rules)
        self.test_05_list_secgroups()

    def test_09_secgroups_remove(self):
        self.p.remove_secgroup(self.secgroupname)
        self.test_05_list_secgroups()

    def test_10_create(self):
        HEADING()
        image = "CC-Ubuntu16.04"
        size = "m1.medium"
        self.p.create(name=self.name,
                      image=image,
                      size=size,
                      # username as the keypair name based on
                      # the key implementation logic
                      ex_keyname=self.user,
                      ex_security_groups=['default'])
        time.sleep(5)
        nodes = self.p.list()
        node = self.p.find(nodes, name=self.name)
        pprint(node)

        nodes = self.p.list(raw=True)
        for node in nodes:
            if node.name == self.name:
                self.testnode = node
                break

        assert node is not None

    def test_11_publicIP_attach(self):
        HEADING()
        pubip = self.p.get_publicIP()
        pprint(pubip)
        nodes = self.p.list(raw=True)
        for node in nodes:
            if node.name == self.name:
                self.testnode = node
                break
        if self.testnode:
            print("attaching public IP...")
            self.p.attach_publicIP(self.testnode, pubip)
            time.sleep(5)
        self.test_04_list_vm()

    def test_12_publicIP_detach(self):
        print("detaching and removing public IP...")
        time.sleep(5)
        nodes = self.p.list(raw=True)
        for node in nodes:
            if node.name == self.name:
                self.testnode = node
                break
        ipaddr = self.testnode.public_ips[0]
        pubip = self.p.cloudman.ex_get_floating_ip(ipaddr)
        self.p.detach_publicIP(self.testnode, pubip)
        time.sleep(5)
        self.test_04_list_vm()

    # def test_11_printer(self):
    #    HEADING()
    #    nodes = self.p.list()

    #    print(Printer.write(nodes, order=["name", "image", "size"]))

    # def test_01_start(self):
    #    HEADING()
    #    self.p.start(name=self.name)

    # def test_12_list_vm(self):
    #    self.test_04_list_vm()

    def test_13_info(self):
        HEADING()
        self.p.info(name=self.name)

    def test_14_destroy(self):
        HEADING()
        self.p.destroy(names=self.name)
        nodes = self.p.list()
        node = self.p.find(nodes, name=self.name)

        pprint(node)

        assert node["extra"]["task_state"] == "deleting"

    def test_15_list_vm(self):
        self.test_04_list_vm()

    def test_16_vm_login(self):
        self.test_04_list_vm()
        self.test_10_create()
        # use the self.testnode for this test
        time.sleep(30)
        self.test_11_publicIP_attach()
        time.sleep(5)
        nodes = self.p.list(raw=True)
        for node in nodes:
            if node.name == self.name:
                self.testnode = node
                break
        # pprint (self.testnode)
        # pprint (self.testnode.public_ips)
        pubip = self.testnode.public_ips[0]

        COMMAND = "cat /etc/*release*"

        ssh = subprocess.Popen(
            ["ssh", "%s@%s" % (self.clouduser, pubip), COMMAND],
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        result = ssh.stdout.readlines()
        if result == []:
            error = ssh.stderr.readlines()
            print("ERROR: %s" % error)
        else:
            print("RESULT:")
            for line in result:
                line = line.decode("utf-8")
                print(line.strip("\n"))

        self.test_14_destroy()
        self.test_04_list_vm()


class other:

    def test_10_rename(self):
        HEADING()

        self.p.rename(name=self.name, destination=self.new_name)

    # def test_01_stop(self):
    #    HEADING()
    #    self.stop(name=self.name)

    # def test_01_suspend(self):
    #    HEADING()
    #    self.p.suspend(name=self.name)

    # def test_01_resume(self):
    #    HEADING()
    #    self.p.resume(name=self.name)
