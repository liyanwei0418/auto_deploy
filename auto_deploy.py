import paramiko
import time

import configer_util


class SSHConnection:

    def __init__(self, namespace):
        conf_util = configer_util.ConfigUtil('config.ini')
        self.host = conf_util.get(namespace, 'host')
        self.port = conf_util.get(namespace, 'port')
        self.user = conf_util.get(namespace, 'user')
        self.password = conf_util.get(namespace, 'password')
        self.target_path = conf_util.get(namespace, 'target_path')
        self.target_file = conf_util.get(namespace, 'target_file')
        self.project_path = conf_util.get(namespace, 'project_path')
        self.shell_path = conf_util.get(namespace, 'shell_path')
        self.source_file = conf_util.get(namespace, 'source_file')
        self.client = None
        self.sftp = None

        self.ssh_connection()
        self.open_sftp()

    def ssh_connection(self):
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
            self.client.connect(self.host, self.port, self.user, self.password)
            print('ssh connection is successful')
        except Exception as ex:
            print('ssh {0}@{1}: {2}'.format(self.user, self.host, ex))

    def open_sftp(self):
        self.sftp = self.client.open_sftp()
        print('sftp connection is successful')

    def send_to_host(self):
        self.sftp.put(self.source_file, self.target_path + self.target_file)
        print('target_file:' + self.target_path + self.target_file)
        print('transmission is completely done')

    def get_from_host(self):
        self.sftp.get(self.source_file, self.target_file)
        print('transmission is completely done')

    def ssh_close(self):
        try:
            self.client.close()
            print('ssh is closed')
        except Exception as ex:
            print('ssh is not closed. {0}'.format(ex))

    def kill_progress(self):
        command = "kill `ps -ef| grep " + self.project_path + "| awk '{print $2,$8}'| grep 'java$'| awk '{print $1}'`"
        self.execute(command)

    def del_project_file(self):
        project_file = self.target_path + self.project_path
        command = 'rm -rf ' + project_file + '/*'
        self.execute(command)

    def unzip_project(self):
        deployed_path = self.target_path + self.project_path
        cp_command = 'cp ' + self.target_path + self.target_file + " " + deployed_path
        self.execute(cp_command)
        time.sleep(2)
        unzip_command = 'unzip ' + deployed_path + '/' + self.target_file + ' -d ' + deployed_path
        self.execute(unzip_command)

    def start_project(self):
        start_command = 'sh ' + self.shell_path
        self.execute(start_command)

    def execute(self, command):
        print(command)
        self.client.exec_command(command)
