package com.example.gife;

import com.example.gife.books.book1;
import com.example.gife.books.book2;
import com.example.gife.books.book3;
import com.example.gife.books.book4;


import android.content.Intent;
import android.media.MediaPlayer;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;


import androidx.appcompat.app.AppCompatActivity;

public class BookActivity extends AppCompatActivity {
    Button harryButton;
    Button infernoButton;
    Button faultButton;
    Button littleprButton;
    MediaPlayer mediaPlayerad1,mediaPlayerad2;
    Button audio1,audio2,audio1stp,audio2stp;

    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.book_activity);
        harryButton = (Button) findViewById(R.id.harrypotterButton);
        infernoButton = (Button) findViewById(R.id.infernoButton);
        faultButton = (Button) findViewById(R.id.faltStarsButton);
        littleprButton = (Button) findViewById(R.id.littlePrinceButton);
        audio1 = (Button)findViewById(R.id.audiobookbutton1);
        audio2 = (Button)findViewById(R.id.audiobookbutton2);
        audio1stp = (Button)findViewById(R.id.audio1pause);
        audio2stp = (Button)findViewById(R.id.audio2pause);
        mediaPlayerad1 = MediaPlayer.create(this, R.raw.househill);
        mediaPlayerad2 = MediaPlayer.create(this, R.raw.blackcat);
        audio1stp.setEnabled(false);
        audio2stp.setEnabled(false);

        harryButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intentLoadNewActivity = new Intent(BookActivity.this, book1.class);
                startActivity(intentLoadNewActivity);
            }

        });

        infernoButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intentLoadNewActivity = new Intent(BookActivity.this, book2.class);
                startActivity(intentLoadNewActivity);
            }

        });

        faultButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intentLoadNewActivity = new Intent(BookActivity.this, book3.class);
                startActivity(intentLoadNewActivity);
            }

        });

        littleprButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intentLoadNewActivity = new Intent(BookActivity.this, book4.class);
                startActivity(intentLoadNewActivity);
            }

        });

    }
    public void audio1start(View view){
        mediaPlayerad1.start();
        audio1stp.setEnabled(true);
        audio1.setEnabled(false);
    }
    public void audio1stop (View view){
        mediaPlayerad1.pause();
        audio1stp.setEnabled(false);
        audio1.setEnabled(true);
    }
    public void audio2start (View view){
        mediaPlayerad2.start();
        audio2stp.setEnabled(true);
        audio2.setEnabled(false);
    }
    public void audio2stop (View view){
        mediaPlayerad2.pause();
        audio2stp.setEnabled(false);
        audio2.setEnabled(true);
    }
}
