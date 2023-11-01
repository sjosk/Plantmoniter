#include <ESP8266WiFi.h>
#include <ESP8266WiFiAP.h>
#include <ESP8266WiFiGeneric.h>
#include <ESP8266WiFiMulti.h>
#include <ESP8266WiFiScan.h>
#include <ESP8266WiFiSTA.h>
#include <ESP8266WiFiType.h>
#include <WiFiClient.h>
#include <WiFiClientSecure.h>
#include <WiFiServer.h>
#include <WiFiUdp.h>
#include "SlackWebhook.h"

SlackWebhook::SlackWebhook(const char* _host, String _url, const char* _fingerprint){
  host = "hooks.slack.com";
  url = "https://hooks.slack.com/services/TOKEN";
  fingerprint = "‎‎ab f0 5b a9 1a e0 ae 5f ce 32 2e 7c 66 67 49 ec dd 6d 6a 38";
}

boolean SlackWebhook::postMessageToSlack(String postData){
    Serial.println("Creating client connection to host..");
  WiFiClientSecureBearSSL wifiClient;

    if(!client.connect(host, 443)){
      Serial.println("SlackWebhook: could not connect to host");
      Serial.print("Host: ");
      Serial.print(host);

      return false;
    }
    Serial.println("Client connection successful!");
    Serial.print("Connected to ");
    Serial.print(host);
    Serial.println();
    
    Serial.println("Verifying SSL fingerprint..");
    //Ignore the error here
    wifiClient.setFingerprint(fingerprint);

    //fingerprint verification complete
    //build POST request..        
    int dataLength = postData.length();
      
    //build the POST string..
    String POST =    "POST " + url +" HTTP/1.1\r\n"
                     "Host: " + host + "\r\n"
                     "User-Agent: ArduinoIoT/1.0\r\n"
                     "Connection: close\r\n"
                     "Content-Type: application/x-www-form-urlencoded\r\n"
                     "Content-Length: " + dataLength + "\r\n\r\n"
                     "" + postData;

    Serial.println("Writing POST request to client..");
    client.print(POST);
    delay(500);

    Serial.println();
    while(client.available()) {
      Serial.println(client.readStringUntil('\r'));
    }

    delay(500);
    Serial.print("POST request complete!");
    return true;
}
