#!/usr/bin/env python3

import socket, time, requests

aws_sup_ec2_endpoint = "54.149.127.24"
aws_ga_endpoint = "15.197.156.123"
port = 10009
test_round = 1
socket_round = 10

def do_socket(host):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        t1 = time.time()
        s.connect((host, port))
        t2 = time.time()
        s.sendall(bytes('a', encoding='utf-8'))
        data = s.recv(1024)
        print(data)
        t3 = time.time()
        for i in range(socket_round):
            s.sendall(b'zhenghui-sgsb')
            data = s.recv(1024)
            print(data)
        t4 = time.time()
        s.sendall(b'0')
    # 依次返回，tcp握手时间，首字节返回时间（加上握手时间），平均12字节response返回时间
    return (t2-t1)*1000, (t3-t1)*1000, (t4-t3)*1000/socket_round


if __name__ == '__main__':
    ga_connect_time = 0
    ga_message_time = 0
    ga_total_time = 0
    dx_connect_time = 0
    dx_message_time = 0
    dx_total_time = 0
    count = 0
    print("test_round = %d" % test_round)
    print("socket_round = %d" % socket_round)
    for i in range(test_round):
        print("Round %d" % (i+1))
        print("Test EC2 IP: %s" % aws_sup_ec2_endpoint)
        ec2_dx1, ec2_dx2, ec2_dx3 = do_socket(aws_sup_ec2_endpoint)
        print("Test GA IP: %s" % aws_ga_endpoint)
        ga1, ga2, ga3 = do_socket(aws_ga_endpoint)

        dx_connect_time += ec2_dx1
        dx_message_time += ec2_dx2
        dx_total_time   += ec2_dx3

        ga_connect_time += ga1
        ga_message_time += ga2
        ga_total_time   += ga3

    print("tcp握手时间 -> EC2: %d ms, GA: %d ms" %
        (dx_connect_time/test_round, ga_connect_time/test_round))
    print("业务包首字节 返回 -> EC2: %d ms, GA: %d ms" %
        (dx_message_time/test_round, ga_message_time/test_round))
    print("后续tcp业务包通信平均时间 -> EC2: %d ms, GA: %d ms" %
        (dx_total_time/test_round,   ga_total_time/test_round))

