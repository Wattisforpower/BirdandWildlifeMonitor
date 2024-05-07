#include "mbed.h"
#include <cstdlib>

/*
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
            //float num = generator();
            //cs = 0;

            //printf("%0.3f \n", num);

            //spi.reply(num);

            uint8_t num = 21;

            SeperateIntoBytesandSend(num);

            //cs = 1;
        }
    }
}

#endif
*/

/*
#include "mbed.h"
 
SPI spi(PE_6, PE_5, PE_2); // mosi, miso, sclk
DigitalOut cs(PF_1);
 
int main() {
    // Chip must be deselected
    cs = 1;

    // Setup the spi for 8 bit data, high steady state clock,
    // second edge capture, with a 1MHz clock rate
    spi.format(8,3);
    spi.frequency(1000000);
 
    // Select the device by seting chip select low
    cs = 0;
 
    // Send 0x8f, the command to read the WHOAMI register
    spi.write(0x8F);
 
    // Send a dummy byte to receive the contents of the WHOAMI register
    int whoami = spi.write(0x00);
    printf("WHOAMI register = 0x%X\n", whoami);
 
    // Deselect the device
    cs = 1;
}
*/

#include "mbed.h"

SPISlave device(PE_6, PE_5, PE_2, PE_4); // mosi, miso, sclk, ssel


int main() {

    int counter = 1;

    device.format(8,3);        // Setup:  bit data, high steady state clock, 2nd edge capture
    device.frequency(1000000); // 1MHz

    int reply = 99;
    device.reply(reply);              // Prime SPI with first reply
    device.reply(reply);              // Prime SPI with first reply, again

    printf("======================================================\r\n");
    printf("Startup Next reply will be %d\r\n", reply);

    while (1) {
        if (device.receive()) {
            int valueFromMaster = device.read();
            printf("%d Something rxvd, and should have replied with %d\n\r", counter++, reply);
            device.reply(reply);              // Prime SPI with next reply
            printf("    Received value from Master (%d) Next reply will be %d \r\n", valueFromMaster, reply);
        }
    }
}