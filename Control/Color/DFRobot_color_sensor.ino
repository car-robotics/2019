int s0=3,s1=4,s2=5,s3=6;
int out=2;
int flag=0;
byte counter=0;
byte countR=0,countG=0,countB=0;
const int calibration = 95;
void setup()
 {
 Serial.begin(115200);
 pinMode(s0,OUTPUT);
 pinMode(s1,OUTPUT); 
 pinMode(s2,OUTPUT);
 pinMode(s3,OUTPUT);

 }
void TCS()
 {
 flag=0;  
 digitalWrite(s1,HIGH);
 digitalWrite(s0,HIGH);
 digitalWrite(s2,LOW);
 digitalWrite(s3,LOW);
 attachInterrupt(0, ISR_INTO, CHANGE);
 timer0_init();

 }
void ISR_INTO()
 {
 counter++;
 }
 void timer0_init(void)
 {
  TCCR2A=0x00;
  TCCR2B=0x07;   //the clock frequency source 1024 points
  TCNT2= 100;    //10 ms overflow again
  TIMSK2 = 0x01; //allow interrupt
 }
 int i=0;
 ISR(TIMER2_OVF_vect)//the timer 2, 10ms interrupt overflow again. Internal overflow interrupt executive function
{
    TCNT2=100;
    flag++;
 if(flag==1)
  {
    countR=counter;
    Serial.print("red: ");
    Serial.print(countR,DEC);
    Serial.print(" ");
    digitalWrite(s2,HIGH);
    digitalWrite(s3,HIGH);
  }
  else if(flag==2)
   {
    countG=counter;
    Serial.print("green: ");
    Serial.print(countG,DEC);
    Serial.print(" ");
    digitalWrite(s2,LOW);
    digitalWrite(s3,HIGH);
   }
   else if(flag==3)
    {
    countB=counter;
    Serial.print("blue: ");
    Serial.println(countB,DEC);
    Serial.print(" ");
    Serial.println("\n"); 
    digitalWrite(s2,LOW);
    digitalWrite(s3,LOW);
   
    }
    else if(flag==4)
     {
     if(countR > calibration || countG > calibration || countB > calibration) {
     
     if(countR > countG && countR > countB) {
        if(countG > countB) Serial.println("YELLOW");
        else Serial.println("RED");}
     else if(countB > countR && countB > countG) Serial.println("BLUE"); //lacks the 100 delay
     else if(countG > countR && countG > countB) Serial.println("GREEN"); //lacks the 100 delay
     }
     else Serial.println("I DUNNO");
     
     flag=0;
     
     }
       counter=0;
}
void loop()
 {
  TCS();
while(1);
 }

