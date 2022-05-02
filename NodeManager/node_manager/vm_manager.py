# Import the needed credential and management objects from the libraries.
from azure.identity import EnvironmentCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.compute import ComputeManagementClient
import os
from fabric import Connection
import patchwork.transfers

import dotenv

dotenv.load_dotenv()

def createVM(VM_NAME):
    try:
        # Acquire a credential object using CLI-based authentication.
        credential = EnvironmentCredential()

        # Retrieve subscription ID from environment variable.
        subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]

        print(f"Provisioning a virtual machine...some operations might take a minute or two.")
        # Step 1: Provision a resource group

        # Obtain the management object for resources, using the credentials from the CLI login.
        resource_client = ResourceManagementClient(credential, subscription_id)

        # Constants we need in multiple places: the resource group name and the region
        # in which we provision resources. You can change these values however you want.
        RESOURCE_GROUP_NAME = "IASPlatform"
        LOCATION1 = "southindia"
        LOCATION2 = "southindia"

        # Provision the resource group.
        rg_result = resource_client.resource_groups.create_or_update(RESOURCE_GROUP_NAME,
            {
                "location": LOCATION1
            }
        )


        print(f"Provisioned resource group {rg_result.name} in the {rg_result.location} region")

        # For details on the previous code, see Example: Provision a resource group
        # at https://docs.microsoft.com/azure/developer/python/azure-sdk-example-resource-group


        # Step 2: provision a virtual network

        # A virtual machine requires a network interface client (NIC). A NIC requires
        # a virtual network and subnet along with an IP address. Therefore we must provision
        # these downstream components first, then provision the NIC, after which we
        # can provision the VM.

        # Network and IP address names
        VNET_NAME = "IASPlatform-vnet"
        SUBNET_NAME = "default"
        IP_NAME = VM_NAME+"-ip"
        IP_CONFIG_NAME = "ipconfig1"
        NIC_NAME = VM_NAME+"-nic"

        # Obtain the management object for networks
        network_client = NetworkManagementClient(credential, subscription_id)

        # Provision the virtual network and wait for completion
        poller = network_client.virtual_networks.get(RESOURCE_GROUP_NAME,
            VNET_NAME,
            # {
            #     "location": LOCATION,
            #     "address_space": {
            #         "address_prefixes": ["10.0.0.0/16"]
            #     }
            # }
        )

        vnet_result = poller

        print(f"Provisioned virtual network {vnet_result.name} with address prefixes {vnet_result.address_space.address_prefixes}")

        # Step 3: Provision the subnet and wait for completion
        poller = network_client.subnets.get(RESOURCE_GROUP_NAME, 
            VNET_NAME, SUBNET_NAME,
            # { "address_prefix": "10.0.0.0/24" }
        )
        subnet_result = poller

        print(f"Provisioned virtual subnet {subnet_result.name} with address prefix {subnet_result.address_prefix}")

        # Step 4: Provision an IP address and wait for completion
        poller = network_client.public_ip_addresses.begin_create_or_update(RESOURCE_GROUP_NAME,
            IP_NAME,
            {
                "location": LOCATION1,
                "sku": { "name": "Standard" },
                "public_ip_allocation_method": "Static",
                "public_ip_address_version" : "IPV4"
            }
        )

        ip_address_result = poller.result()

        print(f"Provisioned public IP address {ip_address_result.name} with address {ip_address_result.ip_address}")

        # Step 5: Provision the network interface client
        poller = network_client.network_interfaces.begin_create_or_update(RESOURCE_GROUP_NAME,
            NIC_NAME, 
            {
                "location": LOCATION1,
                "ip_configurations": [ {
                    "name": IP_CONFIG_NAME,
                    "subnet": { "id": subnet_result.id },
                    "public_ip_address": {"id": ip_address_result.id }
                }]
            }
        )

        nic_result = poller.result()

        print(f"Provisioned network interface client {nic_result.name}")

        # Step 6: Provision the virtual machine

        # Obtain the management object for virtual machines
        compute_client = ComputeManagementClient(credential, subscription_id)

        USERNAME = "azureuser"
        PASSWORD = "password"

        print(f"Provisioning virtual machine {VM_NAME}; this operation might take a few minutes.")

        # Provision the VM specifying only minimal arguments, which defaults to an Ubuntu 18.04 VM
        # on a Standard DS1 v2 plan with a public IP address and a default virtual network/subnet.

        poller = compute_client.virtual_machines.begin_create_or_update(RESOURCE_GROUP_NAME, VM_NAME,
            {
                "location": LOCATION2,
                "storage_profile": {
                    "image_reference": {
                        "publisher": 'canonical',
                        "offer": "0001-com-ubuntu-server-focal",
                        "sku": "20_04-lts-gen2",
                        "version": "latest"
                    }
                },
                "hardware_profile": {
                    "vm_size": "Standard_DS1"
                },
                "os_profile": {
                    "computer_name": VM_NAME,
                    "admin_username": USERNAME,
                    "linuxConfiguration": {
                                "disablePasswordAuthentication": True,
                                "ssh": {
                                    "publicKeys": [
                                        {
                                            "path": "/home/azureuser/.ssh/authorized_keys",
                                            "keyData": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDVmkI9pDoqJTWLI0gtt92jEAej\r\nPC2fSJkdM+1rkvTYTOCmmK6/yY1L3Ty9+aOpVA20ldYvr5OMpFOYV2PJSSzgoe0D\r\n0Ja2CUkqZoVclTvFzuPvCrzeD7zhX6yErtstp5Aqy3WU0PIXGJ3itmK2r0WCFXEL\r\nGak8vq0QVKpk4adD2QV7MUMGCS22mBc9F4o3GYuayKShyQ2ENtQuoclKaZdR1M8E\r\nbE2r+4lTI4x+DFoCCIgB+2RVLDP3nuIBblE++lPQPRDsSBs7pDYWdPuKchlkOOfL\r\nwSbsE0FtxMxzpDRgZtvD0Hv3ilJWCIk426esf09ssq28DWemTXivjHDCB6seAijX\r\nxYnwogYnCh9EPs35gyWXSE80qFGw3449MvjGVyaIlIwwO3GJbmociI/bHD/NAzOE\r\n6U9nibUphwweLlKKb1QM4VBrAo3WiAArY8QnbqFzAWeVNamALe3Tkx612XDCZTrl\r\nMTRHBdnIiGNTJNlkPmfZL+YimQ6a0JPzU0A7ARk= generated-by-azure\r\n"
                                        }
                                    ]
                                }
                            }
                },
                "network_profile": {
                    "network_interfaces": [{
                        "id": nic_result.id,
                    }]
                }        
            }
        )

        vm_result = poller.result()

        print(f"Provisioned virtual machine {vm_result.name}")

        return ip_address_result.ip_address
    except Exception as e:
        print(e)
        return None

def setupVM(VM_IP_ADDRESS):
    conn = Connection(VM_IP_ADDRESS, user='azureuser', connect_kwargs={'key_filename' : '/home/app/node_manager/azurekeys.pem'})
    result = conn.put('/home/app/setuphostvm.sh', remote='/home/azureuser/')
    print("Uploaded {0.local} to {0.remote}".format(result))
    conn.run('chmod +x /home/azureuser/setuphostvm.sh')
    conn.run('sudo /home/azureuser/setuphostvm.sh')

def copyFolderToVM(VM_IP_ADDRESS, sourcePath, targetPath):
    conn = Connection(VM_IP_ADDRESS, user='azureuser', connect_kwargs={'key_filename' : '/home/app/node_manager/azurekeys.pem'})
    patchwork.transfers.rsync(conn, sourcePath, targetPath, strict_host_keys=False)

def runOnVM(VM_IP_ADDRESS, command):
    conn = Connection(VM_IP_ADDRESS, user='azureuser', connect_kwargs={'key_filename' : '/home/app/node_manager/azurekeys.pem'})
    result = conn.run(command)
    return result.stdout