yhtools
=======

[YHTools](http://myip.tw/itsmw/index.php?title=YHTools) 本套工具的開發工具有兩種，一種是以 python3.x 開發（副檔名為 pyw），需要圖形化介面暨 UTF-8 中文顯示的能力，因此請在具有 python3 環境下的 linux 套件執行。另一種是 BASH ，副檔名為「.sh」可直接在終端機畫面執行。

1. 系統要求
--------

1. Debian Squeeze 或 Ubuntu 10.10 以上並必須安裝 X-Window 視窗
1. python3.1.x, python3-tk(8.5以上)
	
	apt-get update; apt-get install python3 python3-tk

2. 各工具簡介
--------

請參考: http://myip.tw/itsmw/index.php/YHTools


3. 工具集程式列表
--------

	|-- chmodadv.sh
	|-- dhcpconf
	|   |-- dhcp3-server
	|   |-- dhcpconf.pyw
	|   `-- dhcpd.conf
	|-- dnsconf
	|-- dnsconf.pyw
	|-- dnsconf.sample
	|   |-- db.0
	|   |-- db.127
	|   |-- db.255
	|   |-- db.local
	|   |-- db.root
	|   |-- named.conf
	|   |-- named.conf.default-zones
	|   `-- named.conf.options
	|-- firewall
	|   |-- fw4br.pyw
	|   |-- fw4local.pyw
	|   |-- fw4nat.pyw
	|   |-- fwtc4_l7filter.sh
	|   `-- fwtc.sh
	|-- homechown.sh
	|-- maccount
	|   |-- maccount.sh
	|   |-- passwd.txt
	|   `-- readme.txt
	|-- pubfolder.sh
	|-- README.TXT
	|-- rsync
	|   |-- rsync_c.pyw
	|   `-- rsync_s.pyw
	`-- test.py

