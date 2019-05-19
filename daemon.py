import argparse
import inotify.adapters
import os
import paramiko
import logging
logging.basicConfig()

parser = argparse.ArgumentParser()
parser.add_argument('--src')
parser.add_argument('--host')
parser.add_argument('--dst', default='.')

args = parser.parse_args()

def setup_ssh(args):
    ssh_config_file = os.path.expanduser("~/.ssh/config")
    client = paramiko.SSHClient()
    conf = paramiko.SSHConfig()
    with open(ssh_config_file) as f:
        conf.parse(f)
    host_config = conf.lookup(args.host)
    client.load_system_host_keys()
    if 'port' not in host_config:
        host_config['port'] = 22
    key_success = False
    for key in host_config['identityfile']:
        try:
            client.connect(hostname=host_config['hostname'], port=host_config['port'], username=host_config['user'], key_filename=key)
            key_success = True
        except:
            print(key, 'is invalid')
    assert key_success
    sftp = client.open_sftp()
    sftp.sshclient = client
    args.sftp = sftp

def sync_file(args, name):
    if os.path.islink(os.path.join(args.src, name)):
        return
    args.sftp.put(os.path.join(args.src, name), os.path.join(args.dst, name))
    print('sync file', name)

def del_file(args, name):
    try:
        args.sftp.remove(os.path.join(args.dst, name))
        print('del file', name)
    except FileNotFoundError:
        print('file already deleted', name)

def sync_dir(args, name):
    args.sftp.mkdir(os.path.join(args.dst, name))
    for f in os.listdir(os.path.join(args.dst, name)):
        if os.path.isdir(os.path.join(args.dst, name, f)):
            sync_dir(args, os.path.join(name, f))
        else:
            sync_file(args, os.path.join(name, f))
    print('sync dir', name)

def del_dir(args, name):
    print('del dir', name)


def event_loop(args):
    print('source', args.src)
    setup_ssh(args)
    i = inotify.adapters.InotifyTree(args.src)
    for _, types, path, fname in i.event_gen(yield_nones=False):
        isdir = 'IN_ISDIR' in types
        fullname = os.path.join(path, fname)
        relname = os.path.relpath(fullname, start=args.src)
        #print(types, fullname)
        if 'IN_CREATE' in types:
            if isdir:
                sync_dir(args, relname)
        elif 'IN_CLOSE_WRITE' in types:
            sync_file(args, relname)
        elif 'IN_DELETE' in types:
            if isdir:
                del_dir(args, relname)
            else:
                del_file(args, relname)
        elif 'IN_MOVED_TO' in types:
            if isdir:
                sync_dir(args, relname)
            else:
                sync_file(args, relname)
        elif 'IN_MOVED_FROM' in types:
            if isdir:
                del_dir(args, relname)
            else:
                del_file(args, relname)

event_loop(args)