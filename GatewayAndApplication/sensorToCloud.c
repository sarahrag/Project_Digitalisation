#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#include "net/emcute.h"
#include "net/ipv6/addr.h"

#ifndef EMCUTE_ID
#define EMCUTE_ID    ("gertrud")
#endif

#ifndef CONFIG_EMCUTE_DEFAULT_PORT
#define CONFIG_EMCUTE_DEFAULT_PORT    (1883U)

int main(void)
{
    puts("Application to send sensor data to cloud\n");

    char *topic = NULL;
    char *message = NULL;
    size_t len = 0;

    sock_udp_ep_t gw = { .family = AF_INET6, .port = CONFIG_EMCUTE_DEFAULT_PORT };
    ipv6_addr_from_str((ipv6_addr_t *)&gw.addr.ipv6, "2001:660:5307:3000::68");
    gw.port = atoi("1885");

    topic = "sensorData";

    bool firstRun = true;

    while(1)
    {
        // read sensor
        int currVal = 30;
        char newMsg[20];
        sprintf(newMsg, "Lux Value: %d", currVal);
        message = newMsg;
        len = strlen(message);

        if(firstRun)
        {
            if(emcute_con(&gw, true, topic, message, len, 0) != EMCUTE_OK)
            {
                printf("unable to connect\n");
                break;
            }
        }
        else
        {
            emcute_topic_t t;
            unsigned flags = EMCUTE_QOS_0;
            t.name = topic;
            if (emcute_reg(&t) != EMCUTE_OK)
            {
                puts("error: unable to obtain topic ID");
                break;
            }

            if(emcute_pub(&t, message, len, flags) != EMCUTE_OK)
            {
                printf("error: unable to publish data on topic\n");
                break;
            }
        }
    }
    return 0;
}
