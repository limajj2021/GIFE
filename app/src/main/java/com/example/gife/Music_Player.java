package com.example.gife;

import android.media.MediaPlayer;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;


import androidx.appcompat.app.AppCompatActivity;

public class Music_Player extends AppCompatActivity {

    MediaPlayer mediaPlayer1,mediaPlayer2,mediaPlayer3,mediaPlayer4,mediaPlayer5,mediaPlayer6,mediaPlayer7,mediaPlayer8,mediaPlayer9,mediaPlayer10,mediaPlayer11,mediaPlayer12;
    Button pop1start,pop2start,pop3start,classic1start,classic2start,classic3start,rock1start,rock2start,kids1start,kids2start,other1start,other2start;
    Button pop1stop,pop2stop,pop3stop,classic1stop,classic2stop,classic3stop,rock1stop,rock2stop,kids1stop,kids2stop,other1stop,other2stop;
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.music_player_activity);
        pop1start = (Button) findViewById(R.id.pop1start);
        pop1stop = (Button) findViewById(R.id.pop1stop);
        pop2start = (Button) findViewById(R.id.pop2start);
        pop2stop = (Button) findViewById(R.id.pop2stop);
        pop3start = (Button) findViewById(R.id.pop3start);
        pop3stop = (Button) findViewById(R.id.pop3stop);
        classic1start = (Button) findViewById(R.id.classic1start);
        classic1stop = (Button) findViewById(R.id.classic1stop);
        classic2start = (Button) findViewById(R.id.classic2start);
        classic2stop = (Button) findViewById(R.id.classic2stop);
        classic3start = (Button) findViewById(R.id.classic3start);
        classic3stop = (Button) findViewById(R.id.classic3stop);
        rock1start = (Button) findViewById(R.id.rock1start);
        rock1stop = (Button) findViewById(R.id.rock1stop);
        rock2start = (Button) findViewById(R.id.rock2start);
        rock2stop = (Button) findViewById(R.id.rock2stop);
        other1start = (Button) findViewById(R.id.other1start);
        other1stop = (Button) findViewById(R.id.other1stop);
        other2start = (Button) findViewById(R.id.other2start);
        other2stop = (Button) findViewById(R.id.other2stop);
        kids1start = (Button) findViewById(R.id.classic1start);
        kids1stop = (Button) findViewById(R.id.classic1stop);
        kids2start = (Button) findViewById(R.id.kids2start);
        kids2stop = (Button) findViewById(R.id.kids2stop);
        mediaPlayer2 = MediaPlayer.create(this, R.raw.pop2);
        mediaPlayer1 = MediaPlayer.create(this, R.raw.pop1);
        mediaPlayer3 = MediaPlayer.create(this, R.raw.pop3);
        mediaPlayer4 = MediaPlayer.create(this, R.raw.classic1);
        mediaPlayer5 = MediaPlayer.create(this, R.raw.classic2);
        mediaPlayer6 = MediaPlayer.create(this, R.raw.classic3);
        mediaPlayer7 = MediaPlayer.create(this, R.raw.rock1);
        mediaPlayer8 = MediaPlayer.create(this, R.raw.rock2);
        mediaPlayer9 = MediaPlayer.create(this, R.raw.kids2);
        mediaPlayer10 = MediaPlayer.create(this, R.raw.kids1);
        mediaPlayer11 = MediaPlayer.create(this, R.raw.other2);
        mediaPlayer12 = MediaPlayer.create(this, R.raw.other1);
        pop1stop.setEnabled(false);
        pop2stop.setEnabled(false);
        pop3stop.setEnabled(false);
        classic1stop.setEnabled(false);
        classic2stop.setEnabled(false);
        classic3stop.setEnabled(false);
        rock1stop.setEnabled(false);
        rock2stop.setEnabled(false);
        kids1stop.setEnabled(false);
        kids2stop.setEnabled(false);
        other1stop.setEnabled(false);
        other2stop.setEnabled(false);


    }
    public void pop1start (View view){
        mediaPlayer1.start();
        pop1stop.setEnabled(true);
        pop1start.setEnabled(false);
    }
    public void pop1stop (View view){
        mediaPlayer1.pause();
        pop1stop.setEnabled(false);
        pop1start.setEnabled(true);
    }
    public void pop2start (View view){
        mediaPlayer2.start();
        pop2stop.setEnabled(true);
        pop2start.setEnabled(false);
    }
    public void pop2stop (View view){
        mediaPlayer2.pause();
        pop2stop.setEnabled(false);
        pop2start.setEnabled(true);
    }
    public void pop3start (View view){
        mediaPlayer3.start();
        pop3stop.setEnabled(true);
        pop3start.setEnabled(false);
    }
    public void pop3stop (View view){
        mediaPlayer3.pause();
        pop3stop.setEnabled(false);
        pop3start.setEnabled(true);
    }
    public void classic1start (View view){
        mediaPlayer4.start();
        classic1stop.setEnabled(true);
        classic1start.setEnabled(false);
    }
    public void classic1stop (View view){
        mediaPlayer4.pause();
        classic1stop.setEnabled(false);
        classic1start.setEnabled(true);
    }
    public void classic2start (View view){
        mediaPlayer5.start();
        classic2stop.setEnabled(true);
        classic2start.setEnabled(false);
    }
    public void classic2stop (View view){
        mediaPlayer5.pause();
        classic2stop.setEnabled(false);
        classic2start.setEnabled(true);
    }
    public void classic3start (View view){
        mediaPlayer6.start();
        classic3stop.setEnabled(true);
        classic3start.setEnabled(false);
    }
    public void classic3stop (View view){
        mediaPlayer6.pause();
        classic3stop.setEnabled(false);
        classic3start.setEnabled(true);
    }
    public void rock1start (View view){
        mediaPlayer7.start();
        rock1stop.setEnabled(true);
        rock1start.setEnabled(false);
    }
    public void rock1stop (View view){
        mediaPlayer7.pause();
        rock1stop.setEnabled(false);
        rock1start.setEnabled(true);
    }
    public void rock2start (View view){
        mediaPlayer8.start();
        rock2stop.setEnabled(true);
        rock2start.setEnabled(false);
    }
    public void rock2stop (View view){
        mediaPlayer8.pause();
        rock2stop.setEnabled(false);
        rock2start.setEnabled(true);
    }
    public void kids1start (View view){
        mediaPlayer9.start();
        kids1stop.setEnabled(true);
        kids1start.setEnabled(false);
    }
    public void kids1stop (View view){
        mediaPlayer9.pause();
        kids1stop.setEnabled(false);
        kids1start.setEnabled(true);
    }
    public void kids2start (View view){
        mediaPlayer10.start();
        kids2stop.setEnabled(true);
        kids2start.setEnabled(false);
    }
    public void kids2stop (View view){
        mediaPlayer10.pause();
        kids2stop.setEnabled(false);
        kids2start.setEnabled(true);
    }
    public void other1start (View view){
        mediaPlayer11.start();
        other1stop.setEnabled(true);
        other1start.setEnabled(false);
    }
    public void other1stop (View view){
        mediaPlayer11.pause();
        other1stop.setEnabled(false);
        other1start.setEnabled(true);
    }
    public void other2start (View view){
        mediaPlayer12.start();
        other2stop.setEnabled(true);
        other2start.setEnabled(false);
    }
    public void other2stop (View view){
        mediaPlayer12.pause();
        other2stop.setEnabled(false);
        other2start.setEnabled(true);
    }
}
