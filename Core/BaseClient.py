import paramiko
import os


def clear_null_str(obj):
    for i in range(0, obj.count("")):
        obj.remove("")
    return obj


class SSHResult:
    def __init__(self):
        self.std_out = None
        self.std_in = None
        self.std_err = None
        self.suc = False
        self.__is_init = False
        self.__key_map = {
            'out': self.std_out,
            'in': self.std_in,
            'err': self.std_err
        }

    def __init_data(self):
        if not self.__is_init:
            self.std_out = self.std_out.readlines()
            self.std_in = self.std_in.readlines()
            self.__is_init = True
        return self

    def get_out(self):
        return self.std_out.readlines()


class SSHClient:
    def __init__(self, _options):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.options = _options

    def connect(self, timeout=5, reconnect=1):
        _ret = SSHResult()
        for count in range(0, reconnect + 1):
            try:
                self.client.connect(self.options['f_host'], int(self.options['f_port']), self.options['f_user'], self.options['f_password'], timeout=timeout)
                _ret.suc = True
                return _ret
            except Exception as _e:
                print(count, _e)
                _ret.std_err = _e
        return _ret

    def download(self, remote_path, local_path):
        _ret = SSHResult()
        sftp = self.client.open_sftp()
        _filename = remote_path.split("/")[-1]
        try:
            sftp.get(remote_path, os.path.join(local_path, _filename))
            _ret.suc = True
        except Exception as __e:
            _ret.std_err = __e
            os.remove(os.path.join(local_path, _filename))
        finally:
            sftp.close()

        return _ret

    def upload(self, local_path, remote_path):
        _ret = SSHResult()
        sftp = self.client.open_sftp()
        _filename = local_path.split("/")[-1]
        if remote_path[-1] == '/':
            remote_path += _filename
        else:
            remote_path += '/' + _filename
        try:
            sftp.put(local_path, remote_path)
            _ret.suc = True
        except Exception as _e:
            _ret.std_err = _e
        finally:
            sftp.close()

        return _ret

    def run(self, command):
        _ret = SSHResult()
        try:
            _ret.std_in, _ret.std_out, _ret.std_err = self.client.exec_command(command)
            _ret.suc = True
        except Exception as e:
            _ret.std_err = e

        return _ret

    def quit(self):
        self.client.close()


