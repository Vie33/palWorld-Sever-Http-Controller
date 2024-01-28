import requests
import tkinter as tk
import configparser

config = configparser.ConfigParser()
config.read('palSeverController.ini')
serverIp = config.get('Sever Http Controller Config', 'severIp')

def showResponseMsg(msg):
    text_area.delete("1.0", tk.END)
    text_area.insert(tk.END,msg)

def save_game():
    response = requests.get('http://'+serverIp+'/saveGame')
    showResponseMsg(response.text)

def view_server_info():
    print("View server info button clicked")
    response = requests.get('http://'+serverIp+'/showInfo')
    showResponseMsg(response.text)

def restart_server(isRestart):
    waitTime = input_delay_entry.get()
    broadcastMsg = input_broadcast_entry.get()
    print("Restart server button clicked")
    response = requests.get('http://'+serverIp+'/reStartServer?waitTime='+waitTime+'&remindMsg='+broadcastMsg+'&isRestart='+isRestart)
    showResponseMsg(response.text)

def view_player_info():
    print("View player info button clicked")
    response = requests.get('http://'+serverIp+'/showPlayers')
    showResponseMsg(response.text)

def view_memory_info():
    print("View memory info button clicked")
    response = requests.get('http://'+serverIp+'/showServerMemory')
    showResponseMsg(response.text)

def start_sever():
    print("start sever button clicked")
    response = requests.get('http://'+serverIp+'/startSever')
    showResponseMsg(response.text)

def clear_default_text(event):
    input_delay_entry.delete(0, tk.END)

root = tk.Tk()
root.title("帕鲁服务器面板 v0.1 developed by Vie3")
# 第零行
save_game_button = tk.Button(root, text="启动服务器", command=start_sever)
save_game_button.grid(row=0, column=2)
# 第一行
save_game_button = tk.Button(root, text="保存游戏", command=save_game)
save_game_button.grid(row=1, column=2)

# 第二行
view_server_info_button = tk.Button(root, text="查看服务器信息", command=view_server_info)
view_server_info_button.grid(row=2, column=2)

# 第三行
default_delay_text = "延迟"
input_delay_label = tk.Label(root, text=default_delay_text)
input_delay_label.grid(row=3, column=0)

input_delay_entry = tk.Entry(root)
input_delay_entry.grid(row=3, column=1)

default_broadcast_text = "全服广播内容"
input_broadcast_label = tk.Label(root, text=default_broadcast_text)
input_broadcast_label.grid(row=3, column=2)

input_broadcast_entry = tk.Entry(root)
input_broadcast_entry.grid(row=3, column=3)

restart_server_button = tk.Button(root, text="重启服务器", command=lambda:restart_server('1'))
restart_server_button.grid(row=3, column=4)

shutdown_server_button = tk.Button(root, text="关闭服务器", command=lambda:restart_server('0'))
shutdown_server_button.grid(row=3, column=5)

# 第四行
view_player_info_button = tk.Button(root, text="查看玩家信息", command=view_player_info)
view_player_info_button.grid(row=4, column=2)

# 第五行
view_memory_info_button = tk.Button(root, text="查看服务器内存信息", command=view_memory_info)
view_memory_info_button.grid(row=5, column=2)

# 第六行
text_area = tk.Text(root, height=10, width=80)
text_area.grid(row=6, column=0, columnspan=5)

root.mainloop()