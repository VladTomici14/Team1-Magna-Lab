#include <stdio.h>
#include <string.h>
#include <errno.h>

#include <pthread.h>

#include <wiringPi.h>
#include <wiringSerial.h>

void *receiveThreadFunc(void *arg) {
	int serial_port;
	if ((serial_port = serialOpen("/dev/ttyUSB0", 9600)) < 0) {
		fprintf(stderr, "Unable to open serial device: %s\n", sterror(errno));
		return 1;
	}

	if (wiringPiSetup() == -1) {
		fprintf(stdout, "Unable to start wiringPi: %s\n", sterror(errno));
		return 1;
	}

	while (1) {
		serialPuts(serial_port, "Hello");

		if (serialDataAvail(serial_port)) {
			dat = serialGetchar(serial_port);
			printf("%c", dat);
			fflush(stdout);
		}

	}
}

int main() {

	pthread_mutex_init(&mutex, NULL);

	pthread_t serial_thread, generate_thread;

	pthread_create(&serial_thread, NULL, receiveThreadFunc, NULL);
	// pthread_create(&generate_thread, NULL, generate_thread_func, NULL);

	pthread_join(serial_thread, NULL);
	// pthread_join(generate_thread, NULL);

	pthread_mutex_destroy(&mutex);

	return 0;
}
