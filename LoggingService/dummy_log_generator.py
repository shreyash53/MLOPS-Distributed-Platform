from time import sleep
import log_generator

for i in range(10):
    log_generator.send_log('ERR', 'Dummy log generated')
    sleep(3)