#encoding=utf-8
#基于modbus协议的服务器（从机）程序，仿真gantry角度的变化
import modbus_tk.modbus_tcp
import struct
import time

#每次改变寄存器数据的周期
sleep_time=0.07

server = modbus_tk.modbus_tcp.TcpServer()
#server = modbus_tk.modbus_tcp.TcpServer(port=502, address='0.0.0.0', timeout_in_sec=3)
server.start()
slave_1 = server.add_slave(1)
slave_1.add_block('block1',modbus_tk.defines.HOLDING_REGISTERS,12288,2,)
for i in range(1,999):
    start = time.time()
    a = struct.unpack('<HH', struct.pack('<f',i))
    slave_1.set_values('block1',12288,a)
    time.sleep(sleep_time)
    end = time.time()
    print("Server Cycle period:",end - start)

#重要：关闭套接字，释放资源
server.remove_all_slaves()
server.stop()