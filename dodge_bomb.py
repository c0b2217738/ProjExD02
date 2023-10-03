import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1600, 900

move_d = {
    pg.K_UP:(0,-5),
    pg.K_DOWN:(0, +5),
    pg.K_LEFT:(-5,0),
    pg.K_RIGHT:(+5, 0),
}
kk_img = pg.image.load("ex02/fig/3.png")
kk_img_r = pg.transform.flip(kk_img, True, False)
mv_img = { #画像保存場所
    (-5, 0):pg.transform.rotozoom(kk_img, 0, 2.0),
    (-5,-5):pg.transform.rotozoom(kk_img, -45, 2.0),#斜め左上
    (+5,0):pg.transform.rotozoom(kk_img_r, 0, 2.0),#反転
    (-5,+5):pg.transform.rotozoom(kk_img, 45, 2.0),#斜め左下
    (0,-5):pg.transform.rotozoom(kk_img_r, 90, 2.0),#上
    (+5,-5):pg.transform.rotozoom(kk_img_r, 45, 2.0),#斜め右上
    (+5, +5):pg.transform.rotozoom(kk_img_r, -45, 2.0),#斜め右下
    (0,+5):pg.transform.rotozoom(kk_img_r, -90, 2.0),#下
}

def cheak_inout(obj_rct:pg.Rect):
    """
    オブジェクトが画面内外どちらにあるかを判定、真理値タプルで返す
    obj_rctはこうかとんsurfaceのrect
    戻り値はタプル(横方向結果,縦判定結果)
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate



def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    bg_rct = bg_img.get_rect()

    """こうかとん"""
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)#通常
    kk_rct = kk_img.get_rect()
    kk_rct.center = (900,400)

    """爆弾"""
    bd_img = pg.Surface((20, 20)) #爆弾のsurface
    pg.draw.circle(bd_img, (255, 0, 0), (10, 10), 10)
    bd_img.set_colorkey((0,0,0))
    bd_rct = bd_img.get_rect() #練習1
    x,y = random.randint(0,WIDTH), random.randint(0,HEIGHT) #練習1
    bd_rct.center = (x,y) #練習1
    vx = +5
    vy = +5

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bd_rct): #鳥と爆弾が触れたとき 
            print("ゲームオーバー")
            return

        screen.blit(bg_img, bg_rct)

        #動きつける
        key_lst = pg.key.get_pressed()
        sub_mv = [0,0]
        for key, mv in move_d.items():
            if key_lst[key]:
                sub_mv[0] += mv[0]
                sub_mv[1] += mv[1]
        kk_rct.move_ip(sub_mv[0], sub_mv[1])

        #画面外に行ってしまった時
        if cheak_inout(kk_rct) != (True,True):
            kk_rct.move_ip(-sub_mv[0], -sub_mv[1])

        #こうかとんの移動に合わせて画像を変える 
        for t, img in mv_img.items():
            if sub_mv[0] == t[0] and sub_mv[1] == t[1]:
                screen.blit(img, kk_rct)
            #何も入力されていない時
            if sub_mv == [0,0]: 
                screen.blit(kk_img, kk_rct)
                

        bd_rct.move_ip(vx,vy)
        yoko, tate = cheak_inout(bd_rct)
        if not yoko :
            vx *= -1
        if not tate :
            vy *= -1
        screen.blit(bd_img, bd_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()