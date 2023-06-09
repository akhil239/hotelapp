import socket
import pickle
import threading


stack = []


def app():
    from kivy.app import App
    from kivy.lang import Builder
    from kivy.core.window import Window
    from kivy.uix.gridlayout import GridLayout


    Window.clearcolor = "#EDF9C8"
    Window.size = (400,720)
    Builder.load_string("""
#:import hex kivy.utils.get_color_from_hex
<Sever_app>:
    GridLayout:
        rows:1
        size_hint_x:1000
        canvas.before:
            Color:
                rgba:hex("#060F0F")
            Rectangle:
                pos: (0,500)
                
                size: (5000,600)
        GridLayout:
            Label:
                text:"Hotel name"
                color:"#FFFFFF"
                pos:(150,560)
                font_size:50
                #font_name: 'Library3am-5V3Z'
    GridLayout:
        Button:
            text:"view list"
            on_press:root.thread()
            size:(100,50)
            pos:(300,320)
            background_color:[255, 255, 255, 1]
            color:"#060F0F"
        
    GridLayout:
        Button:
            text:"connect"
            on_press:root.SServer.server()
            pos:(300,400)
            size:(100,40)
            background_color:[255, 255, 255, 1]
            color:"#060F0F"
            border:(10,10,10,10)


    GridLayout:
        rows:3
        cols:2
        canvas.before:
            Color:
                rgba:hex("#FFFFFF")
            Rectangle:
                pos: self.pos
                size: self.size
        pos:(50,100)
        size:(200,200)
        Label:
            id:ittem
            text:"item"
            color:"#060F0F"
            pos:(80,255)
        Label:
            id:item
            text:"3"
            color:"#060F0F"
            pos:(200,200)
        
        Label:
            id:ttable
            text:"table"
            color:"#060F0F"
            pos:(80,100)
        Label:
            id:table
            text:"8"
            color:"#060F0F"
            pos:(150,100)
        Label:
            id:qquantity
            text:"quantity"
            color:"#060F0F"
            pos:(80,190)

        Label:
            id:quantity
            text:"5"
            color:"#060F0F"
            pos:(150,190)
        

    """)
    class Server:
        def __init__(self,conn,addr):
            self.conn = conn 
            self.addr = addr
        def handle(conn,addr):
            print("client_socket",conn,"addr",addr)
            #print('Connected by', address)
            while True:  
                data = conn.recv(97)
                from_client = pickle.loads(data)
                stack.append(from_client)
                print(stack)
                data = None
                if data :
                    break
                print('Received from client:', from_client)
                #client_socket.sendall(data.encode())
            conn.close()
            

    class Sever_app(GridLayout):
        def __init__(self,**kwargs):
            super().__init__(**kwargs)
            self.rows = 2
            self.cols = 1
            self.padding = (25,250)
        def stack1(self):
            global stack
            if len(stack) != 0:
                pick = stack.pop(0)
                item = pick["item"]
                quantity = pick["quantity"]
                table = pick["table"]
                self.ids.item.text = str(item)
                self.ids.quantity.text = str(quantity)
                self.ids.table.text = str(table)

            else:
                print("no items on the stack....")
        def thread(self):
            t = threading.Thread(target=self.stack1).start()
        class SServer: 
            def __init__(self, **kwargs):
                super().__init__(**kwargs) 
            def server():
                host = socket.gethostbyname(socket.gethostname())
                port = 8080
                server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server_socket.bind((host,port))
                server_socket.listen(10)
                print('Waiting for a connection...')
                client_socket, address = server_socket.accept()
                thread = threading.Thread(target=Server.handle,args=(client_socket,address))
                thread.start()
                #thread.join()       
    class Run(App):
        def build(self):
            return Sever_app()
    Run().run()
    
        

if __name__ == '__main__':
        thread2 = threading.Thread(target=app)
        thread2.start()
        thread2.join()
    