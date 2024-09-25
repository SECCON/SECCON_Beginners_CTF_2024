timeout --foreground 300 qemu-system-x86_64 \
     -m 64M \
     -nographic \
     -kernel ../files/bzImage \
     -initrd debugfs.cpio \
     -drive file=../files/flag.txt,format=raw \
     -snapshot \
     -append "console=ttyS0 loglevel=3 oops=panic panic=-1 pti=on kaslr root=/dev/sda" \
     -no-reboot \
     -cpu qemu64,+smap,+smep \
     -monitor /dev/null \
     -net nic,model=virtio \
     -net user \
     -gdb tcp::12345 2>/dev/null

