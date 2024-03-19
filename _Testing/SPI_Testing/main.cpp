#include "mbed.h"
#include <cstdlib>

SPISlave spi(D11, D12, D13, PA_4);
//DigitalOut cs(PA_4);

// main() runs in its own thread in the OS

float generator(){
    return rand();
}

void SeperateIntoBytesandSend(float value){
    uint8_t *p = (uint8_t*) &value;

    for (int i = 0; i < sizeof(value); i++){
        printf("%d \n", p[i]);
        spi.reply(p[i]);
    }
}

int main()
{
    //cs = 1;

    //spi.format(8, 3);

    spi.frequency(48000);

    //cs = 0;

    spi.reply(0x00);

    while (true) {
        if (spi.receive()){
            // Generate a string of random numbers
            float num = generator();
            //cs = 0;

            //printf("%0.3f \n", num);

            //spi.reply(num);

            SeperateIntoBytesandSend(num);

            //cs = 1;
        }
    }
}

