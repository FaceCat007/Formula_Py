# -*- coding:utf-8 -*-
#! python3

# FaceCat-Python(OpenSource)
#Shanghai JuanJuanMao Information Technology Co., Ltd 

import math
import requests
import time
from requests.adapters import HTTPAdapter
from facecat import *
import facecat
from ctypes import *
import os

#K线数据转字符串
#datas 数据
def securityDatasToStr(datas):
	result = ""
	for i in range(0, len(datas)):
		data = datas[i]
		result = result + str(data.m_date) + "," + str(data.m_close) + "," + str(data.m_high) + "," + str(data.m_low) + "," + str(data.m_open) + "," + str(data.m_volume) + "\r"
	return result

current_file_path = __file__
current_file_dir = os.path.dirname(current_file_path)
facecatcpp = cdll.LoadLibrary(current_file_dir + r"\\facecatcpp.dll")
cdll.argtypes = [c_char_p, c_int, c_double, c_long, c_wchar_p]

#调用C++计算指标
#formula 公式
#datas 数据
def calculateFormula(formula, datas):
	recvData = create_string_buffer(1024 * 1024 * 10)
	sendStr = securityDatasToStr(datas)
	facecatcpp.calcFormula(c_char_p(formula.encode('gbk')), c_char_p(sendStr.encode('gbk')), recvData)
	return str(recvData.value, encoding="gbk")

m_shapes = ""
#调用C++计算指标，附带图形返回
#formula 公式
#datas 数据
def calculateFormulaWithShapes(formula, datas):
	global m_shapes
	recvData = create_string_buffer(1024 * 1024 * 10)
	recvData2 = create_string_buffer(1024 * 1024)
	sendStr = securityDatasToStr(datas)
	facecatcpp.calcFormulaWithShapes(c_char_p(formula.encode('gbk')), c_char_p(sendStr.encode('gbk')), recvData, recvData2)
	m_shapes = str(recvData2.value, encoding="gbk")
	return str(recvData.value, encoding="gbk")

#读取指标公式
current_file_path = __file__
current_file_dir = os.path.dirname(current_file_path)
file0 = open(current_file_dir + "\\指数平滑异同平均线(MACD).js", encoding="UTF-8")
formulaStr = file0.read()
file0.close()

file1 = open(current_file_dir + "\\SH600000.txt", encoding="UTF-8")
dataText = file1.read()
file1.close()
strs = dataText.split("\n")
strLen = len(strs)
#拼凑数据
datas = []
for i in range(2, strLen - 1):
	subStrs = strs[i].split(",")
	if(len(subStrs) > 5):			
		data = SecurityData()
		data.m_date = i
		data.m_close = float(subStrs[4])
		data.m_high = float(subStrs[2])
		data.m_low = float(subStrs[3])
		data.m_open = float(subStrs[1])
		data.m_volume = float(subStrs[6])
		datas.append(data)
#计算指标
result = calculateFormulaWithShapes(formulaStr, datas)
print(m_shapes)
print(result)
