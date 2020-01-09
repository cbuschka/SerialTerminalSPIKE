# Code to generate a generic webpage

Start_html = '''
<html>
<head>
  <title>MicroPython on {}</title>
</head>

<body style="width:1200px; margin: 5px auto;">

<section style="width: 98%;height: 45px;background:#FFCC00;margin: auto;padding: 10px ;float:right">
<div style="width: 80%;margin: auto;height: 35px;float: left;">
<p style="font-size: 18 px;color:white;">You are connected to <b>{}</b> on <b>{}</b></p> 
</div>
<div style="margin: auto;float: right;">
<form action="/IP" method="POST">
<button style="background-color:red;font-size: 15px;color:white;" name="Close" type="submit" value="Close">Disconnect</button>
</form>
</div>
</section>



<section style="width: 98%;height: 650px;background: #FFCC00;margin: auto;padding: 10px;float:right">
    <div style="width: 48%;height: 620px;background: #FFFFFF;float: left;overflow: scroll;padding: 10px 10px 10px 10px">
    <form action="/" method="POST">

     <i style="font-size: 14px;"> Select Chapter. </i> <br>
<select style="background-color:blue;padding: 10px 12px;font-size: 12px;margin: 2px 1px;color:white;" name = "page">
{}
</select>
<button style="background-color:blue;padding: 5px 12px;font-size: 12px;margin: 2px 1px;color:white;" name="Page" type="submit" value="Close">Go To</button>
</form>
       
        <hr>
        '''


Form_html = '''
        <form action="/" method="POST">
<section>
    <div style="width: 550px;background-color: #FFFFFF;font-size: 12px;float: left;padding: 5px">
    <h3>{}</h3>
    <p style="font-family:Helvetica"> {} </p> <br>

        <div style="width: 420px;font-size: 12px;float: left;">

            <textarea rows="{}" cols="80" name = "{}" style="width: 420px;background-color: #E1E1E1; font-family:Courier New;padding: 5px">{}</textarea>
        </div>
        <div style="width: 100px;background-color: #FFFFFF;color:black;font-size: 12px; float: right;">
            <center> <button style="   text-align: center;background-color:  #FFFFFF;padding: 5px 12px;" name="REPL" type="submit" > Try it!!! </button> </center>
        </div>
        <p style="font-family:Helvetica;float: left;"> {} </p> <br>


    </div>
 
</section>
  </form>







'''
Rest_html = '''
</p>

</div>
<div style=" margin-left: 1%;height: 620px;background:  #FFFFFF;float: right;padding: 10px 10px 10px 10px">
<center><h4>{} Terminal Window</h4></center>
<center> <b>Script</b> </center>
<form action="/" method="POST">
<textarea style="background:  #E1E1E1" rows="15" cols="70" name = "Text to send"> {} </textarea><br>

<input style="background-color:green;color:white;"  type="submit" name="SendCommand" value="Run Script">
</form>
<center><b>REPL</b></center>
<form action="/" method="POST">
<textarea style="background: #E1E1E1" rows="18" cols="70" name = "TerminalWindow">{} </textarea><br>


<section style="width: 100%;height: 10px;background:#FFFFFF;margin: auto;padding: 2px ;float:right">
<div style="width: 50%;margin: auto;height: 35px;float: left;">

<input style="background-color:green;color:white;" type="submit" name="SendCommand" value="UPDATE">
</form>
</div>
<div style="margin: auto;height: 35px;float: right;">
<form action="/" method="POST">
<input style="background-color:green;color:white;"  type="submit" name="Clear" value="Clear REPL" onclick="myFunction()">
</form>

</div>
</section>
</div>
</section>
</body>
</html>
'''

Init_html = '''
            <html>
            <body style="width:960px; margin: 20px auto;">
            <br> <br> 
            <center>
            
             <h1> <form action="/" method="POST">{} Terminal Window</h1>
              <br> 
              <hr>
            <form action="/IP" method="POST">
          
            <p>Select port and press Connect to connect to {}</p>
               <form action="/" method="POST">
                 <select name = "processors">
                   {}
                   </select>
                <input type="submit" name = "Connect", value = "Connect">
               </form>

               <p>
            
                <i> If it does not connect, make sure it is on and plugged in. </i>
              </p>
              </center>
       
            </body>
            </html>
'''


from time import sleep
from http.server import BaseHTTPRequestHandler
import getpass, sys, socket, os
import serial,glob,time

from urllib.parse import unquote

# Initialize global variables
connected = False
terminal = "" #intialize blank terminal
ser = None
spike = ''
page = "start"
script = 'Type Here'

def InitSerial(port, bps = 115200, to = 0):
    global ser
    ser = serial.Serial(port, bps, timeout = to)  # open serial port
    return (ser.name)

def CloseSerial():
    global ser
    ser.close()
    return('done')

def WriteSerial(string):
    global ser
    return(ser.write(string.encode()))    # write a string

