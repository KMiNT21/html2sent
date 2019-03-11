import html2sent

html = """
<h2>Golden FTP Server - free and PRO versions</h2></b><p style="color: red;">Version 5.00 - June, 2012</p>
Golden FTP Server is extremely easy to use personal FTP server for Windows and can be run by any person who has the most basic computer skills. The program loads automatically on Windows startup and you can identify the files you want to share with two mouse clicks via the dialog window that works in the same way as the standard Windows "Open File:" dialog or via the Windows Explorer context menu. Golden FTP Server features clean and easy to understand multi-lingual interface. Multi-threaded downloads and ability to resume aborted downloads are supported.
<center><br><br><b>Golden FTP Server Pro</b><br><img src="screenshots/pro.jpg" width="430" height="265"><br><br><br><b>Golden FTP Server Free</b><br><img src="screenshots/small-main-window.jpg" width="430" height="278"></center>
<br><hr size="1"><Br><hr size="1"><div align="center"><b><a href="order.html" target="_blank">FREE registration key for Golden FTP Server PRO!</a></b></div><hr size="1"><b>Press Release - October , 2004</b><br><br>For Immediate Release<br><br>KMiNT21 Software Releases Golden FTP Server 1.32<br><br>Free FTP server for file sharing.
<br><br>Golden FTP Server is a free Windows FTP server specially designed for PC novices.  While most advanced PC users know what FTP is and how to use it, it's a complete mystery for the beginners.  Yet, there is often a need to share a large amount of data, like 200 MB worth of wedding photos, music files or videos with friends and relatives scattered all over the country.  This is where Golden FTP Server comes to the rescue.
<br><br>This is how Golden FTP Server works - the program builds itself into Windows shell (Explorer's context menu) and is loaded upon startup.  User then selects a file or files that he or she wants to share by clicking them and selecting an appropriate option.  One click and the files start being uploaded.  The session may be aborted, paused or exited any time.  The process is resumed from the place where it was left off.  Since the program supports anonymous FTPs only, there is absolutely no room for "I-don't-know's" and "it-does-not-work's".  Two mouse clicks do it all and multi-threading does it fast.
<br><br>Golden FTP Server is probably the most uncomplicated FTP server in the entire world.  The interface consists of three buttons and a vertical panel with four icons.  That's it.  Combined with intellectual shares control, multilingual interface and a whooping price of 0, Golden FTP Server is an FTP server of choice for regular PC users who like sharing files.
<br><br>Golden FTP Server is available for free download at www.goldenftpserver.com<br><br>If you would like to get a comment, have a businesses proposal or want to learn more about KMiNT21 Software products and services, please contact Mikhail N. Kalinskiy at info@kmint21.com
<br><br>System Requirements: no special requirements<br><br>Company: KMiNT21 Software<br><br>Product Page: www.goldenftpserver.com<br><br>Download: www.goldenftpserver.com/golden-ftp-server.zip<br><br>Screenshot: www.goldenftpserver.com/screenshots.html
"""

sentences = html2sent.tokenize(html, language='english')
text = '\n'.join(sentences)
print(text)

