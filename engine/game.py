"""Supplied game framework. Exercises live in student/*.py and harbor.tmx."""
from pathlib import Path
import argparse, importlib.util, math, sys, xml.etree.ElementTree as ET
import pykraken as kn
from engine.lettering import text
ROOT=Path(__file__).resolve().parents[1]
W,H=640,360

def load_module(folder,name):
    spec=importlib.util.spec_from_file_location(f'{folder.name}_{name}',folder/f'{name}.py')
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module

def rect(x,y,w,h,c): kn.draw.rect(kn.Rect(x,y,w,h),kn.Color(*c))
def circle(x,y,r,c): kn.draw.circle(kn.Circle(x,y,r),kn.Color(*c))

class Game:
    def __init__(self):
        self.folder=ROOT/"student"
        self.movement=load_module(self.folder,'movement')
        self.animation=load_module(self.folder,'boss_animation')
        self.audio=load_module(self.folder,'audio').Audio(ROOT/'assets/audio')
        self.map=kn.tilemap.Map(self.folder/'harbor.tmx')
        self.world=kn.physics.World()
        self.ground=kn.physics.StaticBody(self.world)
        # Every occupied Platforms tile is solid. Scenery is visual only.
        xml=ET.parse(self.folder/'harbor.tmx').getroot()
        width=int(xml.get('width')); tw=int(xml.get('tilewidth'))
        layer=xml.find("layer[@name='Platforms']")
        if layer is None: raise ValueError('Map needs a Platforms tile layer')
        data=layer.find('data')
        if data.get('encoding')!='csv': raise ValueError('Save the Tiled map with CSV tile layer data')
        ids=[int(n) for n in data.text.replace('\n','').split(',') if n.strip()]
        self.solids=[]
        for row in range(int(xml.get('height'))):
            start=None
            for col in range(width+1):
                solid=col<width and ids[row*width+col]!=0
                if solid and start is None: start=col
                if not solid and start is not None:
                    box=kn.Rect(start*tw,row*tw,(col-start)*tw,tw)
                    self.ground.add_collider(box);self.solids.append((start*tw,row*tw,(col-start)*tw,tw));start=None
        self.markers={o.get('name'):(float(o.get('x')),float(o.get('y'))) for o in xml.findall("objectgroup[@name='Markers']/object")}
        self.player=kn.physics.CharacterBody(self.world)
        self.player.capsule_shape=kn.Capsule(0,-4,0,4,6)
        self.player.friction=0;self.player.stop_speed=0
        self.camera=kn.Camera()
        names=['hero_idle','hero_run','boss_idle','boss_attack','boss_hurt','gem']
        self.tex={n:kn.Texture(ROOT/'assets'/f'{n}.png') for n in names}
        self.reset()

    def reset(self):
        self.spawn=self.markers['Spawn'];self.checkpoint=False
        self.hp=3;self.boss_hp=12;self.won=False;self.elapsed=0;self.invuln=0
        self.bullets=[];self.enemy=[];self.cooldown=0;self.face=1;self.jump_buffer=False
        self.boss_active=False;self.phase=0;self.volley=0
        self.muted=getattr(self,"muted",False)
        self.boss_x,self.boss_y=self.markers['Boss']
        self.boss_transform=kn.Transform()
        self.orch=self.animation.build(self.boss_transform)
        self.respawn()
    def respawn(self):
        self.player.pos=kn.Vec2(*self.spawn);self.player.velocity=kn.Vec2(0,0)
        self.hp=3;self.invuln=1.0;self.enemy.clear()
    def hurt(self):
        if self.movement.can_take_hit(self.invuln):
            self.hp-=1;self.invuln=1.0;self.audio.play('hurt')
            if self.hp<=0:self.respawn()
    def warp(self):
        # Review shortcut: both versions can reach the boss without a finished map.
        self.spawn=(1580,260);self.checkpoint=True;self.respawn()
    def update(self,dt,left=False,right=False,jump=False,shoot=False):
        if self.won:return
        self.elapsed+=dt;self.invuln=max(0,self.invuln-dt);self.cooldown=max(0,self.cooldown-dt)
        if left!=right:self.face=1 if right else -1
        if self.movement.step(self.player,dt,left,right,jump):self.audio.play('jump')
        self.world.step(dt)
        p=self.player.pos
        if p.y>380 or p.x<0: self.respawn();return
        # Checkpoint on the route; its marker is editable in Tiled.
        cx,cy=self.markers['Checkpoint']
        if not self.checkpoint and abs(p.x-cx)<28 and abs(p.y-cy)<40:
            self.spawn=(cx,cy);self.checkpoint=True;self.audio.play('checkpoint')
        if shoot and self.cooldown<=0:
            self.bullets.append([p.x+self.face*10,p.y-2,self.face*300,1.8]);self.cooldown=.28;self.audio.play('shot')
        if p.x>1500 and self.boss_hp>0:
            if not self.boss_active:
                self.boss_active=True;self.phase=0;self.volley=0
                if self.orch:self.orch.play()
            before=self.phase;self.phase+=dt
            for index,timing in enumerate([.8,1.1,1.4]):
                if before<timing<=self.phase:
                    # Alternating low waves and aimed orbs. Attacks work in BOTH versions.
                    y=258 if index!=1 else 225
                    self.enemy.append([self.boss_x-35,y,-125,0])
            if self.phase>=4:
                self.phase-=4
                if self.orch:self.orch.play()
        for b in self.bullets:
            b[0]+=b[2]*dt;b[3]-=dt
            if self.boss_hp>0 and abs(b[0]-self.boss_x)<34 and abs(b[1]-self.boss_y)<34:
                if self.phase>=1.8:
                    self.boss_hp-=1
                    if self.boss_hp==0:self.enemy.clear();self.audio.play('win')
                b[3]=0
        self.bullets=[b for b in self.bullets if b[3]>0]
        for b in self.enemy:
            b[0]+=b[2]*dt
            # A lingering orb is intentional: tests the invulnerability bug.
            if abs(b[0]-p.x)<15 and abs(b[1]-p.y)<16:self.hurt()
        self.enemy=[b for b in self.enemy if b[0]>1450]
        if self.boss_hp>0 and abs(p.x-self.boss_x)<35 and abs(p.y-self.boss_y)<40:self.hurt()
        ex,ey=self.markers['Exit']
        if self.boss_hp<=0 and abs(p.x-ex)<28 and abs(p.y-ey)<45:
            self.won=True;self.audio.play('win')

    def draw(self):
        p=self.player.pos; cam=round(max(0,min(p.x-200,1980-W)));t=self.elapsed
        kn.renderer.clear(kn.Color(12,24,44))
        # Parallax harbor backdrop is drawn from vector shapes, independent of terrain.
        circle(505-cam*.04,72,28,(242,216,156))
        for i in range(18):
            x=(i*137-cam*.12)%750-60; y=150+(i%3)*16
            rect(x,y,42,150,(22,47,65));rect(x+12,y-20,18,20,(22,47,65))
            for j in range(3):rect(x+8+j*11,y+15,3,8,(53,89,99))
        rect(0,245,W,115,(21,67,81))
        for i in range(32):
            x=(i*53-cam*.3+t*8)%700-40;y=254+(i*19)%70
            rect(x,y,18+(i%4)*7,1,(38,101,111))
        # Tiled map uses the camera; HUD is drawn after unsetting it.
        self.camera.transform.pos=kn.Vec2(cam+W/2,H/2);self.camera.set()
        self.map.get_layer('Platforms').draw();self.map.get_layer('Scenery').draw()
        self.camera.unset()
        for x in range(300,1450,90):
            rect(x-cam,270,32,1,(63,106,115))
        if cam<400:text('BUILD YOUR ROUTE IN TILED',290-cam,210,1,(111,188,184))
        cx,cy=self.markers['Checkpoint'];rect(cx-cam,cy-25,2,33,(192,219,207));rect(cx-cam+2,cy-25,14,10,(102,226,174) if self.checkpoint else (234,178,101))
        for b in self.bullets:circle(b[0]-cam,b[1],3,(249,223,137))
        for b in self.enemy:
            circle(b[0]-cam,b[1],7,(230,103,97));circle(b[0]-cam-2,b[1]-2,3,(255,202,149))
        if self.boss_hp>0:
            xf=self.boss_transform
            tex=self.tex['boss_attack' if self.phase<1.8 and self.boss_active else 'boss_idle']
            bw,bh=76*xf.scale.x,70*xf.scale.y
            kn.renderer.draw(tex,kn.Rect(self.boss_x-cam+xf.pos.x-bw/2,self.boss_y+xf.pos.y-bh/2,bw,bh))
            if self.boss_active:
                text('TIDE WARDEN',W//2-66,52,1,(248,191,130))
                rect(230,65,180,4,(61,73,90));rect(230,65,180*self.boss_hp/12,4,(233,137,111))
                text('DODGE' if self.phase<1.8 else 'SHOOT - SHIELD DOWN',250 if self.phase<1.8 else 211,77,1)
        ex,ey=self.markers['Exit']
        rect(ex-cam-8,ey-20,16,48,(62,109,116) if self.boss_hp else (132,225,183))
        if self.invuln<=0 or int(t*12)%2==0:
            tex=self.tex['hero_run' if abs(self.player.velocity.x)>1 and int(t*8)%2 else 'hero_idle']
            kn.renderer.draw(tex,kn.Rect(p.x-cam-9,p.y-12,18,24),options=kn.DrawOptions(flip_h=self.face<0))
        # Fixed HUD.
        rect(0,0,W,40,(9,20,35));rect(0,39,W,1,(47,83,96))
        text('STORMLIGHT HARBOR',16,9,2,(244,219,170))
        text('STUDENT WORKSHOP',16,28,1,(109,181,179))
        for i in range(3):circle(560+i*20,18,6,(236,129,123) if i<self.hp else (49,64,79))
        rect(0,331,W,29,(9,20,35));text('A D / ARROWS MOVE   SPACE JUMP   J SHOOT',14,337,1)
        text('R RESET   B BOSS LAB   M MUTE   ESC CLOSE',14,349,1,(111,159,169))
        if self.elapsed<8 and not self.boss_active:
            rect(17,64,254,59,(16,35,51))
            text('01 / RELIGHT THE HARBOR',27,74,1,(242,192,123))
            text('CROSS THE ISLANDS. REACH THE WARDEN.',27,91,1)
            text('DODGE ITS ORBS. FIRE WHEN IT RESTS.',27,107,1)
        if self.won:
            rect(130,122,380,105,(9,24,39));text('HARBOR RESTORED',166,144,3,(246,221,160))
            text('YOU BROUGHT THE LIGHT BACK.',214,179,1)
            text('R TO PLAY AGAIN',274,203,1,(119,204,180))
        kn.renderer.present()


def run(frames=0,screenshot=None,boss=False):
    kn.init()
    try:
        kn.window.create('Stormlight Harbor | Student Workshop',1280,720)
        kn.renderer.set_default_filter_mode(kn.FilterMode.NEAREST)
        kn.renderer.set_virtual_resolution(W,H);kn.time.set_target(60)
        game=Game()
        if boss:game.warp()
        count=0
        while kn.window.is_open():
            kn.event.poll()
            if not kn.window.is_open():break
            key=kn.key;S=kn.Scancode
            if key.is_just_pressed(S.S_ESC):break
            if key.is_just_pressed(S.S_r):game.reset()
            if key.is_just_pressed(S.S_b):game.warp()
            if key.is_just_pressed(S.S_m):
                game.muted=not game.muted;kn.mixer.set_master_volume(0 if game.muted else 1)
            game.jump_buffer |= key.is_just_pressed(S.S_SPACE)
            for dt in kn.physics.fixed_steps():
                game.update(dt,key.is_pressed(S.S_a) or key.is_pressed(S.S_LEFT),key.is_pressed(S.S_d) or key.is_pressed(S.S_RIGHT),game.jump_buffer,key.is_pressed(S.S_j))
                game.jump_buffer=False
            game.draw();count+=1
            if count == 1: print("READY: Student workshop window is running", flush=True)
            if frames and count>=frames:
                if screenshot:kn.window.save_screenshot(screenshot)
                break
        game.audio.close()
    finally:kn.quit()

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--frames',type=int,default=0);ap.add_argument('--screenshot');ap.add_argument('--boss',action='store_true');args=ap.parse_args()
    run(args.frames,args.screenshot,args.boss)