def ReadSerial():
    global ser
    reply = ''
    if ser.in_waiting:
        reply = ser.read(ser.in_waiting).decode()
    return(reply)

def serial_ports():
    result = []
    if sys.platform.startswith('win'):
        for i in range(256):
            try:
                s = serial.Serial('COM%s' % (i + 1))
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
        for port in ports:
            result.append(port)
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
        for port in ports:
            if 'usbmodem' in port:
                result.append(port)
    else:
        raise EnvironmentError('Unsupported platform')
    print(result)
    return result

def StartConnection():

    print('looking')
    reply = ''
    try:
        reply = serial_ports()
    except:
        pass
    return(reply)

def WaitForIt():
    doneReading = False
    text = ''
    starttime = time.time()
    while not doneReading:
        text = text + ReadSerial()
        doneReading = '>>>' in text
        if (time.time() > starttime+1):
            break
    return text

def SendIt(text):
    global ser
    
    WriteSerial(text + '\r\n')
    reply = WaitForIt()
    return(reply)

# Webserver
class MyServer(BaseHTTPRequestHandler):

    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def _redirect(self, path):
        self.send_response(303)
        self.send_header('Content-type', 'text/html')
        self.send_header('Location', path)
        self.end_headers()

    def do_GET(self):
        global connected
        global terminal,script
        global spike

        print('page = ' + page)
        self.do_HEAD()
        if  (page == 'start'):
            connections = StartConnection()
            p_list = ''
            for p in connections:
                p_list = p_list + '''<option selected="{}">{}</option>'''.format(p,p)
            self.wfile.write(Init_html.format(processor,processor,p_list).encode("utf-8"))
        else:
            page_list = ''
            for p in pyCode:
                if p == page:
                    select = 'selected'
                else:
                    select = ''
                page_list = page_list + '<option {}>{}</option>'.format(select,p)
            pageContent = Start_html.format(processor,processor,spike,page_list)
            if  page  in pyCode:
                for line in pyCode[page]:
                    endnote= pyCode[page][line][3]
                    buttonName = pyCode[page][line][0]
                    python = pyCode[page][line][2]
                    rows = len(python.split('\n'))
                    introText = pyCode[page][line][1]
                    pageAppend = Form_html.format(buttonName,introText,rows,line,python,endnote)
                    pageContent = pageContent + pageAppend
            else:
                pageContent = 'Error - you are asking for a page that does not exist'
            pageContent = pageContent + Rest_html.format(processor,script.strip(),terminal)
            self.wfile.write(pageContent.encode("utf-8"))

    def do_POST(self):
        global connected
        global terminal,script
        global ser
        global spike, page

        content_length = int(self.headers['Content-Length'])  # Get the size of data
        post_data = self.rfile.read(content_length).decode('utf-8')  # Get the data
        #print(post_data)
        post_data = post_data.split("=")[1]  # Only keep the value
        print('POST data ' + post_data) # Uncomment for debugging
        

        if 'Connect' in post_data and spike == '':
            spike = unquote(post_data.split("&")[0]) #StartConnection()[0].strip()
            if not (spike == ''):
                InitSerial(spike)
                WriteSerial('\x03\n')
                reply = WaitForIt()
                terminal = "Starting...\n"+ reply
                page = 'Chapter1_GettingStarted'
            else:
                terminal = "Failed to connect\n"
            print("-----------Connection Initiated-----------")

        elif 'SendCommand' in post_data and not (spike == ''):
            command = post_data.split("&")[0]
            if not (len(command) == 0):
                command = command.replace("+", " ")
                command = unquote(command).split(">>>")[-1]
                command = command.strip()  #replace('\r','\n')
                script = command   #keep this in memory to update the terminal
                cmds = command.split('\n')
                for sendcmd in cmds:
                    sendcmd = sendcmd.strip()
                    print('Command to send ' + sendcmd)
                    terminal = terminal+SendIt(sendcmd)

        elif 'Close' in post_data and not (spike == ''):
            CloseSerial()
            terminal = terminal + '\n closed'
            spike = ''
            page = 'start'
            
        elif 'Clear' in post_data:
            print('clearing')
            SendIt("\n")
            SendIt("\n")
            SendIt("\n")
            terminal = '>>>'
            
        elif 'Page' in post_data:
            print('new page: ' + post_data)
            if 'Chapter1_GettingStarted' in post_data:
                page = 'Chapter1_GettingStarted'
            if 'Chapter2_Accelerometer' in post_data:
                page = 'Chapter2_Accelerometer'
            if 'sensor' in post_data:
                page = 'sense'
            if 'advance' in post_data:
                page = 'advance'
            
        elif not (spike == ''):
            LinesOfCode = unquote(post_data.split("&")[0].replace("+", " ")).split('\n')
            print(LinesOfCode)
            for line in LinesOfCode:
                terminal = terminal + SendIt(line.strip())
            
            
        self._redirect('/')  # Redirect back to the root url
