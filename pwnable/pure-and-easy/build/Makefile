all: dist

image: Dockerfile
	docker image build -t pwn_builder:24.04 .

build: src.c Makefile
	docker run -it --rm -v $(shell pwd):/build pwn_builder:24.04

chall: src.c Makefile
	gcc src.c -o chall -fcf-protection=none -no-pie -Wl,-z,lazy,-z,relro

clean:
	rm -f chall ../files/chall ../solver/chall
	docker container rm pure_and_easy_chall
	docker image rm pure_and_easy_pure_and_easy

dist: build
	cp chall ../files/
	cp src.c ../files/
	cp chall ../solver/

serve: dist
	docker compose -f ../compose.yml up --build
