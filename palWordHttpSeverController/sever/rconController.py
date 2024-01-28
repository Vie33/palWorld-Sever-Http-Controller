from flask import Flask, jsonify,request
import management
import logging
import configparser

# 配置日志记录
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
config = configparser.ConfigParser()
config.read('rconControllerConfig.ini')
listenPort = config.get('Sever Http Controller Config','listenPort')

app = Flask(__name__)

# 处理/saveGame请求
@app.route('/saveGame', methods=['GET'])
def save_game():
    # 处理保存游戏的逻辑
    logging.info('start save game...')
    response = management.saveGame()
    return response

# 处理/reStartServer请求
@app.route('/reStartServer', methods=['GET'])
def restart_server():
    # 处理重新启动服务器和关闭服务器的逻辑
    logging.info('start reStart Server...')
    waitTime = request.args.get('waitTime')
    remindMsg = request.args.get('remindMsg')
    isRestart = request.args.get('isRestart')
    response = management.reStartSever(waitTime,remindMsg,isRestart)
    return response

# 处理/showPlayers请求
@app.route('/showPlayers', methods=['GET'])
def show_players():
    # 处理显示玩家列表的逻辑
    logging.info('start show players...')
    response = management.showPlayers()
    return response
    
# 处理/showInfo请求
@app.route('/showInfo', methods=['GET'])
def show_info():
    # 处理显示服务器信息的逻辑
    logging.info('start show info...')
    response = management.showSeverInfo()
    return response

# 处理/showServerMemory请求
@app.route('/showServerMemory', methods=['GET'])
def show_memory():
    # 处理显示服务器当前内存的请求
    logging.info('start show info...')
    response = management.showSeverMemory()
    return response

# 处理/startSever请求
@app.route('/startSever', methods=['GET'])
def start_sever():
    # 处理开启服务器的请求
    logging.info('start sever...')
    response = management.startSever()
    return response

if __name__ == '__main__':
    logging.info('system listening at 8882...')
    app.run(host='0.0.0.0', port=listenPort)