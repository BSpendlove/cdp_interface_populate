import textfsm
import sys
import os
import time
from datetime import datetime
from netmiko import ConnectHandler

def cdp_log(type='detailed', Logmessage=''):
        with open('cdp.log','a') as file:
            now = datetime.now()
            file.write("{0} : {1: <8} --- {2: <10}\n".format(now.strftime('%m-%d-%Y %H:%M:%S'), type, Logmessage))

def textfsm_extractor(template_name, raw_text):
        textfsm_data = list()
        fsm_handler = None

        template_path = '{0}'.format(template_name)

        with open(template_path) as f:
            fsm_handler = textfsm.TextFSM(f)

            for obj in fsm_handler.ParseText(raw_text):
                entry = {}

                for index, entry_value in enumerate(obj):
                    entry[fsm_handler.header[index].lower()] = entry_value

                textfsm_data.append(entry)

            return(textfsm_data)

if __name__ == "__main__":

    details = {'device_type' : 'cisco_ios',
               'ip' : sys.argv[1],
               'username' : sys.argv[2],
               'password' : sys.argv[3],
               'secret' : sys.argv[4]}

    current_session = ConnectHandler(**details) #Establish Session
    cdp_log(Logmessage='Connecting to device %s' %(details['ip']))

    output = current_session.send_command('show cdp neighbor detail') #Get CDP neighbors detail information

    cdp_neighbors = textfsm_extractor('cisco_ios_show_cdp_neighbors_detail.template', output) #Parse via TextFSM template
    current_session.enable()

    for neighbor in cdp_neighbors:
        local_interface = neighbor['local_port']
        remote_interface = neighbor['remote_port']
        remote_host = neighbor['destination_host']

        #Change this if you want format to look different
        initial_description = 'Link to' #Example of current format: description Link to ** RTR01.domain.com (GigabitEthernet0/0) **
        
        cmds = ['interface %s' %(local_interface), 'description ** %s %s (%s) **' %(initial_description, remote_host, remote_interface)]
        cdp_log(Logmessage='Configuring interface - %s' %(cmds))
        print('Found CDP Entry: %s on interface %s' %(remote_host, local_interface))
        print(current_session.send_config_set(cmds))

    input('Finished...')