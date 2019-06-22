/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package lista.pkg9;

import java.awt.*;
import javax.swing.*;

/**
 *
 * @author jacek
 */
public class Map {
    
    private JPanel cells[][];
    private String type[][];
    public int height;
    public int width;
    public int sx;
    public int sy;
    public int sdr;
    public int presents;
    
    public Map(JFrame body, int height, int width, int size){
        cells = new JPanel[height][width];
        type = new String[height][width];
        this.width = width;
        this.height = height;
        this.presents = 0;
        for(int i = 0; i != height; i++){
            for(int j = 0; j != width; j++){
                cells[i][j] = new JPanel();
                cells[i][j].setBackground(Color.WHITE);
                cells[i][j].setBorder(BorderFactory.createMatteBorder(1,1,1,1,Color.BLACK));
                cells[i][j].setPreferredSize(new Dimension(size,size));
                body.add(cells[i][j]);
                type[i][j] = "Tile";
            }
        }
    }
    
    public void setColor(int x, int y, Color color){
        cells[x][y].setBackground(color);
    }
    
    public Color getColor(int x, int y){
        return cells[x][y].getBackground();
    }
    
    public void setType(int x, int y, String s){
        type[x][y] = s;
    }
    
    public String getType(int x, int y){
        return type[x][y];
    }
}
