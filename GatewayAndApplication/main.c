#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>
#include <unistd.h>
#include <math.h>
#include <time.h>

#include "net/emcute.h"
#include "net/ipv6/addr.h"
#include "thread.h"

#include "xtimer.h"
#include "ztimer/periodic.h"

#ifndef EMCUTE_ID
#define EMCUTE_ID    ("gertrud")
#endif
#define EMCUTE_PRIO  (THREAD_PRIORITY_MAIN - 1)

#ifndef CONFIG_EMCUTE_DEFAULT_PORT
#define CONFIG_EMCUTE_DEFAULT_PORT    (1883U)
#endif

static char stack[THREAD_STACKSIZE_DEFAULT];
float currVal = 0.0;
float counter = 0.0;

static void *emcute_thread(void *arg)
{
    (void)arg;
    emcute_run(CONFIG_EMCUTE_DEFAULT_PORT, EMCUTE_ID);
    return NULL;
}

static int callback(void* arg)
{
    (void)arg;
    currVal = 1.2 * sin(counter) + 2.0;
    counter=counter+0.5;
    return 0;
}

int main(void)
{
    puts("Application to send sensor data to cloud\n");

    // periodic timer to call driver function
    static ztimer_periodic_t timer;
    ztimer_periodic_init(ZTIMER_MSEC, &timer, callback,  "test", 2000);
    ztimer_periodic_start(&timer);

    thread_create(stack, sizeof(stack), EMCUTE_PRIO, 0,
                  emcute_thread, NULL, "emcute");
    char *topic = NULL;
    char *message = NULL;
    size_t len = 0;

    sock_udp_ep_t gw = { .family = AF_INET6, .port = CONFIG_EMCUTE_DEFAULT_PORT };
    ipv6_addr_from_str((ipv6_addr_t *)&gw.addr.ipv6, "2001:660:5307:3000::68");
    gw.port = atoi("1885");

    topic = "sensorData";

    bool firstRun = true;

    time_t current_time;
    struct tm* time_info;
    char timestring[9];
    while(1)
    {
        // read sensor
        char newMsg[100];
        time(&current_time);
        time_info=localtime(&current_time);
        strftime(timestring, sizeof(timestring), "%H:%M:%S", time_info);
        sprintf(newMsg, "{\"Lux_Value\": %.2f,  \"timestamp\": \"", currVal);
        sprintf(newMsg + strlen(newMsg), "%s", timestring);
        sprintf(newMsg + strlen(newMsg), "\"}");
        message = newMsg;
        len = strlen(message);

        if(firstRun)
        {
            if(emcute_con(&gw, true, topic, message, len, 0) != EMCUTE_OK)
            {
                printf("unable to connect\n");
                break;
            }
            ztimer_sleep(ZTIMER_MSEC, 3000);
            firstRun = false;
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
        ztimer_sleep(ZTIMER_MSEC, 1000);
    }
    return 0;
}
