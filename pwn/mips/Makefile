all:
	docker run -it --rm -v ${PWD}:/workdir legoclones/mips-compile:mipsel32r5-glibc mipsel-linux-gcc mips.c -no-pie -fstack-protector-all -s -o ctf/mips