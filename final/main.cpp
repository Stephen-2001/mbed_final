#include "mbed.h"
#include "bbcar.h"
#include "mbed_rpc.h"
#include <string.h>


Ticker servo_ticker;
Timer t;
PwmOut pin5(D5), pin6(D6);
DigitalInOut ping(D11);
BufferedSerial pc(USBTX,USBRX); //tx,rx
BufferedSerial uart(D10 ,D9); //tx,rx
BufferedSerial xbee(D1, D0);
BBCar car(pin5, pin6, servo_ticker);

void rotate();
void pingrun(Arguments *in, Reply *out);
RPCFunction rpcping(&pingrun, "pingcheck");
int main() {
    // The mbed RPC classes are now wrapped to create an RPC enabled version - see RpcClasses.h so don't add to base class
    // receive commands, and send back the responses
    xbee.set_baud(9600);
    char buf[256], outbuf[256];
    FILE *devin = fdopen(&uart, "r");
    FILE *devout = fdopen(&uart, "w");

    while(1) {
        char cmp[10] = "finish\n";
        memset(buf, 0, 256);      // clear buffer
        for(int i=0; ; i++) {
            char recv = fgetc(devin);
            if (recv == '\n') {
                printf("\r\n");
                break;
            }
            buf[i] = fputc(recv, devout);
        }
        if (buf[0] == 'f') {
            xbee.write("FINISH\n", 8);
            // break;
        }
        //Call the static call method on the RPC class
        RPC::call(buf, outbuf);
        printf("%s\r\n", outbuf);
    }
}

void pingrun(Arguments *in, Reply *out) {
    float val;
    pc.set_baud(9600);
    float distance;
    bool rotate_check = false;
    ThisThread::sleep_for(10s);
    xbee.write("Ready\n", 7);
    xbee.write("Start\n", 7);
    ThisThread::sleep_for(1s);
    while(!rotate_check) {
        ping.output();
        ping = 0; wait_us(200);
        ping = 1; wait_us(5);
        ping = 0; wait_us(5);

        ping.input();
        while(ping.read() == 0);
        t.start();
        while(ping.read() == 1);
        val = t.read();
        distance = val * 17700.4f;
        printf("Ping = %lf\r\n", distance);
        if (distance < 20 && distance > 10) {
            xbee.write("Obstacle\n", 10);
            car.stop();
            ThisThread::sleep_for(5s);
            rotate_check = true;
        } else {
            car.goStraight(30);
        }
        // printf("Ping = %lf\r\n", val*17700.4f);
        t.stop();
        t.reset();

        ThisThread::sleep_for(100ms);
    }
    rotate();
}

void rotate() {
    xbee.write("Rotate\n", 8);
    car.turn(30, -0.01);
    ThisThread::sleep_for(3s);
    car.turn(55, 0.6);
    ThisThread::sleep_for(16s);
    car.stop();
    return ;
}
   
