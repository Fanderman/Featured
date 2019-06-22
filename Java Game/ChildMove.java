/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package lista.pkg9;

/**
 *
 * @author jacek
 */
public class ChildMove {
    
    public int move(Map m, int x, int y, int dir){
        if(dir == 0){
            if(m.getType(x,((y-1)%m.width +m.width) %m.width).equals("Tile")){
                m.setType(x,((y-1)%m.width +m.width) %m.width,"Child");
                m.setType(x,y,"Tile");
                return 2;
            }
            if(m.getType(x,((y-1)%m.width +m.width) %m.width).equals("Santa")){
                System.out.println("You Lost!");
                System.exit(0);
            }
            if(m.getType(x,((y-1)%m.width +m.width) %m.width).equals("Present")){
               m.setType(x,((y-1)%m.width +m.width) %m.width,"Sleeping");
               m.setType(x,y,"Tile");
               m.presents = 0;
               return 1;
            }
        }
        if(dir == 2){
            if(m.getType(x,(y+1)%m.width).equals("Tile")){
                m.setType(x,(y+1)%m.width,"Child");
                m.setType(x,y,"Tile");
                return 4;
            }
            if(m.getType(x,(y+1)%m.width).equals("Santa")){
                System.out.println("You Lost!");
                System.exit(0);
            }
            if(m.getType(x,(y+1)%m.width).equals("Present")){
               m.setType(x,(y+1)%m.width,"Sleeping");
               m.setType(x,y,"Tile");
               m.presents = 0;
               return 1;
            }
        }
        if(dir == 1){
            if(m.getType((x+1)%m.height,y).equals("Tile")){
                m.setType((x+1)%m.height,y, "Child");
                m.setType(x,y,"Tile");
                return 3;
            }
            if(m.getType((x+1)%m.height,y).equals("Santa")){
                System.out.println("You Lost!");
                System.exit(0);
            }
            if(m.getType((x+1)%m.height,y).equals("Present")){
               m.setType((x+1)%m.height,y,"Sleeping");
               m.setType(x,y,"Tile");
               m.presents = 0;
               return 1;
            }
        }
        if(dir == 3){
            if(m.getType(((x-1)%m.height + m.height)%m.height,y).equals("Tile")){
                m.setType(((x-1)%m.height + m.height)%m.height,y, "Child");
                m.setType(x,y,"Tile");
                return 5;
            }
            if(m.getType(((x-1)%m.height + m.height)%m.height,y).equals("Santa")){
                System.out.println("You Lost!");
                System.exit(0);
            }
            if(m.getType(((x-1)%m.height + m.height)%m.height,y).equals("Present")){
               m.setType(((x-1)%m.height + m.height)%m.height,y,"Sleeping");
               m.setType(x,y,"Tile");
               m.presents = 0;
               return 1;
            }
        }
        return 0;
    }
}
