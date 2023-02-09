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

#include "lsm303dlhc.h"
#include "lsm303dlhc_params.h"

#include "xtimer.h"
#include "ztimer/periodic.h"

#ifndef EMCUTE_ID
#define EMCUTE_ID    ("gertrud")
#endif
#define EMCUTE_PRIO  (THREAD_PRIORITY_MAIN - 1)

#ifndef CONFIG_EMCUTE_DEFAULT_PORT
#define CONFIG_EMCUTE_DEFAULT_PORT    (1883U)
#endif

#define MAX_COUNT_VAL 100000.0

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
    currVal = 1.2 * sin(counter) + 30.0;
    if(counter < MAX_COUNT_VAL)
    {
        counter=counter+0.5;
    }
    else
    {
        counter = 0.0;
    }
    return 0;
}

static lsm303dlhc_t lsm303dlhc;

int main(void)
{
    // initialize real acceleration sensor
    lsm303dlhc_init(&lsm303dlhc, &lsm303dlhc_params[0]);

    // periodic timer to call fake driver function
    static ztimer_periodic_t timer;
    ztimer_periodic_init(ZTIMER_MSEC, &timer, callback,  "test", 500);
    ztimer_periodic_start(&timer);

    thread_create(stack, sizeof(stack), EMCUTE_PRIO, 0, emcute_thread, NULL, "emcute");

    char *topic = NULL;
    char *messageFake = NULL;
    size_t lenFake = 0;
    char *messageReal = NULL;
    size_t lenReal = 0;

    sock_udp_ep_t gw = { .family = AF_INET6, .port = CONFIG_EMCUTE_DEFAULT_PORT };
    ipv6_addr_from_str((ipv6_addr_t *)&gw.addr.ipv6, "2001:660:5307:3000::5");
    gw.port = atoi("1885");

    topic = "sensorData";

    bool firstRun = true;

    time_t current_time;
    struct tm* time_info;
    char timestring[9];
    while(1)
    {
        // read real acceleration sensor
        char realMsg[100];
        lsm303dlhc_3d_data_t acc_value;
        lsm303dlhc_read_acc(&lsm303dlhc, &acc_value);

        char fakeLightMsg[100];

        time(&current_time);
        time_info=localtime(&current_time);
        strftime(timestring, sizeof(timestring), "%H:%M:%S", time_info);

        // prepare fake data message in json format
        sprintf(fakeLightMsg, "{\"Lux_ValueFake\": %.2f,  \"timestamp\": \"", currVal);
        sprintf(fakeLightMsg + strlen(fakeLightMsg), "%s", timestring);
        sprintf(fakeLightMsg + strlen(fakeLightMsg), "\"}");
        messageFake = fakeLightMsg;
        lenFake = strlen(messageFake);

        // prepare real data message in json format
        sprintf(realMsg, "{\"AccelY\": %i, \"timestamp\": \"", acc_value.y_axis);
        sprintf(realMsg + strlen(realMsg), "%s", timestring);
        sprintf(realMsg + strlen(realMsg), "\"}");
        messageReal = realMsg;
        lenReal = strlen(messageReal);

        if(firstRun)
        {   //connect only it first run
            if(emcute_con(&gw, true, topic, messageFake, lenFake, 0) != EMCUTE_OK)
            {
                printf("unable to connect\n");
                break;
            }
            //ztimer_sleep(ZTIMER_MSEC, 2000);
            firstRun = false;
        }

        emcute_topic_t t;
        unsigned flags = EMCUTE_QOS_0;
        t.name = topic;
        if (emcute_reg(&t) != EMCUTE_OK)
        {
            puts("error: unable to obtain topic ID");
            break;
        }

        if(emcute_pub(&t, messageFake, lenFake, flags) != EMCUTE_OK)
        {
            printf("error: unable to publish data on topic\n");
            break;
        }

        //ztimer_sleep(ZTIMER_MSEC, 250);

        if(emcute_pub(&t, messageReal, lenReal, flags) != EMCUTE_OK)
        {
            printf("error: unable to publish data on topic\n");
            break;
        }

        ztimer_sleep(ZTIMER_MSEC, 1500);
    }
    return 0;
}
