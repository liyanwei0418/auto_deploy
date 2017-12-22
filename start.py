import time

import auto_deploy

ssh_client = auto_deploy.SSHConnection('team')
try:
    ssh_client.send_to_host()
    ssh_client.kill_progress()
    time.sleep(5)
    ssh_client.del_project_file()
    time.sleep(2)
    ssh_client.unzip_project()
    time.sleep(2)
    ssh_client.start_project()
finally:
    ssh_client.ssh_close()
