
#include "main.h"
#include "usb_device.h"
#define ARM_MATH_CM7
#include "arm_math.h"
#include "usbd_cdc_if.h"
#include "stdio.h"

I2S_HandleTypeDef hi2s2;
I2S_HandleTypeDef hi2s3;
DMA_HandleTypeDef hdma_spi2_rx;
DMA_HandleTypeDef hdma_spi3_tx;

SPI_HandleTypeDef hspi4;
DMA_HandleTypeDef hdma_spi4_tx;

#define SAMPLE_RATE 48339.0f
#define BUFFER_SIZE 8192//minimum of 8
#define INT32_TO_FLOAT32 1.0f / 2147483648.0f
#define FLOAT32_TO_INT32 2147483648.0f
#define STE_AVG_SIZE 64
#define STE_FRAME_HOLD 5
#define STE_AVG_THRESHOLD_OFFSET 0.1
#define FFT_BUFFER_SIZE 4096
#define AVG_NOISE_ESTIMATE_LENGTH 512 //provides estimated 45second convergence time and <0.6% inaccuracy tested over 100mill iterations

#define SPI_BUFFER_SIZE 500	//MUST BE MULTIPLE OF 5

uint16_t rx_buffer[BUFFER_SIZE];
uint16_t tx_buffer[BUFFER_SIZE];
uint8_t i2s_rx_half_complete_flag = 0;
uint8_t i2s_rx_full_complete_flag = 0;
float32_t left_sample[BUFFER_SIZE / 8];
float32_t right_sample[BUFFER_SIZE / 8];

int ste_frame_count = 0;
float ste_avg_array[STE_AVG_SIZE];
int ste_avg_head = 0;

arm_rfft_fast_instance_f32 fft_handler;
float32_t fft_input_buffer[FFT_BUFFER_SIZE];
float32_t fft_output_buffer[FFT_BUFFER_SIZE];
int fft_idx = 0;

float phases[FFT_BUFFER_SIZE/2];
float magnitudes[FFT_BUFFER_SIZE/2];
float avg_noise_magnitudes[FFT_BUFFER_SIZE/2];
float clean_magnitudes[FFT_BUFFER_SIZE/2];

uint8_t spi_buffer_0[SPI_BUFFER_SIZE] = {0};
uint8_t spi_buffer_1[SPI_BUFFER_SIZE] = {0};
uint8_t *spi_buffer_pointer = &spi_buffer_0[0];
int spi_buffer_head = 0;
int spi_buffer_idx= 0;
static volatile int spi_tx_ready_flag = 1;

void SystemClock_Config(void);
void PeriphCommonClock_Config(void);
static void MX_GPIO_Init(void);
static void MX_DMA_Init(void);
static void MX_SPI4_Init(void);
static void MX_I2S2_Init(void);
static void MX_I2S3_Init(void);

//SEND SPI DATA
uint8_t spi_data_send(int32_t data)
{

	if (spi_buffer_head <= SPI_BUFFER_SIZE-5)//BUFFER IS NOT FULL
	{
		//SERIALISE FLOAT
		int bit_shift_number = 24;
		for(int idx = 0; idx < 4;idx++)
		{
			*spi_buffer_pointer = data >> bit_shift_number;		//store next data bit
			spi_buffer_pointer++;			//point to next data bit location
			spi_buffer_head++;				//increment buffer size
			bit_shift_number -= 8;
		}
		*spi_buffer_pointer = '\n';		//store next data bit
		spi_buffer_pointer++;			//point to next data bit location
		spi_buffer_head++;
	}
	if (spi_buffer_head >= SPI_BUFFER_SIZE)//BUFFER IS FULL
	{
		if((spi_buffer_idx == 0)&&spi_tx_ready_flag)//BUFFER 0 IS FULL and buffer 1 has been transfered
		{
			spi_buffer_head = 0;					//set buffer head to 0
			spi_buffer_pointer = &spi_buffer_1[0];	//start filling buffer 1
			spi_buffer_idx = 1;						//set buffer 1 to input buffer

			spi_tx_ready_flag = 0; 					//tell system transmit is in process
			HAL_SPI_Transmit_DMA(&hspi4, (uint8_t*)spi_buffer_0, SPI_BUFFER_SIZE);//initiate dma transmit

		}
		else if((spi_buffer_idx == 1)&&spi_tx_ready_flag)//BUFFER 1 IS FULLand buffer 0 has been transfered
		{
			spi_buffer_head = 0;					//set buffer head to 0
			spi_buffer_pointer = &spi_buffer_0[0];	//start filling buffer 0
			spi_buffer_idx = 0;						//set buffer 0 to input buffer

			spi_tx_ready_flag = 0; 					//tell system transmit is in process
			HAL_SPI_Transmit_DMA(&hspi4, (uint8_t*)spi_buffer_1, SPI_BUFFER_SIZE);//initiate dma transmit
		}
		else if(!spi_tx_ready_flag)
		{
			return 0;
		}
	}
	return 1;
}

