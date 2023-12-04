import logging as log
import paramiko
from getpass import getpass
# wrapper for paramiko ssh client


def get_pas(): # for shading password
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
        self.sshclient.connect(hostname=self.hostname, username=self.user, key_filename=self.keyfile)       
    
        
    def Execute(self, command, isSudo=False):
        try:
            stdin, stdout, stderr = self.sshclient.exec_command(command=command, timeout=2.5)
            if isSudo:
                #paswrd = str(input("please enter the sudo password :  "))
                paswrd = get_pas()
                stdin.write(paswrd+'\n')
        except TimeoutError as e:
            log.info("connection timed out")
        
        stdin.flush()
        out_stdout = stdout.read().decode("utf-8")
        out_stderr = stderr.read().decode("utf-8")
        stdin.close()
        #self.sshclient.close()
        if len(out_stderr) != 0:
            log.error(out_stderr)
        else:
            log.info(out_stdout)
            return out_stdout


if __name__ == '__main__':
    t = Client("192.168.51.112", "rightbot", "/home/shiva/.ssh/known_hosts")
    ts = t.Execute("supervisorctl status", False)
    print(ts)
    t.sshclient.close()
    



