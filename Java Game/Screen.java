/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package lista.pkg9;

import java.awt.*;
import java.awt.event.*;
import javax.swing.*;

import java.util.List;
import java.util.ArrayList;
import java.io.*;

/**
 *
 * @author jacek
 */
public class Screen {
    private final int height, width;
    private final int size;
    private final int FPS = 60;
    private final int children;
    private boolean loaded = false;

    private JFrame frame;
    private Map m;
    private Operator mobs;
    
    public Screen (int height, int width, int size, int children) {
        this.height = height;
        this.width = width;
        this.size = size;
        this.children = children;
    }
    public void repaintScreen(){
        int left = 0;
        for(int i = 0; i != height; i++){
            for(int j = 0; j != width; j++){
                String type = m.getType(i, j);
                switch(type){
                    case "Tile":
                        m.setColor(i, j, Color.WHITE);
                        break;
                    case "Santa":
                        m.setColor(i, j, Color.RED);
                        break;
                    case "Child":
                        left++;
                        m.setColor(i, j, Color.BLUE);
                        break;
                    case "Present":
                        m.setColor(i, j, Color.YELLOW);
                        break;
                    case "Sleeping":
                        m.setColor(i, j, Color.GRAY);
                        break;
                    case "Resting":
                        left++;
                        m.setColor(i, j, Color.BLUE.darker());
                        break;
                }
            }
        }
        if(left == 0){
            System.out.println("You win!");
            System.exit(0);
        }
    }
    
    public void run () {
        final int delay = 1000/FPS;

        frame = new JFrame("Santa Run");
        frame.setLayout(new GridLayout(height, width));
        m = new Map(frame,height,width,size);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setResizable(false);
        frame.pack();
        frame.setLocationRelativeTo(null);
        
        Timer refresh = new Timer(delay, new ActionListener(){
            @Override
            public void actionPerformed(ActionEvent event) {
                repaintScreen();
            }
        });
        
        mobs = new Operator(children,m);
        frame.addKeyListener(new KeyAdapter(){
            @Override
            public void keyPressed (KeyEvent event) {
                mobs.Keyboard(event.getKeyChar(), m, mobs.cm);
            }
        });
        refresh.setRepeats(true);
        refresh.start();
      
        frame.setVisible(true);
    }
}
