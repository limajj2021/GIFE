package com.example.gife;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.view.View;
import android.widget.Button;
import android.os.Bundle;

public class MainActivity extends AppCompatActivity {
    Button videoButton;
    Button musicButton;
    Button bookButton;
    Button foodButton;
    Button gameButton;
    Button mapButton;
    Button helpButton;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        videoButton = (Button) findViewById(R.id.videoButton);
        bookButton = (Button) findViewById(R.id.bookButton);
        gameButton = (Button) findViewById(R.id.gameButton);
        mapButton = (Button) findViewById(R.id.mapButton);
        helpButton = (Button) findViewById(R.id.helpButton);
        musicButton = (Button) findViewById(R.id.musicButton);
        foodButton = (Button) findViewById(R.id.foodButton);

        videoButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intentLoadNewActivity = new Intent(MainActivity.this, Movie_Player.class);
                startActivity(intentLoadNewActivity);
            }

        });

        bookButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intentLoadNewActivity = new Intent(MainActivity.this, BookActivity.class);
                startActivity(intentLoadNewActivity);
            }

        });

        gameButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intentLoadNewActivity = new Intent(MainActivity.this, GameActivity.class);
                startActivity(intentLoadNewActivity);
            }

        });

        mapButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intentLoadNewActivity = new Intent(MainActivity.this, Map_Activity.class);
                startActivity(intentLoadNewActivity);
            }

        });

        helpButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intentLoadNewActivity = new Intent(MainActivity.this, HelpActivity.class);
                startActivity(intentLoadNewActivity);
            }

        });
        foodButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intentLoadNewActivity = new Intent(MainActivity.this, Food_Menu.class);
                startActivity(intentLoadNewActivity);
            }

        });
        musicButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intentLoadNewActivity = new Intent(MainActivity.this, Music_Player.class);
                startActivity(intentLoadNewActivity);
            }

        });
    }

}