//BIRD ACTIVITY DETECTION
int BAD()
{
	//CALCULATE STE
	float ste = 0;
	for (int idx = 0; idx < FFT_BUFFER_SIZE; idx++)
	{
		ste = ste + (fft_input_buffer[idx]*fft_input_buffer[idx]);
	}

	//GET STE AVERAGE
	ste_avg_array[ste_avg_head] = ste;
	ste_avg_head++;
	if (ste_avg_head >= STE_AVG_SIZE)
	{
		ste_avg_head = 0;
	}

	float sum = 0;
	for (int idx = 0; idx < STE_AVG_SIZE; idx++)
	{
		sum += ste_avg_array[idx];
	}

	float ste_avg =(sum/STE_AVG_SIZE);
	if((ste_avg + (ste_avg * STE_AVG_THRESHOLD_OFFSET)) <= ste)
	{
		ste_frame_count = STE_FRAME_HOLD;
		HAL_GPIO_WritePin(LED_3_GPIO_Port, LED_3_Pin, 1);
		HAL_GPIO_WritePin(PIN_F0_GPIO_Port, PIN_F0_Pin, 1);
		return 1;
	}
	else if(ste_frame_count > 0)
	{
		ste_frame_count--;
		HAL_GPIO_WritePin(LED_3_GPIO_Port, LED_3_Pin, 1);
		HAL_GPIO_WritePin(PIN_F0_GPIO_Port, PIN_F0_Pin, 1);
		return 1;
	}
	else
	{
		HAL_GPIO_WritePin(LED_3_GPIO_Port, LED_3_Pin, 0);
		HAL_GPIO_WritePin(PIN_F0_GPIO_Port, PIN_F0_Pin, 0);
		return 0;
	}
}

//SPECTRAL SUBTRACTION
void spectral_subtraction()
{
	int activity = BAD();

	arm_rfft_fast_f32(&fft_handler, (float32_t*)fft_input_buffer, (float32_t*)fft_output_buffer, 0);

	//PHASE CORRECTION COEFFICIENT CALCULATION
	uint16_t buffer_index = 0;
	for(uint16_t i = 0 ; i< FFT_BUFFER_SIZE ; i = i + 2)
	{
		phases[buffer_index] = atan2(fft_output_buffer[i + 1],fft_output_buffer[i]);
		buffer_index++;
	}
	buffer_index = 0;

	//COMPUTE MAGNITUDES
	arm_cmplx_mag_f32(fft_output_buffer, magnitudes, FFT_BUFFER_SIZE/2);

	//UPDATE AVERAGE NOISE
	if(activity == 0)
	{
		for (int idx = 0; idx < (FFT_BUFFER_SIZE/2);idx++)
		{
			avg_noise_magnitudes[idx] = ((avg_noise_magnitudes[idx]  * (AVG_NOISE_ESTIMATE_LENGTH - 1)) / AVG_NOISE_ESTIMATE_LENGTH) + (magnitudes[idx] / AVG_NOISE_ESTIMATE_LENGTH);
		}
	}

	//SPECTRAL SUBTRACTION PROCESS
	for (int idx = 0; idx < (FFT_BUFFER_SIZE/2);idx++)
	{
		clean_magnitudes[idx] = magnitudes[idx] - avg_noise_magnitudes[idx];
	}

	//PHASE CORRECTION
	for(uint16_t i = 0 ; i< FFT_BUFFER_SIZE ; i++)
	{
		if((i % 2 ) == 0)
		{
			fft_output_buffer[i] = cos(phases[buffer_index])*clean_magnitudes[buffer_index];
		}
		else
		{
			fft_output_buffer[i] = sin(phases[buffer_index])*clean_magnitudes[buffer_index];
			buffer_index++;
		}
	}

	//INVERSE FFT TO RECONSTRUCT SIGNAL
	arm_rfft_fast_f32(&fft_handler, (float32_t*)fft_output_buffer, (float32_t*)fft_input_buffer, 1);

	//SPI TRANSFER
	int32_t data_to_transfer = 0;
	for (int idx = 0; idx < FFT_BUFFER_SIZE; idx++)
	{
		data_to_transfer = (int32_t)(FLOAT32_TO_INT32 * fft_input_buffer[idx]);
		spi_data_send(data_to_transfer);
	}
}

