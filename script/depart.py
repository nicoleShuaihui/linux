 def build_partition(self):
        status, con = commands.getstatusoutput("grep -r '/data ' /etc/fstab")
        if "xfs" in con and os.path.exists("/data "):
            pass
        else:
            con = os.popen("fdisk -l | grep 'Disk /dev'")
            output = con.read()
            if output.find(" /dev/sdb:") != -1:
                script = """
                exec 2>&1
                mkdir -p /data
                awk '{if($2 != "/data"){print $0 > "/etc/fstab"}}' /etc/fstab || exit 1

                flag=1
                for i in $(seq 10)
                do
                    umount /data
                    if [ $? -eq 32 ]; then
                        flag=0
                        break
                    fi
                done
                test $flag -eq 0 || exit 1

                parted -s /dev/sdb mklabel gpt && parted -s /dev/sdb mkpart primary 0% 100% && mkfs.xfs -n ftype=1 /dev/sdb1 -f || exit 1
                sed -i '/UUID=.* \/data xfs defaults 1 1/d' /etc/fstab
                echo `blkid |grep sdb1|awk '{print $2}'` /data xfs defaults 1 1 >> /etc/fstab
                mount -a
                mount | grep "/dev/sdb1 on /data type xfs"

                """
                fd = subprocess.Popen(script, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                output = fd.stdout.read()
                fd.wait()

