# Builds the McGinn Page for Spike
import RogersSerial2
RogersSerial2.processor = 'SPIKE Prime'

RogersSerial2.pyCode = \
    {'Chapter1_GettingStarted':
         {'lights':['Change LED Color','''To begin, try running this code by clicking on the <b>Try it!!! </b> button: ''','''import hub\nhub.led(3) # blue   (colors 0 - 10)''', '''Can you make it go green? <br> <br>Notice the \'import\' command - that pulls in a python library that lets you talk to Spike.
                    '''],
          'REPL':['Do Math',
                  '''One of the more powerful attributes of Python is that you can test anything out before writing code in the REPL (read eval print loop).
                    It will execute any python command. <br><br>Try typing 2 + 2 in the REPL Window and hit \'UPDATE' and see what it says.''',
                  '''2 + 2''', '''Clear the REPL Screen by hitting <b> Clear REPL </b> .'''],
          'Display':['Display a name',
                     '''Now try displaying your name - note that since you already imported hub above,
                        it is already in memory and you do not need to type it again.  If it were not, you would get an error.''',
                     '''hub.display.show(\'fred\')''', '''You can also copy the code to the  <b> Script </b> window and hit <b> Run Script </b> to execute the code.'''],
          'Motor':['Turn on a motor','''Or maybe you want to turn a motor on?  Plug a motor and try to make it run''',
                   '''import hub, utime\nhub.port.A.motor.pwm(100)\nutime.sleep(1)\nhub.port.A.motor.float()''',''''''],
          'Motors':['Turn on a pair of motors','''It is even more important for motors to work together in pairs so that
                    they go at the same speed''',
                    '''import hub \n# only works if both motors are connected \nmotor =hub.port.A.motor.pair(hub.port.B.motor)\nmotor.pwm(40,-40) # drive straight\nmotor.run_for_time(2000,40,-40)''', ''''''],
          
          },
    'Chapter2_Accelerometer':
          {'ReadAccel':['Read Acclerometer','''SPIKE Prime has built-in accelerometer that you can access. Try the code below to read data.''','''import hub\nhub.motion.accelerometer()''',  ''''''],
           'Monitor':['Monitor Acceleration','''some text here''',
                        '''while not hub.button.center.is_pressed(): 
                        \n&nbsp;&nbsp;&nbsp;&nbsp;gravity = hub.motion.accelerometer()
                        \n&nbsp;&nbsp;&nbsp;&nbsp;Xgravity = gravity [0] /100
                        \n&nbsp;&nbsp;&nbsp;&nbsp;Ygravity = gravity [1] /100
                        \n&nbsp;&nbsp;&nbsp;&nbsp;Zgravity = gravity[2] /100
                        \n&nbsp;&nbsp;&nbsp;&nbsp;print('%g, %g, %g' % (Xgravity,Ygravity,Zgravity))
                        \n&nbsp;&nbsp;&nbsp;&nbsp;freq = int(-Xgravity *100)
                        \n&nbsp;&nbsp;&nbsp;&nbsp;hub.sound.beep(freq, 10, 1)
                        \n&nbsp;&nbsp;&nbsp;&nbsp;utime.sleep_ms(9)''', ''''''],
          }
      }


from http.server import HTTPServer
import webbrowser

# Set host port
host_port = 8000
ip_address = 'localhost'


# Create Webserver
if __name__ == '__main__':

    http_server = HTTPServer((ip_address, host_port), RogersSerial2.MyServer)
    print("Server Starts - %s:%s" % (ip_address, host_port))
    webbrowser.open_new('http://%s:%s' %  (ip_address, host_port))

    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()
        print("\n-------------------EXIT-------------------")
