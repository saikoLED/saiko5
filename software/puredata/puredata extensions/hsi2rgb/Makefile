CC=gcc
LIBS=-lm -llo
CFLAGS=-O3 -Wall -std=gnu99
TARGETS=

pd_client_mac: pd_hsi2rgb.c
	$(CC) $(LIBS) $(CFLAGS) -DPD -W -Wshadow -Wstrict-prototypes -Wno-unused -Wno-parentheses -Wno-switch -o pd_hsi2rgb.o -c pd_hsi2rgb.c
	$(CC) $(LIBS) -bundle -undefined suppress -flat_namespace -o hsi2rgb.pd_darwin pd_hsi2rgb.o

pd_client_linux: pd_hsi2rgb.c
	$(CC) $(LIBS) $(CFLAGS) -DPD -fpic -o pd_hsi2rgb_linux.o -c pd_hsi2rgb.c
	$(CC) $(LIBS) -export_dynamic -shared -o hsi2rgb.pd_linux pd_hsi2rgb_linux.o
