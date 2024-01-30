import os
from rcon.source import Client
import psutil
import subprocess
import time
import logging
import configparser
import threading
import shutil
from datetime import datetime,timedelta

# 配置日志记录
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

#获取服务器控制器插件的配置参数
config = configparser.ConfigParser()
config.read('rconControllerConfig.ini')
path = config.get('Sever Http Controller Config', 'palSeverPath')
backupFolder = os.path.join(os.path.dirname(path),'backupSaved')
backup_folders = os.listdir(backupFolder)
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

#服务器关闭备份存档的线程运行指示参数
is_backup_thread_running = False
#上一次备份时间
lastest_backup_dateTime = None


def callRcon(command):
    logging.info('call rcon command:'+command)
    if check_process_exists():      
        with Client('localhost', int(rconPort), passwd=password) as client:
            response = client.run(command)
        return response
    else:
        logging.error('sever not start...')
        return 'Sever not start...'

def reStartSever(waitTime,msg,isRestart):
    logging.info('reStartSever() working...')
    if is_backup_thread_running:
        response = 'Error: system is backing up saved'
        logging.error('Error: system is backing up saved')
        return response
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
    logging.info('startSever() working...')
    if is_backup_thread_running:
        response = 'Error: system is backing up saved'
        logging.error('Error: system is backing up saved')
        return response
    if check_process_exists():
        logging.error('sever already start...')
        response = 'Error:Game sever already start....'
    else:
        logging.info("path:"+path)
        subprocess.Popen(path)
        response = 'Game sever start...'
    return response

def showPlayers():
    logging.info('showPlayers() working...')
    response = callRcon('ShowPlayers')
    logging.info('show players success...')
    return response

def saveGame():
    logging.info('saveGame() working...')
    if is_backup_thread_running:
        response = 'Error: system is backing up saved'
        logging.error('Error: system is backing up saved')
        return response
    response = callRcon('Save')
    logging.info('save game success...')
    return response

def showSeverInfo():
    logging.info('showSeverInfo() working...')
    if is_backup_thread_running:
        response = 'Error: system is backing up saved'
        logging.error('Error: system is backing up saved')
        return response
    response = callRcon('Info')
    logging.info('show sever info success...')
    return response

def showSeverMemory():
    logging.info('showSeverMemory() working...')
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

def backupSaved():
    logging.info('back up saved job working...')
    while True:
        logging.info('back up saved job checking...')
        if len(showPlayers()) == 2:
            #服务器没人
            deltTime = timedelta(hours=12)
            backup(deltTime,'1','',True)
        else:
            #服务器有人
            deltTime = timedelta(hours=1)
            backup(deltTime,'60','即将重启服务器备份存档!',True)
        time.sleep(30*60)
       
    

def backup(deltTime,delay,msg,needRebot):
    
    def async_backup():
        #执行备份逻辑
        logging.info('start back up saved async...')
        global is_backup_thread_running
        global lastest_backup_dateTime
        if check_process_exists():
            logging.info('the game sever is running,before copy saved folder, now shutdown sever...')
            saveGame()
            reStartSever(delay,msg,'0')
        is_backup_thread_running = True
        while True:
            time.sleep(1)
            if not check_process_exists():
                #复制saved文件夹到目标backup路径
                shutil.copytree(os.path.join(os.path.dirname(path),"Pal\\Saved"),os.path.join(backupFolder,datetime.now().strftime('%Y-%m-%d-%H-%M-%S')))
                lastest_backup_dateTime = datetime.now()
                break
            logging.info('waiting game sever exit....')
        is_backup_thread_running = False
        if needRebot:
            logging.info('need rebot, now restart sever...')
            startSever()
        else:
            logging.info('not need rebot...')
        logging.info('finish back up saved...')

    global lastest_backup_dateTime
    logging.info('start comparing lastest_backup_dateTime:'+str(lastest_backup_dateTime)+' and deltTime:'+str(deltTime))
    if datetime.now() > lastest_backup_dateTime + deltTime:
        logging.info('The current time exceeds the set time,start back up...')
        thread = threading.Thread(target=async_backup)
        thread.start()
    else:
        logging.info('The current time not exceeds the set time,continue job...')
def checkLastestBackup():
    logging.info('start getting lastest saved dateTime...')
    global lastest_backup_dateTime
    for folder in backup_folders:
        try:
            backup_time = datetime.strptime(folder, '%Y-%m-%d-%H-%M-%S')
            # 比较最新备份时间
            if lastest_backup_dateTime is None or backup_time > lastest_backup_dateTime:
                lastest_backup_dateTime = backup_time
        except IndexError:
        # 文件夹名称不符合格式，跳过
            continue
    if not lastest_backup_dateTime:
        lastest_backup_dateTime = datetime.now()
        
    logging.info('the lastest back up dateTime is'+ lastest_backup_dateTime.strftime('%Y-%m-%d-%H-%M-%S'))

checkLastestBackup()
thread = threading.Thread(target=backupSaved)
thread.start()
    

    

