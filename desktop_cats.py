#!/usr/bin/env python3
"""Cross-platform transparent desktop cats made from the user's photos."""
from __future__ import annotations
import argparse, math, random, sys, time
from pathlib import Path
from PySide6.QtCore import QPoint, QTimer, Qt
from PySide6.QtGui import QAction, QCursor, QPixmap, QTransform
from PySide6.QtWidgets import QApplication, QLabel, QMenu

ASSET_DIR=Path(__file__).resolve().parent/'cat_assets'
FILES=['ragdoll_paw.png','ragdoll_portrait.png','gray_loaf.png','silver_closeup.png','silver_lounging.png','gray_mirror.png','silver_bed.png']

class CatWindow(QLabel):
    def __init__(self, app_controller, image:Path, size:int, speed:float, index:int):
        super().__init__(); self.controller=app_controller; self.index=index
        flags=Qt.FramelessWindowHint|Qt.Tool|Qt.WindowStaysOnTopHint
        self.setWindowFlags(flags); self.setAttribute(Qt.WA_TranslucentBackground,True)
        self.setAttribute(Qt.WA_NoSystemBackground,True); self.setStyleSheet('background:transparent;')
        source=QPixmap(str(image))
        if source.isNull(): raise RuntimeError(f'Could not load {image}')
        self.base=source.scaledToHeight(size,Qt.SmoothTransformation)
        self.direction=random.choice((-1,1)); self.speed=speed*random.uniform(.82,1.18)
        self.x=0.0; self.ground=random.randint(0,16); self.phase=random.random()*math.tau
        self.paused=False; self.pause_until=0.0; self.next_pause=time.monotonic()+random.uniform(5,12)
        self.dragging=False; self.drag_delta=QPoint(); self.press_global=QPoint(); self._set_facing(); self.resize(self.pixmap().size())
        geo=QApplication.primaryScreen().availableGeometry(); self.x=random.uniform(0,max(1,geo.width()-self.width()))
        self.move(int(geo.left()+self.x),geo.bottom()-self.height()-self.ground+1); self.show()

    def _set_facing(self):
        pix=self.base
        if self.direction<0: pix=pix.transformed(QTransform().scale(-1,1),Qt.SmoothTransformation)
        self.setPixmap(pix); self.resize(pix.size())

    def tick(self,dt:float,now:float):
        if self.dragging:return
        geo=self.screen().availableGeometry() if self.screen() else QApplication.primaryScreen().availableGeometry()
        if now>=self.next_pause:
            self.paused=not self.paused
            if self.paused:self.pause_until=now+random.uniform(1.2,3.2);self.next_pause=self.pause_until
            else:self.next_pause=now+random.uniform(5,12)
        if self.paused and now>=self.pause_until:self.paused=False;self.next_pause=now+random.uniform(5,12)
        if not self.paused:
            self.x+=self.direction*self.speed*dt
            right=max(0,geo.width()-self.width())
            if self.x<0:self.x=0;self.direction=1;self._set_facing()
            elif self.x>right:self.x=right;self.direction=-1;self._set_facing()
            self.phase+=dt*7.5
        bob=0 if self.paused else math.sin(self.phase)*3.0
        self.move(geo.left()+int(self.x),geo.bottom()-self.height()-self.ground+1+int(bob))

    def mousePressEvent(self,event):
        if event.button()==Qt.LeftButton:
            self.dragging=True;self.press_global=event.globalPosition().toPoint();self.drag_delta=self.press_global-self.frameGeometry().topLeft();event.accept()
        elif event.button()==Qt.RightButton:self.show_menu(event.globalPosition().toPoint());event.accept()

    def mouseMoveEvent(self,event):
        if self.dragging:
            pos=event.globalPosition().toPoint()-self.drag_delta;self.move(pos);self.x=float(pos.x()-self.screen().availableGeometry().left());event.accept()

    def mouseReleaseEvent(self,event):
        if event.button()==Qt.LeftButton:
            moved=(event.globalPosition().toPoint()-self.press_global).manhattanLength()>4
            self.dragging=False
            if not moved:self.paused=not self.paused;self.pause_until=time.monotonic()+999999 if self.paused else 0
            event.accept()

    def mouseDoubleClickEvent(self,event):
        if event.button()==Qt.LeftButton:self.direction*=-1;self._set_facing();event.accept()

    def show_menu(self,pos):
        menu=QMenu(); pause=QAction('Resume this cat' if self.paused else 'Pause this cat',menu)
        pause.triggered.connect(self.toggle_pause); menu.addAction(pause)
        menu.addAction('Pause / resume all',self.controller.toggle_all)
        menu.addAction('Hide / show all',self.controller.toggle_visibility)
        menu.addSeparator();menu.addAction('Quit desktop cats',self.controller.quit);menu.exec(pos)

    def toggle_pause(self):
        self.paused=not self.paused;self.pause_until=time.monotonic()+999999 if self.paused else 0

class Controller:
    def __init__(self,args):
        chosen=FILES[:max(1,min(args.count,len(FILES)))]
        self.cats=[CatWindow(self,ASSET_DIR/f,args.size,args.speed,i) for i,f in enumerate(chosen)]
        self.timer=QTimer();self.timer.timeout.connect(self.tick);self.last=time.monotonic();self.timer.start(16);self.hidden=False
    def tick(self):
        now=time.monotonic();dt=min(.05,now-self.last);self.last=now
        for cat in self.cats:cat.tick(dt,now)
    def toggle_all(self):
        target=not all(c.paused for c in self.cats)
        for c in self.cats:c.paused=target;c.pause_until=time.monotonic()+999999 if target else 0
    def toggle_visibility(self):
        self.hidden=not self.hidden
        for c in self.cats:c.setVisible(not self.hidden)
    def quit(self):QApplication.quit()

def main():
    parser=argparse.ArgumentParser(description='Transparent desktop cats')
    parser.add_argument('--count',type=int,default=7,help='number of cats, 1-7')
    parser.add_argument('--size',type=int,default=150,help='cat height in pixels')
    parser.add_argument('--speed',type=float,default=55.0,help='average walking speed in pixels/second')
    args=parser.parse_args();app=QApplication(sys.argv);app.setQuitOnLastWindowClosed(False)
    app.setApplicationName('Desktop Cats');controller=Controller(args);sys.exit(app.exec())
if __name__=='__main__':main()
