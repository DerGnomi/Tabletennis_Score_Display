//**************************************************************//
//  Name    : 7 Segment LED with IR Transmitter
//  Author  : Dominic Hößl
//  Date    : 15 Sep 2018
//  Modified: 15 Mar 2018
//  Version : 1.0
//  Notes   : Code for controlling 2 7 Segment LEDs            //
//          : with IR Transmitter
//****************************************************************
#include <IRremote.h>

//Pin connected to ST_CP of 74HC595
const int latchPin = 8;
//Pin connected to SH_CP of 74HC595
const int clockPin = 12;
////Pin connected to DS of 74HC595
const int dataPin = 11;

//IR Transmitter config
const int RECV_PIN = 7;
IRrecv irrecv(RECV_PIN);
decode_results results;

unsigned long key_value = 0;

unsigned int numbers[100] = {61404, 60996, 61304, 61292, 61156, 61356, 61372, 61252, 61436, 61420, 9180, 8772, 9080, 9068, 8932, 9132, 9148, 9028, 9212, 9196, 48604, 48196, 48504, 48492, 48356, 48556, 48572, 48452, 48636, 48620, 47068, 46660, 46968, 46956, 46820, 47020, 47036, 46916, 47100, 47084, 29660, 29252, 29560, 29548, 29412, 29612, 29628, 29508, 29692, 29676, 55260, 54852, 55160, 55148, 55012, 55212, 55228, 55108, 55292, 55276, 57308, 56900, 57208, 57196, 57060, 57260, 57276, 57156, 57340, 57324, 41948, 41540, 41848, 41836, 41700, 41900, 41916, 41796, 41980, 41964, 65500, 65092, 65400, 65388, 65252, 65452, 65468, 65348, 65532, 65516, 63452, 63044, 63352, 63340, 63204, 63404, 63420, 63300, 63484, 63468 };
unsigned int currentnumber = 0;
//Control 1 für rechts / 2 für links
int control = 0;
int nl = 0;
int nr = 0;


void setup() {
  //Debuggingconsole
  Serial.begin(9600);
  //Set up the IR transmitter
  irrecv.enableIRIn();
  irrecv.blink13(true);
  //Treiber Pins als Ausgabe setzen
  pinMode(latchPin, OUTPUT);
  pinMode(clockPin, OUTPUT);
  pinMode(dataPin, OUTPUT);
}

void loop() {
  //Zahl an den LED Treiber übergeben
  digitalWrite(latchPin, LOW);
  //da jeder Treiber nur 8 Bit halten kann muss man die Zahl teilen und getrennt übergeben
  shiftOut(dataPin, clockPin, LSBFIRST, numbers[currentnumber]+control);
  shiftOut(dataPin, clockPin, LSBFIRST, numbers[currentnumber]+control >> 8);
  digitalWrite(latchPin, HIGH);
  delay(500);
  //Revicing IR signal
  if (irrecv.decode(&results)){
    Serial.println(results.value, HEX);
    if( results.value == 0XFFFFFFFF ){
      //Wiederholten aufruf abfangen
      results.value = key_value;
    }
    //Nummer auswählen
    if( control == 1 || control == 2 ){
      switch(results.value){
        case 0xFF38C7:
          control = 0;
          break;
        case 0x488F3CBB:
          control = 0;
          break;
        case 0xFF9867:
          if( control == 2 )
            nl = 0;
          else
            nr = 0;
          break;
        case 0x97483BFB:
          if( control == 2 )
            nl = 0;
          else
            nr = 0;
          break;
        case 0xFFA25D:
          if( control == 2 )
            nl = 10;
          else
            nr = 1;
          break;
        case 0xE318261B:
          if( control == 2 )
            nl = 10;
          else
            nr = 1;
          break;
        case 0xFF629D:
          if( control == 2 )
            nl = 20;
          else
            nr = 2;
          break;
        case 0x511DB:
          if( control == 2 )
            nl = 20;
          else
            nr = 2;
          break;
        case 0xFFE21D:
          if( control == 2 )
            nl = 30;
          else
            nr = 3;
          break;
        case 0xEE886D7F:
          if( control == 2 )
            nl = 30;
          else
            nr = 3;
          break;
        case 0xFF22DD:
          if( control == 2 )
            nl = 40;
          else
            nr = 4;
          break;
        case 0x52A3D41F:
          if( control == 2 )
            nl = 40;
          else
            nr = 4;
          break;
        case 0xFF02FD:
          if( control == 2 )
            nl = 50;
          else
            nr = 5;
          break;
        case 0xD7E84B1B:
          if( control == 2 )
            nl = 50;
          else
            nr = 5;
          break;
        case 0xFFC23D:
          if( control == 2 )
            nl = 60;
          else
            nr = 6;
          break;
        case 0x20FE4DBB:
          if( control == 2 )
            nl = 60;
          else
            nr = 6;
          break;
        case 0xFFE01F:
          if( control == 2 )
            nl = 70;
          else
            nr = 7;
          break;
        case 0xF076C13B:
          if( control == 2 )
            nl = 70;
          else
            nr = 7;
          break;
        case 0xFFA857:
          if( control == 2 )
            nl = 80;
          else
            nr = 8;
          break;
        case 0xA3C8EDDB:
          if( control == 2 )
            nl = 80;
          else
            nr = 8;
          break;
        case 0xFF906F:
          if( control == 2 )
            nl = 90;
          else
            nr = 9;
          break;
        case 0xE5CFBD7F:
          if( control == 2 )
            nl = 90;
          else
            nr = 9;
          break;
        default:
          break;
      }
      if( nr+nl != currentnumber)
        control = 0;
      currentnumber = nl+nr;
    }
    else if (results.value == 0xFF10EF	|| results.value == 0x8C22657B){
      //links Seite aktivieren
      control = 2;
    }
    else if (results.value == 0xFF5AA5	|| results.value == 0x449E79F){
      //rechte Seite aktivieren
      control = 1;
    }
    else if (results.value == 0xFFB04F	|| results.value == 0xF0C41643){
      //rechte Seite +1
      if ( nr < 9){
        nr = nr+1;
      }
      else{
        nr = 0;
      }
      currentnumber = nl+nr;
    }
    else if (results.value == 0xFF6897	|| results.value == 0xC101E57B){
      //linke Seite +1
      if(nl < 90){
        nl = nl+10;
      }
      else{
        nl = 0;
      }
      currentnumber = nl+nr;
    }
    else if (results.value == 0xFF4AB5	|| results.value == 0x1BC0157B){
      //Reset button down
      control = 0;
      nl = 0;
      nr = 0;
      currentnumber = 0;
    }

    //letzten Empfangen Tastendruck speichern
    key_value = results.value;
    //IR reciver Zurücksetzen
    irrecv.resume();
  }

}
