#!/usr/bin/env python

import  os,sys,subprocess
import argparse,dump


def startDump(udid,appName,outputPath,waitTimeout):
    p  = subprocess.Popen('python3 /Users/du/git/iOSAPIScan/fridaios/dump.py '+appName+ ' -D '+udid+' -o '+outputPath,stdout = subprocess.PIPE,shell = True)
    try:
        p.wait(waitTimeout)
    except:
        p.kill()
        (ver, error) = p.communicate()
        plog=str(ver, encoding="utf-8")
        if len(plog)<=0:
            print('plog 为空')
            os.system('python3 /Users/du/git/iOSAPIScan/fridaios/dump.py '+appName+ ' -D '+udid+' -o '+outputPath)
            return
        if(plog.__contains__('start dump ')):
            #
            startDump(udid, appName, outputPath, 300)
        else:
            startDump(udid,appName,outputPath,10)
def killApp(udid,name_or_bundleid):
    # app已经启动的，先杀死app
    device = dump.get_usb_iphone(udid)
    bundleID = None
    for application in dump.get_applications(device):
        if name_or_bundleid == application.identifier or name_or_bundleid == application.name:
            pid = application.pid
            bundleID = application.identifier
            if pid > 0:
                device.kill(pid)
                break
    return bundleID

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='frida-ios-dump (by AloneMonkey v2.0)')
    parser.add_argument('-l', '--list', dest='list_applications', action='store_true', help='List the installed apps')
    parser.add_argument('-o', '--output', dest='output_ipa', help='Specify name of the decrypted IPA')
    parser.add_argument('-D', '--udid', dest='udid', help='Device udid')
    parser.add_argument('target', nargs='?', help='Bundle identifier or display name of the target app')

    args = parser.parse_args()

    exit_code = 0
    ssh = None

    if not len(sys.argv[1:]):
        parser.print_help()
        sys.exit(exit_code)
    if args.udid:
        udid = args.udid
    name_or_bundleid = args.target
    output_ipa = args.output_ipa
    name_or_bundleid = args.target
    #dump前杀死app
    bundleID = killApp(udid,name_or_bundleid)

    startDump(udid,name_or_bundleid,output_ipa,20)
    # dump后杀死app
    bundleID = killApp(udid, name_or_bundleid)