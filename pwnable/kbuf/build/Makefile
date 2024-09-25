obj-m := driver.o
KBUILD_DIR := /home/ptr/app/buildroot/output/build/linux-6.8.9

all:
        $(MAKE) CC=gcc-12 -C $(KBUILD_DIR) M=$(shell pwd) modules

clean:
        $(MAKE) CC=gcc-12 -C $(KBUILD_DIR) M=$(shell pwd) clean
