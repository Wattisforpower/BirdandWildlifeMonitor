#include "mbed.h"

BufferedSerial LoRaReceive(D1, D0);
char Buffer[18];

// main() runs in its own thread in the OS
int main()
{
    while (true) {
        if (LoRaReceive.readable() > 0){
            LoRaReceive.read(Buffer, sizeof(Buffer));

            printf("%s", Buffer);
        }
    }
}

