# encoding=utf-8
#基于modbus协议的客户端（主机）程序，读取gantry角度的变化
import modbus_tk.modbus_tcp
import time
import struct

# 全局变量,便于修改
GApath = u"D:\GantryAngle.txt"
cycle_time = 1000                            #主循环的次数
sleep_time = 0.009                          #每次循环的等待时间

# 将GantryAngle从元组中写入txt,这个慢速的I\O操作耗时1s+，所以不放在循环中
def TXTCreator(gas):
    global GApath
    f = open(GApath, 'w')
    for i in gas:
        for j in i:
            f.write(str(j) + '\n')
    f.close()

# 从PLC中使用modbus协议读取GantryAngle
def GasReader():
    global cycle_time
    global sleep_time
    gas = []
    ga_0 = (0,0)

    s = time.time()
    #master = modbus_tk.modbus_tcp.TcpMaster('169.254.254.118',502)
    master = modbus_tk.modbus_tcp.TcpMaster()
    # master address:('0.0.0.0', 502)(master_ip,port)
    master.set_timeout(3)
    # timeout表示若超过3秒没有连接上slave就会自动断开
    e = time.time()
    print("Established Time:",e-s)

    #每次循环通过modbus_tcp从PLC的寄存器读取数据
    for i in range(0, cycle_time):
        start = time.time()
        ga_1 = master.execute(1,modbus_tk.defines.HOLDING_REGISTERS,12288,2,)
        # （slave_id，操作码，起始地址,个数）
        if ga_0!=ga_1:
            gas.append(ga_1)
            ga_0 = ga_1
        time.sleep(sleep_time)
        end = time.time()
        #输出一次循环的时间，判断是否可以接受
        print("Client Cycle period:",end-start)
    return gas

#将从寄存器中取到的2个unsigned short转换成float并放入元组gas中
def ShortToFloat(gas):
    gas_0 = []
    for ga in gas:
        ga_0 = struct.unpack('<f', struct.pack('<HH',ga[0],ga[1]))
        gas_0.append(ga_0)
    return gas_0

def main():
    gas = GasReader()
    print(gas)
    #下面2个子函数不放入循环中，降低每次循环的时间
    gas = ShortToFloat(gas)
    print(gas)
    TXTCreator(gas)

main()