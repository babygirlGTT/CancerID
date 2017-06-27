import time, os 
import diagnose_test

def re_exe(cmd, inc = 30): 
    while True: 
        os.system(cmd); 
        diagnose_test.main() 
        time.sleep(inc) 
    
re_exe("echo %time%", 60)
