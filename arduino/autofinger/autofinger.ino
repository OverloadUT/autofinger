#include <LiquidCrystal.h>
#include <Servo.h>

LiquidCrystal lcd(8,7,4,2,1,0);
Servo servo1;
Servo servo2;

char command[32];

char prevCommand[32] = { '1','2','3','4','1','2','3','4','1','2','3','4','1','2','3','4','1','2','3','4','1','2','3','4','1','2','3','4','1','2','3','4' };
String parsedCommand;
int parsedServoDegreeOne = 90;
int parsedServoDegreeTwo = 90;
String parsedLCDMessageTop = "1234123412341234";
String parsedLCDMessageBot = "1234123412341234";
int parsedLEDRed = 0;
int parsedLEDGreen = 0;
int parsedLEDBlue = 0;

String parseCommand(char cmd[])
{
  String temp = "";
  int i=0;
  
  //parse instruction
  for(; i<8; i++)
  {
    temp += cmd[i];
  }
  return temp; 
}

int parseLEDRed(char cmd[])
{
  String temp = "";
  int i=14;
  
  //parse instruction
  for(; i<17; i++)
  {
    temp += cmd[i];
  }
  return temp.toInt();
}

int parseLEDBlue(char cmd[])
{
  String temp = "";
  int i=20;
  
  //parse instruction
  for(; i<23; i++)
  {
    temp += cmd[i];
  }
  return temp.toInt();
}

int parseLEDGreen(char cmd[])
{
  String temp = "";
  int i=17;
  
  //parse instruction
  for(; i<20; i++)
  {
    temp += cmd[i];
  }
  return temp.toInt();
}

int parseServoDegreeOne(char cmd[])
{
  String temp = "";
  int i=8;
  
  //parse instruction
  for(; i<11; i++)
  {
    temp += cmd[i];
  }
  return temp.toInt();
}

int parseServoDegreeTwo(char cmd[])
{
  String temp = "";
  int i=11;
  
  //parse instruction
  for(; i<14; i++)
  {
    temp += cmd[i];
  }
  return temp.toInt();
}

String parseLCDMessage(char cmd[])
{
  String temp = "";
  int i=8;
  
  for(; i<24; i++)
  {
    temp += cmd[i];
  }
  //Serial.println(temp);
  return temp; 
}

// writes a string to a row on the display
// 0 for top row
// 1 for bottom row
void writeToDisplay(String text, int row)
{
    lcd.setCursor(0,row); 
    lcd.print("                ");
    lcd.setCursor(0,row);
    lcd.print(text);
}

void moveServos(int degreeOne, int degreeTwo)
{
  degreeOne = constrain(degreeOne,0,180);
  degreeTwo = constrain(degreeTwo,0,180);
  servo1.write(degreeOne);
  servo2.write(degreeTwo);
  //Serial.println("servo movement complete");
}

void setLEDColor(int r, int b, int g)
{
  constrain(r, 0, 255);
  constrain(g, 0, 255);
  constrain(b, 0, 255);
  analogWrite(9,b);
  analogWrite(10,r);
  analogWrite(11,g);
}

void stateDump()
{
  for(int i=0; i<32;i++)
  {
    //Serial.print(prevCommand[i]);
  }
  //Serial.print("|");
  //Serial.print(parsedCommand);
  //Serial.print("|");
  //Serial.print(parsedServoDegreeOne);
  //Serial.print("|");
  //Serial.print(parsedServoDegreeTwo);
  //Serial.print("|");
  //Serial.print(parsedLCDMessageTop);
  //Serial.print("|");
  //Serial.print(parsedLCDMessageBot);
  //Serial.print("|");
  //Serial.print(parsedLEDRed);
  //Serial.print("|");
  //Serial.print(parsedLEDGreen);
  //Serial.print("|");
  //Serial.println(parsedLEDBlue);
}

void setup()
{
  pinMode(8,OUTPUT);
  
  lcd.begin(16, 2);

  lcd.clear();
 
  servo1.attach(5);
  servo2.attach(6);
 
  Serial.begin(9600);
  //Serial.println("please input something.");
}

void loop()
{
  if(Serial.available())
  {
    Serial.readBytesUntil('|', command, 32);
    parsedCommand = parseCommand(command);
    //Serial.println(parsedCommand);
    
    if (parsedCommand.equalsIgnoreCase("allinone"))
    {
      parsedLEDRed = parseLEDRed(command);
      parsedLEDGreen = parseLEDGreen(command);
      parsedLEDBlue = parseLEDBlue(command);
      parsedServoDegreeOne = parseServoDegreeOne(command);
      parsedServoDegreeTwo = parseServoDegreeTwo(command);
      setLEDColor(parsedLEDRed,parsedLEDGreen,parsedLEDBlue);
      moveServos(parsedServoDegreeOne, parsedServoDegreeTwo);
    }
    else if(parsedCommand.equalsIgnoreCase("movsrvos"))
    {
      parsedServoDegreeOne = parseServoDegreeOne(command);
      parsedServoDegreeTwo = parseServoDegreeTwo(command);
      moveServos(parsedServoDegreeOne, parsedServoDegreeTwo);
    }
    else if(parsedCommand.equalsIgnoreCase("stledcol"))    
    {
       parsedLEDRed = parseLEDRed(command);
       parsedLEDGreen = parseLEDGreen(command);
       parsedLEDBlue = parseLEDBlue(command);
       //Serial.println(parsedLEDRed);
       //Serial.println(parsedLEDGreen);
       //Serial.println(parsedLEDBlue);
       setLEDColor(parsedLEDRed,parsedLEDGreen,parsedLEDBlue);
    }
    else if(parsedCommand.equalsIgnoreCase("statdump"))    
    {
      stateDump();
    }
    
    for(int i=0;i<32;i++)
    {
      prevCommand[i] = command[i];
      command[i] = '_';
    }
  } 
}
