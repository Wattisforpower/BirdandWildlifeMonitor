# Bird and Wildlife Monitor
## Digital Signal Processing Firmware
### Authors:
James Davis
### Aims:
- Accurately sample audio at 48kHz 24 bits
- Filter background noise from the audio
- Accurately remove wind and rain sounds from audio
- All Audio is removed using adaptive spectral subtraction
- All processing is performed in real time
- Clean audio is sent to _Raspberry Pi 4-B_ via SPI
### Hardware Description:
- Custom designed PCB 
- Using _STM32F767ZI_ MCU
- Using _CS5343-CZZ_ ADC IC
- Interfaces with and powers a _Raspberry Pi 4-B_
### Firmware Description:
- All firmware is produced using STM32CubeIDE
