from data import *
import subprocess
import time
from IO.rs232 import RS232

class common:
    def __init__(self,argv):
        self.rs232={}

    def callexe(self,argv):
        cmd=argv['exe']
        try:
            has=argv['has']
        except:
            has=''
        rtbuf=''
        logV(cmd)
        try:
            p = subprocess.Popen(cmd, 0, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                 cwd='.', shell=False)

            while True:
                buf = p.stdout.readline()
                if not buf:
                    break
                logV(buf)
                rtbuf+=buf
                time.sleep(0.005)
            logV('return code:', p.returncode)
            if not rtbuf.find(has)>=0:
                DATA.op(argv['name'] + ',1,FAIL,N/A,N/A')
            else:
                DATA.op(argv['name'] + ',0,PASS,N/A,N/A')
            return rtbuf
        except Exception,e:
            logV(Exception,e)
            DATA.op(argv['name'] + ',' + '1,FAIL,N/A,N/A')
            return ''

    def open_com_port(self,argv):
        name=argv['com_name']
        self.rs232[name]=RS232(argv)
        self.rs232[name]._connect()

    def close_com_port(self,argv):
        name = argv['com_name']
        self.rs232[name].disconnect()

    def send_cmd(self,argv):
        com_name = argv['com_name']
        cmd=argv['cmd'].encode('ascii')
        try:
            end=argv['end']
        except:
            end=''
        try:
            has=argv['has']
        except:
            has=''
        try:
            timeout=argv['timeout']
        except:
            timeout=1
        r,v=self.rs232[com_name].wr(cmd,end,has,timeout)
        logV(r,repr(v))
        if r:
            DATA.op(argv['name'] + ',0,PASS,N/A,N/A')
        else:
            DATA.op(argv['name'] + ',' + '1,FAIL,N/A,N/A')
