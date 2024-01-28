from rcon.source import Client
import psutil
import subprocess
import time
import logging
import configparser
import threading

# 配置日志记录
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

#获取服务器控制器插件的配置参数
config = configparser.ConfigParser()
config.read('rconControllerConfig.ini')
path = config.get('Sever Http Controller Config', 'palSeverPath')
rconPort = config.get('Sever Http Controller Config','rconPort')
password = config.get('Sever Http Controller Config','adminPassword')
processName = config.get('Sever Http Controller Config','severProcessName')
# 检查是否存在名为"pal"的进程
def check_process_exists():
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == processName:
            return True
    return False

#等待重启服务器的线程运行指示参数
is_reStart_thread_running = False

def callRcon(command):
    if check_process_exists():      
        with Client('localhost', int(rconPort), passwd=password) as client:
            response = client.run(command)
        return response
    else:
        logging.error('sever not start...')
        return 'Sever not start...'

def reStartSever(waitTime,msg,isRestart):
    if isRestart=='1' and is_reStart_thread_running:
        response = 'Error: Sever is Restarting.Please wait until sever restart finish'
        logging.error('restart thread is running...')
        return response
    response = callRcon('Shutdown '+waitTime+' '+ msg)
    if isRestart=='1' and not response=='Sever not start...':
        #异步等待服务器关闭后重启服务器
        def async_process():
            global is_reStart_thread_running
            is_reStart_thread_running = True
            while True:
                time.sleep(1)
                if not check_process_exists():
                    logging.info("path:" + path)
                    subprocess.Popen(path)
                    break
            is_reStart_thread_running = False

        thread = threading.Thread(target=async_process)
        thread.start()
    return response
    

def startSever():
    if check_process_exists():
        logging.error('sever already start...')
        response = 'Error:Game sever already start....'
    else:
        logging.info("path:"+path)
        subprocess.Popen(path)
        response = 'Game sever start...'
    return response

def showPlayers():
    return callRcon('ShowPlayers')

def saveGame():
    return callRcon('Save')

def showSeverInfo():
    return callRcon('Info')

def showSeverMemory():
    # 获取内存占用情况
    memory = psutil.virtual_memory()
    # To Json
    memory_dict = {
    'total': memory.total,
    'available': memory.available,
    'used': memory.used,
    'percent': memory.percent
    }
    return memory_dict

#Test
# if __name__ == '__main__':
#     print(showSeverMemory())