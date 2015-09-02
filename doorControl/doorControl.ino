#if 0
#include <SPI.h>
#include <PN532_SPI.h>
#include <PN532.h>
#include <NfcAdapter.h>

PN532_SPI pn532spi(SPI, 10);
NfcAdapter nfc = NfcAdapter(pn532spi);
#else

#include <Wire.h>
#include <PN532_I2C.h>
#include <PN532.h>
#include <NfcAdapter.h>

PN532_I2C pn532_i2c(Wire);
NfcAdapter nfc = NfcAdapter(pn532_i2c);
#endif

byte door = 0b11010000; //door byte
byte lock = 0b00000001; //denotes door is unlocked
byte open = 0b00000010; //denotes door is opened
byte bell = 0b00000100; //denotes doorbell is pressed
byte legit = 0b00001000; //denotes legitimate key used to open door

int doorbell = 8;
int doorstatus = 9;
unsigned int doorTimer = 0;
unsigned int lockTimer = 0;
unsigned int bellTimer = 0;
unsigned int Timer = 0;

byte uid[4] = {0xA3,0x68,0x65,0xD0};
NfcTag validTag = NfcTag(uid, 4, "Mifare Classic");

void setup(){
  Serial.begin(9600);
  nfc.begin(false);
  pinMode(doorbell, INPUT_PULLUP);
  pinMode(doorstatus, INPUT_PULLUP);
}

void loop(){
//Check for the doorbell being pressed
  if(digitalRead(doorbell) == LOW){
    if((bellTimer % 5) == 0){
    Serial.write(door | bell);
    //Serial.println("Someone is at the door");
    }
    bellTimer ++;
  }
  else
    bellTimer = 0;
//Check for a keycard being used
  if(nfc.tagPresent(75))
  {
    if((lockTimer % 30) == 0)
    {
    NfcTag tag = nfc.read();  
    //Check if keycard legit
    if(tag == validTag)
    {
      Serial.write(door | lock | legit);  
      //Serial.println("key legit, door unlocked");
    }
    else
    {
      Serial.write(door | legit);
      //Serial.println("key invalid, dorr not unlocked");
    }
    }
    lockTimer ++;
  }
  else
    lockTimer = 0;
//Check for the door open
  if(digitalRead(doorstatus) == HIGH)
  {
    if((doorTimer % 5) == 0)
    {
      Serial.write(door | open );
      //Serial.println("The door is open");
    }
    doorTimer ++;
  }
  else
    doorTimer = 0;
  if((doorTimer + lockTimer + bellTimer) == 0)
  {
    if((Timer % 25) == 0)
    {
      //Serial.println(Timer);
      Serial.write(door);
      //Serial.println("Nothing is happening");
    }
    Timer ++;
  }
  else
    Timer = 0;
}
