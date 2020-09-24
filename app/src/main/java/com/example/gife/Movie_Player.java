package com.example.gife;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

import androidx.appcompat.app.AppCompatActivity;

import com.example.gife.movies.action_movie;
import com.example.gife.movies.comedy_movie;
import com.example.gife.movies.fantasy_movie;
import com.example.gife.movies.horror_movie;
import com.example.gife.movies.kids_movie;
import com.example.gife.movies.romance_movie;


public class Movie_Player extends AppCompatActivity  {
    Button comedyButton;
    Button horrorButton;
    Button kidsButton;
    Button actionButton;
    Button fantasyButton;
    Button romanceButton;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.movie_player_activity);
        comedyButton = (Button) findViewById(R.id.comedyButton);
        horrorButton = (Button) findViewById(R.id.horrorButton);
        actionButton = (Button) findViewById(R.id.actionButton);
        romanceButton = (Button) findViewById(R.id.romanceButton);
        kidsButton = (Button) findViewById(R.id.kidsButton);
        fantasyButton = (Button) findViewById(R.id.fantasyButton);

        comedyButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intentLoadNewActivity = new Intent(Movie_Player.this, comedy_movie.class);
                startActivity(intentLoadNewActivity);
            }

        });
        horrorButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intentLoadNewActivity = new Intent(Movie_Player.this, horror_movie.class);
                startActivity(intentLoadNewActivity);
            }

        });
        romanceButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intentLoadNewActivity = new Intent(Movie_Player.this, romance_movie.class);
                startActivity(intentLoadNewActivity);
            }

        });
        kidsButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intentLoadNewActivity = new Intent(Movie_Player.this, kids_movie.class);
                startActivity(intentLoadNewActivity);
            }

        });
        fantasyButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intentLoadNewActivity = new Intent(Movie_Player.this, fantasy_movie.class);
                startActivity(intentLoadNewActivity);
            }

        });
        actionButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intentLoadNewActivity = new Intent(Movie_Player.this, action_movie.class);
                startActivity(intentLoadNewActivity);
            }

        });
    }

}