//PROCESS AUDIO DATA
void process_data(int m)
{
	i2s_rx_half_complete_flag = 0;
	i2s_rx_full_complete_flag = 0;

	int buffer_start = m * (BUFFER_SIZE/2);
	int buffer_end = buffer_start + (BUFFER_SIZE/2);
	int idx = 0;

	for (int position = buffer_start; position < buffer_end; position += 4)
	{
		left_sample[idx] = INT32_TO_FLOAT32 * ((int)(rx_buffer[position]<<16)|rx_buffer[position + 1]);
		right_sample[idx] = INT32_TO_FLOAT32 * ((int) (rx_buffer[position+2]<<16)|rx_buffer[position + 3]);

		fft_input_buffer[fft_idx] = left_sample[idx];
		fft_idx++;
		if(fft_idx == FFT_BUFFER_SIZE)
		{
			spectral_subtraction();
			fft_idx = 0;
		}
		idx++;
	}
}

//DMA CALLBACKS
void HAL_I2S_RxHalfCpltCallback(I2S_HandleTypeDef *hi2s)
{
	i2s_rx_half_complete_flag = 1;
	HAL_GPIO_WritePin(LED_1_GPIO_Port, LED_1_Pin,1);
}

void HAL_I2S_RxFullCpltCallback(I2S_HandleTypeDef *hi2s)
{
	i2s_rx_full_complete_flag = 1;
	HAL_GPIO_WritePin(LED_1_GPIO_Port, LED_1_Pin,1);
}

void HAL_SPI_TxCpltCallback(SPI_HandleTypeDef *hspi)
{
	spi_tx_ready_flag = 1;
}

//MAIN
int main(void)
{

  //INIT
  HAL_Init();
  SystemClock_Config();
  PeriphCommonClock_Config();
  MX_GPIO_Init();
  MX_DMA_Init();
  MX_SPI4_Init();
  MX_I2S2_Init();
  MX_USB_DEVICE_Init();
  MX_I2S3_Init();

  uint8_t startup_msg[20] = "PROGRAM STARTING\n";
  CDC_Transmit_FS(startup_msg, 20);
  HAL_GPIO_WritePin(LED_2_GPIO_Port, LED_2_Pin,1);

  HAL_I2S_Receive_DMA(&hi2s2, rx_buffer, BUFFER_SIZE/2);
  HAL_I2S_Transmit_DMA(&hi2s3, tx_buffer, BUFFER_SIZE/2);

  arm_rfft_fast_init_f32(&fft_handler, FFT_BUFFER_SIZE);

  //MAIN WHILE LOOP
  while (1)
  {
	  if (i2s_rx_half_complete_flag)
	  {
	  	process_data(0);
	  }
	  else if (i2s_rx_full_complete_flag)
	  {
	  	process_data(1);
	  }
  }
}

//CLOCK CONFIG
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};

  __HAL_RCC_PWR_CLK_ENABLE();
  __HAL_PWR_VOLTAGESCALING_CONFIG(PWR_REGULATOR_VOLTAGE_SCALE1);

  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSE;
  RCC_OscInitStruct.HSEState = RCC_HSE_ON;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
  RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSE;
  RCC_OscInitStruct.PLL.PLLM = 8;
  RCC_OscInitStruct.PLL.PLLN = 216;
  RCC_OscInitStruct.PLL.PLLP = RCC_PLLP_DIV2;
  RCC_OscInitStruct.PLL.PLLQ = 9;
  RCC_OscInitStruct.PLL.PLLR = 2;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }

  if (HAL_PWREx_EnableOverDrive() != HAL_OK)
  {
    Error_Handler();
  }

  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV4;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV2;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_7) != HAL_OK)
  {
    Error_Handler();
  }
}

//PERIPHERAL INIT
void PeriphCommonClock_Config(void)
{
  RCC_PeriphCLKInitTypeDef PeriphClkInitStruct = {0};

  PeriphClkInitStruct.PeriphClockSelection = RCC_PERIPHCLK_I2S;
  PeriphClkInitStruct.PLLI2S.PLLI2SN = 99;
  PeriphClkInitStruct.PLLI2S.PLLI2SP = RCC_PLLP_DIV2;
  PeriphClkInitStruct.PLLI2S.PLLI2SR = 2;
  PeriphClkInitStruct.PLLI2S.PLLI2SQ = 2;
  PeriphClkInitStruct.PLLI2SDivQ = 1;
  PeriphClkInitStruct.I2sClockSelection = RCC_I2SCLKSOURCE_PLLI2S;
  if (HAL_RCCEx_PeriphCLKConfig(&PeriphClkInitStruct) != HAL_OK)
  {
    Error_Handler();
  }
}


