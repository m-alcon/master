CC=gcc
SRC = $(wildcard *.c)
TAR = $(SRC:.c=)

.PHONY: all clean

all: $(TAR)

%: %.c $(TAR)
	$(CC) -o $@ $<

clean:
	rm $(TAR)