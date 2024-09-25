all:
	gcc exploit.c -static -o pwn
	rm -rf mount
	mkdir -p mount
	cd mount; cpio -idv < ../../files/rootfs.cpio; echo satoki
	cp ./pwn ./mount
	cd mount; find . -print0 | cpio -o --format=newc --null --owner=root > ../debugfs.cpio
	./debug.sh