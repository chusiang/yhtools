#!/usr/bin/env python3
#-*- coding:utf-8 -*-
import shlex, subprocess, os, sys
import time
from datetime import date


def print_chtdigits(dtype, digits):
	myreturn = ""
	dtype1 = {0:"零", 1:"壹", 2:"貳", 3:"參", 4:"肆", 5:"伍", 6:"陸", 7:"柒", 8:"捌", 9:"玖"}
	dtype2 = {0:"〇", 1:"一", 2:"二", 3:"三", 4:"四", 5:"五", 6:"六", 7:"七", 8:"八", 9:"九"}
	dictionary = dtype1 if dtype == 1 else dtype2
	if digits.isdigit():
		for mynum in digits:
			myreturn += dictionary[int(mynum)]
	else:
		myreturn = "您輸入的字串含有非數字部分, 無法轉換!"
	return myreturn

myvar = "勇炫第{0}支: {1} 程式"

print(myvar.format("二","Python3"))

ip6_rtype2 = "2001:288:75a6"
ip6_list = ip6_rtype2.split(":")

for i in range(len(ip6_list)):
	ip6_list[i] = "{:0>4}".format(ip6_list[i])

k = len(ip6_list) - 1
ip6_rtype1 = ""
for i in range(len(ip6_list)):
	j = k - i
	for iw in range(4):
		jw = 3 - iw
		ip6_rtype1 = ip6_rtype1 + ip6_list[j][jw] + "."
		
print( ip6_rtype1 )

td = date.today()
print(td.strftime("%Y%m%d"))


