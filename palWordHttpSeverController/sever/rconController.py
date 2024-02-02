from flask import Flask, jsonify,request
import management
import logging
import configparser
from datetime import datetime,timedelta

# 配置日志记录
logger = logging.getLogger('my_logger')
logging.getLogger().propagate = False
config = configparser.ConfigParser()
config.read('rconControllerConfig.ini')
listenPort = config.get('Sever Http Controller Config','listenPort')

app = Flask(__name__)

# 处理/saveGame请求
@app.route('/saveGame', methods=['GET'])
def save_game():
    # 处理保存游戏的逻辑
    logger.info('start save game...')
    logger.info(f"Request: {request.method} {request.url}")
    response = management.saveGame()
    return response

# 处理/reStartServer请求
@app.route('/reStartServer', methods=['GET'])
def restart_server():
    # 处理重新启动服务器和关闭服务器的逻辑
    logger.info('start reStart Server...')
    logger.info(f"Request: {request.method} {request.url}")
    waitTime = request.args.get('waitTime')
    remindMsg = request.args.get('remindMsg')
    isRestart = request.args.get('isRestart')
    response = management.reStartSever(waitTime,remindMsg,isRestart)
    return response

# 处理/showPlayers请求
@app.route('/showPlayers', methods=['GET'])
def show_players():
    # 处理显示玩家列表的逻辑
    logger.info('start show players...')
    logger.info(f"Request: {request.method} {request.url}")
    response = management.showPlayers()
    return response
    
# 处理/showInfo请求
@app.route('/showInfo', methods=['GET'])
def show_info():
    # 处理显示服务器信息的逻辑
    logger.info('start show info...')
    logger.info(f"Request: {request.method} {request.url}")
    response = management.showSeverInfo()
    return response

# 处理/showServerMemory请求
@app.route('/showServerMemory', methods=['GET'])
def show_memory():
    # 处理显示服务器当前内存的请求
    logger.info('start show info...')
    logger.info(f"Request: {request.method} {request.url}")
    response = management.showSeverMemory()
    return response

# 处理/startSever请求
@app.route('/startSever', methods=['GET'])
def start_sever():
    # 处理开启服务器的请求
    logger.info('start sever...')
    logger.info(f"Request: {request.method} {request.url}")
    response = management.startSever()
    return response

# 处理/backupSaved请求
@app.route('/backupSaved', methods=['GET'])
def backup_saved():
    # 处理开始备份服务器存档的请求
    logger.info('start back up saved...')
    logger.info(f"Request: {request.method} {request.url}")
    management.backup(timedelta(seconds=1),'1','即将重启服务器备份存档!',False)
    return 'start back up saved...'

if __name__ == '__main__':
    logger.info('system listening at 8882...')
    app.run(host='0.0.0.0', port=listenPort)