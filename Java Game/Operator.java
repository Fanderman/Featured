/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package lista.pkg9;

import java.util.Random;

/**
 *
 * @author jacek
 */
public class Operator {
    private Child mobs[];
    public int size;
    public ChildMove cm;
    
    public Operator(int size, Map m){
        this.mobs = new Child[size];
        this.size = size;
        this.cm = new ChildMove();
        m.sx = -1;
        m.sy = -1;
        m.sdr = 'd';
        Random rd = new Random();     
        int x = (rd.nextInt()%m.height+m.height)%m.height;
        int y = (rd.nextInt()%m.width+m.width)%m.width;
        m.setType(x, y, "Santa");
        m.sx = x;
        m.sy = y;
        for(int i = 0; i != size; i++){
            while(!m.getType(x,y).equals("Tile")){
                x = (rd.nextInt()%m.height+m.height)%m.height;
                y = (rd.nextInt()%m.width+m.width)%m.width;
            }
            mobs[i] = new Child(Integer.toString(i),x,y,m,cm);
            m.setType(x, y, "Child");
            mobs[i].start();
        }
    }
    public int check(Map m, int x, int y){
        if(m.presents > 0)
            return 0;
        if(!m.getType(x, y).equals("Tile"))
            return 0;
        if(m.getType(((x-1)%m.height+m.height)%m.height,y).equals("Resting"))
            return 1;
        if(m.getType((x+1)%m.height,y).equals("Resting"))
            return 1;
        if(m.getType(x,((y-1)%m.width+m.width)%m.width).equals("Resting"))
            return 1;
        if(m.getType(x,(y+1)%m.width).equals("Resting"))
            return 1;
        return 0;
    }
    public void Keyboard(char input, Map m, ChildMove cm){
        synchronized(cm){
            if(input == 'w' && m.getType(((m.sx-1)%m.height+m.height)%m.height,m.sy).equals("Tile")){
                m.setType(m.sx,m.sy,"Tile");
                m.sx = ((m.sx-1)%m.height+m.height)%m.height; 
                m.setType(m.sx,m.sy,"Santa");
                m.sdr = input;
            }
            if(input == 'a' && m.getType(m.sx,((m.sy-1)%m.width+m.width)%m.width).equals("Tile")){
                m.setType(m.sx,m.sy,"Tile");
                m.sy = ((m.sy-1)%m.width+m.width)%m.width;
                m.setType(m.sx,m.sy,"Santa");
                m.sdr = input;
            }
            if(input == 'd' && m.getType(m.sx,(m.sy+1)%m.width).equals("Tile")){
                m.setType(m.sx,m.sy,"Tile");
                m.sy = (m.sy+1)%m.width;
                m.setType(m.sx,m.sy,"Santa");
                m.sdr = input;
            }
            if(input == 's' && m.getType((m.sx+1)%m.height,m.sy).equals("Tile")){
                m.setType(m.sx,m.sy,"Tile");
                m.sx = (m.sx+1)%m.height;
                m.setType(m.sx,m.sy,"Santa");
                m.sdr = input;
            }
            if(input == ' '){
                if(m.sdr == 's'){
                    int nx = (m.sx+1)%m.height;
                    if(check(m,nx,m.sy) == 1){
                        m.presents++;
                        m.setType(nx,m.sy,"Present");
                    }
                }
                if(m.sdr == 'w'){
                    int nx = ((m.sx-1)%m.height+m.height)%m.height; 
                    if(check(m,nx,m.sy) == 1){
                        m.presents++;
                        m.setType(nx,m.sy,"Present");
                    }
                }
                if(m.sdr == 'd'){
                    int ny = (m.sy+1)%m.width;
                    if(check(m,m.sx,ny) == 1){
                        m.presents++;
                        m.setType(m.sx,ny,"Present");
                    }
                }
                if(m.sdr == 'a'){
                    int ny = ((m.sy-1)%m.width+m.width)%m.width;
                    if(check(m,m.sx,ny) == 1){
                        m.presents++;
                        m.setType(m.sx,ny,"Present");
                    }
                }
            }
        }
    }
    
}
