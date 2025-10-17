from hub import light_matrix, sound
import runloop

# Beeps every three seconds forever
async def beepEveryThreeSeconds():
    while True:
        await runloop.sleep_ms(3000)# wait for three seconds
        sound.beep()# play a beep

# Heart beats every two seconds forever
async def heartBeatEveryTwoSeconds():
    while True:
        await runloop.sleep_ms(1000)
        light_matrix.show_image(light_matrix.IMAGE_HEART)
        await runloop.sleep_ms(1000)
        light_matrix.clear()

# Run both concurrently
runloop.run(
    beepEveryThreeSeconds(),
    heartBeatEveryTwoSeconds()
)