static void MX_I2S2_Init(void)
{

  hi2s2.Instance = SPI2;
  hi2s2.Init.Mode = I2S_MODE_MASTER_RX;
  hi2s2.Init.Standard = I2S_STANDARD_PHILIPS;
  hi2s2.Init.DataFormat = I2S_DATAFORMAT_24B;
  hi2s2.Init.MCLKOutput = I2S_MCLKOUTPUT_ENABLE;
  hi2s2.Init.AudioFreq = I2S_AUDIOFREQ_48K;
  hi2s2.Init.CPOL = I2S_CPOL_LOW;
  hi2s2.Init.ClockSource = I2S_CLOCK_PLL;
  if (HAL_I2S_Init(&hi2s2) != HAL_OK)
  {
    Error_Handler();
  }
}

static void MX_I2S3_Init(void)
{
  hi2s3.Instance = SPI3;
  hi2s3.Init.Mode = I2S_MODE_MASTER_TX;
  hi2s3.Init.Standard = I2S_STANDARD_PHILIPS;
  hi2s3.Init.DataFormat = I2S_DATAFORMAT_24B;
  hi2s3.Init.MCLKOutput = I2S_MCLKOUTPUT_DISABLE;
  hi2s3.Init.AudioFreq = I2S_AUDIOFREQ_48K;
  hi2s3.Init.CPOL = I2S_CPOL_LOW;
  hi2s3.Init.ClockSource = I2S_CLOCK_PLL;
  if (HAL_I2S_Init(&hi2s3) != HAL_OK)
  {
    Error_Handler();
  }
}

static void MX_SPI4_Init(void)
{
  hspi4.Instance = SPI4;
  hspi4.Init.Mode = SPI_MODE_SLAVE;
  hspi4.Init.Direction = SPI_DIRECTION_2LINES;
  hspi4.Init.DataSize = SPI_DATASIZE_8BIT;
  hspi4.Init.CLKPolarity = SPI_POLARITY_LOW;
  hspi4.Init.CLKPhase = SPI_PHASE_1EDGE;
  hspi4.Init.NSS = SPI_NSS_SOFT;
  hspi4.Init.FirstBit = SPI_FIRSTBIT_MSB;
  hspi4.Init.TIMode = SPI_TIMODE_DISABLE;
  hspi4.Init.CRCCalculation = SPI_CRCCALCULATION_DISABLE;
  hspi4.Init.CRCPolynomial = 7;
  hspi4.Init.CRCLength = SPI_CRC_LENGTH_DATASIZE;
  hspi4.Init.NSSPMode = SPI_NSS_PULSE_DISABLE;
  if (HAL_SPI_Init(&hspi4) != HAL_OK)
  {
    Error_Handler();
  }
}

static void MX_DMA_Init(void)
{
  __HAL_RCC_DMA1_CLK_ENABLE();
  __HAL_RCC_DMA2_CLK_ENABLE();
  HAL_NVIC_SetPriority(DMA1_Stream1_IRQn, 0, 0);
  HAL_NVIC_EnableIRQ(DMA1_Stream1_IRQn);
  HAL_NVIC_SetPriority(DMA1_Stream5_IRQn, 0, 0);
  HAL_NVIC_EnableIRQ(DMA1_Stream5_IRQn);
  HAL_NVIC_SetPriority(DMA2_Stream1_IRQn, 0, 0);
  HAL_NVIC_EnableIRQ(DMA2_Stream1_IRQn);

}

static void MX_GPIO_Init(void)
{
  GPIO_InitTypeDef GPIO_InitStruct = {0};
  __HAL_RCC_GPIOE_CLK_ENABLE();
  __HAL_RCC_GPIOF_CLK_ENABLE();
  __HAL_RCC_GPIOH_CLK_ENABLE();
  __HAL_RCC_GPIOC_CLK_ENABLE();
  __HAL_RCC_GPIOA_CLK_ENABLE();
  __HAL_RCC_GPIOB_CLK_ENABLE();
  HAL_GPIO_WritePin(PIN_F0_GPIO_Port, PIN_F0_Pin, GPIO_PIN_RESET);
  HAL_GPIO_WritePin(GPIOA, LED_1_Pin|LED_3_Pin, GPIO_PIN_RESET);
  HAL_GPIO_WritePin(LED_2_GPIO_Port, LED_2_Pin, GPIO_PIN_RESET);
  GPIO_InitStruct.Pin = PIN_F0_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(PIN_F0_GPIO_Port, &GPIO_InitStruct);
  GPIO_InitStruct.Pin = LED_1_Pin|LED_3_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
  GPIO_InitStruct.Pin = LED_2_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(LED_2_GPIO_Port, &GPIO_InitStruct);
}

//ERROR HANDLER
void Error_Handler(void)
{
  __disable_irq();
  while (1)
  {
  }
}

#ifdef  USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
     ex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */
