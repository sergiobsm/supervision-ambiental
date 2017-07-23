#include <16f877.h>  
#device adc= 10
#fuses XT,NOWDT
#use delay(clock=4M)
#use i2c(SLAVE,SDA=PIN_C4,FAST,SCL=PIN_C3,ADDRESS=0x48,NOFORCE_SW)
#use standard_io(b)
#rom 0x2100={51,31,5,21,12,252}
float Humedad,temperatura,ruido,CO,UV; 
int r;
int i=0;


void main(){
   setup_adc_ports(ALL_analog);
   setup_adc(ADC_CLOCK_INTERNAL);
   enable_interrupts(INT_SSP);       
   enable_interrupts(GLOBAL);
   output_high(PIN_B5);
   delay_ms(500);

   i=0;
   while (TRUE){         
      output_low(PIN_B4); 
      delay_ms(1000);
      output_high(PIN_B4);
      delay_ms(1000);
   }
}

#INT_SSP
void ssp_interrupt(){
   i2c_write(read_eeprom(i));
   i++;
   if(i==6)i=0;
      set_adc_channel(0);
      delay_us(20);
      Humedad=read_adc()*250.0/1023.0;
      r=Humedad*1;
      write_eeprom(0,r);
      
      set_adc_channel(1);
      delay_us(20);
      temperatura=read_adc()*250.0/1023.0;
      r=temperatura*1;
      write_eeprom(1,r);
      
      set_adc_channel(2);
      delay_us(20);
      ruido=read_adc()*250.0/1023.0;
      r=ruido*1;
      write_eeprom(2,r);
      
      set_adc_channel(3);
      delay_us(20);      
      CO=read_adc()*250.0/1023.0;    
      r=CO*1;
      write_eeprom(3,r);
      
      set_adc_channel(4);      
      delay_us(20);      
      UV=read_adc()*250.0/1023.0;
      r=UV*1;
      write_eeprom(4,r);
}

