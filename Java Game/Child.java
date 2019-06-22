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
public class Child extends Thread{
    public int x;
    public int y;
    public String name;
    private Thread t;
    private Map m;
    private ChildMove cm;
    
    public Child(String name, int x, int y, Map m, ChildMove cm){
        this.x = x;
        this.y = y;
        this.name = name;
        this.m = m;
        this.cm = cm;
    }
    
    @Override
    public void run(){
        Random rd = new Random();
        int end = 0;
        while(end == 0){
            try{
                int r = rd.nextInt();
                Thread.sleep(1000 + (r%150+150)%150);
            }
            catch(InterruptedException e){
                System.out.println("Interrupted: " + e);
            }
            int direction = -1;
            int distance = 0;
            int witness = 0;
            if(x == m.sx &&(Math.abs(y - m.sy) < 10 || m.width - Math.abs(y-m.sy) < 10)){
                distance = Math.min(Math.abs(y - m.sy),m.width - Math.abs(y - m.sy)) + (rd.nextInt()%6+6)%6;
                if((y - m.sy) > 0){
                    if(Math.abs(y-m.sy) > m.width - Math.abs(y-m.sy))
                        direction = 2;
                    else
                        direction = 0;
                }
                else{
                    if(Math.abs(y-m.sy) > m.width - Math.abs(y-m.sy))
                        direction = 0;
                    else
                        direction = 2;
                }
                witness = 1;
            }
            if(y == m.sy &&( Math.abs(x - m.sx) < 10 ||  m.height - Math.abs(x-m.sx) < 10)){
                distance = Math.min(Math.abs(x - m.sx),m.height - Math.abs(x-m.sx)) + (rd.nextInt()%6+6)%6;
                if((x - m.sx) > 0){
                    if(Math.abs(x-m.sx) > m.height - Math.abs(x-m.sx))
                        direction = 1;
                    else
                        direction = 3;
                }
                else{
                    if(Math.abs(x-m.sx) > m.height - Math.abs(x-m.sx))
                        direction = 3;
                    else
                        direction = 1;
                }
                witness = 1;
            }
            if(m.getType(x,((y-1)%m.width+m.width)%m.width).equals("Present")){
                direction = 0;
                distance = 1;
            }
            if(m.getType(x,(y+1)%m.width).equals("Present")){
                direction = 2;
                distance = 1;
            }
            if(m.getType((x+1)%m.height,y).equals("Present")){
                direction = 1;
                distance = 1;
            }
            if(m.getType(((x-1)%m.height+m.height)%m.height,y).equals("Present")){
                direction = 3;
                distance = 1;
            }
            if(direction == -1 && distance == 0){
                direction = (rd.nextInt()%4+4)%4;
                distance = 1;
            }
            int totalDistance = distance;
            while(distance > 0 && end == 0){
                synchronized(cm){
                    end = cm.move(m,x,y,direction);
                }
                if(end != 1){
                    if(end == 2)
                        y = ((y-1)%m.width + m.width )% m.width;
                    if(end == 3)
                        x = (x+1)%m.height;
                    if(end == 4)
                        y = (y+1)%m.width;
                    if(end == 5)
                        x = ((x-1)%m.height + m.height )% m.height;
                    end = 0;
                    try{
                        Thread.sleep(500/distance + (rd.nextInt()%25+25) %25);
                    }
                    catch(InterruptedException e){
                        System.out.println("Interrupted: " + e);
                    }
                    distance--;
                }
            }
            if(witness == 1 && end != 1){
                try{
                    int r = rd.nextInt();
                    m.setType(x,y,"Resting");
                    Thread.sleep(2500 + totalDistance*(r%200+200)%200);
                    m.setType(x,y,"Child");
                }
                catch(InterruptedException e){
                    System.out.println("Interrupted: " + e);
                }
            }
                
        }
    }
    @Override
    public void start() {
      if (t == null) {
         t = new Thread (this, name);
         t.start();
      }
   }
}
