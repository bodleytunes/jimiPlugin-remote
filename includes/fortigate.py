from paramiko import SSHClient, AutoAddPolicy
import time
import re
import os
from pathlib import Path


class fortigate:
    def __init__(
        self,
        host,
        deviceHostname,
        username="admin",
        password="",
        port="",
        maxRecvTime=5,
    ):
        self.host = host
        self.deviceHostname = deviceHostname
        self.username = username
        self.password = password
        if port:
            self.port = int(port)
        self.maxRecvTime = maxRecvTime
        self.error = ""

        self.client = self.connect(self.host, self.username, password=self.password)

    def connect(self, host, username, password="", port=""):
        try:
            client = SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(AutoAddPolicy())

            client.connect(
                host,
                username=username,
                password=password,
                look_for_keys=True,
                timeout=5000,
            )

            self.channel = client.invoke_shell()

            detectedDevice = (
                self.channel.recv(len(self.deviceHostname) + 2).decode().strip()
            )
            if detectedDevice != "{0} #".format(
                self.deviceHostname
            ) and detectedDevice != "{0} $".format(self.deviceHostname):
                self.error = (
                    "Device detected name does not match the device name provided."
                )
                self.disconnect
                return None
            return client
        except Exception as e:
            self.error = e
            return None

    def disconnect(self):
        if self.client:
            self.client.close()
            self.client = None

    def recv(self):
        startTime = time.time()
        recvBuffer = ""
        while time.time() - startTime < self.maxRecvTime:
            if self.channel.recv_ready():
                recvBuffer += self.channel.recv(1024).decode().strip()
                if recvBuffer.split("\n")[-1] == "--More--":
                    self.channel.send(" ")
                    recvBuffer = recvBuffer[:-8]
                elif re.match(
                    r"^{0} ((#|\$)|\([a-z]+\) (#|\$))$".format(self.deviceHostname),
                    recvBuffer.split("\n")[-1],
                ):
                    break
            time.sleep(0.1)
        return recvBuffer

    def command(self, command, args=[], elevate=False, runAs=None, timeout=None):
<<<<<<< HEAD
        self.channel.send("{0}{1}".format(command,"\n"))
=======
        self.channel.send("{0}{1}".format(command, "\n"))
>>>>>>> fee6751d186d9d22bfe4a46a02ce2c05a7f03e7a
        return (0, self.recv(), "")

    def reboot(self, timeout):
        # Not implimented yet!
        self.error = "Not implimented"
        pass

    def upload(self, localFile, remotePath):
        # Not supported!
        self.error = "Not supported"
        return False

    def download(self, remoteFile, localPath, createMissingFolders):
        # Not supported!
        self.error = "Not supported"
        return False

    def download_config(
        self, command, args=[], elevate=False, runAs=None, timeout=None, dstFolder=None
    ):
        # todo - WIP
        self.channel.send("{0}{1}".format(command, "\n"))
        # receive config
        output = self.recv()
        # create dirs
        Path(dstFolder).mkdir(parents=True, exist_ok=True)
        # create file
        file = open(
            os.path.join(dstFolder, f"{self.deviceHostname}-{self.host}.cfg"), "w"
        )
        file.write(output)
        file.close()
        return (0, "")

    def __del__(self):
        self.disconnect()
