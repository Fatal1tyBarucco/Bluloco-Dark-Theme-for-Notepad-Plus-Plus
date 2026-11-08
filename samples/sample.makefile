# Sample Makefile to test Bluloco Dark
CC = gcc
CFLAGS = -Wall -Wextra -O2
TARGET = theme_app

OBJS = main.o utils.o

$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) -o $(TARGET) $(OBJS)

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(OBJS) $(TARGET)
